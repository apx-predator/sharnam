# add_trunks_access.py
import logging
import re
import mysql.connector
import paramiko

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional

from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.plugins.inventory import InventoryPluginRegister

from nornir_scrapli.tasks import netconf_edit_config, netconf_get_config

paramiko.Transport._banner_timeout = 60.0

# Log to both file and stdout
log = logging.getLogger("configure")
log.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
logging.basicConfig(filename="trunks_access.log", level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh = logging.FileHandler("trunks_access.log", mode="a")
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
    id: str
    name: Optional[str] = ""

class Port(BaseModel):
    int_id: int
    int_name: str

class Device(BaseModel):
    id: str
    management_ip: Optional[str] = None
    platform: Optional[str] = None
    version: Optional[str] = None
    family: Optional[str] = None
    ports: List[Port]

class ConfigureRequest(BaseModel):
    action: Optional[str] = "configure"
    job_id: Optional[str] = None
    profile: Credentials
    mode: str                                    # "access" | "trunk"
    vlans: List[Vlan]
    vlan_action: Optional[str] = "replace"       # add | except | replace
    native_vlan: Optional[str] = None
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


# ---------- Interface name parser ----------

_INTERFACE_RE = re.compile(
    r"^(?P<parent>[A-Za-z][A-Za-z\-]+)(?P<child>[0-9][0-9/\.:]*)$"
)

def parse_interface_name(int_name: str):
    """
    'GigabitEthernet1/0/1'      -> ('GigabitEthernet', '1/0/1')
    'TenGigabitEthernet1/0/1'   -> ('TenGigabitEthernet', '1/0/1')
    'Port-channel10'            -> ('Port-channel', '10')
    'TwentyFiveGigE1/0/1'       -> ('TwentyFiveGigE', '1/0/1')
    Returns (None, None) if unparseable.
    """
    m = _INTERFACE_RE.match(int_name.strip())
    if not m:
        return (None, None)
    return (m.group("parent"), m.group("child"))


# ---------- Helpers ----------

def _has_candidate(conn) -> bool:
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
    conn.send_rpc(
        payload=(
            '<rpc message-id="102" xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">'
            f'<commit><confirmed/><confirm-timeout>{timeout}</confirm-timeout></commit>'
            '</rpc>'
        ),
        operation="commit",
    )


def _vlans_to_string(vlans: List[dict]) -> str:
    """[{'id':'10'},{'id':'20'},{'id':'30-40'}] -> '10,20,30-40'"""
    return ",".join(str(v["id"]) for v in vlans if v.get("id"))


def _filter_interface(parent: str, child: str) -> str:
    return (
        '<native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">'
        f'<interface><{parent}><name>{child}</name></{parent}></interface>'
        '</native>'
    )


def _parse_vlans_from_running(xml: str) -> List[str]:
    """Extract comma-separated VLAN IDs from a get_config reply."""
    m = re.search(r"<vlans>([^<]+)</vlans>", xml)
    if not m:
        return []
    raw = m.group(1).strip()
    if not raw:
        return []
    return [v.strip() for v in raw.split(",") if v.strip()]


def _merge_vlans(current: List[str], incoming: List[str], action: str) -> List[str]:
    """Client-side merge — used by the 16.12 variant which lacks add/remove XML ops."""
    if action == "replace":
        return list(incoming)
    if action == "add":
        return list(dict.fromkeys(current + incoming))   # dedupe, preserve order
    if action == "except":
        return [v for v in current if v not in incoming]
    return list(incoming)


# ---------- NETCONF XML templates ----------
#
# Variant 17: switchport-config wrapper + vlan-v2 (add-vlans / remove)
# Variant 16: no wrapper + vlan-choice/vlans (client-side merge)


# ---- ACCESS (identical across versions) ----

SWITCHPORT_ACCESS_TEMPLATE = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <{parent}>
        <name>{child}</name>
        <switchport-config>
          <switchport>
            <mode xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-switch">
              <access/>
            </mode>
            <access xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-switch">
              <vlan>
                <vlan>{vlan_id}</vlan>
              </vlan>
            </access>
          </switchport>
        </switchport-config>
      </{parent}>
    </interface>
  </native>
</config>
"""


# ---- TRUNK variant 17 ----

_SW_NS = "http://cisco.com/ns/yang/Cisco-IOS-XE-switch"

_TRUNK_17_BASE = f"""
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <{{parent}}>
        <name>{{child}}</name>
        <switchport-config>
          <switchport>
            <mode xmlns="{_SW_NS}">
              <trunk/>
            </mode>
            <trunk xmlns="{_SW_NS}">
              {{allowed_block}}
              {{native_block}}
            </trunk>
          </switchport>
        </switchport-config>
      </{{parent}}>
    </interface>
  </native>
</config>
"""

# Replace the list: "switchport trunk allowed vlan 10,20"
_ALLOWED_17_REPLACE = (
    "<allowed><vlan-v2><vlan-choices>"
    "<vlans>{vlans}</vlans>"
    "</vlan-choices></vlan-v2></allowed>"
)

# "switchport trunk allowed vlan add 30"
_ALLOWED_17_ADD = (
    "<allowed><vlan-v2><add-vlans>"
    "<add><vlans>{vlans}</vlans></add>"
    "</add-vlans></vlan-v2></allowed>"
)

# "switchport trunk allowed vlan except 10,20"
_ALLOWED_17_EXCEPT = (
    "<allowed><vlan-v2>"
    "<except>{vlans}</except>"
    "</vlan-v2></allowed>"
)

# (optional) "switchport trunk allowed vlan remove 30"
_ALLOWED_17_REMOVE = (
    "<allowed><vlan-v2>"
    "<remove>{vlans}</remove>"
    "</vlan-v2></allowed>"
)

# "switchport trunk allowed vlan none"
_ALLOWED_17_NONE = (
    "<allowed><vlan-v2><vlan-choices><none/></vlan-choices></vlan-v2></allowed>"
)

_NATIVE_17 = (
    "<native><vlan><vlan-id>{native_vlan}</vlan-id></vlan></native>"
)


# ---- TRUNK variant 16 ----

_TRUNK_16_BASE = """
<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <interface>
      <{parent}>
        <name>{child}</name>
        <switchport-config>
         <switchport>
          <mode xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-switch">
            <trunk/>
          </mode>
          <trunk xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-switch">
            <allowed>
              <vlan>               
                  <vlans>{vlans}</vlans>               
              </vlan>
            </allowed>
            {native_block}
          </trunk>
         </switchport>
        </switchport-config>
      </{parent}>
    </interface>
  </native>
</config>
"""

_NATIVE_16 = (
    "<native>"
    "<vlan>"         
    "<vlan-id>{native_vlan}</vlan-id>"
    "</vlan>"
    "</native>"
)


# ---- Builders ----

def _build_trunk_17(parent: str, child: str, vlans_str: str,
                    action: str, native_vlan: Optional[str]) -> str:
    if action == "add":
        allowed_block = _ALLOWED_17_ADD.format(vlans=vlans_str)
    elif action == "except":
        allowed_block = _ALLOWED_17_EXCEPT.format(vlans=vlans_str)
    else:
        allowed_block = _ALLOWED_17_REPLACE.format(vlans=vlans_str)

    native_block = _NATIVE_17.format(native_vlan=native_vlan) if native_vlan else ""

    return _TRUNK_17_BASE.format(
        parent=parent, child=child,
        allowed_block=allowed_block, native_block=native_block,
    )


def _build_trunk_16(parent: str, child: str, vlans_str: str,
                    native_vlan: Optional[str]) -> str:
    # 16.12 has no add/except; vlans_str is already the merged final list
    native_block = _NATIVE_16.format(native_vlan=native_vlan) if native_vlan else ""

    return _TRUNK_16_BASE.format(
        parent=parent, child=child,
        vlans=vlans_str, native_block=native_block,
    )


def _build_access_payload(parent: str, child: str, vlan_id: str) -> str:
    return SWITCHPORT_ACCESS_TEMPLATE.format(
        parent=parent, child=child, vlan_id=vlan_id
    )


# ---------- Push helper (per-port, per-variant) ----------

def _try_edit(task, conn, rpc_payload, filter_xml, label, has_candidate):
    """
    Push one payload. Returns (success: bool, error_msg: str).
    Handles candidate discard on failure so the next variant starts clean.
    """
    if has_candidate:
        try:
            netconf_edit_config(task, config=rpc_payload, target="candidate")
            _confirmed_commit(conn, timeout=120)
            conn.commit()
            return True, ""
        except Exception as e:
            try:
                conn.discard()
            except Exception:
                pass
            return False, f"{type(e).__name__}: {e}"
    else:
        try:
            result_obj = netconf_edit_config(task, config=rpc_payload, target="running")
            if getattr(result_obj, "failed", False):
                return False, (str(result_obj.result) or "")[:300]
            return True, ""
        except Exception as e:
            return False, f"{type(e).__name__}: {e}"


# ---------- Configure task ----------

def iosxe_switchport_task(task):
    """Configure access or trunk switchport on a device's ports.

    Trunk mode: try 17.x variant first, fall back to 16.12 variant.
    Access mode: single template (works on both version families).
    """
    conn = task.host.get_connection("scrapli_netconf", task.nornir.config)
    has_candidate = _has_candidate(conn)
    log.info("[%s] candidate: %s", task.host.name, "YES" if has_candidate else "NO")

    mode        = task.host["mode"]
    vlans       = task.host["vlans"]
    vlan_action = task.host["vlan_action"] or "replace"
    native_vlan = task.host["native_vlan"]

    log.info("[%s] mode=%s action=%s native=%s",
             task.host.name, mode, vlan_action, native_vlan)

    incoming_str = _vlans_to_string(vlans)
    if not incoming_str:
        log.warning("[%s] no vlans — skipping", task.host.name)
        return

    first_vlan = str(vlans[0]["id"]) if vlans else None

    # ---------- Stage: push config ----------
    for port in task.host["ports"]:
        int_name = port["int_name"]
        parent, child = parse_interface_name(int_name)

        if parent is None:
            log.warning("[%s] cannot parse %s — skipping", task.host.name, int_name)
            continue

        label = int_name
        filter_xml = _filter_interface(parent, child)

        # ---- ACCESS MODE ----
        if mode == "access":
            if not first_vlan:
                log.warning("[%s] access with no vlans — skipping %s",
                            task.host.name, label)
                continue
            rpc_payload = _build_access_payload(parent, child, first_vlan)
            ok, err = _try_edit(task, conn, rpc_payload, filter_xml, label, has_candidate)
            if not ok:
                raise RuntimeError(f"access config failed for {label}: {err}")
            log.info("[%s] access OK on %s", task.host.name, label)
            continue

        # ---- TRUNK MODE (with fallback) ----
        # Attempt 1: 17.x variant
        rpc_17 = _build_trunk_17(parent, child, incoming_str, vlan_action, native_vlan)
        ok_17, err_17 = _try_edit(task, conn, rpc_17, filter_xml, label, has_candidate)

        if ok_17:
            log.info("[%s] trunk OK on %s (variant 17)", task.host.name, label)
            continue

        # Attempt 2: 16.x variant
        log.warning("[%s] variant 17 failed on %s — trying variant 16: %s",
                    task.host.name, label, err_17)

        if vlan_action in ("add", "except"):
            try:
                current_xml = netconf_get_config(
                    task, source="running", filter_=filter_xml
                ).result or ""
                current = _parse_vlans_from_running(current_xml)
                merged = _merge_vlans(current, incoming_str.split(","), vlan_action)
                payload_vlans = ",".join(merged)
            except Exception as e:
                log.warning("[%s] could not read current vlans for %s: %s",
                            task.host.name, label, e)
                payload_vlans = incoming_str
        else:
            payload_vlans = incoming_str

        rpc_16 = _build_trunk_16(parent, child, payload_vlans, native_vlan)
        ok_16, err_16 = _try_edit(task, conn, rpc_16, filter_xml, label, has_candidate)

        if ok_16:
            log.info("[%s] trunk OK on %s (variant 16 fallback)", task.host.name, label)
            continue

        # Both variants failed
        raise RuntimeError(
            f"trunk config failed for {label} on {task.host.name}:\n"
            f"  variant 17: {err_17}\n"
            f"  variant 16: {err_16}"
        )

    # ---------- Verify ----------
    for port in task.host["ports"]:
        int_name = port["int_name"]
        parent, child = parse_interface_name(int_name)
        if parent is None:
            continue
        running = netconf_get_config(
            task, source="running", filter_=_filter_interface(parent, child)
        )
        if child not in (running.result or ""):
            raise RuntimeError(f"post-check failed for {int_name}: not in running")

    log.info("[%s] configure task done", task.host.name)


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
            "ports": [p.dict() for p in dev.ports],
            # global settings — copied per host
            "mode": payload.mode,
            "vlans": [v.dict() for v in payload.vlans],
            "vlan_action": payload.vlan_action,
            "native_vlan": payload.native_vlan,
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
        result = filtered.run(task=iosxe_switchport_task)

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