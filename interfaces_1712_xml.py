# interface_attrs_1712.py
# Modular NETCONF XML bodies for Cisco-IOS-XE-native (IOS XE 17.12).
# Same conventions / public API as interface_attrs_1715.py. Suffix: _1712.
#
# SOURCE YANG (all supplied, all VERIFIED against):
#   Cisco-IOS-XE-native      2023-07-01 (12.0.0)   global + document skeleton
#   Cisco-IOS-XE-interfaces  2023-07-01 (11.0.0)   submodule of native (same namespace N)
#   Cisco-IOS-XE-switch      2019-07-01 (1.0.0)    namespace $SW
#   Cisco-IOS-XE-vlan        2019-07-01 (1.0.0)    namespace $VLAN
#   Cisco-IOS-XE-nd          2019-07-01 (1.0.0)    namespace $ND
#   Cisco-IOS-XE-arp         2019-07-01 (1.0.0)    namespace $ARP
#
# KEY FINDINGS FROM THE SUPPLIED 17.12 YANG
#   1. The switch module (rev 2019-07-01) augments /native/interface/<TYPE>/switchport, which in
#      the supplied native is the DEPRECATED `switchport` container. `switchport-config/switchport`
#      (what the 1715 catalogue uses) is NOT augmented by any supplied 17.12 module. All L2
#      switchport families therefore render under <switchport>. The wrapper is one function
#      (_sp below): if your 17.12 box only accepts switchport-config, change that one line and
#      supply a newer switch module to re-verify.
#   2. L2PT thresholds: drop/shutdown-threshold children are uint16 leaves (<cdp>$pps</cdp>);
#      <packet-rate> is a sibling leaf. The 1715 shape <$proto><packet-rate>.. is NOT valid here.
#   3. Port-security in this switch module is a simple presence container
#      (aging/mac-address/maximum/violation), not the 1715 *-conf/*-config split.
#   4. No keepalive-config, no ip verify ACL leaf, no arp-inspection burst, no ipv6 verify,
#      no ipv6 nd dad/nud, no vlan shutdown, no port-channel hash-algo (see NOT_PRESENT).
#   5. SVI_PRIVATE_VLAN_MAPPING is interface-scoped (parent="Vlan"). In the 1715 file it was
#      wrongly matched by NATIVE_SCOPED's "SVI_PRIVATE_VLAN" prefix; fixed here.
#
# RESIDUAL UNVERIFIABLE (dependency modules not supplied)
#   * NVE_SOURCE_INTERFACE child names come from Cisco-IOS-XE-interface-common (ios-ifc).
#   * GLOBAL_ND_*: /native/ipv6/nd is defined in the ipv6 submodule; the nd module's augment
#     target proves the path, but its own ancestry (ipv6) was not supplied.
#   * Value syntax of ios-types (exp-acl-type, ipv6-prefix, storm-control-threshold-type, dscp).
#   * if-feature availability (switching-platform, macsec-common, private-vlan, l2cp-fwd,
#     l2pt-more-protocols, routing-platform, wpan, cable-config) depends on the device.
#
# NOT MAPPED (present in supplied YANG, out of this catalogue's scope): SW-namespace
#   l2protocol-tunnel (pps_num form), energywise, datalink flow, macro auto, location,
#   vlan-range service-policy, switch virtual, openflow, service-template, glbp, mdns-sd.
#
# Interface scaffolding is added by wrap_interface()/build_config(); bodies here are bare.

import re
from string import Template as _Template

# $N    = http://cisco.com/ns/yang/Cisco-IOS-XE-native
# $NC   = urn:ietf:params:xml:ns:netconf:base:1.0
# $SW   = http://cisco.com/ns/yang/Cisco-IOS-XE-switch
# $ST   = http://cisco.com/ns/yang/Cisco-IOS-XE-spanning-tree
# $VLAN = http://cisco.com/ns/yang/Cisco-IOS-XE-vlan
# $ND   = http://cisco.com/ns/yang/Cisco-IOS-XE-nd
# $ARP  = http://cisco.com/ns/yang/Cisco-IOS-XE-arp


def _sp(inner):
    """Wrap switch-module (SW namespace) nodes that hang off the interface switchport container.
    Supplied 17.12 switch module augments the deprecated <switchport>; see KEY FINDING 1."""
    return "<switchport>" + inner + "</switchport>"


def _w(inner):
    """Wrap native-namespace switchport-wrapper/switchport nodes (Gig/AppGig + deprecated types)."""
    return "<switchport-wrapper><switchport>" + inner + "</switchport></switchport-wrapper>"


# ============================================================
# 1. GENERAL ATTRIBUTES
# ============================================================
DESCRIPTION_1712          = "<description>$desc</description>"          # length 0..200
DESCRIPTION_REMOVE_1712   = '<description nc:operation="remove"/>'
EXPORT_NAME_1712          = "<export-name>$export</export-name>"        # length 1..128
EXPORT_NAME_REMOVE_1712   = '<export-name nc:operation="remove"/>'
MAC_ADDRESS_1712          = "<mac-address>$mac</mac-address>"
MAC_ADDRESS_REMOVE_1712   = '<mac-address nc:operation="remove"/>'

SHUTDOWN_1712             = "<shutdown/>"
SHUTDOWN_REMOVE_1712      = '<shutdown nc:operation="remove"/>'

MTU_1712                  = "<mtu>$mtu</mtu>"                           # 64..18000
MTU_REMOVE_1712           = '<mtu nc:operation="remove"/>'
DELAY_1712                = "<delay>$delay</delay>"                     # 1..16777215
DELAY_REMOVE_1712         = '<delay nc:operation="remove"/>'
LOAD_INTERVAL_1712        = "<load-interval>$seconds</load-interval>"  # 30..600, multiple of 30, default 300
LOAD_INTERVAL_REMOVE_1712 = '<load-interval nc:operation="remove"/>'
MAX_BANDWIDTH_1712        = "<max-reserved-bandwidth>$percent</max-reserved-bandwidth>"  # 1..100
MAX_BANDWIDTH_REMOVE_1712 = '<max-reserved-bandwidth nc:operation="remove"/>'

# negotiation: ucse, Ethernet-Internal only (interface-negotiation-grouping); only <auto> exists
NEGOTIATION_1712          = "<negotiation><auto>$flag</auto></negotiation>"
NEGOTIATION_REMOVE_1712   = '<negotiation nc:operation="remove"/>'
GEN_MDIX_1712             = "<mdix><auto>$flag</auto></mdix>"
GEN_MDIX_REMOVE_1712      = '<mdix nc:operation="remove"/>'

SERVICE_INSERTION_1712        = "<service-insertion>$svc</service-insertion>"   # waas | appqoe
SERVICE_INSERTION_REMOVE_1712 = '<service-insertion nc:operation="remove"/>'
QOS_TRUST_1712                = '<interface_qos><trust><device>$device</device></trust></interface_qos>'  # cisco-phone
QOS_TRUST_REMOVE_1712         = '<interface_qos nc:operation="remove"/>'
# interface-level trust container: cisco-phone | cts | ip-camera | media-player
TRUST_DEVICE_1712             = "<trust><device>$device</device></trust>"
TRUST_DEVICE_REMOVE_1712      = '<trust nc:operation="remove"/>'


# ============================================================
# 2. L2 SWITCHING
# ============================================================
L2_SWITCHPORT_TRUE_1712   = "<switchport-conf><switchport>true</switchport></switchport-conf>"
L2_SWITCHPORT_FALSE_1712  = "<switchport-conf><switchport>false</switchport></switchport-conf>"
L2_SWITCHPORT_REMOVE_1712 = '<switchport-conf><switchport nc:operation="remove"/></switchport-conf>'

# --- DTP (nonegotiate) ---
L2_DTP_DISABLE_TRUE_1712  = _sp('<nonegotiate xmlns="$SW"/>')
L2_DTP_DISABLE_FALSE_1712 = _sp('<nonegotiate xmlns="$SW" nc:operation="remove"/>')

# --- mode (choice: access | dot1q-tunnel | dynamic | private-vlan | trunk) ---
L2_MODE_ACCESS_1712       = _sp('<mode xmlns="$SW"><access/></mode>')
L2_MODE_TRUNK_1712        = _sp('<mode xmlns="$SW"><trunk/></mode>')
L2_MODE_DOT1Q_TUNNEL_1712 = _sp('<mode xmlns="$SW"><dot1q-tunnel/></mode>')
L2_MODE_DYNAMIC_1712      = _sp('<mode xmlns="$SW"><dynamic>$dyn</dynamic></mode>')   # auto | desirable
L2_MODE_PVLAN_HOST_1712        = _sp('<mode xmlns="$SW"><private-vlan><host/></private-vlan></mode>')
L2_MODE_PVLAN_PROMISCUOUS_1712 = _sp('<mode xmlns="$SW"><private-vlan><promiscuous/></private-vlan></mode>')
L2_MODE_REMOVE_1712       = _sp('<mode xmlns="$SW" nc:operation="remove"/>')

# --- voice / access vlan ---
L2_VOICE_FULL_1712 = _sp(
    '<voice xmlns="$SW"><vlan><vlan>$voice_vlan</vlan></vlan>'
    '<detect><cisco-phone><full-duplex/></cisco-phone></detect></voice>'
    '<access xmlns="$SW"><vlan><vlan>$access_vlan</vlan></vlan></access>'
)
L2_VOICE_FULL_REMOVE_1712 = _sp(
    '<voice xmlns="$SW" nc:operation="remove"/><access xmlns="$SW" nc:operation="remove"/>'
)
L2_VOICE_VLAN_ID_1712       = _sp('<voice xmlns="$SW"><vlan><vlan>$voice_vlan</vlan></vlan></voice>')
L2_VOICE_VLAN_DOT1P_1712    = _sp('<voice xmlns="$SW"><vlan><vlan>dot1p</vlan></vlan></voice>')
L2_VOICE_VLAN_NONE_1712     = _sp('<voice xmlns="$SW"><vlan><vlan>none</vlan></vlan></voice>')
L2_VOICE_VLAN_UNTAGGED_1712 = _sp('<voice xmlns="$SW"><vlan><vlan>untagged</vlan></vlan></voice>')
L2_VOICE_VLAN_NAME_1712     = _sp('<voice xmlns="$SW"><vlan><name>$vlan_name</name></vlan></voice>')
L2_VOICE_VLAN_REMOVE_1712   = _sp('<voice xmlns="$SW"><vlan nc:operation="remove"/></voice>')
L2_VOICE_DETECT_1712        = _sp('<voice xmlns="$SW"><detect><cisco-phone><full-duplex/></cisco-phone></detect></voice>')
L2_VOICE_DETECT_REMOVE_1712 = _sp('<voice xmlns="$SW"><detect nc:operation="remove"/></voice>')
L2_ACCESS_VLAN_1712         = _sp('<access xmlns="$SW"><vlan><vlan>$access_vlan</vlan></vlan></access>')
L2_ACCESS_VLAN_DYNAMIC_1712 = _sp('<access xmlns="$SW"><vlan><vlan>dynamic</vlan></vlan></access>')
L2_ACCESS_VLAN_NAME_1712    = _sp('<access xmlns="$SW"><vlan><name>$vlan_name</name></vlan></access>')
L2_ACCESS_VLAN_REMOVE_1712  = _sp('<access xmlns="$SW"><vlan nc:operation="remove"/></access>')

# --- trunk (SW module: allowed = vlans|all|none only; add/remove/except were removed 2018-07) ---
L2_TRUNK_ENCAPSULATION_1712        = _sp('<trunk xmlns="$SW"><encapsulation>$encap</encapsulation></trunk>')  # dot1q|isl|negotiate
L2_TRUNK_ENCAPSULATION_REMOVE_1712 = _sp('<trunk xmlns="$SW"><encapsulation nc:operation="remove"/></trunk>')
L2_TRUNK_ALLOWED_VLANS_1712        = _sp('<trunk xmlns="$SW"><allowed><vlan><vlans>$vlans</vlans></vlan></allowed></trunk>')
L2_TRUNK_ALLOWED_ALL_1712          = _sp('<trunk xmlns="$SW"><allowed><vlan><all/></vlan></allowed></trunk>')
L2_TRUNK_ALLOWED_NONE_1712         = _sp('<trunk xmlns="$SW"><allowed><vlan><none/></vlan></allowed></trunk>')
L2_TRUNK_ALLOWED_REMOVE_1712       = _sp('<trunk xmlns="$SW"><allowed nc:operation="remove"/></trunk>')
L2_TRUNK_NATIVE_VLAN_ID_1712       = _sp('<trunk xmlns="$SW"><native><vlan-id><vlan-id>$native_vlan</vlan-id></vlan-id></native></trunk>')
L2_TRUNK_NATIVE_VLAN_ID_REMOVE_1712 = _sp('<trunk xmlns="$SW"><native><vlan-id nc:operation="remove"/></native></trunk>')
L2_TRUNK_NATIVE_VLAN_TAG_1712      = _sp('<trunk xmlns="$SW"><native><vlan><tag>$flag</tag></vlan></native></trunk>')

# --- trunk pruning (choice: vlans (leaf-list) | add | except (leaf-list) | none | remove) ---
L2_TRUNK_PRUNING_ADD_1712    = _sp('<trunk xmlns="$SW"><pruning><vlan><add>$vlans</add></vlan></pruning></trunk>')
L2_TRUNK_PRUNING_REMOVE_1712 = _sp('<trunk xmlns="$SW"><pruning><vlan><remove>$vlans</remove></vlan></pruning></trunk>')
# replace is applied on the vlan container so the whole choice/leaf-list is replaced
L2_TRUNK_PRUNING_REPLACE_1712 = _sp(
    '<trunk xmlns="$SW"><pruning><vlan nc:operation="replace"><vlans>$vlans</vlans></vlan></pruning></trunk>'
)
L2_TRUNK_PRUNING_NONE_1712   = _sp('<trunk xmlns="$SW"><pruning><vlan><none/></vlan></pruning></trunk>')
L2_TRUNK_PRUNING_REMOVE_ALL_1712 = _sp('<trunk xmlns="$SW"><pruning nc:operation="remove"/></trunk>')

# --- native-namespace switchport-wrapper (Gig / AppGig; ucse, Ethernet-Internal, Wlan-Gig deprecated) ---
L2W_MODE_1712               = _w("<mode>$wmode</mode>")                          # access | trunk
L2W_MODE_REMOVE_1712        = _w('<mode nc:operation="remove"/>')
L2W_ACCESS_VLAN_1712        = _w("<access><vlan>$access_vlan</vlan></access>")
L2W_ACCESS_VLAN_REMOVE_1712 = _w('<access nc:operation="remove"/>')
L2W_NATIVE_VLAN_1712        = _w("<native><vlan>$native_vlan</vlan></native>")
L2W_NATIVE_VLAN_REMOVE_1712 = _w('<native nc:operation="remove"/>')
L2W_TRUNK_ALLOWED_VLANS_1712 = _w("<trunk><allowed><vlan><vlans>$vlans</vlans></vlan></allowed></trunk>")
L2W_TRUNK_ALLOWED_ADD_1712   = _w("<trunk><allowed><vlan><add>$vlans</add></vlan></allowed></trunk>")
L2W_TRUNK_ALLOWED_REMOVE_VLANS_1712 = _w("<trunk><allowed><vlan><remove>$vlans</remove></vlan></allowed></trunk>")
L2W_TRUNK_ALLOWED_EXCEPT_1712 = _w("<trunk><allowed><vlan><except>$vlans</except></vlan></allowed></trunk>")
L2W_TRUNK_ALLOWED_ALL_1712   = _w("<trunk><allowed><vlan><all/></vlan></allowed></trunk>")
L2W_TRUNK_ALLOWED_NONE_1712  = _w("<trunk><allowed><vlan><none/></vlan></allowed></trunk>")
L2W_TRUNK_ALLOWED_REMOVE_1712 = _w('<trunk><allowed nc:operation="remove"/></trunk>')

# --- PVLAN interface bindings (SW module) ---
PVLAN_HOST_ASSOC_1712 = _sp(
    '<mode xmlns="$SW"><private-vlan><host/></private-vlan></mode>'
    '<private-vlan xmlns="$SW"><host-association>'
    '<primary-range>$primary_vlan</primary-range>'
    '<secondary-range>$secondary_vlan</secondary-range>'
    '</host-association></private-vlan>'
)
PVLAN_HOST_ASSOC_REMOVE_1712 = _sp(
    '<private-vlan xmlns="$SW"><host-association nc:operation="remove"/></private-vlan>'
)
PVLAN_PROMISCUOUS_MAP_1712 = _sp(
    '<mode xmlns="$SW"><private-vlan><promiscuous/></private-vlan></mode>'
    '<private-vlan xmlns="$SW"><mapping>'
    '<primary-range>$primary_vlan</primary-range>'
    '<secondary-range>$secondary_vlans</secondary-range>'
    '</mapping></private-vlan>'
)
PVLAN_PROMISCUOUS_MAP_ADD_1712 = _sp(
    '<private-vlan xmlns="$SW"><mapping><primary-range>$primary_vlan</primary-range>'
    '<add>$secondary_vlans</add></mapping></private-vlan>'
)
PVLAN_PROMISCUOUS_MAP_REMOVE_VLANS_1712 = _sp(
    '<private-vlan xmlns="$SW"><mapping><primary-range>$primary_vlan</primary-range>'
    '<remove>$secondary_vlans</remove></mapping></private-vlan>'
)
PVLAN_PROMISCUOUS_MAP_REMOVE_1712 = _sp(
    '<private-vlan xmlns="$SW"><mapping nc:operation="remove"/></private-vlan>'
)

# --- PVLAN global (Cisco-IOS-XE-vlan; NATIVE-scoped, if-feature private-vlan) ---
PVLAN_GLOBAL_1712 = (
    '<vlan xmlns="$N"><vlan-list xmlns="$VLAN">'
    '<id>$primary_vlan</id>'
    '<private-vlan><primary/><association>$secondary_vlans</association></private-vlan>'
    '</vlan-list></vlan>'
)
PVLAN_GLOBAL_PRIMARY_1712 = (
    '<vlan xmlns="$N"><vlan-list xmlns="$VLAN">'
    '<id>$primary_vlan</id><private-vlan><primary/></private-vlan>'
    '</vlan-list></vlan>'
)
PVLAN_GLOBAL_ASSOC_1712 = (
    '<vlan xmlns="$N"><vlan-list xmlns="$VLAN">'
    '<id>$primary_vlan</id><private-vlan><association>$secondary_vlans</association></private-vlan>'
    '</vlan-list></vlan>'
)
PVLAN_GLOBAL_REMOVE_1712 = (
    '<vlan xmlns="$N"><vlan-list xmlns="$VLAN">'
    '<id>$primary_vlan</id><private-vlan nc:operation="remove"/>'
    '</vlan-list></vlan>'
)
# $pvlan_type: community | isolated
PVLAN_SECONDARY_1712 = (
    '<vlan xmlns="$N"><vlan-list xmlns="$VLAN">'
    '<id>$secondary_vlan</id><private-vlan><$pvlan_type/></private-vlan>'
    '</vlan-list></vlan>'
)
PVLAN_SECONDARY_REMOVE_1712 = (
    '<vlan xmlns="$N"><vlan-list xmlns="$VLAN" nc:operation="remove"><id>$secondary_vlan</id></vlan-list></vlan>'
)

# --- port-security (presence container: aging / mac-address / maximum / violation) ---
L2_PORTSEC_ENABLE_1712        = _sp('<port-security xmlns="$SW"/>')
L2_PORTSEC_ENABLE_REMOVE_1712 = _sp('<port-security xmlns="$SW" nc:operation="remove"/>')
L2_PORTSEC_MAX_1712 = _sp(          # max-addresses 1..4097
    '<port-security xmlns="$SW"><maximum><max-addresses>$max</max-addresses></maximum></port-security>'
)
L2_PORTSEC_MAX_VLAN_1712 = _sp(     # vlan leaf is a string ("access", "voice", list ...)
    '<port-security xmlns="$SW"><maximum><max-addresses>$max</max-addresses>'
    '<vlan>$vlan_kind</vlan></maximum></port-security>'
)
L2_PORTSEC_MAX_REMOVE_1712 = _sp(
    '<port-security xmlns="$SW"><maximum nc:operation="remove"/></port-security>'
)
# $violation in: protect | restrict | shutdown   (leaf enumeration)
L2_PORTSEC_VIOLATION_1712 = _sp(
    '<port-security xmlns="$SW"><violation>$violation</violation></port-security>'
)
L2_PORTSEC_VIOLATION_REMOVE_1712 = _sp(
    '<port-security xmlns="$SW"><violation nc:operation="remove"/></port-security>'
)
L2_PORTSEC_STICKY_1712 = _sp(       # mac-address sticky (leaf empty)
    '<port-security xmlns="$SW"><mac-address><sticky/></mac-address></port-security>'
)
L2_PORTSEC_STICKY_REMOVE_1712 = _sp(
    '<port-security xmlns="$SW"><mac-address><sticky nc:operation="remove"/></mac-address></port-security>'
)
L2_PORTSEC_AGING_1712 = _sp(        # time 1..1440; type absolute|inactivity
    '<port-security xmlns="$SW"><aging><time>$minutes</time><type>$aging_type</type></aging></port-security>'
)
L2_PORTSEC_AGING_STATIC_1712 = _sp(
    '<port-security xmlns="$SW"><aging><static/></aging></port-security>'
)
L2_PORTSEC_AGING_REMOVE_1712 = _sp(
    '<port-security xmlns="$SW"><aging nc:operation="remove"/></port-security>'
)
# mac-address is a container with ONE hw-address leaf (yang:mac-address => xx:xx:xx:xx:xx:xx)
L2_PORTSEC_MAC_ACCESS_1712 = _sp(
    '<port-security xmlns="$SW"><mac-address><hw-address>$hwaddr</hw-address></mac-address></port-security>'
)
L2_PORTSEC_MAC_ACCESS_VLAN_1712 = _sp(
    '<port-security xmlns="$SW"><mac-address><hw-address>$hwaddr</hw-address>'
    '<vlan>$vlan_id</vlan></mac-address></port-security>'
)
L2_PORTSEC_MAC_ACCESS_REMOVE_1712 = _sp(
    '<port-security xmlns="$SW"><mac-address><hw-address nc:operation="remove"/></mac-address></port-security>'
)

# --- protected / host / block / vepa ---
L2_PROTECTED_1712        = _sp('<protected xmlns="$SW"/>')
L2_PROTECTED_REMOVE_1712 = _sp('<protected xmlns="$SW" nc:operation="remove"/>')
L2_HOST_1712             = _sp('<host xmlns="$SW"/>')
L2_HOST_REMOVE_1712      = _sp('<host xmlns="$SW" nc:operation="remove"/>')
L2_BLOCK_MULTICAST_1712        = _sp('<block xmlns="$SW"><multicast/></block>')
L2_BLOCK_MULTICAST_REMOVE_1712 = _sp('<block xmlns="$SW"><multicast nc:operation="remove"/></block>')
L2_BLOCK_UNICAST_1712          = _sp('<block xmlns="$SW"><unicast/></block>')
L2_BLOCK_UNICAST_REMOVE_1712   = _sp('<block xmlns="$SW"><unicast nc:operation="remove"/></block>')
L2_VEPA_1712             = _sp('<vepa xmlns="$SW"><enabled/></vepa>')
L2_VEPA_REMOVE_1712      = _sp('<vepa xmlns="$SW"><enabled nc:operation="remove"/></vepa>')
L2_AUTOSTATE_EXCLUDE_1712        = _sp('<autostate xmlns="$SW"><exclude/></autostate>')
L2_AUTOSTATE_EXCLUDE_REMOVE_1712 = _sp('<autostate xmlns="$SW"><exclude nc:operation="remove"/></autostate>')
L2_PRIORITY_EXTEND_TRUST_1712    = _sp('<priority xmlns="$SW"><extend><trust/></extend></priority>')
L2_PRIORITY_EXTEND_COS_1712      = _sp('<priority xmlns="$SW"><extend><cos>$cos</cos></extend></priority>')
L2_PRIORITY_EXTEND_REMOVE_1712   = _sp('<priority xmlns="$SW"><extend nc:operation="remove"/></priority>')

# --- L2PT (native-namespace l2protocol-tunnel; presence container) ---
# $proto in: cdp stp vtp lldp (+ mvrp dtp ptppd mmrp elmi link-oam esmc if feature l2pt-more-protocols)
L2PT_TUNNEL_CORE_1712            = '<l2protocol-tunnel><$proto/></l2protocol-tunnel>'
L2PT_TUNNEL_CORE_REMOVE_1712     = '<l2protocol-tunnel><$proto nc:operation="remove"/></l2protocol-tunnel>'
L2PT_TUNNEL_P2P_1712             = '<l2protocol-tunnel><point-to-point><$p2p_proto/></point-to-point></l2protocol-tunnel>'
L2PT_TUNNEL_P2P_REMOVE_1712      = '<l2protocol-tunnel><point-to-point><$p2p_proto nc:operation="remove"/></point-to-point></l2protocol-tunnel>'
L2PT_TUNNEL_CORE_BLOCK_1712      = '<l2protocol-tunnel>$core_block</l2protocol-tunnel>'
L2PT_TUNNEL_CORE_BLOCK_REMOVE_1712 = '<l2protocol-tunnel nc:operation="remove"/>'
L2PT_TUNNEL_P2P_BLOCK_1712       = '<l2protocol-tunnel><point-to-point>$p2p_block</point-to-point></l2protocol-tunnel>'
L2PT_TUNNEL_P2P_BLOCK_REMOVE_1712 = '<l2protocol-tunnel><point-to-point nc:operation="remove"/></l2protocol-tunnel>'

# thresholds: uint16 leaves directly under drop-/shutdown-threshold (1..4096)
L2PT_DROP_THRESHOLD_1712 = '<l2protocol-tunnel><drop-threshold><$proto>$pps</$proto></drop-threshold></l2protocol-tunnel>'
L2PT_DROP_THRESHOLD_REMOVE_1712 = (
    '<l2protocol-tunnel><drop-threshold><$proto nc:operation="remove"/></drop-threshold></l2protocol-tunnel>'
)
L2PT_DROP_THRESHOLD_RATE_1712 = (
    '<l2protocol-tunnel><drop-threshold><packet-rate>$pps</packet-rate></drop-threshold></l2protocol-tunnel>'
)
L2PT_DROP_THRESHOLD_RATE_REMOVE_1712 = (
    '<l2protocol-tunnel><drop-threshold><packet-rate nc:operation="remove"/></drop-threshold></l2protocol-tunnel>'
)
L2PT_DROP_THRESHOLD_P2P_1712 = (
    '<l2protocol-tunnel><drop-threshold><point-to-point><$p2p_proto>$pps</$p2p_proto>'
    '</point-to-point></drop-threshold></l2protocol-tunnel>'
)
L2PT_DROP_THRESHOLD_P2P_REMOVE_1712 = (
    '<l2protocol-tunnel><drop-threshold><point-to-point><$p2p_proto nc:operation="remove"/>'
    '</point-to-point></drop-threshold></l2protocol-tunnel>'
)
L2PT_SHUTDOWN_THRESHOLD_1712 = (
    '<l2protocol-tunnel><shutdown-threshold><$proto>$pps</$proto></shutdown-threshold></l2protocol-tunnel>'
)
L2PT_SHUTDOWN_THRESHOLD_REMOVE_1712 = (
    '<l2protocol-tunnel><shutdown-threshold><$proto nc:operation="remove"/></shutdown-threshold></l2protocol-tunnel>'
)
L2PT_SHUTDOWN_THRESHOLD_RATE_1712 = (
    '<l2protocol-tunnel><shutdown-threshold><packet-rate>$pps</packet-rate></shutdown-threshold></l2protocol-tunnel>'
)
L2PT_SHUTDOWN_THRESHOLD_RATE_REMOVE_1712 = (
    '<l2protocol-tunnel><shutdown-threshold><packet-rate nc:operation="remove"/></shutdown-threshold></l2protocol-tunnel>'
)
L2PT_SHUTDOWN_THRESHOLD_P2P_1712 = (
    '<l2protocol-tunnel><shutdown-threshold><point-to-point><$p2p_proto>$pps</$p2p_proto>'
    '</point-to-point></shutdown-threshold></l2protocol-tunnel>'
)
L2PT_SHUTDOWN_THRESHOLD_P2P_REMOVE_1712 = (
    '<l2protocol-tunnel><shutdown-threshold><point-to-point><$p2p_proto nc:operation="remove"/>'
    '</point-to-point></shutdown-threshold></l2protocol-tunnel>'
)

# --- l2protocol forward (if-feature l2cp-fwd) ---
L2PT_FORWARD_PROTOCOL_1712        = '<l2protocol><forward><protocols>$proto</protocols></forward></l2protocol>'
L2PT_FORWARD_PROTOCOL_REMOVE_1712 = '<l2protocol><forward><protocols nc:operation="remove">$proto</protocols></forward></l2protocol>'
L2PT_FORWARD_BLOCK_1712           = '<l2protocol><forward>$proto_block</forward></l2protocol>'
L2PT_FORWARD_BLOCK_REMOVE_1712    = '<l2protocol><forward nc:operation="remove"/></l2protocol>'
L2PT_FORWARD_DROP_1712 = (
    '<l2protocol><forward><drop-threshold><threshold-list>'
    '<proto-type>$proto</proto-type><pps-num>$pps</pps-num>'
    '</threshold-list></drop-threshold></forward></l2protocol>'
)
L2PT_FORWARD_DROP_REMOVE_1712 = '<l2protocol><forward><drop-threshold nc:operation="remove"/></forward></l2protocol>'
L2PT_FORWARD_SHUTDOWN_1712 = (
    '<l2protocol><forward><shutdown-threshold><threshold-list>'
    '<proto-type>$proto</proto-type><pps-num>$pps</pps-num>'
    '</threshold-list></shutdown-threshold></forward></l2protocol>'
)
L2PT_FORWARD_SHUTDOWN_REMOVE_1712 = '<l2protocol><forward><shutdown-threshold nc:operation="remove"/></forward></l2protocol>'


# ============================================================
# 3. ARP + LINK TUNING
# ============================================================
ARP_TIMEOUT_1712         = "<arp><timeout>$secs</timeout></arp>"       # 0..2147483
ARP_TIMEOUT_REMOVE_1712  = '<arp><timeout nc:operation="remove"/></arp>'
ARP_SNAP_TRUE_1712       = "<arp><snap/></arp>"
ARP_SNAP_FALSE_1712      = '<arp><snap nc:operation="remove"/></arp>'
ARP_AUTHORIZED_1712        = "<arp><authorized/></arp>"
ARP_AUTHORIZED_REMOVE_1712 = '<arp><authorized nc:operation="remove"/></arp>'
ARP_LOG_THRESHOLD_1712 = "<arp><log><threshold><entries>$count</entries></threshold></log></arp>"
ARP_LOG_THRESHOLD_REMOVE_1712 = '<arp><log nc:operation="remove"/></arp>'
ARP_ENTRY_LIMIT_1712 = (
    "<arp><entries><interface-limit>"
    "<entry-count>$count</entry-count><log>$log_secs</log>"
    "</interface-limit></entries></arp>"
)
ARP_ENTRY_LIMIT_REMOVE_1712 = '<arp><entries><interface-limit nc:operation="remove"/></entries></arp>'
ARP_PACKET_PRIORITY_1712 = "<arp><packet-priority><enable/></packet-priority></arp>"
ARP_PACKET_PRIORITY_REMOVE_1712 = (
    '<arp><packet-priority><enable nc:operation="remove"/></packet-priority></arp>'
)

PQ_OUT_ENABLE_1712        = "<priority-queue><out/></priority-queue>"
PQ_OUT_ENABLE_REMOVE_1712 = '<priority-queue><out nc:operation="remove"/></priority-queue>'
# cos-map under priority-queue is a CONTAINER (single instance); cos-values max 8, 0..7
PQ_COS_MAP_1712 = (
    "<priority-queue><cos-map><id>$qid</id>$cos_values_block</cos-map></priority-queue>"
)
PQ_COS_MAP_REMOVE_1712 = '<priority-queue><cos-map nc:operation="remove"/></priority-queue>'
RCV_QUEUE_COS_MAP_1712 = (
    "<rcv-queue><cos-map><queue-id>$qid</queue-id><threshold-id>$tid</threshold-id>"
    "$cos_values_block</cos-map></rcv-queue>"
)
RCV_QUEUE_COS_MAP_REMOVE_1712 = (
    '<rcv-queue><cos-map nc:operation="remove">'
    '<queue-id>$qid</queue-id><threshold-id>$tid</threshold-id></cos-map></rcv-queue>'
)

FLOWCONTROL_1712        = "<flowcontrol><receive>$rx</receive><send>$tx</send></flowcontrol>"
FLOWCONTROL_REMOVE_1712 = '<flowcontrol nc:operation="remove"/>'
HOLD_QUEUE_1712 = (
    "<hold-queue><direction>$direction</direction><queue-length>$qlen</queue-length></hold-queue>"
)
HOLD_QUEUE_REMOVE_1712 = (
    '<hold-queue nc:operation="remove"><direction>$direction</direction></hold-queue>'
)

LINK_BANDWIDTH_1712        = "<bandwidth><kilobits>$kbps</kilobits></bandwidth>"   # 1..200000000
LINK_BANDWIDTH_REMOVE_1712 = '<bandwidth nc:operation="remove"/>'
LINK_BANDWIDTH_QOS_REF_1712        = "<bandwidth><qos-reference>$kbps</qos-reference></bandwidth>"  # 1..10000000
LINK_BANDWIDTH_QOS_REF_REMOVE_1712 = '<bandwidth><qos-reference nc:operation="remove"/></bandwidth>'

DAMPENING_FULL_1712 = (
    "<dampening>"
    "<dampening-time>$half_life</dampening-time>"
    "<start-reusing-time>$reuse</start-reusing-time>"
    "<start-supressing-time>$suppress</start-supressing-time>"
    "<maximum-supressing-time>$max_suppress</maximum-supressing-time>"
    "</dampening>"
)
DAMPENING_DEFAULT_1712 = "<dampening/>"
DAMPENING_REMOVE_1712  = '<dampening nc:operation="remove"/>'

SRLG_1712        = "<srlg><gid>$srlg_values_block</gid></srlg>"     # block = <value>n</value>...
SRLG_REMOVE_1712 = '<srlg nc:operation="remove"/>'

DOMAIN_NAME_1712        = "<domain><name>$domain</name></domain>"
DOMAIN_NAME_REMOVE_1712 = '<domain><name nc:operation="remove"/></domain>'
DOMAIN_PATH_1712        = "<domain><path>$sp_path</path><path-id>$path_id</path-id></domain>"
DOMAIN_PATH_REMOVE_1712 = '<domain><path nc:operation="remove">$sp_path</path></domain>'

# keepalive: choice { leaf keepalive (boolean, default true) | keepalive-settings/keepalive{period,retries} }
KEEPALIVE_TIMERS_1712 = (
    "<keepalive-settings><keepalive>"
    "<period>$period</period><retries>$retries</retries>"
    "</keepalive></keepalive-settings>"
)
KEEPALIVE_TIMERS_REMOVE_1712 = '<keepalive-settings nc:operation="remove"/>'
KEEPALIVE_DISABLE_1712       = "<keepalive>false</keepalive>"
KEEPALIVE_REMOVE_1712        = '<keepalive nc:operation="remove"/>'

# --- logging ---
LINK_LOGGING_LINK_STATUS_1712 = (
    "<logging><event><link-status-enable>$flag</link-status-enable></event></logging>"
)
LINK_LOGGING_LINK_STATUS_REMOVE_1712 = (
    '<logging><event><link-status-enable nc:operation="remove"/></event></logging>'
)
# $event in: bundle-status trunk-status nfas-status power-inline-status status
LINK_LOGGING_EVENT_1712        = "<logging><event><$event/></event></logging>"
LINK_LOGGING_EVENT_REMOVE_1712 = '<logging><event><$event nc:operation="remove"/></event></logging>'
LINK_LOGGING_EVENTS_BLOCK_1712        = "<logging><event>$events_block</event></logging>"
LINK_LOGGING_EVENTS_BLOCK_REMOVE_1712 = '<logging><event nc:operation="remove"/></logging>'
LINK_LOGGING_SPANNING_TREE_1712 = (
    "<logging><event><spanning-tree><status/></spanning-tree></event></logging>"
)
LINK_LOGGING_SPANNING_TREE_REMOVE_1712 = (
    '<logging><event><spanning-tree nc:operation="remove"/></event></logging>'
)
LINK_LOGGING_SUBIF_1712 = (
    "<logging><event><subif-link-status>$ignore_bulk_block</subif-link-status></event></logging>"
)
LINK_LOGGING_SUBIF_REMOVE_1712 = (
    '<logging><event><subif-link-status nc:operation="remove"/></event></logging>'
)

FAIR_QUEUE_1712        = "<fair-queue><incomplete/></fair-queue>"
FAIR_QUEUE_REMOVE_1712 = '<fair-queue nc:operation="remove"/>'
FAIR_QUEUE_CONF_1712   = "<fair-queue-conf><fair-queue>$flag</fair-queue></fair-queue-conf>"


# ============================================================
# 4. IPv4
# ============================================================
IP4_PRIMARY_1712 = (
    "<ip><address><primary><address>$ip</address><mask>$mask</mask></primary></address></ip>"
)
IP4_PRIMARY_REMOVE_1712 = '<ip><address><primary nc:operation="remove"/></address></ip>'
IP4_SECONDARY_1712 = (
    "<ip><address><secondary><address>$ip</address><mask>$mask</mask><secondary/>"
    "</secondary></address></ip>"
)
IP4_SECONDARY_REMOVE_1712 = (
    '<ip><address><secondary nc:operation="remove">'
    '<address>$ip</address></secondary></address></ip>'
)
IP4_DHCP_1712               = "<ip><address><dhcp/></address></ip>"
IP4_DHCP_REMOVE_1712        = '<ip><address><dhcp nc:operation="remove"/></address></ip>'
IP4_NEGOTIATED_1712         = "<ip><address><negotiated/></address></ip>"
IP4_NEGOTIATED_REMOVE_1712  = '<ip><address><negotiated nc:operation="remove"/></address></ip>'
# $client_id_block e.g. <client-id><GigabitEthernet>1/0/1</GigabitEthernet></client-id>
IP4_DHCP_OPTIONS_1712 = "<ip><address><dhcp>$client_id_block$hostname_block</dhcp></address></ip>"
IP4_UNNUMBERED_1712         = "<ip><unnumbered>$src_if</unnumbered></ip>"
IP4_UNNUMBERED_REMOVE_1712  = '<ip><unnumbered nc:operation="remove"/></ip>'

IP4_ACCESS_GROUP_IN_1712 = (
    "<ip><access-group><in><acl><acl-name>$acl</acl-name><in/></acl></in></access-group></ip>"
)
IP4_ACCESS_GROUP_IN_REMOVE_1712 = '<ip><access-group><in nc:operation="remove"/></access-group></ip>'
IP4_ACCESS_GROUP_OUT_1712 = (
    "<ip><access-group><out><acl><acl-name>$acl</acl-name><out/></acl></out></access-group></ip>"
)
IP4_ACCESS_GROUP_OUT_REMOVE_1712 = '<ip><access-group><out nc:operation="remove"/></access-group></ip>'
IP4_ACCESS_GROUP_COMMON_IN_1712 = (
    "<ip><access-group><in><common-acl><common>$common_acl</common>"
    "<acl-name>$acl</acl-name><in/></common-acl></in></access-group></ip>"
)
IP4_ACCESS_GROUP_COMMON_IN_REMOVE_1712 = (
    '<ip><access-group><in><common-acl nc:operation="remove"/></in></access-group></ip>'
)
IP4_ACCESS_GROUP_COMMON_OUT_1712 = (
    "<ip><access-group><out><common-acl><common>$common_acl</common>"
    "<acl-name>$acl</acl-name><out/></common-acl></out></access-group></ip>"
)
IP4_ACCESS_GROUP_COMMON_OUT_REMOVE_1712 = (
    '<ip><access-group><out><common-acl nc:operation="remove"/></out></access-group></ip>'
)

IP4_VRF_FORWARDING_1712        = "<vrf><forwarding>$vrf</forwarding></vrf>"
IP4_VRF_FORWARDING_REMOVE_1712 = '<vrf><forwarding nc:operation="remove">$vrf</forwarding></vrf>'
IP4_VRF_DOWNSTREAM_1712        = "<vrf><forwarding>$vrf</forwarding><downstream>$vrf_down</downstream></vrf>"
IP4_VRF_RECEIVE_1712           = "<ip><vrf><receive>$vrf</receive></vrf></ip>"
IP4_VRF_RECEIVE_REMOVE_1712    = '<ip><vrf><receive nc:operation="remove">$vrf</receive></vrf></ip>'
IP4_VRF_SITEMAP_1712           = "<ip><vrf><sitemap>$route_map</sitemap></vrf></ip>"
IP4_VRF_SITEMAP_REMOVE_1712    = '<ip><vrf><sitemap nc:operation="remove">$route_map</sitemap></vrf></ip>'

IP4_HELPER_1712        = "<ip><helper-address><address>$helper</address></helper-address></ip>"
IP4_HELPER_REMOVE_1712 = (
    '<ip><helper-address nc:operation="remove"><address>$helper</address></helper-address></ip>'
)
IP4_HELPER_GLOBAL_1712 = (
    "<ip><helper-address><address>$helper</address><global/></helper-address></ip>"
)
IP4_HELPER_GLOBAL_REMOVE_1712 = (
    '<ip><helper-address nc:operation="remove"><address>$helper</address><global/></helper-address></ip>'
)
IP4_HELPER_VRF_1712 = (
    "<ip><helper-address><address>$helper</address><vrf>$vrf</vrf></helper-address></ip>"
)
IP4_HELPER_VRF_REMOVE_1712 = (
    '<ip><helper-address nc:operation="remove"><address>$helper</address><vrf>$vrf</vrf></helper-address></ip>'
)

IP4_POLICY_ROUTE_MAP_1712        = "<ip><policy><route-map>$route_map</route-map></policy></ip>"
IP4_POLICY_ROUTE_MAP_REMOVE_1712 = '<ip><policy><route-map nc:operation="remove"/></policy></ip>'

IP4_PROXY_ARP_1712              = "<ip><proxy-arp>$flag</proxy-arp></ip>"
IP4_PROXY_ARP_REMOVE_1712       = '<ip><proxy-arp nc:operation="remove"/></ip>'
IP4_LOCAL_PROXY_ARP_1712        = "<ip><local-proxy-arp/></ip>"
IP4_LOCAL_PROXY_ARP_REMOVE_1712 = '<ip><local-proxy-arp nc:operation="remove"/></ip>'
IP4_REDIRECTS_1712              = "<ip><redirects>$flag</redirects></ip>"
IP4_REDIRECTS_REMOVE_1712       = '<ip><redirects nc:operation="remove"/></ip>'
IP4_CLEAR_DF_1712               = "<ip><clear-dont-fragment>$flag</clear-dont-fragment></ip>"
IP4_CLEAR_DF_REMOVE_1712        = '<ip><clear-dont-fragment nc:operation="remove"/></ip>'
IP4_NETWORK_BROADCAST_1712        = "<ip><network-broadcast/></ip>"
IP4_NETWORK_BROADCAST_REMOVE_1712 = '<ip><network-broadcast nc:operation="remove"/></ip>'
IP4_MASK_REPLY_1712             = "<ip><mask-reply/></ip>"
IP4_MASK_REPLY_REMOVE_1712      = '<ip><mask-reply nc:operation="remove"/></ip>'
IP4_TCP_MSS_1712                = "<ip><tcp><adjust-mss>$mss</adjust-mss></tcp></ip>"      # 500..1460
IP4_TCP_MSS_REMOVE_1712         = '<ip><tcp><adjust-mss nc:operation="remove"/></tcp></ip>'
IP4_MTU_1712                    = "<ip><mtu>$ip_mtu</mtu></ip>"                            # 68..18000
IP4_MTU_REMOVE_1712             = '<ip><mtu nc:operation="remove"/></ip>'

# uRPF: verify/unicast/source {reachable-via any|rx, allow-self-ping, allow-default}; no ACL leaf
# $allow_block e.g. "<allow-default/><allow-self-ping/>" ("" to omit)
IP4_URPF_1712 = (
    "<ip><verify><unicast><source>"
    "<reachable-via>$via</reachable-via>$allow_block"
    "</source></unicast></verify></ip>"
)
IP4_URPF_REMOVE_1712 = '<ip><verify><unicast nc:operation="remove"/></verify></ip>'
IP4_URPF_REVERSE_PATH_1712        = "<ip><verify><unicast><reverse-path/></unicast></verify></ip>"
IP4_URPF_REVERSE_PATH_REMOVE_1712 = '<ip><verify><unicast><reverse-path nc:operation="remove"/></unicast></verify></ip>'

IP4_ARP_INSPECT_TRUST_1712 = "<ip><arp><inspection><trust/></inspection></arp></ip>"
IP4_ARP_INSPECT_TRUST_REMOVE_1712 = (
    '<ip><arp><inspection><trust nc:operation="remove"/></inspection></arp></ip>'
)
IP4_ARP_INSPECT_RATE_1712 = "<ip><arp><inspection><limit><rate>$pps</rate></limit></inspection></arp></ip>"
IP4_ARP_INSPECT_RATE_REMOVE_1712 = (
    '<ip><arp><inspection><limit nc:operation="remove"/></inspection></arp></ip>'
)
IP4_ARP_INSPECT_RATE_NONE_1712 = "<ip><arp><inspection><limit><none/></limit></inspection></arp></ip>"

IP4_DIRECTED_BROADCAST_1712        = "<ip><directed-broadcast/></ip>"
IP4_DIRECTED_BROADCAST_REMOVE_1712 = '<ip><directed-broadcast nc:operation="remove"/></ip>'
IP4_DIRECTED_BROADCAST_ACL_1712 = (
    "<ip><directed-broadcast><direct-broadcast>$acl</direct-broadcast></directed-broadcast></ip>"
)


# ============================================================
# 5. IPv6
# ============================================================
IP6_ENABLE_1712        = "<ipv6><enable/></ipv6>"
IP6_ENABLE_REMOVE_1712 = '<ipv6><enable nc:operation="remove"/></ipv6>'

IP6_ADDRESS_PREFIX_1712 = "<ipv6><address><prefix-list><prefix>$ipv6</prefix></prefix-list></address></ipv6>"
IP6_ADDRESS_PREFIX_REMOVE_1712 = (
    '<ipv6><address><prefix-list nc:operation="remove"><prefix>$ipv6</prefix></prefix-list></address></ipv6>'
)
IP6_ADDRESS_EUI64_1712 = (
    "<ipv6><address><prefix-list><prefix>$ipv6</prefix><eui-64/></prefix-list></address></ipv6>"
)
IP6_ADDRESS_EUI64_REMOVE_1712 = (
    '<ipv6><address><prefix-list nc:operation="remove"><prefix>$ipv6</prefix></prefix-list></address></ipv6>'
)
IP6_ADDRESS_ANYCAST_1712 = (
    "<ipv6><address><prefix-list><prefix>$ipv6</prefix><anycast/></prefix-list></address></ipv6>"
)
IP6_ADDRESS_ANYCAST_REMOVE_1712 = (
    '<ipv6><address><prefix-list nc:operation="remove"><prefix>$ipv6</prefix></prefix-list></address></ipv6>'
)
IP6_ADDRESS_LINK_LOCAL_1712 = (
    "<ipv6><address><link-local-address><address>$ll</address><link-local/>"
    "</link-local-address></address></ipv6>"
)
IP6_ADDRESS_LINK_LOCAL_REMOVE_1712 = (
    '<ipv6><address><link-local-address nc:operation="remove"><address>$ll</address>'
    '</link-local-address></address></ipv6>'
)
IP6_ADDRESS_AUTOCONFIG_1712        = "<ipv6><address><autoconfig/></address></ipv6>"
IP6_ADDRESS_AUTOCONFIG_REMOVE_1712 = '<ipv6><address><autoconfig nc:operation="remove"/></address></ipv6>'
IP6_ADDRESS_AUTOCONFIG_DEFAULT_1712 = "<ipv6><address><autoconfig><default/></autoconfig></address></ipv6>"
IP6_ADDRESS_AUTOCONFIG_DEFAULT_REMOVE_1712 = (
    '<ipv6><address><autoconfig><default nc:operation="remove"/></autoconfig></address></ipv6>'
)
IP6_ADDRESS_DHCP_1712        = "<ipv6><address><dhcp/></address></ipv6>"
IP6_ADDRESS_DHCP_REMOVE_1712 = '<ipv6><address><dhcp nc:operation="remove"/></address></ipv6>'
IP6_ADDRESS_DHCP_RAPID_COMMIT_1712 = "<ipv6><address><dhcp><rapid-commit/></dhcp></address></ipv6>"
IP6_ADDRESS_DHCP_RAPID_COMMIT_REMOVE_1712 = (
    '<ipv6><address><dhcp><rapid-commit nc:operation="remove"/></dhcp></address></ipv6>'
)
IP6_ADDRESS_PREFIX_NAME_1712 = (
    "<ipv6><address><prefix-name><name>$pfx_name</name><prefix-options>"
    "<ipv6-prefix><prefix>$ipv6</prefix></ipv6-prefix></prefix-options></prefix-name></address></ipv6>"
)
IP6_ADDRESS_PREFIX_NAME_REMOVE_1712 = (
    '<ipv6><address><prefix-name nc:operation="remove"><name>$pfx_name</name></prefix-name></address></ipv6>'
)

IP6_UNNUMBERED_1712        = "<ipv6><unnumbered>$src_if</unnumbered></ipv6>"
IP6_UNNUMBERED_REMOVE_1712 = '<ipv6><unnumbered nc:operation="remove"/></ipv6>'
IP6_MTU_1712               = "<ipv6><mtu>$ip6_mtu</mtu></ipv6>"                   # 1280..9976
IP6_MTU_REMOVE_1712        = '<ipv6><mtu nc:operation="remove"/></ipv6>'
IP6_TCP_ADJUST_MSS_1712        = "<ipv6><tcp><adjust-mss>$mss</adjust-mss></tcp></ipv6>"   # 40..1454
IP6_TCP_ADJUST_MSS_REMOVE_1712 = '<ipv6><tcp><adjust-mss nc:operation="remove"/></tcp></ipv6>'
IP6_REDIRECTS_1712        = "<ipv6><redirects>$flag</redirects></ipv6>"
IP6_REDIRECTS_REMOVE_1712 = '<ipv6><redirects nc:operation="remove"/></ipv6>'
IP6_POLICY_ROUTE_MAP_1712        = "<ipv6><policy><route-map>$route_map</route-map></policy></ipv6>"
IP6_POLICY_ROUTE_MAP_REMOVE_1712 = '<ipv6><policy><route-map nc:operation="remove"/></policy></ipv6>'
# $direction: in | out ; access-list must start with a letter
IP6_TRAFFIC_FILTER_1712 = (
    "<ipv6><traffic-filter><direction>$direction</direction>"
    "<access-list>$acl</access-list></traffic-filter></ipv6>"
)
IP6_TRAFFIC_FILTER_REMOVE_1712 = (
    '<ipv6><traffic-filter nc:operation="remove"><direction>$direction</direction></traffic-filter></ipv6>'
)
IP6_SOURCE_GUARD_1712        = "<ipv6><source-guard><attach-policy>$policy_name</attach-policy></source-guard></ipv6>"
IP6_SOURCE_GUARD_REMOVE_1712 = '<ipv6><source-guard nc:operation="remove"/></ipv6>'
IP6_DESTINATION_GUARD_1712        = "<ipv6><destination-guard><attach-policy>$policy_name</attach-policy></destination-guard></ipv6>"
IP6_DESTINATION_GUARD_REMOVE_1712 = '<ipv6><destination-guard nc:operation="remove"/></ipv6>'

# --- interface ipv6 nd (Cisco-IOS-XE-nd augments /native/interface/<TYPE>/ipv6/nd; children are in $ND) ---
IP6_ND_RAGUARD_ATTACH_1712        = '<ipv6><nd><raguard xmlns="$ND"><attach-policy>$policy_name</attach-policy></raguard></nd></ipv6>'
IP6_ND_RAGUARD_ATTACH_REMOVE_1712 = '<ipv6><nd><raguard xmlns="$ND" nc:operation="remove"/></nd></ipv6>'
IP6_ND_AUTOCONFIG_DEFAULT_ROUTE_1712 = '<ipv6><nd><autoconfig xmlns="$ND"><default-route/></autoconfig></nd></ipv6>'
IP6_ND_AUTOCONFIG_PREFIX_1712        = '<ipv6><nd><autoconfig xmlns="$ND"><prefix/></autoconfig></nd></ipv6>'
IP6_ND_AUTOCONFIG_REMOVE_1712        = '<ipv6><nd><autoconfig xmlns="$ND" nc:operation="remove"/></nd></ipv6>'
IP6_ND_MANAGED_CONFIG_FLAG_1712        = '<ipv6><nd><managed-config-flag xmlns="$ND"/></nd></ipv6>'
IP6_ND_MANAGED_CONFIG_FLAG_REMOVE_1712 = '<ipv6><nd><managed-config-flag xmlns="$ND" nc:operation="remove"/></nd></ipv6>'
IP6_ND_OTHER_CONFIG_FLAG_1712        = '<ipv6><nd><other-config-flag xmlns="$ND"/></nd></ipv6>'
IP6_ND_OTHER_CONFIG_FLAG_REMOVE_1712 = '<ipv6><nd><other-config-flag xmlns="$ND" nc:operation="remove"/></nd></ipv6>'
IP6_ND_ROUTER_PREFERENCE_1712        = '<ipv6><nd><router-preference xmlns="$ND">$pref</router-preference></nd></ipv6>'  # High|Medium|Low
IP6_ND_ROUTER_PREFERENCE_REMOVE_1712 = '<ipv6><nd><router-preference xmlns="$ND" nc:operation="remove"/></nd></ipv6>'
IP6_ND_PREFIX_1712 = (
    '<ipv6><nd><prefix xmlns="$ND"><ipv6-prefix-list><ipv6-prefix>$ipv6</ipv6-prefix>'
    '</ipv6-prefix-list></prefix></nd></ipv6>'
)
IP6_ND_PREFIX_NO_ADVERTISE_1712 = (
    '<ipv6><nd><prefix xmlns="$ND"><ipv6-prefix-list><ipv6-prefix>$ipv6</ipv6-prefix>'
    '<no-advertise/></ipv6-prefix-list></prefix></nd></ipv6>'
)
IP6_ND_PREFIX_REMOVE_1712 = (
    '<ipv6><nd><prefix xmlns="$ND"><ipv6-prefix-list nc:operation="remove">'
    '<ipv6-prefix>$ipv6</ipv6-prefix></ipv6-prefix-list></prefix></nd></ipv6>'
)
IP6_ND_RA_SUPPRESS_1712        = '<ipv6><nd><ra xmlns="$ND"><suppress/></ra></nd></ipv6>'
IP6_ND_RA_SUPPRESS_ALL_1712    = '<ipv6><nd><ra xmlns="$ND"><suppress><all/></suppress></ra></nd></ipv6>'
IP6_ND_RA_SUPPRESS_REMOVE_1712 = '<ipv6><nd><ra xmlns="$ND"><suppress nc:operation="remove"/></ra></nd></ipv6>'
IP6_ND_NS_INTERVAL_1712        = '<ipv6><nd><ns-interval xmlns="$ND">$ns_ms</ns-interval></nd></ipv6>'      # 1000..172800000
IP6_ND_NS_INTERVAL_REMOVE_1712 = '<ipv6><nd><ns-interval xmlns="$ND" nc:operation="remove"/></nd></ipv6>'
IP6_ND_REACHABLE_TIME_1712        = '<ipv6><nd><reachable-time xmlns="$ND">$reach_ms</reachable-time></nd></ipv6>'  # 0..3600000
IP6_ND_REACHABLE_TIME_REMOVE_1712 = '<ipv6><nd><reachable-time xmlns="$ND" nc:operation="remove"/></nd></ipv6>'


# ============================================================
# 6. ACCESS-SESSION
# ============================================================
AS_CLOSED_1712        = "<access-session><closed/></access-session>"
AS_CLOSED_REMOVE_1712 = '<access-session><closed nc:operation="remove"/></access-session>'
AS_PORT_CONTROL_1712 = "<access-session><port-control-config>$pc</port-control-config></access-session>"
AS_PORT_CONTROL_REMOVE_1712 = '<access-session><port-control-config nc:operation="remove"/></access-session>'
AS_CONTROL_DIRECTION_1712 = (
    "<access-session><control-direction-config>$dir</control-direction-config></access-session>"
)
AS_CONTROL_DIRECTION_REMOVE_1712 = (
    '<access-session><control-direction-config nc:operation="remove"/></access-session>'
)
AS_HOST_MODE_1712 = (
    "<access-session><host-mode-config><modes>$hm</modes></host-mode-config></access-session>"
)
AS_HOST_MODE_REMOVE_1712 = '<access-session><host-mode-config nc:operation="remove"/></access-session>'
AS_HOST_MODE_PEER_1712 = (
    "<access-session><host-mode-config><modes>multi-host</modes><peer/></host-mode-config></access-session>"
)
AS_HOST_MODE_PEER_REMOVE_1712 = (
    '<access-session><host-mode-config><peer nc:operation="remove"/></host-mode-config></access-session>'
)
AS_MONITOR_1712 = "<access-session><monitor>$flag</monitor></access-session>"
AS_MONITOR_REMOVE_1712 = '<access-session><monitor nc:operation="remove"/></access-session>'
AS_INHERIT_DISABLE_AUTOCONF_1712 = "<access-session><inherit><disable><autoconf/></disable></inherit></access-session>"
AS_INHERIT_DISABLE_TEMPLATE_STICKY_1712 = (
    "<access-session><inherit><disable><interface-template-sticky/></disable></inherit></access-session>"
)
AS_INHERIT_DISABLE_SERVICE_POLICY_1712 = (
    "<access-session><inherit><disable><service-policy/></disable></inherit></access-session>"
)
AS_INHERIT_DISABLE_REMOVE_1712 = '<access-session><inherit nc:operation="remove"/></access-session>'
AS_TEMPLATE_STICKY_1712 = (
    "<access-session><interface-template><sticky><timer>$secs</timer></sticky></interface-template></access-session>"
)
AS_TEMPLATE_STICKY_REMOVE_1712 = (
    '<access-session><interface-template><sticky nc:operation="remove"/></interface-template></access-session>'
)


# ============================================================
# 7. STORM-CONTROL   ($sc_type: broadcast|multicast|unicast|unknown-unicast)
# ============================================================
SC_ACTION_LEVEL_1712    = "<storm-control><action><level>$pct</level></action></storm-control>"
SC_ACTION_SHUTDOWN_1712 = "<storm-control><action><shutdown/></action></storm-control>"
SC_ACTION_TRAP_1712     = "<storm-control><action><trap/></action></storm-control>"
SC_ACTION_REMOVE_1712   = '<storm-control><action nc:operation="remove"/></storm-control>'
SC_THRESHOLD_PERCENT_1712 = (
    "<storm-control><$sc_type><level><threshold>"
    "<rising-threshold>$rise</rising-threshold>"
    "<falling-threshold>$fall</falling-threshold>"
    "</threshold></level></$sc_type></storm-control>"
)
SC_THRESHOLD_BPS_1712 = (
    "<storm-control><$sc_type><level><bps>"
    "<rising-threshold>$rise</rising-threshold>"
    "<falling-threshold>$fall</falling-threshold>"
    "</bps></level></$sc_type></storm-control>"
)
SC_THRESHOLD_PPS_1712 = (
    "<storm-control><$sc_type><level><pps>"
    "<rising-threshold>$rise</rising-threshold>"
    "<falling-threshold>$fall</falling-threshold>"
    "</pps></level></$sc_type></storm-control>"
)
SC_THRESHOLD_REMOVE_1712 = '<storm-control><$sc_type nc:operation="remove"/></storm-control>'
SC_BROADCAST_INCLUDE_MULTICAST_1712 = (
    "<storm-control><broadcast><include><multicast/></include></broadcast></storm-control>"
)
SC_BROADCAST_INCLUDE_MULTICAST_REMOVE_1712 = (
    '<storm-control><broadcast><include nc:operation="remove"/></broadcast></storm-control>'
)


# ============================================================
# 8. MACSEC  (native-namespace, if-feature macsec-common)
# ============================================================
MSEC_ENABLE_1712        = "<macsec-enable><macsec/></macsec-enable>"
MSEC_ENABLE_REMOVE_1712 = '<macsec-enable><macsec nc:operation="remove"/></macsec-enable>'
MSEC_REPLAY_PROTECTION_1712 = (
    "<macsec-option><macsec><replay-protection>"
    "<window-size>$window</window-size>"
    "</replay-protection></macsec></macsec-option>"
)
MSEC_REPLAY_PROTECTION_REMOVE_1712 = (
    '<macsec-option><macsec><replay-protection nc:operation="remove"/></macsec></macsec-option>'
)
MSEC_ACCESS_CONTROL_1712 = (       # must-secure | should-secure
    "<macsec-option><macsec><access-control>$macsec_ac</access-control></macsec></macsec-option>"
)
MSEC_ACCESS_CONTROL_REMOVE_1712 = (
    '<macsec-option><macsec><access-control nc:operation="remove"/></macsec></macsec-option>'
)
# SW-namespace macsec network-link (switch module, separate node from the native macsec-option)
MSEC_NETWORK_LINK_1712 = '<macsec-option xmlns="$SW"><macsec><network-link/></macsec></macsec-option>'
MSEC_NETWORK_LINK_REMOVE_1712 = (
    '<macsec-option xmlns="$SW"><macsec><network-link nc:operation="remove"/></macsec></macsec-option>'
)


# ============================================================
# 9. MISC — SUBSCRIBER   (choice: inactivity-timer | probe)
# ============================================================
MISC_SUBSCRIBER_INACTIVITY_1712 = (
    "<subscriber><aging><inactivity-timer><value>$secs</value>$probe_block"
    "</inactivity-timer></aging></subscriber>"
)
MISC_SUBSCRIBER_INACTIVITY_REMOVE_1712 = (
    '<subscriber><aging><inactivity-timer nc:operation="remove"/></aging></subscriber>'
)
MISC_SUBSCRIBER_PROBE_1712 = "<subscriber><aging><probe/></aging></subscriber>"
MISC_SUBSCRIBER_PROBE_REMOVE_1712 = '<subscriber><aging><probe nc:operation="remove"/></aging></subscriber>'


# ============================================================
# 10. PHYSICAL LAYER (type-specific, see applies_to)
# ============================================================
PHY_MEDIA_TYPE_1712        = "<media-type>$media</media-type>"     # auto-select|rj45|sfp
PHY_MEDIA_TYPE_REMOVE_1712 = '<media-type nc:operation="remove"/>'
PHY_PORT_TYPE_NNI_1712        = "<port-type>nni</port-type>"
PHY_PORT_TYPE_NNI_REMOVE_1712 = '<port-type nc:operation="remove"/>'
PHY_FEC_1712               = "<fec>$fec</fec>"                     # TwentyFiveGigE only: auto|cl108|cl74|cl91|off
PHY_FEC_REMOVE_1712        = '<fec nc:operation="remove"/>'


# ============================================================
# 11. PORT-CHANNEL
# ============================================================
PO_PC_SPEED_1712        = "<pc-speed>$speed</pc-speed>"            # 10|100|1000|nonegotiate|auto
PO_PC_SPEED_REMOVE_1712 = '<pc-speed nc:operation="remove"/>'
PO_LOAD_BALANCING_1712        = "<load-balancing>$lb</load-balancing>"   # vlan | flow
PO_LOAD_BALANCING_REMOVE_1712 = '<load-balancing nc:operation="remove"/>'
PO_PUNT_CONTROL_1712        = "<punt-control><enable><pps>$pps</pps></enable></punt-control>"
PO_PUNT_CONTROL_REMOVE_1712 = '<punt-control><enable nc:operation="remove"/></punt-control>'
PO_MIN_LINKS_1712             = "<port-channel><min-links>$min_links</min-links></port-channel>"   # 2..8
PO_MIN_LINKS_REMOVE_1712      = '<port-channel><min-links nc:operation="remove"/></port-channel>'
PO_STANDALONE_DISABLE_1712        = "<port-channel><standalone-disable/></port-channel>"
PO_STANDALONE_DISABLE_REMOVE_1712 = '<port-channel><standalone-disable nc:operation="remove"/></port-channel>'


# ============================================================
# 12. OTHER TYPE LEAVES
# ============================================================
TYPE_VLAN_AUTOSTATE_1712        = "<autostate>$flag</autostate>"
TYPE_VLAN_AUTOSTATE_REMOVE_1712 = '<autostate nc:operation="remove"/>'
TYPE_TUNNEL_QOS_PRE_CLASSIFY_1712 = "<qos><pre-classify/></qos>"
TYPE_TUNNEL_QOS_PRE_CLASSIFY_REMOVE_1712 = '<qos><pre-classify nc:operation="remove"/></qos>'
TYPE_VIRTUAL_TEMPLATE_TYPE_1712        = "<type>$vt_type</type>"      # ethernet|serial|tunnel|vpn
TYPE_VIRTUAL_TEMPLATE_TYPE_REMOVE_1712 = '<type nc:operation="remove"/>'


# ============================================================
# 13. NVE / VXLAN   (parent="nve")
# ============================================================
NVE_HOST_REACHABILITY_BGP_1712 = "<host-reachability><protocol><bgp/></protocol></host-reachability>"
NVE_HOST_REACHABILITY_BGP_REMOVE_1712 = '<host-reachability nc:operation="remove"/>'
NVE_GROUP_BASED_POLICY_1712        = "<group-based-policy/>"
NVE_GROUP_BASED_POLICY_REMOVE_1712 = '<group-based-policy nc:operation="remove"/>'
NVE_VXLAN_UDP_PORT_1712        = "<vxlan><udp><port>$udp_port</port></udp></vxlan>"     # 1024..65535
NVE_VXLAN_UDP_PORT_REMOVE_1712 = '<vxlan><udp nc:operation="remove"/></vxlan>'
NVE_VXLAN_ENCAP_1712           = "<vxlan><encapsulation><protocol>$encap_proto</protocol></encapsulation></vxlan>"  # ipv4|ipv6
NVE_VXLAN_ENCAP_REMOVE_1712    = '<vxlan><encapsulation nc:operation="remove"/></vxlan>'
# source-interface child names come from Cisco-IOS-XE-interface-common (not supplied): UNVERIFIED
NVE_SOURCE_INTERFACE_1712 = "<source-interface><$src_type>$src_name</$src_type></source-interface>"
NVE_SOURCE_INTERFACE_REMOVE_1712 = '<source-interface nc:operation="remove"/>'
NVE_MEMBER_VNI_VRF_1712 = (
    "<member-in-one-line><member><vni><vni-range>$vni</vni-range><vrf>$vrf</vrf>"
    "</vni></member></member-in-one-line>"
)
NVE_MEMBER_VNI_VRF_REMOVE_1712 = (
    '<member-in-one-line><member><vni nc:operation="remove"><vni-range>$vni</vni-range></vni>'
    '</member></member-in-one-line>'
)
NVE_MEMBER_VNI_MCAST_GROUP_1712 = (
    "<member><vni><vni-range>$vni</vni-range><mcast-group>"
    "<multicast-group-min>$mc_min</multicast-group-min>$mc_max_block"
    "</mcast-group></vni></member>"
)
NVE_MEMBER_VNI_MCAST_GROUP_REMOVE_1712 = (
    '<member><vni nc:operation="remove"><vni-range>$vni</vni-range></vni></member>'
)
# ingress replication: BGP-signalled (requires host-reachability protocol bgp) or static peers (requires NOT bgp)
NVE_MEMBER_VNI_IR_BGP_1712 = (
    "<member><vni><vni-range>$vni</vni-range><ir-cp-config><ingress-replication/></ir-cp-config></vni></member>"
)
NVE_MEMBER_VNI_IR_PEER_1712 = (
    "<member><vni><vni-range>$vni</vni-range><ir-peer-config><peer-addr>$peer</peer-addr></ir-peer-config></vni></member>"
)


# ============================================================
# 14. VLAN DATABASE + SVI  (Cisco-IOS-XE-vlan 2019-07-01, VERIFIED)
# ============================================================
# NATIVE-scoped bodies (use wrap_native()/build_config(); no interface scaffold).
# Everything augmented into /native/vlan lives in the $VLAN namespace.
# Constraints: names must satisfy "vtp version 3 or length <= 32"; group needs >= 1 member.
VLAN_CREATE_1712 = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN"><id>$vlan_id</id></vlan-list></vlan>'
VLAN_DELETE_1712 = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN" nc:operation="remove"><id>$vlan_id</id></vlan-list></vlan>'

VLAN_NAME_1712        = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN"><id>$vlan_id</id><name>$vlan_name</name></vlan-list></vlan>'
VLAN_NAME_REMOVE_1712 = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN"><id>$vlan_id</id><name nc:operation="remove"/></vlan-list></vlan>'
VLAN_STATE_1712        = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN"><id>$vlan_id</id><state>$vlan_state</state></vlan-list></vlan>'
VLAN_STATE_REMOVE_1712 = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN"><id>$vlan_id</id><state nc:operation="remove"/></vlan-list></vlan>'
VLAN_REMOTE_SPAN_1712        = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN"><id>$vlan_id</id><remote-span/></vlan-list></vlan>'
VLAN_REMOTE_SPAN_REMOVE_1712 = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN"><id>$vlan_id</id><remote-span nc:operation="remove"/></vlan-list></vlan>'
VLAN_LLDP_RUN_1712        = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN"><id>$vlan_id</id><lldp><run/></lldp></vlan-list></vlan>'
VLAN_LLDP_RUN_REMOVE_1712 = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN"><id>$vlan_id</id><lldp><run nc:operation="remove"/></lldp></vlan-list></vlan>'
# $uni_type: community | isolated
VLAN_UNI_1712        = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN"><id>$vlan_id</id><uni-vlan>$uni_type</uni-vlan></vlan-list></vlan>'
VLAN_UNI_REMOVE_1712 = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN"><id>$vlan_id</id><uni-vlan nc:operation="remove"/></vlan-list></vlan>'

# vlan group (vlan-lists is a leaf-list; group must keep >= 1 member)
VLAN_GROUP_1712 = (
    '<vlan xmlns="$N"><group xmlns="$VLAN"><name>$group_name</name><vlan-lists>$vlan_id</vlan-lists></group></vlan>'
)
VLAN_GROUP_REMOVE_1712 = (
    '<vlan xmlns="$N"><group xmlns="$VLAN" nc:operation="remove"><name>$group_name</name></group></vlan>'
)
VLAN_GROUP_MEMBER_REMOVE_1712 = (
    '<vlan xmlns="$N"><group xmlns="$VLAN"><name>$group_name</name>'
    '<vlan-lists nc:operation="remove">$vlan_id</vlan-lists></group></vlan>'
)

# vlan filter (apply a VLAN map to vlans)
VLAN_FILTER_1712 = (
    '<vlan xmlns="$N"><filter xmlns="$VLAN"><word>$map_name</word><vlan-lists>$vlan_id</vlan-lists></filter></vlan>'
)
VLAN_FILTER_REMOVE_1712 = (
    '<vlan xmlns="$N"><filter xmlns="$VLAN" nc:operation="remove"><word>$map_name</word></filter></vlan>'
)

# vlan access-map (key=name; one sequence value per name in this model); $vacl_action: drop | forward
VLAN_ACCESS_MAP_1712 = (
    '<vlan xmlns="$N"><access-map xmlns="$VLAN"><name>$map_name</name><value>$seq</value>'
    '<match><ip><address>$acl</address></ip></match><action>$vacl_action</action></access-map></vlan>'
)
VLAN_ACCESS_MAP_REMOVE_1712 = (
    '<vlan xmlns="$N"><access-map xmlns="$VLAN" nc:operation="remove"><name>$map_name</name></access-map></vlan>'
)

VLAN_DOT1Q_TAG_NATIVE_1712 = '<vlan xmlns="$N"><dot1q xmlns="$VLAN"><tag><native/></tag></dot1q></vlan>'
VLAN_DOT1Q_TAG_NATIVE_REMOVE_1712 = (
    '<vlan xmlns="$N"><dot1q xmlns="$VLAN"><tag><native nc:operation="remove"/></tag></dot1q></vlan>'
)
# $policy: ascending | descending
VLAN_INTERNAL_ALLOCATION_1712 = (
    '<vlan xmlns="$N"><internal xmlns="$VLAN"><allocation><policy>$policy</policy></allocation></internal></vlan>'
)
VLAN_INTERNAL_ALLOCATION_REMOVE_1712 = (
    '<vlan xmlns="$N"><internal xmlns="$VLAN"><allocation nc:operation="remove"/></internal></vlan>'
)
# presence container; $accounting_block e.g. "<input/><output/>"
VLAN_ACCOUNTING_1712 = '<vlan xmlns="$N"><accounting xmlns="$VLAN">$accounting_block</accounting></vlan>'
VLAN_ACCOUNTING_REMOVE_1712 = '<vlan xmlns="$N"><accounting xmlns="$VLAN" nc:operation="remove"/></vlan>'

# vlan configuration <id> (single vlan-id 1..4094)
VLAN_CONFIG_MEMBER_VNI_1712 = (
    '<vlan xmlns="$N"><configuration xmlns="$VLAN"><vlan-id>$vlan_id</vlan-id>'
    '<member><vni>$vni</vni></member></configuration></vlan>'
)
VLAN_CONFIG_MEMBER_EVPN_1712 = (
    '<vlan xmlns="$N"><configuration xmlns="$VLAN"><vlan-id>$vlan_id</vlan-id>'
    '<member><evpn-instance><evpn-instance>$evi</evpn-instance><vni>$vni</vni></evpn-instance></member>'
    '</configuration></vlan>'
)
VLAN_CONFIG_MEMBER_ACCESS_VFI_1712 = (
    '<vlan xmlns="$N"><configuration xmlns="$VLAN"><vlan-id>$vlan_id</vlan-id>'
    '<member><access-vfi>$vfi</access-vfi></member></configuration></vlan>'
)
VLAN_CONFIG_MEMBER_REMOVE_1712 = (
    '<vlan xmlns="$N"><configuration xmlns="$VLAN"><vlan-id>$vlan_id</vlan-id>'
    '<member nc:operation="remove"/></configuration></vlan>'
)
VLAN_CONFIG_DEVICE_TRACKING_1712 = (
    '<vlan xmlns="$N"><configuration xmlns="$VLAN"><vlan-id>$vlan_id</vlan-id>'
    '<device-tracking><attach-policy>$policy_name</attach-policy></device-tracking></configuration></vlan>'
)
VLAN_CONFIG_RAGUARD_ATTACH_1712 = (
    '<vlan xmlns="$N"><configuration xmlns="$VLAN"><vlan-id>$vlan_id</vlan-id>'
    '<ipv6><nd><raguard><attach-policy>$policy_name</attach-policy></raguard></nd></ipv6></configuration></vlan>'
)
VLAN_CONFIG_ND_SUPPRESS_1712 = (
    '<vlan xmlns="$N"><configuration xmlns="$VLAN"><vlan-id>$vlan_id</vlan-id>'
    '<ipv6><nd><suppress/></nd></ipv6></configuration></vlan>'
)
VLAN_CONFIG_DHCP_GUARD_1712 = (
    '<vlan xmlns="$N"><configuration xmlns="$VLAN"><vlan-id>$vlan_id</vlan-id>'
    '<ipv6><dhcp><guard><attach-policy>$policy_name</attach-policy></guard></dhcp></ipv6></configuration></vlan>'
)
VLAN_CONFIG_REMOVE_1712 = (
    '<vlan xmlns="$N"><configuration xmlns="$VLAN" nc:operation="remove"><vlan-id>$vlan_id</vlan-id></configuration></vlan>'
)

# SVI (interface Vlan, if-feature vlan / private-vlan): INTERFACE-scoped, parent="Vlan"
SVI_PRIVATE_VLAN_MAPPING_1712 = '<private-vlan xmlns="$VLAN"><mapping>$mapping</mapping></private-vlan>'
SVI_PRIVATE_VLAN_MAPPING_REMOVE_1712 = '<private-vlan xmlns="$VLAN"><mapping nc:operation="remove"/></private-vlan>'


# ============================================================
# 15. SWITCH-MODULE INTERFACE EXTRAS (Cisco-IOS-XE-switch, SW namespace, switch-capable types)
# ============================================================
MAC_ACCESS_GROUP_1712 = (
    '<mac xmlns="$SW"><access-group><direction>$direction</direction>'
    '<acl-name>$acl</acl-name></access-group></mac>'
)
MAC_ACCESS_GROUP_REMOVE_1712 = (
    '<mac xmlns="$SW"><access-group nc:operation="remove"><direction>$direction</direction></access-group></mac>'
)
AUTO_QOS_TRUST_COS_1712  = '<auto xmlns="$SW"><qos><trust><cos/></trust></qos></auto>'
AUTO_QOS_TRUST_DSCP_1712 = '<auto xmlns="$SW"><qos><trust><dscp/></trust></qos></auto>'
AUTO_QOS_VOIP_CISCO_PHONE_1712 = '<auto xmlns="$SW"><qos><voip><cisco-phone/></voip></qos></auto>'
AUTO_QOS_VOIP_TRUST_1712       = '<auto xmlns="$SW"><qos><voip><trust/></voip></qos></auto>'
AUTO_QOS_REMOVE_1712     = '<auto xmlns="$SW"><qos nc:operation="remove"/></auto>'
DUAL_ACTIVE_FAST_HELLO_1712        = '<dual-active xmlns="$SW"><fast-hello/></dual-active>'
DUAL_ACTIVE_FAST_HELLO_REMOVE_1712 = '<dual-active xmlns="$SW"><fast-hello nc:operation="remove"/></dual-active>'
SW_LOAD_BALANCING_FLOW_1712 = '<load-balancing xmlns="$SW"><flow/></load-balancing>'
SW_LOAD_BALANCING_VLAN_1712 = '<load-balancing xmlns="$SW"><vlan/></load-balancing>'
SW_LOAD_BALANCING_REMOVE_1712 = '<load-balancing xmlns="$SW" nc:operation="remove"/>'
# srr-queue bandwidth: share weights uint8 1..255, shape weights uint16
SRR_QUEUE_SHARE_1712 = (
    '<srr-queue xmlns="$SW"><bandwidth><share><weight1>$w1</weight1><weight2>$w2</weight2>'
    '<weight3>$w3</weight3><weight4>$w4</weight4></share></bandwidth></srr-queue>'
)
SRR_QUEUE_SHAPE_1712 = (
    '<srr-queue xmlns="$SW"><bandwidth><shape><weight1>$w1</weight1><weight2>$w2</weight2>'
    '<weight3>$w3</weight3><weight4>$w4</weight4></shape></bandwidth></srr-queue>'
)
SRR_QUEUE_REMOVE_1712 = '<srr-queue xmlns="$SW" nc:operation="remove"/>'


# ============================================================
# 16. GLOBAL (NATIVE-scoped) ND + ARP
# ============================================================
# --- ipv6 nd (Cisco-IOS-XE-nd augments /native/ipv6/nd; children in $ND) ---
GLOBAL_ND_RAGUARD_POLICY_1712 = (
    '<ipv6 xmlns="$N"><nd><raguard xmlns="$ND"><policy>'
    '<raguard-policy-name>$policy_name</raguard-policy-name></policy></raguard></nd></ipv6>'
)
GLOBAL_ND_RAGUARD_POLICY_REMOVE_1712 = (
    '<ipv6 xmlns="$N"><nd><raguard xmlns="$ND"><policy nc:operation="remove">'
    '<raguard-policy-name>$policy_name</raguard-policy-name></policy></raguard></nd></ipv6>'
)
# $role: host | monitor | router | switch
GLOBAL_ND_RAGUARD_POLICY_ROLE_1712 = (
    '<ipv6 xmlns="$N"><nd><raguard xmlns="$ND"><policy><raguard-policy-name>$policy_name</raguard-policy-name>'
    '<device-role><$role/></device-role></policy></raguard></nd></ipv6>'
)
GLOBAL_ND_RAGUARD_POLICY_HOP_LIMIT_1712 = (
    '<ipv6 xmlns="$N"><nd><raguard xmlns="$ND"><policy><raguard-policy-name>$policy_name</raguard-policy-name>'
    '<hop-limit><maximum>$hop_max</maximum><minimum>$hop_min</minimum></hop-limit></policy></raguard></nd></ipv6>'
)
GLOBAL_ND_RAGUARD_POLICY_TRUSTED_1712 = (
    '<ipv6 xmlns="$N"><nd><raguard xmlns="$ND"><policy><raguard-policy-name>$policy_name</raguard-policy-name>'
    '<trusted-port/></policy></raguard></nd></ipv6>'
)
# $body_block = any valid children of the inspection policy (device-role, limit, sec-level, tracking, ...)
GLOBAL_ND_INSPECTION_POLICY_1712 = (
    '<ipv6 xmlns="$N"><nd><inspection xmlns="$ND"><policy>'
    '<name-nd-inspection-policy>$policy_name</name-nd-inspection-policy>$body_block'
    '</policy></inspection></nd></ipv6>'
)
GLOBAL_ND_INSPECTION_POLICY_REMOVE_1712 = (
    '<ipv6 xmlns="$N"><nd><inspection xmlns="$ND"><policy nc:operation="remove">'
    '<name-nd-inspection-policy>$policy_name</name-nd-inspection-policy></policy></inspection></nd></ipv6>'
)
GLOBAL_ND_SUPPRESS_POLICY_1712 = (
    '<ipv6 xmlns="$N"><nd><suppress xmlns="$ND"><policy>'
    '<nd-suppress-policy-name>$policy_name</nd-suppress-policy-name></policy></suppress></nd></ipv6>'
)
GLOBAL_ND_SUPPRESS_POLICY_REMOVE_1712 = (
    '<ipv6 xmlns="$N"><nd><suppress xmlns="$ND"><policy nc:operation="remove">'
    '<nd-suppress-policy-name>$policy_name</nd-suppress-policy-name></policy></suppress></nd></ipv6>'
)
# $refresh_block: "<refresh/>" or ""
GLOBAL_ND_CACHE_EXPIRE_1712 = (
    '<ipv6 xmlns="$N"><nd><cache xmlns="$ND"><expire><time>$expire</time>$refresh_block</expire></cache></nd></ipv6>'
)
GLOBAL_ND_CACHE_EXPIRE_REMOVE_1712 = (
    '<ipv6 xmlns="$N"><nd><cache xmlns="$ND"><expire nc:operation="remove"/></cache></nd></ipv6>'
)
GLOBAL_ND_DEFAULT_ROUTE_LIMIT_1712 = (       # 0..5
    '<ipv6 xmlns="$N"><nd><default-route xmlns="$ND"><limit>$limit</limit></default-route></nd></ipv6>'
)
GLOBAL_ND_DEFAULT_ROUTE_VRF_LIMIT_1712 = (
    '<ipv6 xmlns="$N"><nd><default-route xmlns="$ND"><vrf><word>$vrf</word><limit>$limit</limit></vrf>'
    '</default-route></nd></ipv6>'
)

# --- static ARP (Cisco-IOS-XE-arp augments /native with container arp in $ARP) ---
# $arp_type: ARPA | SAP | SMDS | SNAP | SRP-A | SRP-B
GLOBAL_ARP_ENTRY_1712 = (
    '<arp xmlns="$ARP"><arp-entry><ip>$ip</ip><hardware-address>$hwaddr</hardware-address>'
    '<arp-type>$arp_type</arp-type></arp-entry></arp>'
)
GLOBAL_ARP_ENTRY_ALIAS_1712 = (
    '<arp xmlns="$ARP"><arp-entry><ip>$ip</ip><hardware-address>$hwaddr</hardware-address>'
    '<arp-type>$arp_type</arp-type><alias/></arp-entry></arp>'
)
GLOBAL_ARP_ENTRY_REMOVE_1712 = (
    '<arp xmlns="$ARP"><arp-entry nc:operation="remove"><ip>$ip</ip></arp-entry></arp>'
)
GLOBAL_ARP_VRF_ENTRY_1712 = (
    '<arp xmlns="$ARP"><vrf><vrf-name>$vrf</vrf-name><arp-entry><ip>$ip</ip>'
    '<hardware-address>$hwaddr</hardware-address><arp-type>$arp_type</arp-type></arp-entry></vrf></arp>'
)
GLOBAL_ARP_VRF_ENTRY_REMOVE_1712 = (
    '<arp xmlns="$ARP"><vrf><vrf-name>$vrf</vrf-name>'
    '<arp-entry nc:operation="remove"><ip>$ip</ip></arp-entry></vrf></arp>'
)
GLOBAL_ARP_VRF_REMOVE_1712 = (
    '<arp xmlns="$ARP"><vrf nc:operation="remove"><vrf-name>$vrf</vrf-name></vrf></arp>'
)
# --- ARP access-list (switch module augments /native/arp with list access-list in $SW) ---
# $acl_action: permit | deny
GLOBAL_ARP_ACL_CREATE_1712 = (
    '<arp xmlns="$ARP"><access-list xmlns="$SW"><name>$acl</name></access-list></arp>'
)
GLOBAL_ARP_ACL_REMOVE_1712 = (
    '<arp xmlns="$ARP"><access-list xmlns="$SW" nc:operation="remove"><name>$acl</name></access-list></arp>'
)
GLOBAL_ARP_ACL_ANY_1712 = (
    '<arp xmlns="$ARP"><access-list xmlns="$SW"><name>$acl</name>'
    '<$acl_action><ip><any><mac><any/></mac></any></ip></$acl_action></access-list></arp>'
)
GLOBAL_ARP_ACL_HOST_1712 = (
    '<arp xmlns="$ARP"><access-list xmlns="$SW"><name>$acl</name>'
    '<$acl_action><ip><host><ip-address><ip-address>$ip</ip-address>'
    '<mac><host><sender-mac-address><mac-address>$hwaddr</mac-address></sender-mac-address></host></mac>'
    '</ip-address></host></ip></$acl_action></access-list></arp>'
)


# ================================================================
# 1712 FAMILIES WITH NO 17.12 TEMPLATE (verified ABSENT in supplied YANG)
# ================================================================
NOT_PRESENT = {
    "NEGOTIATION_FULL": ("ABSENT", "17.12 negotiation has only <auto>; no speed/duplex leaves -> use NEGOTIATION"),
    "GEN_MDIX_FULL": ("ABSENT", "17.12 mdix has only <auto>; no <mode> leaf -> use GEN_MDIX"),
    "L2_PORTSEC_VIOLATION_SHUTDOWN_VLAN": ("ABSENT", "violation is a plain enum leaf (protect|restrict|shutdown); no shutdown/vlan"),
    "L2_PORTSEC_MAC_STICKY": ("ABSENT", "no hw-address-sticky; use L2_PORTSEC_STICKY (global sticky) + L2_PORTSEC_MAC_ACCESS"),
    "IP6_ND_DAD_ATTEMPTS": ("ABSENT", "Cisco-IOS-XE-nd 17.12 has no dad node"),
    "IP6_ND_DAD_ATTEMPTS_REMOVE": ("ABSENT", "Cisco-IOS-XE-nd 17.12 has no dad node"),
    "IP6_ND_NUD_IGP": ("ABSENT", "Cisco-IOS-XE-nd 17.12 has no nud node"),
    "IP6_VERIFY_UNICAST_REVERSE_PATH": ("ABSENT", "no verify node under interface ipv6 in 17.12 interfaces module"),
    "IP6_VERIFY_UNICAST_REVERSE_PATH_REMOVE": ("ABSENT", "no verify node under interface ipv6 in 17.12 interfaces module"),
    "PO_LOAD_BALANCE_HASH_ALGO": ("ABSENT", "no hash-algo leaf; use PO_LOAD_BALANCING (vlan|flow)"),
    "PO_LOAD_BALANCE_HASH_ALGO_REMOVE": ("ABSENT", "no hash-algo leaf; use PO_LOAD_BALANCING_REMOVE"),
    "VLAN_SHUTDOWN": ("ABSENT", "vlan-list in the 17.12 vlan module has no shutdown leaf"),
    "VLAN_SHUTDOWN_REMOVE": ("ABSENT", "vlan-list in the 17.12 vlan module has no shutdown leaf"),
    "ARP_INSPECT_RATE": 'not modelled on train 1712',
    "ARP_INSPECT_RATE_REMOVE": 'not modelled on train 1712',
    "ARP_INSPECT_TRUST": 'not modelled on train 1712',
    "ARP_INSPECT_TRUST_REMOVE": 'not modelled on train 1712',
    "ARP_SNAP": 'not modelled on train 1712',
    "ARP_SNAP_REMOVE": 'not modelled on train 1712',
    "CLEAR_DF": 'not modelled on train 1712',
    "CLEAR_DF_REMOVE": 'not modelled on train 1712',
    "DAMPENING": 'not modelled on train 1712',
    "DIRECTED_BROADCAST": 'not modelled on train 1712',
    "DIRECTED_BROADCAST_REMOVE": 'not modelled on train 1712',
    "FEC": 'not modelled on train 1712',
    "FEC_REMOVE": 'not modelled on train 1712',
    "HELPER_ADDRESS": 'not modelled on train 1712',
    "HELPER_ADDRESS_REMOVE": 'not modelled on train 1712',
    "IPV4_ACCESS_GROUP": 'not modelled on train 1712',
    "IPV4_ACCESS_GROUP_REMOVE": 'not modelled on train 1712',
    "IPV4_ADDRESS": 'not modelled on train 1712',
    "IPV4_ADDRESS_REMOVE": 'not modelled on train 1712',
    "IPV4_DHCP": 'not modelled on train 1712',
    "IPV4_DHCP_REMOVE": 'not modelled on train 1712',
    "IPV4_UNNUMBERED": 'not modelled on train 1712',
    "IPV4_UNNUMBERED_REMOVE": 'not modelled on train 1712',
    "IPV4_VRF_RECEIVE": 'not modelled on train 1712',
    "IPV4_VRF_RECEIVE_REMOVE": 'not modelled on train 1712',
    "IPV4_VRF_SITEMAP": 'not modelled on train 1712',
    "IPV4_VRF_SITEMAP_REMOVE": 'not modelled on train 1712',
    "IPV6_ADDRESS": 'not modelled on train 1712',
    "IPV6_ADDRESS_REMOVE": 'not modelled on train 1712',
    "IPV6_AUTOCONFIG": 'not modelled on train 1712',
    "IPV6_AUTOCONFIG_REMOVE": 'not modelled on train 1712',
    "IPV6_DHCP": 'not modelled on train 1712',
    "IPV6_DHCP_REMOVE": 'not modelled on train 1712',
    "IPV6_ENABLE": 'not modelled on train 1712',
    "IPV6_ENABLE_REMOVE": 'not modelled on train 1712',
    "IPV6_MTU": 'not modelled on train 1712',
    "IPV6_MTU_REMOVE": 'not modelled on train 1712',
    "IPV6_ND_DAD_ATTEMPTS": 'not modelled on train 1712',
    "IPV6_ND_DAD_ATTEMPTS_REMOVE": 'not modelled on train 1712',
    "IPV6_ND_NUD_IGP": 'not modelled on train 1712',
    "IPV6_ND_NUD_IGP_REMOVE": 'not modelled on train 1712',
    "IPV6_SOURCE_GUARD": 'not modelled on train 1712',
    "IPV6_SOURCE_GUARD_REMOVE": 'not modelled on train 1712',
    "IPV6_TCP_ADJUST_MSS": 'not modelled on train 1712',
    "IPV6_TCP_ADJUST_MSS_REMOVE": 'not modelled on train 1712',
    "IPV6_TRAFFIC_FILTER": 'not modelled on train 1712',
    "IPV6_TRAFFIC_FILTER_REMOVE": 'not modelled on train 1712',
    "IPV6_UNNUMBERED": 'not modelled on train 1712',
    "IPV6_UNNUMBERED_REMOVE": 'not modelled on train 1712',
    "IPV6_VERIFY_REVERSE_PATH": 'not modelled on train 1712',
    "IPV6_VERIFY_REVERSE_PATH_REMOVE": 'not modelled on train 1712',
    "IP_MTU": 'not modelled on train 1712',
    "IP_MTU_REMOVE": 'not modelled on train 1712',
    "KEEPALIVE": 'not modelled on train 1712',
    "L2PT_THRESHOLD": 'not modelled on train 1712',
    "L2PT_THRESHOLD_REMOVE": 'not modelled on train 1712',
    "L2_PORT_SECURITY_AGING": 'not modelled on train 1712',
    "L2_PORT_SECURITY_AGING_REMOVE": 'not modelled on train 1712',
    "L2_PORT_SECURITY_ENABLE": 'not modelled on train 1712',
    "L2_PORT_SECURITY_ENABLE_REMOVE": 'not modelled on train 1712',
    "L2_PORT_SECURITY_MAC": 'not modelled on train 1712',
    "L2_PORT_SECURITY_MAC_REMOVE": 'not modelled on train 1712',
    "L2_PORT_SECURITY_MAX": 'not modelled on train 1712',
    "L2_PORT_SECURITY_MAX_REMOVE": 'not modelled on train 1712',
    "L2_PORT_SECURITY_STICKY": 'not modelled on train 1712',
    "L2_PORT_SECURITY_STICKY_REMOVE": 'not modelled on train 1712',
    "L2_PORT_SECURITY_VIOLATION": 'not modelled on train 1712',
    "L2_PORT_SECURITY_VIOLATION_REMOVE": 'not modelled on train 1712',
    "L2_TRUNK_ALLOWED": 'not modelled on train 1712',
    "L2_TRUNK_NATIVE_VLAN": 'not modelled on train 1712',
    "L2_TRUNK_NATIVE_VLAN_REMOVE": 'not modelled on train 1712',
    "L2_TRUNK_PRUNING": 'not modelled on train 1712',
    "L2_VOICE_VLAN": 'not modelled on train 1712',
    "LOCAL_PROXY_ARP": 'not modelled on train 1712',
    "LOCAL_PROXY_ARP_REMOVE": 'not modelled on train 1712',
    "LOGGING_EVENT": 'not modelled on train 1712',
    "LOGGING_EVENT_REMOVE": 'not modelled on train 1712',
    "LOGGING_LINK_STATUS": 'not modelled on train 1712',
    "LOGGING_LINK_STATUS_REMOVE": 'not modelled on train 1712',
    "LOGGING_SPANNING_TREE": 'not modelled on train 1712',
    "LOGGING_SPANNING_TREE_REMOVE": 'not modelled on train 1712',
    "LOGGING_SUBIF": 'not modelled on train 1712',
    "LOGGING_SUBIF_REMOVE": 'not modelled on train 1712',
    "MACSEC_ENABLE": 'not modelled on train 1712',
    "MACSEC_ENABLE_REMOVE": 'not modelled on train 1712',
    "MACSEC_REPLAY_PROTECTION": 'not modelled on train 1712',
    "MACSEC_REPLAY_PROTECTION_REMOVE": 'not modelled on train 1712',
    "MDIX": 'not modelled on train 1712',
    "MDIX_REMOVE": 'not modelled on train 1712',
    "MEDIA_TYPE": 'not modelled on train 1712',
    "MEDIA_TYPE_REMOVE": 'not modelled on train 1712',
    "POLICY_ROUTE_MAP": 'not modelled on train 1712',
    "POLICY_ROUTE_MAP_REMOVE": 'not modelled on train 1712',
    "PO_LOAD_BALANCE": 'not modelled on train 1712',
    "PO_LOAD_BALANCE_REMOVE": 'not modelled on train 1712',
    "PQ_OUT": 'not modelled on train 1712',
    "PQ_OUT_REMOVE": 'not modelled on train 1712',
    "PROXY_ARP": 'not modelled on train 1712',
    "PROXY_ARP_REMOVE": 'not modelled on train 1712',
    "REDIRECTS": 'not modelled on train 1712',
    "REDIRECTS_REMOVE": 'not modelled on train 1712',
    "STORM_CONTROL_ACTION": 'not modelled on train 1712',
    "STORM_CONTROL_ACTION_REMOVE": 'not modelled on train 1712',
    "STORM_CONTROL_BCAST_INCLUDE_MCAST": 'not modelled on train 1712',
    "STORM_CONTROL_BCAST_INCLUDE_MCAST_REMOVE": 'not modelled on train 1712',
    "STORM_CONTROL_THRESHOLD": 'not modelled on train 1712',
    "STORM_CONTROL_THRESHOLD_REMOVE": 'not modelled on train 1712',
    "SUBSCRIBER_INACTIVITY": 'not modelled on train 1712',
    "SUBSCRIBER_INACTIVITY_REMOVE": 'not modelled on train 1712',
    "SUBSCRIBER_PROBE": 'not modelled on train 1712',
    "SUBSCRIBER_PROBE_REMOVE": 'not modelled on train 1712',
    "TCP_ADJUST_MSS": 'not modelled on train 1712',
    "TCP_ADJUST_MSS_REMOVE": 'not modelled on train 1712',
    "TUNNEL_QOS_PRE_CLASSIFY": 'not modelled on train 1712',
    "TUNNEL_QOS_PRE_CLASSIFY_REMOVE": 'not modelled on train 1712',
    "URPF": 'not modelled on train 1712',
    "URPF_REMOVE": 'not modelled on train 1712',
    "VLAN_AUTOSTATE": 'not modelled on train 1712',
    "VLAN_AUTOSTATE_REMOVE": 'not modelled on train 1712',
    "VLAN_CREATE_REMOVE": 'not modelled on train 1712',
    "VLAN_DELETE_REMOVE": 'not modelled on train 1712',
    "VRF_FORWARDING": 'not modelled on train 1712',
    "VRF_FORWARDING_REMOVE": 'not modelled on train 1712',
}

# Families whose shape differs from (or are new vs) interface_attrs_1715
DIFFS_VS_1715 = {
    "L2PT_DROP_THRESHOLD":              "1715: <$proto><packet-rate>..; 17.12: <$proto>$pps</$proto> (uint16 leaf)",
    "L2PT_DROP_THRESHOLD_P2P":          "1715: <$p2p_proto><packet-rate>..; 17.12: <$p2p_proto>$pps</$p2p_proto>",
    "L2PT_SHUTDOWN_THRESHOLD":          "1715: <$proto><packet-rate>..; 17.12: <$proto>$pps</$proto>",
    "L2PT_SHUTDOWN_THRESHOLD_P2P":      "1715: <$p2p_proto><packet-rate>..; 17.12: <$p2p_proto>$pps</$p2p_proto>",
    "L2_PORTSEC_ENABLE":    "1715: port-security-conf leaf; 17.12: <port-security xmlns=SW/> presence container",
    "L2_PORTSEC_MAX":       "1715: maximum-address-config/maximum/maximum; 17.12: maximum/max-addresses",
    "L2_PORTSEC_MAX_VLAN":  "1715: maximum-address-config/maximum/{maximum,vlan}; 17.12: maximum/{max-addresses,vlan}",
    "L2_PORTSEC_VIOLATION": "1715: <violation><$violation/></violation>; 17.12: <violation>$violation</violation>",
    "L2_PORTSEC_STICKY":    "1715: mac-address-sticky-on/mac-address/sticky; 17.12: mac-address/sticky",
    "L2_PORTSEC_AGING":     "1715: aging/{time,type} under port-security-config; 17.12: aging/{static,time,type}",
    "L2_PORTSEC_MAC_ACCESS": "1715: list hw-address-access; 17.12: mac-address/hw-address (single leaf)",
    "KEEPALIVE_TIMERS":     "1715: keepalive-config/{keepalive,period,retries}; 17.12: keepalive-settings/keepalive/{period,retries}",
    "KEEPALIVE_DISABLE":    "1715: keepalive-config/keepalive=false; 17.12: <keepalive>false</keepalive>",
    "IP4_URPF":             "1715 had $acl_block; 17.12 has no ACL leaf (param removed)",
    "IP4_URPF_REMOVE":      "1715 removed whole verify; 17.12 removes verify/unicast only (keeps source-vlan dhcp-snooping)",
    "IP4_ARP_INSPECT_RATE": "1715 had $burst_block; 17.12 has no burst leaf (param removed)",
    "IP4_SECONDARY_REMOVE": "17.12: list entry removal needs only the key (address); mask dropped",
    "IP6_TRAFFIC_FILTER_REMOVE": "17.12: list entry removal needs only the key (direction)",
    "IP6_SOURCE_GUARD":     "1715 took $policy_block; 17.12 takes $policy_name",
    "MSEC_ENABLE":          "same native-namespace shape; verified in 17.12 (macsec-common feature)",
    "L2_TRUNK_PRUNING_REPLACE": "replace applied on <vlan> container (whole choice/leaf-list), not on one leaf-list entry",
    "SVI_PRIVATE_VLAN_MAPPING": "interface-scoped (parent='Vlan'); 1715 misclassified it as NATIVE_SCOPED",
}
# every L2 switchport family changes wrapper: <switchport-config><switchport> (1715) -> <switchport> (17.12)
for _n in ("L2_DTP_DISABLE_TRUE", "L2_DTP_DISABLE_FALSE", "L2_VOICE_FULL", "L2_VOICE_FULL_REMOVE",
           "L2_VOICE_VLAN_ID", "L2_VOICE_VLAN_DOT1P", "L2_VOICE_VLAN_NONE", "L2_VOICE_VLAN_UNTAGGED",
           "L2_VOICE_VLAN_REMOVE", "L2_VOICE_DETECT", "L2_VOICE_DETECT_REMOVE", "L2_ACCESS_VLAN",
           "L2_ACCESS_VLAN_REMOVE", "L2_TRUNK_PRUNING_ADD", "L2_TRUNK_PRUNING_REMOVE",
           "L2_TRUNK_PRUNING_NONE", "L2_TRUNK_PRUNING_REMOVE_ALL", "PVLAN_HOST_ASSOC",
           "PVLAN_HOST_ASSOC_REMOVE", "PVLAN_PROMISCUOUS_MAP", "PVLAN_PROMISCUOUS_MAP_REMOVE",
           "L2_PORTSEC_ENABLE_REMOVE", "L2_PORTSEC_MAX_REMOVE", "L2_PORTSEC_VIOLATION_REMOVE",
           "L2_PORTSEC_STICKY_REMOVE", "L2_PORTSEC_AGING_REMOVE", "L2_PORTSEC_MAC_ACCESS_REMOVE",
           "L2_PROTECTED", "L2_PROTECTED_REMOVE", "L2_HOST", "L2_HOST_REMOVE",
           "L2_BLOCK_MULTICAST", "L2_BLOCK_MULTICAST_REMOVE", "L2_BLOCK_UNICAST",
           "L2_BLOCK_UNICAST_REMOVE", "L2_VEPA", "L2_VEPA_REMOVE"):
    DIFFS_VS_1715.setdefault(_n, "wrapper: 1715 <switchport-config><switchport>; 17.12 supplied switch module -> <switchport>")


# ================================================================
# TEMPLATE REGISTRY  (base label -> {train: template})
# ================================================================
# Built by scanning this module for NAME_1712 string constants, so the registry cannot drift
# from the definitions (the 1715 file maintained this table by hand).
_TRAINS = ("1712",)


def _t(**kw):
    """Expand a per-train dict to every train slot (None for missing)."""
    return {v: kw.get(v) for v in _TRAINS}


TEMPLATES = {}
for _k, _v in list(globals().items()):
    if _k.isupper() and _k.endswith("_1712") and isinstance(_v, str):
        TEMPLATES[_k[:-5]] = _t(**{"1712": _v})

# Register NOT_PRESENT families with a None slot so resolve() reports the reason
# rather than "unknown family". Collision with an explicit entry aborts the import.
for _name in NOT_PRESENT:
    if _name in TEMPLATES:
        raise ValueError(f"{_name} is both defined in TEMPLATES and listed in NOT_PRESENT")
    TEMPLATES[_name] = _t()

for _name in DIFFS_VS_1715:
    if _name not in TEMPLATES:
        raise ValueError(f"DIFFS_VS_1715 names unknown family {_name}")


def resolve(base, train="1712"):
    """Return the template for base/train. Raises with status + reason when unavailable."""
    if base not in TEMPLATES:
        raise KeyError(f"{base!r} not in 17.12 catalogue ({len(TEMPLATES)} families)")
    tpl = TEMPLATES[base].get(train)
    if tpl is None:
        status, why = NOT_PRESENT.get(base, ("ABSENT", "no template"))
        raise KeyError(f"{base!r} not available on train {train!r} [{status}]: {why}")
    return tpl


def families():
    for name in sorted(TEMPLATES):
        yield name


def supported_on(train="1712"):
    for name, slots in TEMPLATES.items():
        if slots.get(train) is not None:
            yield name


def not_present(status=None):
    """Yield (family, status, reason); optionally filter by EXTERNAL / ABSENT.
    Defensive against non-tuple entries in NOT_PRESENT (treats bare strings as ABSENT)."""
    for name in sorted(NOT_PRESENT):
        entry = NOT_PRESENT[name]
        if isinstance(entry, tuple) and len(entry) == 2:
            st, why = entry
        else:
            st, why = "ABSENT", str(entry)
        if status is None or st == status:
            yield name, st, why


def on_off_pairs(train="1712"):
    for base in TEMPLATES:
        if base.endswith("_REMOVE"):
            continue
        twin = base + "_REMOVE"
        if twin in TEMPLATES and TEMPLATES[twin].get(train) is not None \
                and TEMPLATES[base].get(train) is not None:
            yield (base, twin)


def flag_symmetric(train="1712"):
    for base, slots in TEMPLATES.items():
        tpl = slots.get(train)
        if tpl and "$flag" in tpl:
            yield base


# ================================================================
# STARTUP PLACEHOLDER VALIDATION
# ================================================================
_ALLOWED = {
    # general / namespaces
    "desc", "export", "mac", "mtu", "delay", "seconds", "percent", "flag", "svc", "device",
    "N", "NC", "SW", "ST", "VLAN", "ND", "ARP",
    # L2 switching
    "dyn", "voice_vlan", "access_vlan", "vlan_name", "encap", "vlans", "native_vlan", "wmode", "cos",
    "primary_vlan", "secondary_vlan", "secondary_vlans", "pvlan_type",
    "max", "vlan_kind", "violation", "minutes", "aging_type", "hwaddr", "vlan_id",
    "proto", "p2p_proto", "pps", "core_block", "p2p_block", "proto_block",
    # arp / link tuning
    "secs", "count", "log_secs", "qid", "tid", "cos_values_block", "direction", "qlen", "rx", "tx",
    "kbps", "half_life", "reuse", "suppress", "max_suppress", "srlg_values_block",
    "domain", "sp_path", "path_id", "period", "retries",
    "event", "events_block", "ignore_bulk_block",
    # ipv4
    "ip", "mask", "src_if", "acl", "common_acl", "vrf", "vrf_down", "route_map", "helper",
    "via", "allow_block", "ip_mtu", "mss", "client_id_block", "hostname_block",
    # ipv6 + nd
    "ipv6", "ll", "pfx_name", "ip6_mtu", "policy_name", "pref", "ns_ms", "reach_ms",
    # access-session / storm / macsec
    "pc", "dir", "hm", "pct", "sc_type", "rise", "fall", "window", "macsec_ac", "probe_block",
    # phy / po / type / nve
    "media", "fec", "speed", "lb", "min_links", "vt_type",
    "src_type", "src_name", "vni", "mc_min", "mc_max_block", "udp_port", "encap_proto", "peer",
    # vlan db
    "vlan_state", "uni_type", "group_name", "map_name", "policy", "accounting_block", "mapping",
    "seq", "vacl_action", "evi", "vfi",
    # switch extras
    "w1", "w2", "w3", "w4",
    # global nd / arp
    "role", "hop_max", "hop_min", "limit", "expire", "refresh_block", "body_block",
    "arp_type", "acl_action",
}

_PLACEHOLDER_RE = re.compile(r"\$([A-Za-z_][A-Za-z0-9_]*)")


def _validate_all():
    errors = []
    for family, slots in TEMPLATES.items():
        for train, tpl in slots.items():
            if tpl is None:
                continue
            for ph in _PLACEHOLDER_RE.findall(tpl):
                if ph not in _ALLOWED:
                    errors.append(f"{family}[{train}] unknown placeholder ${ph}")
    if errors:
        raise ValueError("interface_attrs_1712: placeholder validation failed:\n  " + "\n  ".join(errors))


_validate_all()


# ================================================================
# RUNTIME HELPERS
# ================================================================
NS = {
    "N":    "http://cisco.com/ns/yang/Cisco-IOS-XE-native",
    "NC":   "urn:ietf:params:xml:ns:netconf:base:1.0",
    "SW":   "http://cisco.com/ns/yang/Cisco-IOS-XE-switch",
    "ST":   "http://cisco.com/ns/yang/Cisco-IOS-XE-spanning-tree",
    "VLAN": "http://cisco.com/ns/yang/Cisco-IOS-XE-vlan",
    "ND":   "http://cisco.com/ns/yang/Cisco-IOS-XE-nd",
    "ARP":  "http://cisco.com/ns/yang/Cisco-IOS-XE-arp",
}

# list names under /native/interface -- ALL VERIFIED from interfaces submodule config-interface-grouping
_TYPES_TOP = (
    "AppNav-Compress", "AppNav-UnCompress", "ATM", "ATM-ACR", "BDI", "CEM", "CEM-ACR",
    "Embedded-Service-Engine", "Ethernet", "FastEthernet", "ucse", "Ethernet-Internal",
    "Service-Engine", "GigabitEthernet", "TwoGigabitEthernet", "FiveGigabitEthernet",
    "AppGigabitEthernet", "TenGigabitEthernet", "TwentyFiveGigE", "FortyGigabitEthernet",
    "FiftyGigabitEthernet", "HundredGigE", "TwoHundredGigE", "FourHundredGigE", "Loopback",
    "LORAWAN", "WPAN", "Virtual-WPAN", "L2LISP", "LISP", "nve", "overlay", "Port-channel",
    "PRP-channel", "pseudowire", "SM", "Cellular", "Dialer", "Vlan", "GMPLS", "Group-Async",
    "Multilink", "Serial", "Async", "Tunnel", "vmi", "Virtual-Template", "Virtual-PPP",
    "VirtualPortGroup", "vasileft", "vasiright", "Vif", "Wlan-GigabitEthernet", "BD-VIF",
    "MFR", "Bundle",
)
# <X-subinterface><X><name> nesting
_TYPES_SUBIF = (
    "ATM-subinterface/ATM", "ATM-ACRsubinterface/ATM-ACR", "L2LISP-subinterface/L2LISP",
    "LISP-subinterface/LISP", "Port-channel-subinterface/Port-channel",
    "Serial-subinterface/Serial", "MFR-subinterface/MFR",
)
OBSOLETE_INTERFACE_TYPES = frozenset({"TwentyFiveGigabitEthernet"})
INTERFACE_PATHS = frozenset(_TYPES_TOP + _TYPES_SUBIF)
KNOWN_INTERFACE_TYPES = frozenset(p.split("/")[0] for p in INTERFACE_PATHS)

# lists that do NOT use interface-common-grouping (no description/shutdown/ip/... children)
_NO_COMMON = frozenset({"ATM-ACR", "ATM-ACRsubinterface/ATM-ACR", "CEM", "CEM-ACR", "overlay", "pseudowire"})
COMMON_TYPES = INTERFACE_PATHS - _NO_COMMON

# per-feature applicability, derived from the augment targets / grouping uses in the supplied YANG
SWITCHPORT_TYPES = frozenset({      # switch module: /native/interface/<T>/switchport augment
    "FastEthernet", "GigabitEthernet", "TwoGigabitEthernet", "FiveGigabitEthernet",
    "AppGigabitEthernet", "TenGigabitEthernet", "TwentyFiveGigE", "FortyGigabitEthernet",
    "HundredGigE", "Port-channel", "Port-channel-subinterface/Port-channel",
    "ucse", "Ethernet-Internal", "Wlan-GigabitEthernet",     # last three: augment marked deprecated
})
SWITCH_IF_TYPES = frozenset({       # switch module: config-interface-switch-grouping augment
    "FastEthernet", "GigabitEthernet", "TwoGigabitEthernet", "FiveGigabitEthernet",
    "AppGigabitEthernet", "TenGigabitEthernet", "TwentyFiveGigE", "FortyGigabitEthernet",
    "HundredGigE", "Port-channel", "Port-channel-subinterface/Port-channel",
})
ND_IF_TYPES = frozenset({           # nd module: .../<T>/ipv6/nd augment
    "FastEthernet", "GigabitEthernet", "TenGigabitEthernet", "FiveGigabitEthernet",
    "AppGigabitEthernet", "TwentyFiveGigE", "TwoGigabitEthernet", "FortyGigabitEthernet",
    "HundredGigE", "Port-channel", "Loopback", "Tunnel", "vasileft", "vasiright", "Vlan",
})
MACSEC_TYPES = frozenset({          # interface-macsec-grouping users
    "FastEthernet", "GigabitEthernet", "TwoGigabitEthernet", "FiveGigabitEthernet",
    "AppGigabitEthernet", "TenGigabitEthernet", "TwentyFiveGigE", "FortyGigabitEthernet",
    "FiftyGigabitEthernet", "HundredGigE", "TwoHundredGigE", "FourHundredGigE",
    "Port-channel", "Port-channel-subinterface/Port-channel",
})
MEDIA_TYPES = frozenset({           # leaf media-type / port-type
    "GigabitEthernet", "TwoGigabitEthernet", "FiveGigabitEthernet", "AppGigabitEthernet",
    "TenGigabitEthernet", "TwentyFiveGigE", "FortyGigabitEthernet", "FiftyGigabitEthernet",
})
WRAPPER_TYPES = frozenset({"GigabitEthernet", "AppGigabitEthernet", "ucse", "Ethernet-Internal", "Wlan-GigabitEthernet"})

# first match wins; a family that matches nothing is "any interface using interface-common-grouping"
_APPLICABILITY = (
    (("L2_SWITCHPORT_",), COMMON_TYPES),
    (("L2W_",), WRAPPER_TYPES),
    (("L2_", "PVLAN_HOST_ASSOC", "PVLAN_PROMISCUOUS_MAP"), SWITCHPORT_TYPES),
    (("MSEC_NETWORK_LINK", "MAC_ACCESS_GROUP", "AUTO_QOS_", "DUAL_ACTIVE", "SRR_QUEUE", "SW_LOAD_BALANCING"),
     SWITCH_IF_TYPES),
    (("MSEC_",), MACSEC_TYPES),
    (("IP6_ND_",), ND_IF_TYPES),
    (("PHY_FEC",), frozenset({"TwentyFiveGigE"})),
    (("PHY_",), MEDIA_TYPES),
    (("NEGOTIATION",), frozenset({"ucse", "Ethernet-Internal"})),
    (("PO_MIN_LINKS", "PO_STANDALONE_DISABLE", "PO_PC_SPEED", "PO_LOAD_BALANCING", "PO_PUNT_CONTROL"),
     frozenset({"Port-channel"})),
    (("TYPE_VLAN_", "SVI_"), frozenset({"Vlan"})),
    (("TYPE_TUNNEL_",), frozenset({"Tunnel"})),
    (("TYPE_VIRTUAL_TEMPLATE_",), frozenset({"Virtual-Template"})),
    (("NVE_",), frozenset({"nve"})),
)

# bodies that sit directly under <native> (no interface scaffold). SVI_* is interface-scoped.
NATIVE_SCOPED = frozenset(
    n for n in TEMPLATES if n.startswith(("PVLAN_GLOBAL", "PVLAN_SECONDARY", "VLAN_", "GLOBAL_"))
)


def applies_to(base):
    """Set of interface paths the family is valid on, or None for native-scoped families."""
    if base in NATIVE_SCOPED:
        return None
    for prefixes, allowed in _APPLICABILITY:
        if base.startswith(prefixes):
            return allowed
    return COMMON_TYPES


def render(base, train="1712", **kw):
    """Render one family body. Namespaces are injected; every other placeholder must be in kw.
    Booleans are passed as the strings 'true' / 'false'. Raises KeyError for unknown or
    unavailable families and for missing placeholders."""
    return _Template(resolve(base, train)).substitute({**NS, **kw})


def wrap_native(*bodies):
    """<native> root. Use directly for NATIVE_SCOPED families (VLAN_*, PVLAN_GLOBAL*, GLOBAL_*)."""
    return f'<native xmlns="{NS["N"]}" xmlns:nc="{NS["NC"]}">{"".join(bodies)}</native>'


def wrap_interface(parent, name, *bodies, strict=False):
    """<native><interface><TYPE><name>..bodies..</TYPE></interface></native>.
    parent is the list name ('GigabitEthernet') or a nested path for subinterfaces
    ('Port-channel-subinterface/Port-channel'). strict=True rejects paths not in INTERFACE_PATHS."""
    parts = [p for p in parent.split("/") if p]
    if not parts:
        raise ValueError("parent is required")
    path = "/".join(parts)
    if strict and path not in INTERFACE_PATHS:
        why = "obsolete in 17.12" if path in OBSOLETE_INTERFACE_TYPES else "unknown"
        raise ValueError(f"{why} interface path {path!r}")
    opening = "".join(f"<{p}>" for p in parts)
    closing = "".join(f"</{p}>" for p in reversed(parts))
    return wrap_native(f'<interface>{opening}<name>{name}</name>{"".join(bodies)}{closing}</interface>')


def build_config(base, parent=None, name=None, train="1712", strict=False, **kw):
    """Complete NETCONF <config> payload for one family; picks the right scaffold automatically.
    strict=True additionally rejects interface paths the family is not defined on (applies_to)."""
    body = render(base, train, **kw)
    if base in NATIVE_SCOPED:
        inner = wrap_native(body)
    else:
        if not parent or name is None:
            raise ValueError(f"{base} is interface-scoped: parent and name are required")
        if strict:
            allowed = applies_to(base)
            path = "/".join(p for p in parent.split("/") if p)
            if allowed is not None and path not in allowed:
                raise ValueError(f"{base} is not defined on {path!r} in 17.12")
        inner = wrap_interface(parent, name, body, strict=strict)
    return f'<config xmlns="{NS["NC"]}">{inner}</config>'


def diff_vs_1715():
    """Yield (family, note) for families whose shape differs from the 1715 catalogue."""
    for fam in sorted(DIFFS_VS_1715):
        yield fam, DIFFS_VS_1715[fam]


def _selftest():
    """Render every family with dummy values and check well-formedness; exercise the wrappers."""
    import xml.dom.minidom as md

    class _Dummy(dict):
        def __missing__(self, key):
            return "x"

    ok = 0
    for fam in supported_on():
        xml = _Template(resolve(fam)).substitute(_Dummy(NS))
        md.parseString(f'<r xmlns:nc="{NS["NC"]}">{xml}</r>')
        ok += 1
    for fam in NOT_PRESENT:
        try:
            resolve(fam)
        except KeyError:
            pass
        else:
            raise AssertionError(f"{fam} should be unavailable")
    md.parseString(build_config("DESCRIPTION", "GigabitEthernet", "1/0/1", desc="uplink", strict=True))
    md.parseString(build_config("L2_VEPA", "Port-channel-subinterface/Port-channel", "1.100", strict=True))
    md.parseString(build_config("L2_ACCESS_VLAN", "GigabitEthernet", "1/0/2", access_vlan=10, strict=True))
    md.parseString(build_config("IP6_ND_RAGUARD_ATTACH", "Vlan", "10", policy_name="RG1", strict=True))
    md.parseString(build_config("SVI_PRIVATE_VLAN_MAPPING", "Vlan", "100", mapping="101,102", strict=True))
    md.parseString(build_config("VLAN_NAME", vlan_id=10, vlan_name="users"))
    md.parseString(build_config("PVLAN_GLOBAL", primary_vlan=100, secondary_vlans="101,102"))
    md.parseString(build_config("GLOBAL_ARP_ENTRY", ip="10.0.0.1", hwaddr="aaaa.bbbb.cccc", arp_type="ARPA"))
    md.parseString(build_config("GLOBAL_ND_RAGUARD_POLICY", policy_name="RG1"))
    assert "VLAN_NAME" in NATIVE_SCOPED and "DESCRIPTION" not in NATIVE_SCOPED
    assert "SVI_PRIVATE_VLAN_MAPPING" not in NATIVE_SCOPED
    for bad in (("L2_VEPA", "Loopback"), ("PO_MIN_LINKS", "Port-channel-subinterface/Port-channel"),
                ("IP6_ND_RAGUARD_ATTACH", "Dialer"), ("DESCRIPTION", "TwentyFiveGigabitEthernet")):
        try:
            build_config(bad[0], bad[1], "1", strict=True, desc="x", policy_name="x", min_links=2)
        except ValueError:
            pass
        else:
            raise AssertionError(f"strict should reject {bad}")
    for fam in DIFFS_VS_1715:
        assert fam in TEMPLATES, fam
    print(f"selftest OK: {ok} families render to well-formed XML; "
          f"{len(NOT_PRESENT)} verified-absent; {len(NATIVE_SCOPED)} native-scoped; "
          f"{len(DIFFS_VS_1715)} flagged vs 1715; {len(list(on_off_pairs()))} on/off pairs")


if __name__ == "__main__":
    _selftest()