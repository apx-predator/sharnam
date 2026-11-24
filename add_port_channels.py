# add_port_channels.py
import logging
import re
import time
import xml.etree.ElementTree as ET
import mysql.connector
import paramiko

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional

from nornir import InitNornir
from nornir.core.filter import F
from nornir.core.plugins.inventory import InventoryPluginRegister

from nornir_scrapli.tasks import netconf_edit_config, netconf_get_config

from port_channel_xml import TEMPLATES, NATIVE_NS

paramiko.Transport._banner_timeout = 60.0

log = logging.getLogger("configure")
log.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
logging.basicConfig(filename="port_channels.log", level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh = logging.FileHandler("port_channels.log", mode="a")
fh.setFormatter(formatter)
log.addHandler(fh)
sh = logging.StreamHandler()
sh.setFormatter(formatter)
log.addHandler(sh)

app = FastAPI()


# ================================================================
# MODELS
# ================================================================

class Credentials(BaseModel):
    username: str
    password_cipher: str

class Vlan(BaseModel):
    id: str
    name: Optional[str] = ""

class MemberInt(BaseModel):
    int_id: int
    int_name: str

class Device(BaseModel):
    id: str
    management_ip: Optional[str] = None
    platform: Optional[str] = None
    version: Optional[str] = None
    family: Optional[str] = None
    interfaces: Optional[List[MemberInt]] = []

class ConfigureRequest(BaseModel):
    action: Optional[str] = "configure"
    job_id: Optional[str] = None
    profile: Credentials
    operation: str
    details: dict
    devices: List[Device]
    async_: bool = Field(default=False, alias="async")

    model_config = {"populate_by_name": True}


# ================================================================
# DB HELPERS
# ================================================================

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


# ================================================================
# GENERAL HELPERS
# ================================================================

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
    return any("candidate" in str(cap).lower() for cap in caps)


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
    return ",".join(str(v["id"]) for v in vlans if v.get("id"))


def _filter_po(po_number: str) -> str:
    return (
        f'<native xmlns="{NATIVE_NS}">'
        f'<interface><Port-channel><name>{po_number}</name></Port-channel></interface>'
        '</native>'
    )


def _filter_physical(parent: str, child: str) -> str:
    return (
        f'<native xmlns="{NATIVE_NS}">'
        f'<interface><{parent}><name>{child}</name></{parent}></interface>'
        '</native>'
    )


def _parse_vlans_from_running(xml: str) -> List[str]:
    m = re.search(r"<vlans>([^<]+)</vlans>", xml)
    if not m:
        return []
    raw = m.group(1).strip()
    return [v.strip() for v in raw.split(",") if v.strip()] if raw else []


def _merge_vlans(current: List[str], incoming: List[str], action: str) -> List[str]:
    if action == "replace":
        return list(incoming)
    if action == "add":
        return list(dict.fromkeys(current + incoming))
    if action == "except":
        return [v for v in current if v not in incoming]
    return list(incoming)


def _opt(value, template_name: str, version: str, **kw) -> str:
    if value is None or value == "" or value == [] or value is False:
        return ""
    tpl = TEMPLATES[template_name][version]
    if not tpl:
        return ""
    return tpl.format(**kw)


_INTERFACE_RE = re.compile(
    r"^(?P<parent>[A-Za-z][A-Za-z\-]+)(?P<child>[0-9][0-9/\.:]*)$"
)

def parse_interface_name(int_name: str):
    m = _INTERFACE_RE.match(int_name.strip())
    if not m:
        return (None, None)
    return (m.group("parent"), m.group("child"))


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


# ================================================================
# VERSION DETECTION
# ================================================================

def _version_family(version: Optional[str]) -> str:
    if not version:
        return "unknown"
    v = str(version).strip()
    m = re.match(r"^(\d+)\.(\d+)", v)
    if not m:
        return "unknown"
    major, minor = int(m.group(1)), int(m.group(2))
    if major == 16:
        return "1612"
    if major == 17:
        if minor <= 4:
            return "173"
        if minor <= 7:
            return "176"
        if minor <= 10:
            return "179"
        if minor <= 13:
            return "1712"
        return "1715"
    return "unknown"


def _attempt_order(version: Optional[str]) -> List[str]:
    family = _version_family(version)
    orders = {
        "1715": ["1715", "1712", "179", "176", "173", "1612"],
        "1712": ["1712", "1715", "179", "176", "173", "1612"],
        "179":  ["179",  "1712", "1715", "176", "173", "1612"],
        "176":  ["176",  "179",  "1712", "1715", "173", "1612"],
        "173":  ["173",  "176",  "179",  "1712", "1715", "1612"],
        "1612": ["1612", "173",  "176",  "179",  "1712", "1715"],
        "unknown": ["1715", "1712", "179", "176", "173", "1612"],
    }
    return orders[family]


# ================================================================
# STATE READERS
# ================================================================

_SWITCHPORT_FALSE_RE = re.compile(
    r"<switchport-conf>\s*<switchport>false</switchport>\s*</switchport-conf>",
    re.IGNORECASE,
)
_SWITCHPORT_ANY_RE = re.compile(
    r"<switchport-config\b|<switchport\b",
    re.IGNORECASE,
)

def _po_is_l3(running_xml: str) -> bool:
    if _SWITCHPORT_FALSE_RE.search(running_xml):
        return True
    if _SWITCHPORT_ANY_RE.search(running_xml):
        return False
    return True


def _get_po_running(task, po):
    try:
        return netconf_get_config(task, source="running", filter_=_filter_po(po)).result or ""
    except Exception as e:
        log.warning("[%s] get_config Po%s failed: %s", task.host.name, po, e)
        return ""


def _get_all_interfaces_running(task):
    try:
        return netconf_get_config(task, source="running").result or ""
    except Exception as e:
        log.warning("[%s] get_config (all) failed: %s", task.host.name, e)
        return ""


# ================================================================
# MEMBER EXTRACTOR — XML-tree based, no interface type names
# ================================================================

_ETH_NS = "http://cisco.com/ns/yang/Cisco-IOS-XE-ethernet"

_IFACE_CONTAINER_SKIP = {
    "Port-channel-subinterface",
}


def _local_tag(el) -> str:
    """Return the element's tag without namespace, or '' if not an element."""
    if not isinstance(el.tag, str):
        return ""
    return el.tag.split("}")[-1]


def _extract_po_members(running_xml: str, target_po) -> list:
    """
    Return every (parent, child) interface bound to target_po.

    Walks /native/interface in the running config, and for each child
    element (GigabitEthernet, TenGigabitEthernet, TwentyFiveGigE,
    FortyGigabitEthernet, HundredGigE, or any future interface type),
    checks whether it has <name> and a <channel-group><number> equal
    to target_po.

    No interface type names are guessed or hardcoded.
    """
    target = str(target_po)
    members = []
    seen = set()

    if not running_xml or not running_xml.strip():
        return members

    try:
        root = ET.fromstring(running_xml)
    except ET.ParseError as e:
        log.warning("[member_extract] running config not valid XML: %s", e)
        return members

    # Collect every <interface> container anywhere in the tree,
    # regardless of namespace prefix on the reply wrapper.
    interface_containers = [
        el for el in root.iter()
        if _local_tag(el) == "interface"
    ]

    if not interface_containers:
        log.warning("[member_extract] no <interface> element in running config; "
                    "top-level tags: %s", [_local_tag(c) for c in root])
        return members

    for container in interface_containers:
        for iface in container:
            itype = _local_tag(iface)
            if not itype or itype in _IFACE_CONTAINER_SKIP:
                continue

            # Locate <name> regardless of namespace
            name_el = None
            for child_el in iface:
                if _local_tag(child_el) == "name":
                    name_el = child_el
                    break
            if name_el is None or not name_el.text:
                continue
            child = name_el.text.strip()

            # Locate <channel-group><number> regardless of namespace
            for cg in iface:
                if _local_tag(cg) != "channel-group":
                    continue

                num_el = None
                for cgc in cg:
                    if _local_tag(cgc) == "number":
                        num_el = cgc
                        break
                if num_el is None or not num_el.text:
                    continue

                if num_el.text.strip() == target:
                    key = (itype, child)
                    if key not in seen:
                        seen.add(key)
                        members.append(key)
                break   # one channel-group per interface; done with this one

    return members


# ================================================================
# BUILDERS
# ================================================================

def _desc_block(desc, version):
    return _opt(desc, "DESC_BLOCK", version, desc=desc or "")

def _lb_block(lb, version):
    return _opt(lb, "LB_BLOCK", version, lb=lb or "")

def _min_links_block(min_links, version):
    return _opt(min_links, "MIN_LINKS_BLOCK", version, min_links=min_links)

def _native_block(native_vlan, version):
    return _opt(native_vlan, "NATIVE_BLOCK", version, native_vlan=native_vlan)


def _allowed_block(vlans_str, action, version):
    if action == "add":
        tpl = TEMPLATES["ALLOWED_ADD"][version]
    elif action == "except":
        tpl = TEMPLATES["ALLOWED_EXCEPT"][version]
    else:
        tpl = TEMPLATES["ALLOWED_REPLACE"][version]
    if not tpl:
        tpl = TEMPLATES["ALLOWED_REPLACE"][version]
    return tpl.format(vlans=vlans_str)


def build_trunk(version, po, desc, vlans_str, action, native_vlan, min_links, lb):
    desc_blk    = _desc_block(desc, version)
    lb_blk      = _lb_block(lb, version)
    ml_blk      = _min_links_block(min_links, version)
    native_blk  = _native_block(native_vlan, version)
    allowed_blk = _allowed_block(vlans_str, action, version)

    payloads = []
    if version in ("1612", "176", "179"):
        payloads.append(TEMPLATES["PO_L2_INIT"][version].format(
            po=po, desc_block=desc_blk, lb_block=lb_blk, min_links_block=ml_blk,
        ))
    payloads.append(TEMPLATES["PO_L2_TRUNK"][version].format(
        po=po, desc_block=desc_blk, lb_block=lb_blk, min_links_block=ml_blk,
        allowed_block=allowed_blk, native_block=native_blk,
    ))
    return payloads


def build_access(version, po, desc, vlan, min_links, lb):
    desc_blk = _desc_block(desc, version)
    lb_blk   = _lb_block(lb, version)
    ml_blk   = _min_links_block(min_links, version)

    payloads = []
    if version in ("1612", "176", "179"):
        payloads.append(TEMPLATES["PO_L2_INIT"][version].format(
            po=po, desc_block=desc_blk, lb_block=lb_blk, min_links_block=ml_blk,
        ))
    payloads.append(TEMPLATES["PO_L2_ACCESS"][version].format(
        po=po, desc_block=desc_blk, lb_block=lb_blk,
        min_links_block=ml_blk, vlan=vlan,
    ))
    return payloads


def build_l3(version, po, desc, ip, mask, min_links, lb):
    desc_blk = _desc_block(desc, version)
    lb_blk   = _lb_block(lb, version)
    ml_blk   = _min_links_block(min_links, version)
    return [TEMPLATES["PO_L3"][version].format(
        po=po, desc_block=desc_blk, lb_block=lb_blk,
        min_links_block=ml_blk, ip=ip, mask=mask,
    )]


def build_member(version, parent, child, po, mode, po_is_l3):
    key = "MEMBER_L3" if po_is_l3 else "MEMBER"
    return [TEMPLATES[key][version].format(
        parent=parent, child=child, po=po, mode=mode,
    )]


def build_member_unbind(version, parent, child):
    return [TEMPLATES["MEMBER_UNBIND"][version].format(
        parent=parent, child=child,
    )]


def build_subif(version, po, sub, vlan_tag, ip, mask, desc):
    desc_blk = _desc_block(desc, version)
    return [TEMPLATES["PO_SUBIF"][version].format(
        po=po, sub=sub, vlan_tag=vlan_tag, ip=ip, mask=mask,
        desc_block=desc_blk,
    )]


def build_delete(version, po):
    return [TEMPLATES["PO_DELETE"][version].format(po=po)]


# ================================================================
# PUSH HELPERS
# ================================================================

def _reset_connection(task):
    try:
        task.host.close_connection("scrapli_netconf")
    except Exception:
        pass


def _try_edit(task, conn, rpc_payload, filter_xml, label, has_candidate):
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
            _reset_connection(task)
            return False, f"{type(e).__name__}: {e}"
    else:
        try:
            result_obj = netconf_edit_config(task, config=rpc_payload, target="running")
            if getattr(result_obj, "failed", False):
                _reset_connection(task)
                return False, (str(result_obj.result) or "")[:300]
            return True, ""
        except Exception as e:
            _reset_connection(task)
            return False, f"{type(e).__name__}: {e}"


def _try_with_fallback(task, conn, filter_xml, label, has_candidate,
                       build_fn, version):
    errors = []
    for family in _attempt_order(version):
        try:
            payloads = build_fn(family)
        except Exception as e:
            errors.append(f"variant {family}: build error: {e}")
            log.warning("[%s] %s build failed on variant %s: %s",
                        task.host.name, label, family, e)
            continue

        ok_all = True
        for idx, payload in enumerate(payloads):
            ok, err = _try_edit(task, conn, payload, filter_xml, label, has_candidate)
            if not ok:
                errors.append(f"variant {family} step {idx+1}: {err}")
                log.warning("[%s] %s failed on variant %s step %d: %s",
                            task.host.name, label, family, idx + 1, err)
                ok_all = False
                break
        if ok_all:
            log.info("[%s] %s OK (variant %s)", task.host.name, label, family)
            return True, errors

        time.sleep(1.5)

    return False, errors


# ================================================================
# VERSION-AWARE PRE-MERGE
# ================================================================

def _resolve_vlans_for_version(task, conn, version, action, vlans_str, filter_xml):
    if action not in ("add", "except"):
        return vlans_str

    key = "ALLOWED_ADD" if action == "add" else "ALLOWED_EXCEPT"
    if TEMPLATES[key][version]:
        return vlans_str

    try:
        current_xml = netconf_get_config(task, source="running", filter_=filter_xml).result or ""
        current = _parse_vlans_from_running(current_xml)
        incoming = [v.strip() for v in vlans_str.split(",") if v.strip()]
        merged = _merge_vlans(current, incoming, action)
        return ",".join(merged)
    except Exception as e:
        log.warning("[%s] pre-merge failed (%s); falling back to raw vlans",
                    task.host.name, e)
        return vlans_str


# ================================================================
# TASK
# ================================================================

def iosxe_port_channel_task(task):
    conn = task.host.get_connection("scrapli_netconf", task.nornir.config)
    has_candidate = _has_candidate(conn)
    log.info("[%s] candidate: %s", task.host.name, "YES" if has_candidate else "NO")

    operation = task.host["operation"]
    details   = task.host["details"]
    version   = task.host["version"]

    po = str(details.get("portchannel_name", "") or details.get("po_number", ""))
    if not po:
        raise RuntimeError(f"[{task.host.name}] portchannel_name missing")

    log.info("[%s] op=%s po=%s version=%s", task.host.name, operation, po, version)

    filter_xml = _filter_po(po)

    # ------------------------------------------------------------
    # 1) PORTCREATION
    # ------------------------------------------------------------
    if operation == "portcreation":
        mode = details["mode"]
        desc = details.get("description") or ""
        min_links = details.get("min_links")
        lb = details.get("lb")

        if mode == "trunk":
            vlans_str = _vlans_to_string(details.get("vlans") or [])
            if not vlans_str:
                raise RuntimeError(f"[{task.host.name}] trunk needs vlans")
            native_vlan = details.get("native_vlan")
            action = (details.get("vlan_action") or "replace").lower()

            def build(family):
                final_vlans = _resolve_vlans_for_version(
                    task, conn, family, action, vlans_str, filter_xml
                )
                return build_trunk(family, po, desc, final_vlans, action,
                                   native_vlan, min_links, lb)
        else:
            vlan = str(details.get("access_vlan", "") or "")
            if not vlan:
                raise RuntimeError(f"[{task.host.name}] access needs access_vlan")

            def build(family):
                return build_access(family, po, desc, vlan, min_links, lb)

        ok, errors = _try_with_fallback(
            task, conn, filter_xml, f"Port-channel{po}",
            has_candidate, build, version
        )
        if not ok:
            raise RuntimeError(
                f"portcreation failed for Port-channel{po} on {task.host.name}:\n"
                + "\n".join(errors)
            )

    # ------------------------------------------------------------
    # 2) MEMBERCREATION
    # ------------------------------------------------------------
    elif operation == "membercreation":
        mode = details.get("mode") or "active"
        members = task.host.get("interfaces") or []
        if not members:
            raise RuntimeError(f"[{task.host.name}] no members selected")

        po_xml = _get_po_running(task, po)
        po_is_l3 = _po_is_l3(po_xml)
        log.info("[%s] Po%s detected as %s",
                 task.host.name, po,
                 "L3 (routed)" if po_is_l3 else "L2 (switchport)")

        for m in members:
            int_name = m["int_name"]
            parent, child = parse_interface_name(int_name)
            if parent is None:
                log.warning("[%s] cannot parse %s — skipping",
                            task.host.name, int_name)
                continue

            filter_member = _filter_physical(parent, child)

            def build(family, p=parent, c=child, l3=po_is_l3):
                return build_member(family, p, c, po, mode, l3)

            ok, errors = _try_with_fallback(
                task, conn, filter_member, f"{int_name}->Po{po}",
                has_candidate, build, version
            )
            if not ok:
                raise RuntimeError(
                    f"membercreation failed for {int_name} on {task.host.name}:\n"
                    + "\n".join(errors)
                )

    # ------------------------------------------------------------
    # 3) L3PORTCHANNEL
    # ------------------------------------------------------------
    elif operation == "l3portchannel":
        ip    = details["primary_ip"]
        mask  = details["primary_mask"]
        desc  = details.get("description") or ""
        ml    = details.get("min_links")
        lb    = details.get("lb")

        def build(family):
            return build_l3(family, po, desc, ip, mask, ml, lb)

        ok, errors = _try_with_fallback(
            task, conn, filter_xml, f"L3 Port-channel{po}",
            has_candidate, build, version
        )
        if not ok:
            raise RuntimeError(
                f"l3portchannel failed for Port-channel{po} on {task.host.name}:\n"
                + "\n".join(errors)
            )

    # ------------------------------------------------------------
    # 4) L3SUBINTERFACES
    # ------------------------------------------------------------
    elif operation == "l3subinterfaces":
        subs = details.get("subinterfaces") or []
        if not subs:
            raise RuntimeError(f"[{task.host.name}] no subinterfaces")

        for si in subs:
            sub      = si["vlan"]
            vlan_tag = si["vlan"]
            ip       = si["ip"]
            mask     = si["netmask"]
            desc     = si.get("desc") or ""

            filter_sub = _filter_po(f"{po}.{sub}")

            def build(family, s=sub, v=vlan_tag, i=ip, mk=mask, d=desc):
                return build_subif(family, po, s, v, i, mk, d)

            ok, errors = _try_with_fallback(
                task, conn, filter_sub, f"Po{po}.{sub}",
                has_candidate, build, version
            )
            if not ok:
                raise RuntimeError(
                    f"l3subinterfaces failed for Po{po}.{sub} on {task.host.name}:\n"
                    + "\n".join(errors)
                )

    # ------------------------------------------------------------
    # 5) PORTABOLISH
    # ------------------------------------------------------------
    elif operation == "portabolish":

        # Step 0: discover members (XML tree, no type-name guessing)
        all_xml = _get_all_interfaces_running(task)
        members = _extract_po_members(all_xml, po)
        log.info("[%s] found %d member(s) bound to Po%s",
                 task.host.name, len(members), po)

        # Step 1: unbind each member
        unbind_failures = []
        for parent, child in members:
            filter_m = _filter_physical(parent, child)

            def build(family, p=parent, c=child):
                return build_member_unbind(family, p, c)

            ok, errs = _try_with_fallback(
                task, conn, filter_m, f"unbind {parent}{child} from Po{po}",
                has_candidate, build, version
            )
            if not ok:
                unbind_failures.append((parent, child, errs))
                log.warning("[%s] could not unbind %s%s from Po%s: %s",
                            task.host.name, parent, child, po, errs)

        if unbind_failures:
            raise RuntimeError(
                f"portabolish: could not unbind all members of Po{po} on "
                f"{task.host.name}:\n"
                + "\n".join(f"  {p}{c}: {e}" for p, c, e in unbind_failures)
            )

        # Step 2: give device time, then verify zero members remain
        if members:
            time.sleep(3)
            all_after = _get_all_interfaces_running(task)
            remaining = _extract_po_members(all_after, po)
            if remaining:
                raise RuntimeError(
                    f"portabolish: Po{po} on {task.host.name} still has "
                    f"{len(remaining)} member(s) bound after unbind: {remaining}. "
                    f"Refusing to delete Po while members remain."
                )
            log.info("[%s] verified 0 members bound to Po%s before delete",
                     task.host.name, po)

        # Step 3: delete the Port-channel
        def build_delete_(family):
            return build_delete(family, po)

        ok, errs = _try_with_fallback(
            task, conn, filter_xml, f"delete Port-channel{po}",
            has_candidate, build_delete_, version
        )
        if not ok:
            raise RuntimeError(
                f"portabolish failed for Port-channel{po} on {task.host.name}:\n"
                + "\n".join(errs)
            )

        log.info("[%s] portabolish Po%s complete", task.host.name, po)

    else:
        raise RuntimeError(f"[{task.host.name}] unknown operation '{operation}'")

    log.info("[%s] %s task done", task.host.name, operation)


# ================================================================
# NORNIR HOST BUILDER
# ================================================================

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
            "interfaces": [i.dict() for i in (dev.interfaces or [])],
            "operation": payload.operation,
            "details": payload.details,
        })
    return hosts_data


# ================================================================
# RUNNER
# ================================================================

def run_config_job(payload: ConfigureRequest):
    set_job_status(payload.job_id, "running")
    log.info("job %s: starting, %d devices, op=%s",
             payload.job_id, len(payload.devices), payload.operation)

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
        result = filtered.run(task=iosxe_port_channel_task)

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