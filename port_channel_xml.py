# port_channel_xml.py
#
# XML templates for add_port_channels.py.
# Placeholders use str.format() style: {po}, {desc_block}, {allowed_block}, etc.
#
# COMPOSITION CONTRACT (see add_port_channels.py _opt()):
#   * Optional blocks (desc/lb/min_links/native) are substituted as
#     "{desc_block}", "{lb_block}", "{min_links_block}", "{native_block}".
#     When the field is missing, the block renders as "" (empty string)
#     and the surrounding template still forms valid XML.
#   * Required values (po, vlan, vlans, ip, mask, parent, child, sub,
#     vlan_tag, mode) are substituted raw and MUST be supplied by the builder.
#   * `allowed_block` is always present.
#
# MEMBER_L3 is identical to MEMBER plus a `switchport-conf/switchport=false`
# before the channel-group. Needed for members of a routed port-channel.
#
# MEMBER_UNBIND removes channel-group from a member port. Used by abolish
# to unbind members before deleting the Port-channel.

import re


# ================================================================
# NAMESPACES
# ================================================================

NC_NS     = "urn:ietf:params:xml:ns:netconf:base:1.0"
NATIVE_NS = "http://cisco.com/ns/yang/Cisco-IOS-XE-native"
SW_NS     = "http://cisco.com/ns/yang/Cisco-IOS-XE-switch"
ETH_NS    = "http://cisco.com/ns/yang/Cisco-IOS-XE-ethernet"


# ================================================================
# SHARED BLOCK FRAGMENTS
# ================================================================

DESC_BLOCK      = "<description>{desc}</description>"
LB_BLOCK        = "<load-balancing>{lb}</load-balancing>"
MIN_LINKS_BLOCK = "<port-channel><min-links>{min_links}</min-links></port-channel>"


# ================================================================
# 16.12
# ================================================================

NATIVE_BLOCK_1612 = "<native><vlan-id><vlan-id>{native_vlan}</vlan-id></vlan-id></native>"

ALLOWED_1612_REPLACE = (
    '<allowed><vlan nc:operation="replace"><vlans>{vlans}</vlans></vlan></allowed>'
)

PO_L2_INIT_1612 = f"""
<config xmlns="{NC_NS}" xmlns:nc="{NC_NS}">
  <native xmlns="{NATIVE_NS}">
    <interface>
      <Port-channel>
        <name>{{po}}</name>
        {{desc_block}}
        {{lb_block}}
        {{min_links_block}}
        <switchport/>
      </Port-channel>
    </interface>
  </native>
</config>
"""

PO_L2_TRUNK_1612 = f"""
<config xmlns="{NC_NS}" xmlns:nc="{NC_NS}">
  <native xmlns="{NATIVE_NS}">
    <interface>
      <Port-channel>
        <name>{{po}}</name>
        <switchport>
          <mode xmlns="{SW_NS}"><trunk/></mode>
          <trunk xmlns="{SW_NS}">
            {{allowed_block}}
            {{native_block}}
          </trunk>
        </switchport>
      </Port-channel>
    </interface>
  </native>
</config>
"""

PO_L2_ACCESS_1612 = f"""
<config xmlns="{NC_NS}" xmlns:nc="{NC_NS}">
  <native xmlns="{NATIVE_NS}">
    <interface>
      <Port-channel>
        <name>{{po}}</name>
        <switchport>
          <mode xmlns="{SW_NS}"><access/></mode>
          <access xmlns="{SW_NS}"><vlan><vlan>{{vlan}}</vlan></vlan></access>
        </switchport>
      </Port-channel>
    </interface>
  </native>
</config>
"""

PO_L3_1612 = f"""
<config xmlns="{NC_NS}" xmlns:nc="{NC_NS}">
  <native xmlns="{NATIVE_NS}">
    <interface>
      <Port-channel>
        <name>{{po}}</name>
        {{desc_block}}
        {{lb_block}}
        {{min_links_block}}
        <switchport-conf><switchport>false</switchport></switchport-conf>
        <ip><address><primary>
          <address>{{ip}}</address><mask>{{mask}}</mask>
        </primary></address></ip>
      </Port-channel>
    </interface>
  </native>
</config>
"""

MEMBER_1612 = f"""
<config xmlns="{NC_NS}" xmlns:nc="{NC_NS}">
  <native xmlns="{NATIVE_NS}">
    <interface>
      <{{parent}}>
        <name>{{child}}</name>
        <channel-group xmlns="{ETH_NS}">
          <number>{{po}}</number>
          <mode>{{mode}}</mode>
        </channel-group>
      </{{parent}}>
    </interface>
  </native>
</config>
"""

MEMBER_L3_1612 = f"""
<config xmlns="{NC_NS}" xmlns:nc="{NC_NS}">
  <native xmlns="{NATIVE_NS}">
    <interface>
      <{{parent}}>
        <name>{{child}}</name>
        <switchport-conf><switchport>false</switchport></switchport-conf>
        <channel-group xmlns="{ETH_NS}">
          <number>{{po}}</number>
          <mode>{{mode}}</mode>
        </channel-group>
      </{{parent}}>
    </interface>
  </native>
</config>
"""

MEMBER_UNBIND_1612 = f"""
<config xmlns="{NC_NS}" xmlns:nc="{NC_NS}">
  <native xmlns="{NATIVE_NS}">
    <interface>
      <{{parent}}>
        <name>{{child}}</name>
        <channel-group xmlns="{ETH_NS}" nc:operation="remove"/>
      </{{parent}}>
    </interface>
  </native>
</config>
"""

PO_SUBIF_1612 = f"""
<config xmlns="{NC_NS}" xmlns:nc="{NC_NS}">
  <native xmlns="{NATIVE_NS}">
    <interface>
      <Port-channel-subinterface>
        <Port-channel>
          <name>{{po}}.{{sub}}</name>
          {{desc_block}}
          <encapsulation><dot1Q><vlan-id>{{vlan_tag}}</vlan-id></dot1Q></encapsulation>
          <ip><address><primary>
            <address>{{ip}}</address><mask>{{mask}}</mask>
          </primary></address></ip>
        </Port-channel>
      </Port-channel-subinterface>
    </interface>
  </native>
</config>
"""

PO_DELETE_1612 = f"""
<config xmlns="{NC_NS}" xmlns:nc="{NC_NS}">
  <native xmlns="{NATIVE_NS}">
    <interface>
      <Port-channel nc:operation="remove">
        <name>{{po}}</name>
      </Port-channel>
    </interface>
  </native>
</config>
"""


# ================================================================
# 17.3
# ================================================================

NATIVE_BLOCK_173 = "<native><vlan>{native_vlan}</vlan></native>"

ALLOWED_173_REPLACE = (
    '<allowed nc:operation="replace"><vlan><vlans>{vlans}</vlans></vlan></allowed>'
)
ALLOWED_173_ADD     = '<allowed><vlan><add>{vlans}</add></vlan></allowed>'
ALLOWED_173_EXCEPT  = '<allowed><vlan><except>{vlans}</except></vlan></allowed>'

PO_L2_INIT_173 = f"""
<config xmlns="{NC_NS}" xmlns:nc="{NC_NS}">
  <native xmlns="{NATIVE_NS}">
    <interface>
      <Port-channel>
        <name>{{po}}</name>
        {{desc_block}}
        {{lb_block}}
        {{min_links_block}}
        <switchport-config>
          <switchport/>
        </switchport-config>
      </Port-channel>
    </interface>
  </native>
</config>
"""

PO_L2_TRUNK_173 = f"""
<config xmlns="{NC_NS}" xmlns:nc="{NC_NS}">
  <native xmlns="{NATIVE_NS}">
    <interface>
      <Port-channel>
        <name>{{po}}</name>
        <switchport-config>
          <switchport>
            <mode xmlns="{SW_NS}"><trunk/></mode>
            <trunk xmlns="{SW_NS}">
              {{allowed_block}}
              {{native_block}}
            </trunk>
          </switchport>
        </switchport-config>
      </Port-channel>
    </interface>
  </native>
</config>
"""

PO_L2_ACCESS_173 = f"""
<config xmlns="{NC_NS}" xmlns:nc="{NC_NS}">
  <native xmlns="{NATIVE_NS}">
    <interface>
      <Port-channel>
        <name>{{po}}</name>
        <switchport-config>
          <switchport>
            <mode xmlns="{SW_NS}"><access/></mode>
            <access xmlns="{SW_NS}"><vlan>{{vlan}}</vlan></access>
          </switchport>
        </switchport-config>
      </Port-channel>
    </interface>
  </native>
</config>
"""

PO_L3_173 = f"""
<config xmlns="{NC_NS}" xmlns:nc="{NC_NS}">
  <native xmlns="{NATIVE_NS}">
    <interface>
      <Port-channel>
        <name>{{po}}</name>
        {{desc_block}}
        {{lb_block}}
        {{min_links_block}}
        <switchport-conf><switchport>false</switchport></switchport-conf>
        <ip><address><primary>
          <address>{{ip}}</address><mask>{{mask}}</mask>
        </primary></address></ip>
      </Port-channel>
    </interface>
  </native>
</config>
"""

MEMBER_173 = MEMBER_1612
MEMBER_L3_173 = MEMBER_L3_1612
MEMBER_UNBIND_173 = MEMBER_UNBIND_1612
PO_SUBIF_173 = PO_SUBIF_1612

PO_DELETE_173 = f"""
<config xmlns="{NC_NS}" xmlns:nc="{NC_NS}">
  <native xmlns="{NATIVE_NS}">
    <interface>
      <Port-channel nc:operation="delete">
        <name>{{po}}</name>
      </Port-channel>
    </interface>
  </native>
</config>
"""


# ================================================================
# 17.6
# ================================================================

NATIVE_BLOCK_176 = "<native><vlan><vlan-id>{native_vlan}</vlan-id></vlan></native>"

ALLOWED_176_REPLACE = (
    '<allowed><vlan nc:operation="replace"><vlans>{vlans}</vlans></vlan></allowed>'
)

PO_L2_INIT_176 = PO_L2_INIT_173
PO_L2_TRUNK_176 = PO_L2_TRUNK_173
PO_L2_ACCESS_176 = PO_L2_ACCESS_173
PO_L3_176 = PO_L3_173
MEMBER_176 = MEMBER_1612
MEMBER_L3_176 = MEMBER_L3_1612
MEMBER_UNBIND_176 = MEMBER_UNBIND_1612
PO_SUBIF_176 = PO_SUBIF_1612
PO_DELETE_176 = PO_DELETE_1612


# ================================================================
# 17.9 (covers 17.8, 17.9, 17.10)
# ================================================================

NATIVE_BLOCK_179 = NATIVE_BLOCK_176
ALLOWED_179_REPLACE = ALLOWED_176_REPLACE

PO_L2_INIT_179 = PO_L2_INIT_176
PO_L2_TRUNK_179 = PO_L2_TRUNK_176
PO_L2_ACCESS_179 = PO_L2_ACCESS_176
PO_L3_179 = PO_L3_176
MEMBER_179 = MEMBER_1612
MEMBER_L3_179 = MEMBER_L3_1612
MEMBER_UNBIND_179 = MEMBER_UNBIND_1612
PO_SUBIF_179 = PO_SUBIF_1612
PO_DELETE_179 = PO_DELETE_1612


# ================================================================
# 17.12
# ================================================================

NATIVE_BLOCK_1712 = NATIVE_BLOCK_176

ALLOWED_1712_REPLACE = (
    '<allowed nc:operation="replace"><vlan-v2><vlan-choices>'
    '<vlans>{vlans}</vlans>'
    '</vlan-choices></vlan-v2></allowed>'
)
ALLOWED_1712_ADD = (
    '<allowed><vlan-v2><add-vlans>'
    '<add><vlans>{vlans}</vlans></add>'
    '</add-vlans></vlan-v2></allowed>'
)
ALLOWED_1712_EXCEPT = (
    '<allowed><vlan-v2><except>{vlans}</except></vlan-v2></allowed>'
)

PO_L2_INIT_1712 = PO_L2_INIT_176
PO_L2_TRUNK_1712 = PO_L2_TRUNK_176
PO_L2_ACCESS_1712 = PO_L2_ACCESS_176
PO_L3_1712 = PO_L3_176
MEMBER_1712 = MEMBER_1612
MEMBER_L3_1712 = MEMBER_L3_1612
MEMBER_UNBIND_1712 = MEMBER_UNBIND_1612
PO_SUBIF_1712 = PO_SUBIF_1612

PO_DELETE_1712 = f"""
<config xmlns="{NC_NS}" xmlns:nc="{NC_NS}">
  <native xmlns="{NATIVE_NS}">
    <interface>
      <Port-channel nc:operation="delete">
        <name>{{po}}</name>
      </Port-channel>
    </interface>
  </native>
</config>
"""


# ================================================================
# 17.15
# ================================================================

NATIVE_BLOCK_1715 = NATIVE_BLOCK_176
ALLOWED_1715_REPLACE = ALLOWED_1712_REPLACE
ALLOWED_1715_ADD     = ALLOWED_1712_ADD
ALLOWED_1715_EXCEPT  = ALLOWED_1712_EXCEPT

PO_L2_INIT_1715 = PO_L2_INIT_176
PO_L2_TRUNK_1715 = PO_L2_TRUNK_176
PO_L2_ACCESS_1715 = PO_L2_ACCESS_176
PO_L3_1715 = PO_L3_176
MEMBER_1715 = MEMBER_1612
MEMBER_L3_1715 = MEMBER_L3_1612
MEMBER_UNBIND_1715 = MEMBER_UNBIND_1612
PO_SUBIF_1715 = PO_SUBIF_1612
PO_DELETE_1715 = PO_DELETE_1712


# ================================================================
# TEMPLATE REGISTRY
# ================================================================

TEMPLATES = {
    "PO_L2_INIT": {
        "1612": PO_L2_INIT_1612, "173": PO_L2_INIT_173,
        "176": PO_L2_INIT_176,   "179": PO_L2_INIT_179,
        "1712": PO_L2_INIT_1712, "1715": PO_L2_INIT_1715,
    },
    "PO_L2_TRUNK": {
        "1612": PO_L2_TRUNK_1612, "173": PO_L2_TRUNK_173,
        "176": PO_L2_TRUNK_176,   "179": PO_L2_TRUNK_179,
        "1712": PO_L2_TRUNK_1712, "1715": PO_L2_TRUNK_1715,
    },
    "PO_L2_ACCESS": {
        "1612": PO_L2_ACCESS_1612, "173": PO_L2_ACCESS_173,
        "176": PO_L2_ACCESS_176,   "179": PO_L2_ACCESS_179,
        "1712": PO_L2_ACCESS_1712, "1715": PO_L2_ACCESS_1715,
    },
    "PO_L3": {
        "1612": PO_L3_1612, "173": PO_L3_173,
        "176": PO_L3_176,   "179": PO_L3_179,
        "1712": PO_L3_1712, "1715": PO_L3_1715,
    },
    "MEMBER": {
        "1612": MEMBER_1612, "173": MEMBER_173,
        "176": MEMBER_176,   "179": MEMBER_179,
        "1712": MEMBER_1712, "1715": MEMBER_1715,
    },
    "MEMBER_L3": {
        "1612": MEMBER_L3_1612, "173": MEMBER_L3_173,
        "176": MEMBER_L3_176,   "179": MEMBER_L3_179,
        "1712": MEMBER_L3_1712, "1715": MEMBER_L3_1715,
    },
    "MEMBER_UNBIND": {
        "1612": MEMBER_UNBIND_1612, "173": MEMBER_UNBIND_173,
        "176": MEMBER_UNBIND_176,   "179": MEMBER_UNBIND_179,
        "1712": MEMBER_UNBIND_1712, "1715": MEMBER_UNBIND_1715,
    },
    "PO_SUBIF": {
        "1612": PO_SUBIF_1612, "173": PO_SUBIF_173,
        "176": PO_SUBIF_176,   "179": PO_SUBIF_179,
        "1712": PO_SUBIF_1712, "1715": PO_SUBIF_1715,
    },
    "PO_DELETE": {
        "1612": PO_DELETE_1612, "173": PO_DELETE_173,
        "176": PO_DELETE_176,   "179": PO_DELETE_179,
        "1712": PO_DELETE_1712, "1715": PO_DELETE_1715,
    },
    "NATIVE_BLOCK": {
        "1612": NATIVE_BLOCK_1612, "173": NATIVE_BLOCK_173,
        "176": NATIVE_BLOCK_176,   "179": NATIVE_BLOCK_179,
        "1712": NATIVE_BLOCK_1712, "1715": NATIVE_BLOCK_1715,
    },
    "ALLOWED_REPLACE": {
        "1612": ALLOWED_1612_REPLACE, "173": ALLOWED_173_REPLACE,
        "176": ALLOWED_176_REPLACE,   "179": ALLOWED_179_REPLACE,
        "1712": ALLOWED_1712_REPLACE, "1715": ALLOWED_1715_REPLACE,
    },
    "ALLOWED_ADD": {
        "1612": None, "173": ALLOWED_173_ADD,
        "176": None,  "179": None,
        "1712": ALLOWED_1712_ADD, "1715": ALLOWED_1715_ADD,
    },
    "ALLOWED_EXCEPT": {
        "1612": None, "173": ALLOWED_173_EXCEPT,
        "176": None,  "179": None,
        "1712": ALLOWED_1712_EXCEPT, "1715": ALLOWED_1715_EXCEPT,
    },
    "DESC_BLOCK":      {v: DESC_BLOCK      for v in ("1612","173","176","179","1712","1715")},
    "LB_BLOCK":        {v: LB_BLOCK        for v in ("1612","173","176","179","1712","1715")},
    "MIN_LINKS_BLOCK": {v: MIN_LINKS_BLOCK for v in ("1612","173","176","179","1712","1715")},
}


# ================================================================
# STARTUP PLACEHOLDER VALIDATION
# ================================================================

_ALLOWED = {
    "po", "desc", "lb", "vlan", "native_vlan", "min_links", "mode",
    "parent", "child", "sub", "vlan_tag", "ip", "mask", "vlans",
    "desc_block", "lb_block", "min_links_block", "native_block",
    "allowed_block",
}

_PLACEHOLDER_RE = re.compile(r"\{([a-z_]+)\}")

def _validate_all():
    errors = []
    seen = set()
    for family, versions in TEMPLATES.items():
        for version, tpl in versions.items():
            if tpl is None or (family, version) in seen:
                continue
            seen.add((family, version))
            for match in _PLACEHOLDER_RE.findall(tpl):
                if match not in _ALLOWED:
                    errors.append(
                        f"{family}[{version}] unknown placeholder {{{match}}}"
                    )
    if errors:
        raise ValueError(
            "port_channel_xml: placeholder validation failed:\n  "
            + "\n  ".join(errors)
        )

_validate_all()