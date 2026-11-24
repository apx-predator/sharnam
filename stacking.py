# stack.py
#
# StackWise (back-panel), StackWise Virtual (front-panel) and
# Dual-Active Detection (DAD) configuration over NETCONF + CLI.
#
# Framework: mirrors add_port_channels.py
#   - Nornir threaded runner, FlatDataInventory
#   - scrapli_netconf for edit-config
#   - scrapli (SSH)  for CLI: priority, renumber, write memory, reload, verify
#
# Compatibility: 16.12 → 17.15. All XML payloads live in stack_xml.TEMPLATES
# and are shape-identical across trains; version-sensitive VALUES (switch
# number range, SKU enum, interface types) are the caller's responsibility.
#
# Operations dispatched by task.host["operation"]:
#   back-panel  → priority CLI → provision NETCONF → stack-mac NETCONF
#                 → save → verify
#   front-panel → force master=1, standby=2 + priorities CLI (both)
#                 → domain NETCONF (both) → link NETCONF (both)
#                 → stack-mac NETCONF (both, timer=0)
#                 → save (both) → verify (pre-reload) → reload standby
#   dad         → pre-check ports not SVL links → DAD NETCONF (both)
#                 → save (both) → verify
#
# All verification is CLI-based and MANDATORY — the job fails if expected
# state isn't observed.

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

from nornir_scrapli.tasks import (
    netconf_edit_config,
    send_command as cli_send_command,
    send_config as cli_send_config,
)

from stack_xml import (
    TEMPLATES,
    NC_NS, NATIVE_NS, SW_NS, SV_NS,
)

paramiko.Transport._banner_timeout = 60.0

log = logging.getLogger("stack")
log.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
logging.basicConfig(filename="stack.log", level=logging.DEBUG,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh = logging.FileHandler("stack.log", mode="a")
fh.setFormatter(formatter)
log.addHandler(fh)
sh = logging.StreamHandler()
sh.setFormatter(formatter)
log.addHandler(sh)

app = FastAPI()


# ================================================================
# MODELS (same surface as add_port_channels.py)
# ================================================================

class Credentials(BaseModel):
    username: str
    password_cipher: str

class Port(BaseModel):
    int_id: int
    int_name: str

class Device(BaseModel):
    id: str
    management_ip: Optional[str] = None
    platform: Optional[str] = None
    version: Optional[str] = None
    family: Optional[str] = None
    ports: Optional[List[Port]] = []

class StackRequest(BaseModel):
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
# GENERAL HELPERS (mirrors add_port_channels.py)
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


def _reset_netconf(task):
    try:
        task.host.close_connection("scrapli_netconf")
    except Exception:
        pass


def _try_edit(task, conn, rpc_payload, label, has_candidate):
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
            _reset_netconf(task)
            return False, f"{type(e).__name__}: {e}"
    else:
        try:
            result_obj = netconf_edit_config(task, config=rpc_payload, target="running")
            if getattr(result_obj, "failed", False):
                _reset_netconf(task)
                return False, (str(result_obj.result) or "")[:300]
            return True, ""
        except Exception as e:
            _reset_netconf(task)
            return False, f"{type(e).__name__}: {e}"


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
        if minor <= 4:   return "173"
        if minor <= 7:   return "176"
        if minor <= 10:  return "179"
        if minor <= 13:  return "1712"
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


def _local_tag(el) -> str:
    if not isinstance(el.tag, str):
        return ""
    return el.tag.split("}")[-1]


# ================================================================
# CLI HELPERS (scrapli)
# ================================================================

def _cli(task, cmd: str, confirm: bool = False, timeout: int = 30) -> str:
    """Run a single CLI command. If confirm=True, expect a [confirm] prompt
    and send a newline in response."""
    result = cli_send_command(task, command=cmd)
    text = result.result or ""
    if confirm and "[confirm]" in text.lower():
        more = cli_send_command(task, command="\n")
        text += more.result or ""
    return text


def _cli_config(task, lines: List[str]) -> str:
    """Enter config mode, send lines, exit. Returns concatenated output."""
    cmds = ["configure terminal"] + lines + ["end"]
    result = cli_send_config(task, configuration="\n".join(cmds))
    return result.result or ""


def _cli_priority(task, num: int, prio: int) -> None:
    out = _cli(task, f"switch {num} priority {prio}", confirm=True)
    log.info("[%s] switch %d priority %d: %s",
             task.host.name, num, prio, out.strip()[:120])


def _cli_renumber(task, old: int, new: int) -> None:
    out = _cli(task, f"switch {old} renumber {new}", confirm=True)
    log.info("[%s] switch %d renumber %d: %s",
             task.host.name, old, new, out.strip()[:120])


def _cli_save(task) -> None:
    out = _cli(task, "write memory")
    if "error" in out.lower() or "% invalid" in out.lower():
        raise RuntimeError(f"[{task.host.name}] write memory failed: {out[:200]}")
    log.info("[%s] write memory OK", task.host.name)


def _cli_reload(task) -> None:
    """Fire-and-forget reload. Handles confirm prompt."""
    try:
        out = _cli(task, "reload", confirm=True, timeout=15)
        log.info("[%s] reload dispatched: %s", task.host.name, out.strip()[:120])
    except Exception as e:
        # connection drops on reload — that's expected
        log.info("[%s] reload connection closed: %s", task.host.name, e)


def _cli_show(task, cmd: str) -> str:
    return _cli(task, cmd)


# ================================================================
# OUTPUT PARSERS
# ================================================================

def _parse_show_switch(text: str) -> dict:
    """Return {"numbers": set(), "roles": {n: role}, "priorities": {n: p},
    "states": {n: state}} by scanning lines starting with a digit."""
    numbers, roles, priorities, states = set(), {}, {}, {}
    for line in text.splitlines():
        m = re.match(r"^\s*(\*?)\s*(\d+)\s+(\S+)\s+(\d+)\s+(\S+)\s+(\S+)", line)
        if not m:
            continue
        n = int(m.group(2))
        numbers.add(n)
        roles[n] = m.group(3).lower()
        priorities[n] = int(m.group(4))
        states[n] = m.group(5).lower()
    return {"numbers": numbers, "roles": roles,
            "priorities": priorities, "states": states}


def _parse_svl_domain(text: str) -> Optional[int]:
    m = re.search(r"Domain\s+(\d+)", text)
    return int(m.group(1)) if m else None


def _parse_svl_links(text: str) -> dict:
    """Return {interface_string: (link_id, status)} from 'show stackwise-virtual link'."""
    links = {}
    for line in text.splitlines():
        m = re.match(
            r"^\s*(\S+)\s+(\d+)\s+(\S+)\s+(\S+)\s+(\S+)", line
        )
        if not m:
            continue
        iface = m.group(1)
        if not re.match(r"^[A-Za-z]", iface):
            continue
        try:
            link_id = int(m.group(2))
        except ValueError:
            continue
        status = m.group(4).upper()
        links[iface] = (link_id, status)
    return links


def _parse_redundancy(text: str) -> dict:
    """Return {'active': bool, 'standby': bool} based on redundancy states."""
    active = bool(re.search(r"Active\s*:\s*(?:Yes|Active)", text, re.I))
    hot = bool(re.search(r"Standby\s*:\s*(?:Hot|Yes)", text, re.I))
    return {"active": active, "standby": hot}


def _parse_dad_ports(text: str) -> set:
    """Return set of interface strings from 'show stackwise-virtual dual-active-detection'."""
    ports = set()
    for line in text.splitlines():
        m = re.match(r"^\s*([A-Za-z][A-Za-z\-]+[0-9][0-9/\.:]*)", line)
        if m:
            ports.add(m.group(1))
    return ports


# ================================================================
# BUILDERS (NETCONF, from stack_xml.TEMPLATES)
# ================================================================

def build_bp_provision(family, switch_num, sku) -> List[str]:
    tpl = TEMPLATES["BP_PROVISION"]
    return [tpl.format(switch_num=switch_num, sku=sku)]

def build_bp_stack_mac(family, minutes=0) -> List[str]:
    tpl = TEMPLATES["BP_STACK_MAC"]
    return [tpl.format(minutes=minutes)]

def build_fp_domain(family, domain) -> List[str]:
    tpl = TEMPLATES["FP_DOMAIN"]
    return [tpl.format(domain=domain)]

def build_fp_link(family, parent, child, link_id) -> List[str]:
    tpl = TEMPLATES["FP_LINK"]
    return [tpl.format(parent=parent, child=child, link_id=link_id)]

def build_dad_port(family, parent, child) -> List[str]:
    tpl = TEMPLATES["DAD_PORT"]
    return [tpl.format(parent=parent, child=child)]


def _push(task, conn, has_candidate, payloads, label):
    """Push a list of NETCONF payloads; fail-fast on first error."""
    for idx, payload in enumerate(payloads):
        ok, err = _try_edit(task, conn, payload, label, has_candidate)
        if not ok:
            raise RuntimeError(
                f"[{task.host.name}] {label} step {idx+1} failed: {err}"
            )


# ================================================================
# VERIFY (CLI, mandatory)
# ================================================================

def _verify_back_panel(task, expected_members, expected_priority):
    """expected_members: [(switch_num, sku), ...] including the master."""
    out = _cli_show(task, "show switch")
    parsed = _parse_show_switch(out)
    expected_numbers = {int(n) for n, _ in expected_members}
    missing = expected_numbers - parsed["numbers"]
    if missing:
        raise RuntimeError(
            f"[{task.host.name}] back-panel verify: switch numbers not present: "
            f"{sorted(missing)}. Got: {sorted(parsed['numbers'])}"
        )

    # Master (switch 1) priority
    if parsed["priorities"].get(1) != expected_priority:
        raise RuntimeError(
            f"[{task.host.name}] back-panel verify: switch 1 priority is "
            f"{parsed['priorities'].get(1)}, expected {expected_priority}"
        )

    # stack-mac timer 0 in running config
    sm = _cli_show(task, "show running-config | include stack-mac")
    if "stack-mac persistent timer 0" not in sm.lower():
        raise RuntimeError(
            f"[{task.host.name}] back-panel verify: "
            f"stack-mac persistent timer 0 not found in running config"
        )

    # provision lines present
    prov = _cli_show(task, "show running-config | include switch .* provision")
    for n, sku in expected_members:
        sku_lc = sku.lower()
        # running-config renders e.g. "switch 2 provision c9300-24t"
        if not re.search(rf"switch\s+{n}\s+provision\s+{re.escape(sku_lc)}",
                         prov, re.I):
            raise RuntimeError(
                f"[{task.host.name}] back-panel verify: "
                f"provision for switch {n} ({sku}) not found in running config"
            )

    log.info("[%s] back-panel verify OK (numbers=%s, priority(1)=%d)",
             task.host.name, sorted(expected_numbers), expected_priority)


def _verify_front_panel(task, expected_domain, link_ports, is_master_chassis):
    """link_ports: [(parent, child, link_id), ...] on this chassis."""
    out = _cli_show(task, "show switch")
    parsed = _parse_show_switch(out)

    expected_num = 1 if is_master_chassis else 2
    if expected_num not in parsed["numbers"]:
        raise RuntimeError(
            f"[{task.host.name}] front-panel verify: switch {expected_num} "
            f"not present. Got: {sorted(parsed['numbers'])}"
        )
    if parsed["roles"].get(expected_num) == "unknown":
        # role parsing may differ; just warn
        log.warning("[%s] front-panel: switch %d role not recognised",
                    task.host.name, expected_num)

    svl = _cli_show(task, "show stackwise-virtual")
    domain = _parse_svl_domain(svl)
    if domain != expected_domain:
        raise RuntimeError(
            f"[{task.host.name}] front-panel verify: SVL domain is {domain}, "
            f"expected {expected_domain}"
        )

    link_out = _cli_show(task, "show stackwise-virtual link")
    links = _parse_svl_links(link_out)
    for parent, child, link_id in link_ports:
        iface = f"{parent}{child}"
        if iface not in links:
            raise RuntimeError(
                f"[{task.host.name}] front-panel verify: {iface} not in "
                f"'show stackwise-virtual link'"
            )
        got_id, status = links[iface]
        if got_id != link_id:
            raise RuntimeError(
                f"[{task.host.name}] front-panel verify: {iface} link id is "
                f"{got_id}, expected {link_id}"
            )
        if status not in ("U", "UP"):
            raise RuntimeError(
                f"[{task.host.name}] front-panel verify: {iface} link status "
                f"is {status}, expected UP"
            )

    log.info("[%s] front-panel verify OK (chassis=%s, domain=%d, links=%d)",
             task.host.name,
             "master" if is_master_chassis else "standby",
             expected_domain, len(link_ports))


def _verify_dad(task, dad_ports, link_ports):
    """dad_ports, link_ports: [(parent, child), ...] / [(parent, child, link_id), ...]"""
    dad_out = _cli_show(task, "show stackwise-virtual dual-active-detection")
    present = _parse_dad_ports(dad_out)
    for parent, child in dad_ports:
        iface = f"{parent}{child}"
        if iface not in present:
            raise RuntimeError(
                f"[{task.host.name}] DAD verify: {iface} not present in "
                f"'show stackwise-virtual dual-active-detection'. Got: {sorted(present)}"
            )

    # DAD ports must NOT be SVL links
    link_out = _cli_show(task, "show stackwise-virtual link")
    links = _parse_svl_links(link_out)
    for parent, child in dad_ports:
        iface = f"{parent}{child}"
        if iface in links:
            raise RuntimeError(
                f"[{task.host.name}] DAD verify: {iface} is also an SVL link "
                f"— device accepted an invalid combination"
            )

    log.info("[%s] DAD verify OK (dad_ports=%s)",
             task.host.name, sorted(f"{p}{c}" for p, c in dad_ports))


# ================================================================
# PER-OPERATION WORKFLOWS
# ================================================================

def _run_back_panel(task, nc, has_candidate, details, version):
    """Single device (master). Provision members, stack-mac, save, verify."""
    master_id = details["master_device_id"]
    master_prio = int(details["master_priority"])
    members = details["members"]   # [{"sku_designation","switch_number"}, ...]

    # 1) Priority on master, forced switch number 1
    _cli_priority(task, 1, master_prio)

    # 2) Provision each member (SKU + number). Master row included so its own
    #    SKU can be pre-staged 
    #    switch 1 in members[]. 
    for m in members:
        sn = int(m["switch_number"])
        sku = m["sku_designation"]
        payloads = build_bp_provision(version, sn, sku)
        _push(task, nc, has_candidate, payloads, f"provision switch {sn}")

    # 3) stack-mac timer 0 (mandatory — keep same MAC after failover)
    payloads = build_bp_stack_mac(version, 0)
    _push(task, nc, has_candidate, payloads, "stack-mac persistent timer 0")

    # 4) write memory
    _cli_save(task)

    # 5) verify
    expected = [(int(m["switch_number"]), m["sku_designation"]) for m in members]
    # If master's own row isn't in members[], still expect switch 1 to exist
    if 1 not in {n for n, _ in expected}:
        expected.append((1, None))
    _verify_back_panel(task, [e for e in expected if e[1] is not None],
                       master_prio)


def _run_front_panel(task, nc, has_candidate, details, version):
    """Called on each of the two chassis. task.host carries is_master flag
    via details routing done by the runner."""
    is_master = task.host["is_master_chassis"]
    domain = int(details["virtual_domain_id"])
    master_prio = int(details["master_chassis_priority"])
    standby_prio = int(details.get("standby_chassis_priority", 10))

    my_num_target = 1 if is_master else 2
    my_prio = master_prio if is_master else standby_prio

    # Ports on this chassis — exactly 2 (both SVL link ports, same link id)
    ports = task.host["ports"]   # [{"int_id","int_name"}, ...]
    if len(ports) != 2:
        raise RuntimeError(
            f"[{task.host.name}] front-panel requires exactly 2 ports, "
            f"got {len(ports)}"
        )
    link_ports = []
    for p in ports:
        parent, child = parse_interface_name(p["int_name"])
        if parent is None:
            raise RuntimeError(
                f"[{task.host.name}] cannot parse interface {p['int_name']}"
            )
        link_ports.append((parent, child))

    # 1) Force switch number: master→1, standby→2. Read current first.
    sw_out = _cli_show(task, "show switch")
    parsed = _parse_show_switch(sw_out)
    # Heuristic: if my_num_target already in numbers, no renumber needed.
    # Otherwise, renumber from the only current number to my_num_target.
    if my_num_target not in parsed["numbers"]:
        current_candidates = parsed["numbers"] - {1, 2}
        if not current_candidates:
            # can't determine current number cleanly — try both
            current_candidates = parsed["numbers"] - {my_num_target}
        if len(current_candidates) == 1:
            old = current_candidates.pop()
            _cli_renumber(task, old, my_num_target)
        else:
            raise RuntimeError(
                f"[{task.host.name}] front-panel: cannot determine current "
                f"switch number to renumber from. Got: {sorted(parsed['numbers'])}"
            )
    else:
        log.info("[%s] front-panel: already switch %d, skipping renumber",
                 task.host.name, my_num_target)

    # 2) Priority
    _cli_priority(task, my_num_target, my_prio)

    # 3) Domain (same on both)
    payloads = build_fp_domain(version, domain)
    _push(task, nc, has_candidate, payloads, f"svl domain {domain}")

    # 4) Link on both ports (same link id)
    for parent, child in link_ports:
        payloads = build_fp_link(version, parent, child, 1)
        _push(task, nc, has_candidate, payloads, f"svl link {parent}{child}")

    # 5) stack-mac timer 0 (mandatory on both)
    payloads = build_bp_stack_mac(version, 0)
    _push(task, nc, has_candidate, payloads, "stack-mac persistent timer 0")

    # 6) save
    _cli_save(task)

    # 7) verify (pre-reload)
    _verify_front_panel(
        task, domain,
        [(p, c, 1) for p, c in link_ports],
        is_master,
    )


def _run_dad(task, nc, has_candidate, details, version):
    """Called on each of the two chassis. task.host carries port_int_name
    (the single DAD port on this chassis)."""
    port_name = task.host["dad_port_int_name"]
    parent, child = parse_interface_name(port_name)
    if parent is None:
        raise RuntimeError(
            f"[{task.host.name}] DAD: cannot parse interface {port_name}"
        )

    # 1) Pre-check: this port must NOT already be an SVL link
    link_out = _cli_show(task, "show stackwise-virtual link")
    links = _parse_svl_links(link_out)
    iface = f"{parent}{child}"
    if iface in links:
        raise RuntimeError(
            f"[{task.host.name}] DAD: {iface} is already an SVL link — "
            f"cannot also be a DAD port"
        )

    # 2) Configure DAD
    payloads = build_dad_port(version, parent, child)
    _push(task, nc, has_candidate, payloads, f"dad {iface}")

    # 3) save
    _cli_save(task)

    # 4) verify
    _verify_dad(task, [(parent, child)], [])


# ================================================================
# TASK
# ================================================================

def iosxe_stack_task(task):
    nc = task.host.get_connection("scrapli_netconf", task.nornir.config)
    has_candidate = _has_candidate(nc)
    log.info("[%s] candidate: %s", task.host.name,
             "YES" if has_candidate else "NO")

    operation = task.host["operation"]
    details   = task.host["details"]
    version   = task.host["version"]

    log.info("[%s] op=%s version=%s", task.host.name, operation, version)

    # Pre-create the CLI connection so failures happen early.
    task.host.get_connection("scrapli", task.nornir.config)

    if operation == "back-panel":
        _run_back_panel(task, nc, has_candidate, details, version)

    elif operation == "front-panel":
        _run_front_panel(task, nc, has_candidate, details, version)
        if not task.host["is_master_chassis"]:
            # Standby reloads last, fire-and-forget
            _cli_reload(task)
            log.info("[%s] standby reload dispatched", task.host.name)

    elif operation == "dad":
        _run_dad(task, nc, has_candidate, details, version)

    else:
        raise RuntimeError(
            f"[{task.host.name}] unknown stack operation '{operation}'"
        )

    log.info("[%s] %s task done", task.host.name, operation)


# ================================================================
# NORNIR HOST BUILDER
# ================================================================

def _build_hosts_data(payload: StackRequest) -> list:
    """Flatten devices → Nornir hosts.

    For front-panel, each device becomes one host with is_master_chassis flag.
    For dad, each device becomes one host with dad_port_int_name set
    (ports[0] → master, ports[1] → standby; runner maps the pair).
    """
    hosts_data = []

    if payload.operation == "front-panel":
        master_id = payload.details.get("master_device_id")
        for dev in payload.devices:
            is_master = (dev.id == master_id)
            hosts_data.append({
                "name": f"{dev.id}",
                "hostname": dev.management_ip,
                "platform": normalize_platform(dev.platform),
                "username": payload.profile.username,
                "password": payload.profile.password_cipher,
                "port": 830,
                "connection_options": {
                    "scrapli": {
                        "extras": {
                            "auth_strict_key": False,
                            "timeout_socket": 10.0,
                            "timeout_transport": 15.0,
                            "timeout_banner": 30,
                        }
                    },
                    "scrapli_netconf": {
                        "extras": {
                            "auth_strict_key": False,
                            "timeout_socket": 10.0,
                            "timeout_transport": 15.0,
                            "timeout_banner": 30,
                        }
                    },
                },
                "device_id": dev.id,
                "version": dev.version or "",
                "family": dev.family or "",
                "ports": [p.dict() for p in (dev.ports or [])],
                "operation": payload.operation,
                "details": payload.details,
                "is_master_chassis": is_master,
            })

    elif payload.operation == "dad":
        # Single request, 2 devices × 1 port each. ports[0] is on
        # devices[0] (master), ports[1] on devices[1] (standby).
        if len(payload.devices) != 2:
            raise RuntimeError(
                "dad: expected 2 devices (one per chassis), got "
                f"{len(payload.devices)}"
            )
        for idx, dev in enumerate(payload.devices):
            if len(dev.ports or []) != 1:
                raise RuntimeError(
                    f"dad: device {dev.id} must have exactly 1 port, got "
                    f"{len(dev.ports or [])}"
                )
            hosts_data.append({
                "name": f"{dev.id}",
                "hostname": dev.management_ip,
                "platform": normalize_platform(dev.platform),
                "username": payload.profile.username,
                "password": payload.profile.password_cipher,
                "port": 830,
                "connection_options": {
                    "scrapli": {
                        "extras": {
                          
                            "port": 22,
                            "auth_strict_key": False,
                            "timeout_socket": 60,
                            "timeout_transport": 60.0,
                            "timeout_banner": 60,
                            "auth_strict_key": False,
                            "platform": "cisco_iosxe",
                            "transport": "paramiko",
                          
                        }
                    },
                    "scrapli_netconf": {
                        "extras": {
                            "auth_strict_key": False,
                            "timeout_socket": 10.0,
                            "timeout_transport": 15.0,
                            "timeout_banner": 30,
                        }
                    },
                },
                "device_id": dev.id,
                "version": dev.version or "",
                "family": dev.family or "",
                "dad_port_int_name": dev.ports[0].int_name,
                "operation": payload.operation,
                "details": payload.details,
            })

    else:  # back-panel — single device (master)
        if len(payload.devices) != 1:
            raise RuntimeError(
                f"back-panel: expected 1 master device, got {len(payload.devices)}"
            )
        dev = payload.devices[0]
        hosts_data.append({
            "name": f"{dev.id}",
            "hostname": dev.management_ip,
            "platform": normalize_platform(dev.platform),
            "username": payload.profile.username,
            "password": payload.profile.password_cipher,
            "port": 830,
            "connection_options": {
                "scrapli": {
                    "extras": {
                        "auth_strict_key": False,
                        "timeout_socket": 10.0,
                        "timeout_transport": 15.0,
                        "timeout_banner": 30,
                    }
                },
                "scrapli_netconf": {
                    "extras": {
                        "auth_strict_key": False,
                        "timeout_socket": 10.0,
                        "timeout_transport": 15.0,
                        "timeout_banner": 30,
                    }
                },
            },
            "device_id": dev.id,
            "version": dev.version or "",
            "family": dev.family or "",
            "operation": payload.operation,
            "details": payload.details,
        })

    return hosts_data


# ================================================================
# RUNNER
# ================================================================

       # ================================================================
# RUNNER
# ================================================================

def run_stack_job(payload: StackRequest):
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
        result = filtered.run(task=iosxe_stack_task)

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