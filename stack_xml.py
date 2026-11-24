# stackwise_svl_dad_xml.py
#
# Universal XML templates for StackWise (back-panel), StackWise Virtual
# (front-panel) and Dual-Active Detection (DAD, fast-hello only).
#
# Scope: 16.12 → 17.15. One template per function — no version branching
# in the XML body. Version-sensitive VALUES (switch number range, SKU enum,
# interface types available per train) are the engineer's responsibility.
#
# Placeholders use str.format() style.
# Templates are complete <config> documents (edit-config payloads only).
#
# EXCLUDED by design decision:
#   * Remove operations (nc:operation="remove"/"delete")
#   * get-config subtree filters
#   * stack-speed (switch-global-config/stack/stack-speed) — 17.15-only
#   * PAgP DAD (dual-active/detection/pagp/...) — using fast-hello only
#   * Priority / renumber — CLI-only (no YANG node/RPC exists)

import re


# ================================================================
# NAMESPACES
# ================================================================

NC_NS     = "urn:ietf:params:xml:ns:netconf:base:1.0"
NATIVE_NS = "http://cisco.com/ns/yang/Cisco-IOS-XE-native"
SW_NS     = "http://cisco.com/ns/yang/Cisco-IOS-XE-switch"
SV_NS     = "http://cisco.com/ns/yang/Cisco-IOS-XE-stackwise-virtual"


# ================================================================
# 1. BACK-PANEL — PROVISION (switch number + SKU)
# ================================================================
# CLI equivalent: switch {switch_num} provision {sku}
# Confirmed shape: <switch><number/><provision/></switch>  (SW ns)
# Value caveats (engineer): {switch_num} 1..9 on 16.12, 1..16 on 17.15;
#                           {sku} is an enum, must match per train exactly.

BP_PROVISION = f"""
<config xmlns="{NC_NS}" xmlns:nc="{NC_NS}">
  <native xmlns="{NATIVE_NS}">
    <switch xmlns="{SW_NS}">
      <number>{{switch_num}}</number>
      <provision>{{sku}}</provision>
    </switch>
  </native>
</config>
"""


# ================================================================
# 2. BACK-PANEL — STACK-MAC PERSISTENT TIMER (0..60 min; 0 = keep MAC)
# ================================================================
# CLI equivalent: stack-mac persistent timer {minutes}
# Confirmed shape: <stack-mac><persistent><timer/></persistent></stack-mac>

BP_STACK_MAC = f"""
<config xmlns="{NC_NS}" xmlns:nc="{NC_NS}">
  <native xmlns="{NATIVE_NS}">
    <stack-mac xmlns="{SW_NS}">
      <persistent>
        <timer>{{minutes}}</timer>
      </persistent>
    </stack-mac>
  </native>
</config>
"""


# ================================================================
# 3. FRONT-PANEL — SVL DOMAIN (1..255, same on both chassis)
# ================================================================
# CLI equivalent: stackwise-virtual domain {domain}
# Confirmed shape: <stackwise-virtual><domain><domain/></domain></stackwise-virtual>
#   outer stackwise-virtual = native ns
#   inner domain container + domain leaf = SV ns
# Defaults to 1 if unset.

FP_DOMAIN = f"""
<config xmlns="{NC_NS}" xmlns:nc="{NC_NS}">
  <native xmlns="{NATIVE_NS}">
    <stackwise-virtual>
      <domain xmlns="{SV_NS}">
        <domain>{{domain}}</domain>
      </domain>
    </stackwise-virtual>
  </native>
</config>
"""


# ================================================================
# 4. FRONT-PANEL — SVL LINK ON ONE PORT (link id 1..2)
# ================================================================
# CLI equivalent: interface {parent}{child} / stackwise-virtual link {link_id}
# Confirmed shape: per-interface stackwise-virtual/link in native ns.
#   {parent} valid values depend on train:
#     16.12: TenGigabitEthernet, TwentyFiveGigE, FortyGigabitEthernet, HundredGigE
#     17.x : adds FiftyGigabitEthernet, TwoHundredGigE, FourHundredGigE
#   {child}: port name, e.g. 1/0/1
#   {link_id}: 1..2; normally the SAME id on both ports of the bundle.

FP_LINK = f"""
<config xmlns="{NC_NS}" xmlns:nc="{NC_NS}">
  <native xmlns="{NATIVE_NS}">
    <interface>
      <{{parent}}>
        <name>{{child}}</name>
        <stackwise-virtual>
          <link>{{link_id}}</link>
        </stackwise-virtual>
      </{{parent}}>
    </interface>
  </native>
</config>
"""


# ================================================================
# 5. DAD — FAST-HELLO ON A PORT (empty leaf; presence = enabled)
# ================================================================
# CLI equivalent: interface {parent}{child} / stackwise-virtual dual-active-detection
# Confirmed shape: per-interface stackwise-virtual/dual-active-detection, native ns.
# DAD ports MUST NOT also be SVL links — device rejects link + DAD on same
# interface at commit.

DAD_PORT = f"""
<config xmlns="{NC_NS}" xmlns:nc="{NC_NS}">
  <native xmlns="{NATIVE_NS}">
    <interface>
      <{{parent}}>
        <name>{{child}}</name>
        <stackwise-virtual>
          <dual-active-detection/>
        </stackwise-virtual>
      </{{parent}}>
    </interface>
  </native>
</config>
"""


# ================================================================
# TEMPLATE REGISTRY (one universal string per function)
# ================================================================
# Keys are function names. Values are single templates valid on every
# train 16.12 → 17.15. Version handling is value-level, not body-level.

TEMPLATES = {
    # Back-panel
    "BP_PROVISION":  BP_PROVISION,
    "BP_STACK_MAC":  BP_STACK_MAC,
    # Front-panel
    "FP_DOMAIN":     FP_DOMAIN,
    "FP_LINK":       FP_LINK,
    # DAD (fast-hello)
    "DAD_PORT":      DAD_PORT,
}


# ================================================================
# STARTUP PLACEHOLDER VALIDATION
# ================================================================

_ALLOWED = {
    "switch_num", "sku", "minutes",
    "domain", "parent", "child", "link_id",
}

_PLACEHOLDER_RE = re.compile(r"\{([a-z_]+)\}")

def _validate_all():
    errors = []
    for name, tpl in TEMPLATES.items():
        for match in _PLACEHOLDER_RE.findall(tpl):
            if match not in _ALLOWED:
                errors.append(f"{name}: unknown placeholder {{{match}}}")
    if errors:
        raise ValueError(
            "stackwise_svl_dad_xml: placeholder validation failed:\n  "
            + "\n  ".join(errors)
        )

_validate_all()