# add_vlans.py
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
logging.basicConfig(filename="vlans.log", level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh = logging.FileHandler("vlans.log", mode="a")
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

class Vlan(BaseModel):
    name: str
    id: str

class Device(BaseModel):
    id: str
    management_ip: Optional[str] = None
    platform: Optional[str] = None
    version: Optional[str] = None
    family: Optional[str] = None
    vlans: List[Vlan]

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
    return False


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


def _filter_vlan(vlan_id: str) -> str:
    return (
        '<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">'
        '<vlan>'
        f'<vlan-list xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-vlan"><id>{vlan_id}</id></vlan-list>'
        '</vlan>'
        '</native>'
    )


# ---------- NETCONF XML templates ----------

# NOTE: vlan-list needs its own namespace (Cisco-IOS-XE-vlan), not just native.
VLAN_RPC_TEMPLATE = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <vlan>
      <vlan-list xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-vlan">
        <id>{vlan_id}</id>
        <name>{vlan_name}</name>
      </vlan-list>
    </vlan>
  </native>
</config>
"""

VLAN_RPC_DELETE_TEMPLATE = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <vlan>
      <vlan-list xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-vlan"
                 nc:operation="delete"
                 xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0">
        <id>{vlan_id}</id>
      </vlan-list>
    </vlan>
  </native>
</config>
"""


# ---------- Configure task ----------

def iosxe_vlan_task(task):
    """Configure VLANs on a single IOS-XE device."""
    conn = task.host.get_connection("scrapli_netconf", task.nornir.config)
    has_candidate = _has_candidate(conn)
    log.info("candidate datastore: %s", "YES" if has_candidate else "NO")

    # ---------- Stage: add VLANs ----------
    for vlan in task.host["vlans"]:
        vlan_id   = str(vlan["id"])
        vlan_name = vlan["name"]
        label     = f"Vlan{vlan_id}"

        rpc_payload = VLAN_RPC_TEMPLATE.format(
            vlan_id=vlan_id, vlan_name=vlan_name
        )

        if has_candidate:
            netconf_edit_config(task, config=rpc_payload, target="candidate")
            staged = netconf_get_config(
                task, source="candidate", filter_=_filter_vlan(vlan_id)
            )
            if vlan_id not in staged.result:
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
    for vlan in task.host["vlans"]:
        vlan_id = str(vlan["id"])
        label   = f"Vlan{vlan_id}"

        running = netconf_get_config(
            task, source="running", filter_=_filter_vlan(vlan_id)
        )
        if vlan_id not in running.result:
            raise RuntimeError(f"post-check failed for {label}: vlan_id {vlan_id} not in running")

    if has_candidate:
        conn.commit()
    log.info("configure task done")


# ---------- Delete task ----------

def iosxe_vlan_del_task(task):
    """Remove VLANs from a single IOS-XE device."""
    conn = task.host.get_connection("scrapli_netconf", task.nornir.config)
    has_candidate = _has_candidate(conn)

    # ---------- Stage deletions ----------
    for vlan in task.host["vlans"]:
        vlan_id = str(vlan["id"])
        label   = f"Vlan{vlan_id}"

        rpc_payload = VLAN_RPC_DELETE_TEMPLATE.format(vlan_id=vlan_id)

        if has_candidate:
            netconf_edit_config(task, config=rpc_payload, target="candidate")
            staged = netconf_get_config(
                task, source="candidate", filter_=_filter_vlan(vlan_id)
            )
            if vlan_id in staged.result:
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
    for vlan in task.host["vlans"]:
        vlan_id = str(vlan["id"])
        label   = f"Vlan{vlan_id}"

        running = netconf_get_config(
            task, source="running", filter_=_filter_vlan(vlan_id)
        )
        if vlan_id in running.result:
            raise RuntimeError(f"post-check failed for deletion of {label}")

    if has_candidate:
        conn.commit()

    log.info("delete task done")


# ---------- Platform normalization ----------

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
            "vlans": [v.dict() for v in dev.vlans],
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
        result = filtered.run(task=iosxe_vlan_task)

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
        result = filtered.run(task=iosxe_vlan_del_task)

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