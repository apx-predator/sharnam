# add_interfaces.py
import logging
from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Optional
import mysql.connector
import os
import json
from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.plugins.inventory import InventoryPluginRegister
import paramiko
from nornir_scrapli.tasks import netconf_edit_config, netconf_get_config


paramiko.Transport._banner_timeout = 60.0


# Log to both file and stdout (terminal)
log = logging.getLogger("configure")
log.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
logging.basicConfig(filename="interfaces.log", level=logging.DEBUG, format= "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh = logging.FileHandler("interfaces.log", mode="a")
fh.setFormatter(formatter)
log.addHandler(fh)

sh = logging.StreamHandler()
sh.setFormatter(formatter)
log.addHandler(sh)

app = FastAPI()


# ---------- Models ----------

class Credentials(BaseModel):
    username: str
    password_cipher: str

class Interface(BaseModel):
    name: str
    desc: Optional[str] = ""
    ip: Optional[str] = ""
    netmask: Optional[str] = ""

class Device(BaseModel):
    id: str
    mode: str
    management_ip: Optional[str] = None
    platform: Optional[str] = None
    version: Optional[str] = None
    family: Optional[str] = None
    interfaces: List[Interface]

class ConfigureRequest(BaseModel):
    action: Optional[str] = "configure"
    job_id: Optional[str] = None
    profile: Credentials
    devices: List[Device]
    async_: bool = Field(default=False, alias="async")

    model_config = {"populate_by_name": True}


# ---------- DB helpers ----------

def db():
    return mysql.connector.connect(
        host="localhost", user="root", password="", database="sharnam_db"
    )

def set_job_status(job_id, status, result=None):
    if not job_id:
        return
    conn = db()
    try:
        cur = conn.cursor()
        if result is None:
            cur.execute("UPDATE jobs SET status=%s WHERE job_id=%s", (status, job_id))
        else:
            cur.execute(
                "UPDATE jobs SET status=%s, result=%s WHERE job_id=%s",
                (status, result, job_id),
            )
        conn.commit()
    finally:
        conn.close()


# ---------- Helpers ----------

def _vlan_from(intf_name: str):
    """Extract vlan number from 'vlan123' or '123' formats."""
    name = intf_name.lower()
    if name.startswith("vlan"):
        return name[4:]
    if name.isdigit():
        return name
    return None
    
def _loopback_from(intf_name: str):
    """Extract number from 'loopback10' / 'Loopback10' / '10' (if caller knows it's a loopback)."""
    name = intf_name.lower()
    if name.startswith("loopback"):
        suffix = name[8:].lstrip("0123456789")  # just sanity, keep number
        number = name[8:]
        return number if number.isdigit() else None
    return None


def _filter_loopback(number: str) -> str:
    return (
        '<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">'
        f'<interface><Loopback><name>{number}</name></Loopback></interface>'
        '</native>'
    )

def _filter_vlan(vlan: str) -> str:
    return (
        '<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">'
        f'<interface><Vlan><name>{vlan}</name></Vlan></interface>'
        '</native>'
    )
    
    
def _tunnel_from(intf_name: str):
    """Extract number from 'tunnel10' / 'Tunnel10'."""
    name = intf_name.lower()
    if name.startswith("tunnel"):
        number = name[6:]
        return number if number.isdigit() else None
    return None


def _filter_tunnel(number: str) -> str:
    return (
        '<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">'
        f'<interface><Tunnel><name>{number}</name></Tunnel></interface>'
        '</native>'
    )


def _has_candidate(conn) -> bool:
    """Detect if device supports NETCONF candidate datastore."""
    try:
        caps = conn.server_capabilities
    except AttributeError:
        try:
            caps = conn.get_capabilities()
        except Exception:
            return False
    if not caps:
        return False
    for cap in caps:
        if "candidate" in str(cap).lower():
            return True
        else:
          return False


# ---------- Confirmed-commit helper ----------

def _confirmed_commit(conn, timeout: int = 120):
    """Send <commit><confirmed/><confirm-timeout>N</confirm-timeout></commit>."""
    conn.send_rpc(
        payload=(
            '<rpc message-id="102" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">'
            f'<commit><confirmed/><confirm-timeout>{timeout}</confirm-timeout></commit>'
            '</rpc>'
        ),
        operation="commit",
    )


# ---------- NETCONF XML templates ----------

  #SVI INTERFACES
SVI_RPC_TEMPLATE = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Vlan>
        <name>{vlan}</name>
        <description>{desc}</description>
        <ip>
          <address>
            <primary>
              <address>{ip}</address>
              <mask>{prefix}</mask>
            </primary>
          </address>
        </ip>
      </Vlan>
    </interface>
  </native>
</config>
"""

SVI_RPC_DELETE_TEMPLATE = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Vlan nc:operation="delete"
             xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <name>{vlan}</name>
      </Vlan>
    </interface>
  </native>
</config>
"""

## LOOPBACK INTERFACES
LOOPBACK_RPC_TEMPLATE = """
  <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Loopback>
        <name>{number}</name>
        <description>{desc}</description>
        <ip>
          <address>
            <primary>
              <address>{ip}</address>
              <mask>{mask}</mask>
            </primary>
          </address>
        </ip>
      </Loopback>
    </interface>
  </native>
</config>

"""
LOOPBACK_RPC_DELETE_TEMPLATE = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Loopback nc:operation="delete"
                 xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <name>{number}</name>
      </Loopback>
    </interface>
  </native>
</config>

"""

TUNNEL_RPC_TEMPLATE = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Tunnel>
        <name>{number}</name>
        <description>{desc}</description>
        <ip>
          <address>
            <primary>
              <address>{ip}</address>
              <mask>{mask}</mask>
            </primary>
          </address>
        </ip>
      </Tunnel>
    </interface>
  </native>
</config>
"""



TUNNEL_RPC_DELETE_TEMPLATE = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <Tunnel nc:operation="delete"
              xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <name>{number}</name>
      </Tunnel>
    </interface>
  </native>
</config>
"""

# ---------- Configure task ----------

def iosxe_svi_task(task):
    """Configure SVIs, Loopbacks, and/or Tunnels on a single IOS-XE device."""
    conn = task.host.get_connection("scrapli_netconf", task.nornir.config)
    has_candidate = _has_candidate(conn)
    log.info("candidate datastore: %s", "YES" if has_candidate else "NO")

    # ---------- Stage: add interfaces ----------
    for intf in task.host["interfaces"]:
        name     = intf["name"]
        vlan     = _vlan_from(name)
        loopback = _loopback_from(name)
        tunnel   = _tunnel_from(name)

        ip   = intf["ip"]
        mask = intf["netmask"]
        desc = intf["desc"]

        if vlan is not None:
            rpc_payload = SVI_RPC_TEMPLATE.format(
                vlan=vlan, desc=desc, ip=ip, prefix=mask
            )
            filter_fn = _filter_vlan
            ident     = vlan
            label     = f"Vlan{vlan}"

        elif loopback is not None:
            rpc_payload = LOOPBACK_RPC_TEMPLATE.format(
                number=loopback, desc=desc, ip=ip, mask=mask
            )
            filter_fn = _filter_loopback
            ident     = loopback
            label     = f"Loopback{loopback}"

        elif tunnel is not None:
            rpc_payload = TUNNEL_RPC_TEMPLATE.format(
                number=tunnel, desc=desc, ip=ip, mask=mask
            )
            filter_fn = _filter_tunnel
            ident     = tunnel
            label     = f"Tunnel{tunnel}"

        else:
            log.warning("skipping unsupported interface: %s", name)
            continue

        if has_candidate:
            netconf_edit_config(task, config=rpc_payload, target="candidate")
            staged = netconf_get_config(
                task, source="candidate", filter_=filter_fn(ident)
            )
            if ip not in staged.result:
                conn.discard()
                raise RuntimeError(f"stage check failed for {label}")
            _confirmed_commit(conn, timeout=120)
        else:
            log.warning("no candidate datastore — writing directly to running")
            result_obj = netconf_edit_config(task, config=rpc_payload, target="running")
            if result_obj.failed:
                raise RuntimeError(
                    f"NETCONF edit_config failed for {label}: {result_obj.result[:300]}"
                )

    # ---------- Verify: read back running config ----------
    for intf in task.host["interfaces"]:
        name     = intf["name"]
        vlan     = _vlan_from(name)
        loopback = _loopback_from(name)
        tunnel   = _tunnel_from(name)

        if vlan is not None:
            label     = f"Vlan{vlan}"
            filter_fn = _filter_vlan
            ident     = vlan
        elif loopback is not None:
            label     = f"Loopback{loopback}"
            filter_fn = _filter_loopback
            ident     = loopback
        elif tunnel is not None:
            label     = f"Tunnel{tunnel}"
            filter_fn = _filter_tunnel
            ident     = tunnel
        else:
            continue

        ip = intf["ip"]
        running = netconf_get_config(
            task, source="running", filter_=filter_fn(ident)
        )
        if ip not in running.result:
            raise RuntimeError(f"post-check failed for {label}: {ip} not in running")

    if has_candidate:
        conn.commit()
    log.info("configure task done")
# ---------- Delete task ----------

def iosxe_del_task(task):
    """Remove SVIs, Loopbacks, and/or Tunnels from a single IOS-XE device."""
    conn = task.host.get_connection("scrapli_netconf", task.nornir.config)
    has_candidate = _has_candidate(conn)

    # ---------- Stage deletions ----------
    for intf in task.host["interfaces"]:
        name     = intf["name"]
        vlan     = _vlan_from(name)
        loopback = _loopback_from(name)
        tunnel   = _tunnel_from(name)

        if vlan is not None:
            rpc_payload = SVI_RPC_DELETE_TEMPLATE.format(vlan=vlan)
            filter_fn   = _filter_vlan
            ident       = vlan
            label       = f"Vlan{vlan}"

        elif loopback is not None:
            rpc_payload = LOOPBACK_RPC_DELETE_TEMPLATE.format(number=loopback)
            filter_fn   = _filter_loopback
            ident       = loopback
            label       = f"Loopback{loopback}"

        elif tunnel is not None:
            rpc_payload = TUNNEL_RPC_DELETE_TEMPLATE.format(number=tunnel)
            filter_fn   = _filter_tunnel
            ident       = tunnel
            label       = f"Tunnel{tunnel}"

        else:
            log.warning("skipping unsupported interface: %s", name)
            continue

        if has_candidate:
            netconf_edit_config(task, config=rpc_payload, target="candidate")
            staged = netconf_get_config(
                task, source="candidate", filter_=filter_fn(ident)
            )
            if label in staged.result:
                conn.discard()
                raise RuntimeError(f"pre-check failed for deletion of {label}")
            _confirmed_commit(conn, timeout=120)
        else:
            log.warning("no candidate datastore — writing directly to running")
            result_obj = netconf_edit_config(task, config=rpc_payload, target="running")
            if result_obj.failed:
                raise RuntimeError(
                    f"NETCONF edit_config failed for {label}: {result_obj.result[:300]}"
                )

    # ---------- Verify gone from running ----------
    for intf in task.host["interfaces"]:
        name     = intf["name"]
        vlan     = _vlan_from(name)
        loopback = _loopback_from(name)
        tunnel   = _tunnel_from(name)

        if vlan is not None:
            label     = f"Vlan{vlan}"
            filter_fn = _filter_vlan
            ident     = vlan
        elif loopback is not None:
            label     = f"Loopback{loopback}"
            filter_fn = _filter_loopback
            ident     = loopback
        elif tunnel is not None:
            label     = f"Tunnel{tunnel}"
            filter_fn = _filter_tunnel
            ident     = tunnel
        else:
            continue

        running = netconf_get_config(
            task, source="running", filter_=filter_fn(ident)
        )
        if label in running.result:
            raise RuntimeError(f"post-check failed for deletion of {label}")

    if has_candidate:
        conn.commit()

    log.info("delete task done")
    
    

def normalize_platform(raw: Optional[str]) -> str:
    if not raw:
        return "linux"
    r = raw.lower().replace("-", "_")
    if "ios_xe" in r or "iosxe" in r:
        return "cisco_iosxe"
    if "ios" in r:
        return "cisco_ios"
    if "nxos" in r or "nx_os" in r:
        return "cisco_nxos"
    if "junos" in r:
        return "juniper_junos"
    if "huawei" in r or "vrp" in r:
        return "huawei_vrp"
    return r


# ---------- Nornir host builder ----------

def _build_hosts_data(payload: ConfigureRequest) -> list:
    logging.basicConfig(filename="interfaces.log", level=logging.DEBUG, format= "%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    hosts_data = []
    for dev in payload.devices:
        hosts_data.append({
            "name": f"{dev.id}",
            "hostname": dev.management_ip,
            "platform": normalize_platform(dev.platform),
            "username": payload.profile.username,
            "password": payload.profile.password_cipher,
            "port": 830,
            "connection_options": {
                "scrapli_netconf": {                                                         
                    "extras": {                     
                      "auth_strict_key": False,
                      "timeout_socket": 10.0,
                      "timeout_transport": 15.0,
                      "timeout_banner": 30,
                    }
                }
                               
            },           
            "device_id": dev.id,
            "version": dev.version or "",
            "family": dev.family or "",
            "interfaces": [i.dict() for i in dev.interfaces],
            
        })
    return hosts_data


# ---------- Async configure job ----------

def run_config_job(payload: ConfigureRequest):
    set_job_status(payload.job_id, "running")
    log.info("job %s: starting, %d devices", payload.job_id, len(payload.devices))

    try:
        hosts_data = _build_hosts_data(payload)

        nr = InitNornir(
            runner={"plugin": "threaded", "options": {"num_workers": 15}},
            inventory={
                "plugin": "FlatDataInventory",
                "options": {"data": hosts_data},
            },
            
            
        )

        filtered = nr.filter(F(platform="cisco_iosxe"))
        result = filtered.run(task=iosxe_svi_task)

        failed = []
        for host, multi in result.items():
            if multi.failed:
                exc = multi.exception
                msg = f"{host}: {type(exc).__name__}: {exc}"
                failed.append(msg)
                log.error("job %s: %s", payload.job_id, msg)

        if failed:
            raise RuntimeError("tasks failed:\n" + "\n".join(failed))

        set_job_status(payload.job_id, "done")
        log.info("job %s: done", payload.job_id)

    except Exception as e:
        log.exception("job %s: failed", payload.job_id)
        set_job_status(payload.job_id, "failed", str(e))


# ---------- Synchronous delete ----------

def do_delete(payload: ConfigureRequest):
    try:
        hosts_data = _build_hosts_data(payload)

        nr = InitNornir(
            runner={"plugin": "threaded", "options": {"num_workers": 5}},
            inventory={
                "plugin": "FlatDataInventory",
                "options": {"data": hosts_data},
            },
        )

        filtered = nr.filter(F(platform="cisco_iosxe"))
        result = filtered.run(task=iosxe_del_task)

        failed = []
        for host, multi in result.items():
            if multi.failed:
                exc = multi.exception
                msg = f"{host}: {type(exc).__name__}: {exc}"
                failed.append(msg)
                log.error("delete job %s: %s", payload.job_id, msg)

        if failed:
            raise RuntimeError("tasks failed:\n" + "\n".join(failed))

        set_job_status(payload.job_id, "done")
        log.info("delete job %s: done", payload.job_id)

    except Exception as e:
        log.exception("delete job %s: failed", payload.job_id)
        set_job_status(payload.job_id, "failed", str(e))
        raise  # so FastAPI returns 500 → PHP refuses DB delete