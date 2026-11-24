# interface_attrs_1612.py
# Consolidated modular interface XML bodies for Cisco-IOS-XE-native (IOS XE 16.12)
# One-to-one counterpart of interface_attrs_1715.py / interface_attrs_173.py:
# same label names, _1612 suffix, same engine contract.
# Placeholders use $…; NS dict supplies $N, $NC, $SW, $ST, $VLAN.
#
# EVIDENCE BASIS (be aware when trusting a template)
#   VERIFIED against 16.12 YANG supplied:
#     * Cisco-IOS-XE-vlan  (rev 2019-07-01, semver 1.0.0)  -> PVLAN global, Vlan SVI
#     * Cisco-IOS-XE-native (rev 2019-07-01, semver 1.0.0) -> <vlan> container, hooks
#   NOT SUPPLIED for 16.12: Cisco-IOS-XE-interfaces (submodule) and Cisco-IOS-XE-switch.
#     Everything under interface scope is therefore carried from the existing 1612
#     catalogue, cross-checked against the 17.3 YANG and its revision history.
#     Families whose 16.12 shape rests on that inference are listed in UNVERIFIED_1612.
#
# SCOPE RULES
#   * Features absent from 16.12 are listed in NOT_PRESENT_1612 with the reason and
#     registered with a None slot, so resolve() raises a clear error.
#   * Shapes that differ from 17.15 are marked "# 1612-ADAPTED".
#   * Same placeholder vocabulary as 1715/173, so the files merge cleanly.
#
# DESIGN RULES (unchanged):
#   * Valued leaves (true|false) are symmetric: caller passes $flag.
#   * Every presence leaf has a matching *_REMOVE_1612 twin.
#   * Every additive/list feature has a *_REMOVE_1612 (remove-by-key) twin.
#   * Bulk forms accept $*_block fragments so the engine controls contents.
#   * Interface scaffolding (<native><interface><TYPE><name>) is owned by
#     wrap_interface()/build_config(); bodies here are bare.
#
# REFINE NOTES vs previous 1612 file
#   * FIXED: TEMPLATES builder checked "_173" (17.3 suffix), so every 16.12
#     constant was skipped and supported_on("1612") yielded 0 families.
#   * Switched to the explicit TEMPLATES dict (same style as 17.3/17.9/17.15).
#   * ADDED _REMOVE twins for port-security (MAX, MAX_VLAN, VIOLATION,
#     MAC_ACCESS, MAC_STICKY) — 17.3/17.9/17.15 already have these.
#   * ADDED L2PT_DROP_THRESHOLD_RATE / L2PT_SHUTDOWN_THRESHOLD_RATE (+ _REMOVE)
#     for 17.9 parity.
#   * ADDED wrap_interface(), wrap_native(), build_config(), NATIVE_SCOPED so
#     the engine can build full NETCONF <config> payloads like the other files.
#   * FIXED placeholder validation error text ("interface_attrs_173" -> "_1612").
#   * _selftest counts supported_on() once instead of three times.
#   * New families registered in UNVERIFIED_1612 (shape rests on the deprecated
#     single <port-security> container and the existing 1612 catalogue).

import re

# ============================================================
# NAMESPACES
# ============================================================
# $N    = http://cisco.com/ns/yang/Cisco-IOS-XE-native
# $NC   = urn:ietf:params:xml:ns:netconf:base:1.0
# $SW   = http://cisco.com/ns/yang/Cisco-IOS-XE-switch
# $ST   = http://cisco.com/ns/yang/Cisco-IOS-XE-spanning-tree
# $VLAN = http://cisco.com/ns/yang/Cisco-IOS-XE-vlan


# ============================================================
# 1. GENERAL ATTRIBUTES
# ============================================================

# --- text / labels ---
DESCRIPTION_1612        = "<description>$desc</description>"
DESCRIPTION_REMOVE_1612 = '<description nc:operation="remove"/>'
MAC_ADDRESS_1612        = "<mac-address>$mac</mac-address>"
MAC_ADDRESS_REMOVE_1612 = '<mac-address nc:operation="remove"/>'
# EXPORT_NAME            -> NOT PRESENT in 16.12

# --- admin state ---
SHUTDOWN_1612           = "<shutdown/>"
SHUTDOWN_REMOVE_1612    = '<shutdown nc:operation="remove"/>'

# --- L2 / MTU / timers ---
MTU_1612                = "<mtu>$mtu</mtu>"                           # 64..18000
MTU_REMOVE_1612         = '<mtu nc:operation="remove"/>'
DELAY_1612              = "<delay>$delay</delay>"
DELAY_REMOVE_1612       = '<delay nc:operation="remove"/>'
LOAD_INTERVAL_1612      = "<load-interval>$seconds</load-interval>"
LOAD_INTERVAL_REMOVE_1612 = '<load-interval nc:operation="remove"/>'

# --- bandwidth ---
MAX_BANDWIDTH_1612        = "<max-reserved-bandwidth>$percent</max-reserved-bandwidth>"
MAX_BANDWIDTH_REMOVE_1612 = '<max-reserved-bandwidth nc:operation="remove"/>'

# --- media / negotiation ---
# NOTE: in 17.3 <negotiation> exists ONLY on list ucse and list Ethernet-Internal
#       (interface-negotiation-grouping). It is not on GigabitEthernet etc.
NEGOTIATION_1612        = "<negotiation><auto>$flag</auto></negotiation>"
GEN_MDIX_1612           = "<mdix><auto>$flag</auto></mdix>"

# --- service / qos ---
SERVICE_INSERTION_1612        = "<service-insertion>$svc</service-insertion>"   # waas|appqoe
SERVICE_INSERTION_REMOVE_1612 = '<service-insertion nc:operation="remove"/>'
QOS_TRUST_1612          = '<interface_qos><trust><device>$device</device></trust></interface_qos>'
QOS_TRUST_REMOVE_1612   = '<interface_qos nc:operation="remove"/>'


# ============================================================
# 2. L2 SWITCHING
# ============================================================

# --- switchport (switchport-conf is in the interfaces submodule) ---
L2_SWITCHPORT_TRUE_1612  = "<switchport-conf><switchport>true</switchport></switchport-conf>"
L2_SWITCHPORT_FALSE_1612 = "<switchport-conf><switchport>false</switchport></switchport-conf>"

# --- switchport children from Cisco-IOS-XE-switch ($SW) ---
# 17.3 shape: the augment target is interface/<type>/switchport, so these nodes
# sit DIRECTLY under <switchport>. There is NO <switchport-config> wrapper (that
# is 17.15). The first child carries xmlns="$SW"; descendants inherit it.
# Present on: FastEthernet, GigabitEthernet, TwoGigabitEthernet, FiveGigabitEthernet,
#   AppGigabitEthernet, TenGigabitEthernet, TwentyFiveGigE, FortyGigabitEthernet,
#   HundredGigE, Port-channel, Port-channel-subinterface/Port-channel
#   (deprecated: ucse, Ethernet-Internal, Wlan-GigabitEthernet).
# Requires feature ios-features:switching-platform.

# --- DTP (nonegotiate) ---
L2_DTP_DISABLE_TRUE_1612  = '<switchport><nonegotiate xmlns="$SW"/></switchport>'
L2_DTP_DISABLE_FALSE_1612 = '<switchport><nonegotiate xmlns="$SW" nc:operation="remove"/></switchport>'

# --- voice vlan ---
L2_VOICE_FULL_1612 = (
    '<switchport>'
    '<voice xmlns="$SW">'
      '<vlan><vlan>$voice_vlan</vlan></vlan>'
      '<detect><cisco-phone><full-duplex/></cisco-phone></detect>'
    '</voice>'
    '<access xmlns="$SW"><vlan><vlan>$access_vlan</vlan></vlan></access>'
    '</switchport>'
)
L2_VOICE_FULL_REMOVE_1612 = (
    '<switchport>'
    '<voice xmlns="$SW" nc:operation="remove"/>'
    '<access xmlns="$SW" nc:operation="remove"/>'
    '</switchport>'
)
L2_VOICE_VLAN_ID_1612 = (
    '<switchport><voice xmlns="$SW"><vlan><vlan>$voice_vlan</vlan></vlan></voice></switchport>'
)
L2_VOICE_VLAN_DOT1P_1612 = (
    '<switchport><voice xmlns="$SW"><vlan><vlan>dot1p</vlan></vlan></voice></switchport>'
)
L2_VOICE_VLAN_NONE_1612 = (
    '<switchport><voice xmlns="$SW"><vlan><vlan>none</vlan></vlan></voice></switchport>'
)
L2_VOICE_VLAN_UNTAGGED_1612 = (
    '<switchport><voice xmlns="$SW"><vlan><vlan>untagged</vlan></vlan></voice></switchport>'
)
L2_VOICE_VLAN_REMOVE_1612 = (
    '<switchport><voice xmlns="$SW"><vlan nc:operation="remove"/></voice></switchport>'
)
L2_VOICE_DETECT_1612 = (
    '<switchport><voice xmlns="$SW"><detect><cisco-phone><full-duplex/></cisco-phone></detect></voice></switchport>'
)
L2_VOICE_DETECT_REMOVE_1612 = (
    '<switchport><voice xmlns="$SW"><detect nc:operation="remove"/></voice></switchport>'
)
# access vlan: 1..4094 | dynamic
L2_ACCESS_VLAN_1612 = (
    '<switchport><access xmlns="$SW"><vlan><vlan>$access_vlan</vlan></vlan></access></switchport>'
)
L2_ACCESS_VLAN_REMOVE_1612 = (
    '<switchport><access xmlns="$SW"><vlan nc:operation="remove"/></access></switchport>'
)

# --- trunk pruning ---
# NOTE: in 17.3 <vlans> and <except> are LEAF-LISTS (repeat the element per value);
#       <add> and <remove> are single leaves taking a range string.
L2_TRUNK_PRUNING_ADD_1612 = (
    '<switchport><trunk xmlns="$SW"><pruning><vlan><add>$vlans</add></vlan></pruning></trunk></switchport>'
)
L2_TRUNK_PRUNING_REMOVE_1612 = (
    '<switchport><trunk xmlns="$SW"><pruning><vlan><remove>$vlans</remove></vlan></pruning></trunk></switchport>'
)
L2_TRUNK_PRUNING_REPLACE_1612 = (
    '<switchport><trunk xmlns="$SW"><pruning><vlan><vlans nc:operation="replace">$vlans</vlans></vlan></pruning></trunk></switchport>'
)
L2_TRUNK_PRUNING_NONE_1612 = (
    '<switchport><trunk xmlns="$SW"><pruning><vlan><none/></vlan></pruning></trunk></switchport>'
)
L2_TRUNK_PRUNING_REMOVE_ALL_1612 = (
    '<switchport><trunk xmlns="$SW"><pruning nc:operation="remove"/></trunk></switchport>'
)

# --- PVLAN global (GLOBAL scope, not interface-scoped) ---
# <vlan> is a native container; <vlan-list> is augmented in by Cisco-IOS-XE-vlan,
# so it carries xmlns="$VLAN". Requires feature ios-features:private-vlan.
# 1612-ADAPTED (VERIFIED, Cisco-IOS-XE-vlan 16.12): <primary/> and <association> are SIBLING leaves, and
# <association> is one string (e.g. "101,102"). There is no add/remove action
# leaf as in 17.15, so $action is no longer used here.
PVLAN_GLOBAL_1612 = (
    '<vlan xmlns="$N"><vlan-list xmlns="$VLAN">'
      '<id>$primary_vlan</id>'
      '<private-vlan><primary/><association>$secondary_vlans</association></private-vlan>'
    '</vlan-list></vlan>'
)
PVLAN_GLOBAL_PRIMARY_1612 = (
    '<vlan xmlns="$N"><vlan-list xmlns="$VLAN">'
      '<id>$primary_vlan</id><private-vlan><primary/></private-vlan>'
    '</vlan-list></vlan>'
)
PVLAN_GLOBAL_ASSOC_1612 = (
    '<vlan xmlns="$N"><vlan-list xmlns="$VLAN">'
      '<id>$primary_vlan</id><private-vlan><association>$secondary_vlans</association></private-vlan>'
    '</vlan-list></vlan>'
)
PVLAN_GLOBAL_REMOVE_1612 = (
    '<vlan xmlns="$N"><vlan-list xmlns="$VLAN">'
      '<id>$primary_vlan</id>'
      '<private-vlan nc:operation="remove"/>'
    '</vlan-list></vlan>'
)
# $pvlan_type: community | isolated
PVLAN_SECONDARY_1612 = (
    '<vlan xmlns="$N"><vlan-list xmlns="$VLAN">'
      '<id>$secondary_vlan</id>'
      '<private-vlan><$pvlan_type/></private-vlan>'
    '</vlan-list></vlan>'
)
PVLAN_SECONDARY_REMOVE_1612 = (
    '<vlan xmlns="$N"><vlan-list xmlns="$VLAN" nc:operation="remove">'
      '<id>$secondary_vlan</id>'
    '</vlan-list></vlan>'
)

# --- PVLAN interface bindings ---
PVLAN_HOST_ASSOC_1612 = (
    '<switchport>'
      '<mode xmlns="$SW"><private-vlan><host/></private-vlan></mode>'
      '<private-vlan xmlns="$SW"><host-association>'
        '<primary-range>$primary_vlan</primary-range>'
        '<secondary-range>$secondary_vlan</secondary-range>'
      '</host-association></private-vlan>'
    '</switchport>'
)
PVLAN_HOST_ASSOC_REMOVE_1612 = (
    '<switchport>'
      '<private-vlan xmlns="$SW"><host-association nc:operation="remove"/></private-vlan>'
    '</switchport>'
)
PVLAN_PROMISCUOUS_MAP_1612 = (
    '<switchport>'
      '<mode xmlns="$SW"><private-vlan><promiscuous/></private-vlan></mode>'
      '<private-vlan xmlns="$SW"><mapping>'
        '<primary-range>$primary_vlan</primary-range>'
        '<secondary-range>$secondary_vlans</secondary-range>'
      '</mapping></private-vlan>'
    '</switchport>'
)
PVLAN_PROMISCUOUS_MAP_REMOVE_1612 = (
    '<switchport>'
      '<private-vlan xmlns="$SW"><mapping nc:operation="remove"/></private-vlan>'
    '</switchport>'
)

# --- port-security ---
# 1612-ADAPTED: single <port-security> presence container under $SW (this is the
# container 17.3 marks deprecated in favour of port-security-cfg / -conf).
#   maximum  : <maximum><max-addresses>[<vlan>]
#   violation: plain leaf  protect | restrict | shutdown   (no "shutdown vlan")
#   sticky   : <mac-address><sticky/>
#   static MAC: <mac-address><hw-address> (+ <sticky/>); one entry per interface
L2_PORTSEC_ENABLE_1612 = (
    '<switchport><port-security xmlns="$SW"/></switchport>'
)
L2_PORTSEC_ENABLE_REMOVE_1612 = (
    '<switchport><port-security xmlns="$SW" nc:operation="remove"/></switchport>'
)
L2_PORTSEC_MAX_1612 = (
    '<switchport><port-security xmlns="$SW"><maximum>'
      '<max-addresses>$max</max-addresses>'
    '</maximum></port-security></switchport>'
)
L2_PORTSEC_MAX_VLAN_1612 = (
    '<switchport><port-security xmlns="$SW"><maximum>'
      '<max-addresses>$max</max-addresses><vlan>$vlan_kind</vlan>'
    '</maximum></port-security></switchport>'
)
# ADDED: remove the <maximum> entry.
L2_PORTSEC_MAX_REMOVE_1612 = (
    '<switchport><port-security xmlns="$SW"><maximum nc:operation="remove"/></port-security></switchport>'
)
# $violation: protect | restrict | shutdown
L2_PORTSEC_VIOLATION_1612 = (
    '<switchport><port-security xmlns="$SW"><violation>$violation</violation></port-security></switchport>'
)
# ADDED: remove the violation leaf.
L2_PORTSEC_VIOLATION_REMOVE_1612 = (
    '<switchport><port-security xmlns="$SW"><violation nc:operation="remove"/></port-security></switchport>'
)
L2_PORTSEC_STICKY_1612 = (
    '<switchport><port-security xmlns="$SW"><mac-address><sticky/></mac-address></port-security></switchport>'
)
L2_PORTSEC_STICKY_REMOVE_1612 = (
    '<switchport><port-security xmlns="$SW"><mac-address><sticky nc:operation="remove"/></mac-address></port-security></switchport>'
)
L2_PORTSEC_AGING_1612 = (
    '<switchport><port-security xmlns="$SW"><aging><time>$minutes</time><type>$aging_type</type></aging></port-security></switchport>'
)
L2_PORTSEC_AGING_REMOVE_1612 = (
    '<switchport><port-security xmlns="$SW"><aging nc:operation="remove"/></port-security></switchport>'
)
L2_PORTSEC_MAC_ACCESS_1612 = (
    '<switchport><port-security xmlns="$SW"><mac-address><hw-address>$hwaddr</hw-address></mac-address></port-security></switchport>'
)
# ADDED: remove a single static MAC by its hw-address.
L2_PORTSEC_MAC_ACCESS_REMOVE_1612 = (
    '<switchport><port-security xmlns="$SW"><mac-address nc:operation="remove">'
    '<hw-address>$hwaddr</hw-address></mac-address></port-security></switchport>'
)
L2_PORTSEC_MAC_STICKY_1612 = (
    '<switchport><port-security xmlns="$SW"><mac-address><sticky/><hw-address>$hwaddr</hw-address></mac-address></port-security></switchport>'
)
# ADDED: remove a single sticky MAC by its hw-address.
L2_PORTSEC_MAC_STICKY_REMOVE_1612 = (
    '<switchport><port-security xmlns="$SW"><mac-address nc:operation="remove">'
    '<hw-address>$hwaddr</hw-address><sticky/></mac-address></port-security></switchport>'
)

# --- protected / host / block / vepa ---
L2_PROTECTED_1612        = '<switchport><protected xmlns="$SW"/></switchport>'
L2_PROTECTED_REMOVE_1612 = '<switchport><protected xmlns="$SW" nc:operation="remove"/></switchport>'
L2_HOST_1612             = '<switchport><host xmlns="$SW"/></switchport>'
L2_HOST_REMOVE_1612      = '<switchport><host xmlns="$SW" nc:operation="remove"/></switchport>'
L2_BLOCK_MULTICAST_1612  = '<switchport><block xmlns="$SW"><multicast/></block></switchport>'
L2_BLOCK_MULTICAST_REMOVE_1612 = (
    '<switchport><block xmlns="$SW"><multicast nc:operation="remove"/></block></switchport>'
)
L2_BLOCK_UNICAST_1612    = '<switchport><block xmlns="$SW"><unicast/></block></switchport>'
L2_BLOCK_UNICAST_REMOVE_1612 = (
    '<switchport><block xmlns="$SW"><unicast nc:operation="remove"/></block></switchport>'
)
L2_VEPA_1612        = '<switchport><vepa xmlns="$SW"><enabled/></vepa></switchport>'
L2_VEPA_REMOVE_1612 = '<switchport><vepa xmlns="$SW"><enabled nc:operation="remove"/></vepa></switchport>'

# --- L2PT (l2protocol-tunnel) ---
# 1612-ADAPTED (existing 1612 catalogue): native node carries cdp|stp|vtp thresholds;
# lldp + point-to-point live in the $SW namespace (switchport l2protocol-tunnel).
# l2protocol *forward* does not exist in 16.12 (added interfaces rev 2020-03).
# $proto     : cdp | stp | vtp
# $p2p_proto : lacp | pagp | udld
L2PT_TUNNEL_CORE_1612        = '<l2protocol-tunnel><$proto/></l2protocol-tunnel>'
L2PT_TUNNEL_CORE_REMOVE_1612 = '<l2protocol-tunnel><$proto nc:operation="remove"/></l2protocol-tunnel>'
L2PT_TUNNEL_P2P_1612         = '<l2protocol-tunnel xmlns="$SW"><point-to-point><$p2p_proto/></point-to-point></l2protocol-tunnel>'
L2PT_TUNNEL_P2P_REMOVE_1612  = '<l2protocol-tunnel xmlns="$SW"><point-to-point><$p2p_proto nc:operation="remove"/></point-to-point></l2protocol-tunnel>'
L2PT_TUNNEL_CORE_BLOCK_1612        = '<l2protocol-tunnel>$core_block</l2protocol-tunnel>'
L2PT_TUNNEL_CORE_BLOCK_REMOVE_1612 = '<l2protocol-tunnel nc:operation="remove"/>'
L2PT_TUNNEL_P2P_BLOCK_1612         = '<l2protocol-tunnel xmlns="$SW"><point-to-point>$p2p_block</point-to-point></l2protocol-tunnel>'
L2PT_TUNNEL_P2P_BLOCK_REMOVE_1612  = '<l2protocol-tunnel xmlns="$SW"><point-to-point nc:operation="remove"/></l2protocol-tunnel>'

# NOTE: 17.3 models these as flat <proto>$pps</proto>; the nested <packet-rate> form
# below is the existing 1612 catalogue shape. Listed in UNVERIFIED_1612.
L2PT_DROP_THRESHOLD_1612 = (
    '<l2protocol-tunnel><drop-threshold>'
      '<$proto><packet-rate>$pps</packet-rate></$proto>'
    '</drop-threshold></l2protocol-tunnel>'
)
L2PT_DROP_THRESHOLD_REMOVE_1612 = (
    '<l2protocol-tunnel><drop-threshold><$proto nc:operation="remove"/></drop-threshold></l2protocol-tunnel>'
)
# ADDED (17.9 parity): sibling <packet-rate> leaf of drop-threshold.
L2PT_DROP_THRESHOLD_RATE_1612 = (
    '<l2protocol-tunnel><drop-threshold><packet-rate>$pps</packet-rate></drop-threshold></l2protocol-tunnel>'
)
L2PT_DROP_THRESHOLD_RATE_REMOVE_1612 = (
    '<l2protocol-tunnel><drop-threshold><packet-rate nc:operation="remove"/></drop-threshold></l2protocol-tunnel>'
)
L2PT_DROP_THRESHOLD_P2P_1612 = (
    '<l2protocol-tunnel xmlns="$SW"><drop-threshold><point-to-point>'
      '<$p2p_proto><pps_num>$pps</pps_num></$p2p_proto>'
    '</point-to-point></drop-threshold></l2protocol-tunnel>'
)
L2PT_DROP_THRESHOLD_P2P_REMOVE_1612 = (
    '<l2protocol-tunnel xmlns="$SW"><drop-threshold><point-to-point>'
      '<$p2p_proto nc:operation="remove"/>'
    '</point-to-point></drop-threshold></l2protocol-tunnel>'
)
L2PT_SHUTDOWN_THRESHOLD_1612 = (
    '<l2protocol-tunnel><shutdown-threshold>'
      '<$proto><packet-rate>$pps</packet-rate></$proto>'
    '</shutdown-threshold></l2protocol-tunnel>'
)
L2PT_SHUTDOWN_THRESHOLD_REMOVE_1612 = (
    '<l2protocol-tunnel><shutdown-threshold><$proto nc:operation="remove"/></shutdown-threshold></l2protocol-tunnel>'
)
# ADDED (17.9 parity): sibling <packet-rate> leaf of shutdown-threshold.
L2PT_SHUTDOWN_THRESHOLD_RATE_1612 = (
    '<l2protocol-tunnel><shutdown-threshold><packet-rate>$pps</packet-rate></shutdown-threshold></l2protocol-tunnel>'
)
L2PT_SHUTDOWN_THRESHOLD_RATE_REMOVE_1612 = (
    '<l2protocol-tunnel><shutdown-threshold><packet-rate nc:operation="remove"/></shutdown-threshold></l2protocol-tunnel>'
)
L2PT_SHUTDOWN_THRESHOLD_P2P_1612 = (
    '<l2protocol-tunnel xmlns="$SW"><shutdown-threshold><point-to-point>'
      '<$p2p_proto><pps_num>$pps</pps_num></$p2p_proto>'
    '</point-to-point></shutdown-threshold></l2protocol-tunnel>'
)
L2PT_SHUTDOWN_THRESHOLD_P2P_REMOVE_1612 = (
    '<l2protocol-tunnel xmlns="$SW"><shutdown-threshold><point-to-point>'
      '<$p2p_proto nc:operation="remove"/>'
    '</point-to-point></shutdown-threshold></l2protocol-tunnel>'
)


# ============================================================
# 3. ARP + LINK TUNING
# ============================================================

# --- ARP ---
# 16.12: timeout only. snap / entries interface-limit / packet-priority were added
# with the "arp model gaps" fix (interfaces rev 2019-11-01, i.e. 17.1+).
ARP_TIMEOUT_1612        = "<arp><timeout>$secs</timeout></arp>"
ARP_TIMEOUT_REMOVE_1612 = '<arp><timeout nc:operation="remove"/></arp>'

# --- priority-queue / rcv-queue ---
PQ_OUT_ENABLE_1612        = "<priority-queue><out/></priority-queue>"
PQ_OUT_ENABLE_REMOVE_1612 = '<priority-queue><out nc:operation="remove"/></priority-queue>'
PQ_COS_MAP_1612 = (
    "<priority-queue><cos-map>"
    "<id>$qid</id>"
    "$cos_values_block"
    "</cos-map></priority-queue>"
)
PQ_COS_MAP_REMOVE_1612 = (
    '<priority-queue><cos-map nc:operation="remove"><id>$qid</id></cos-map></priority-queue>'
)
RCV_QUEUE_COS_MAP_1612 = (
    "<rcv-queue><cos-map>"
    "<queue-id>$qid</queue-id>"
    "<threshold-id>$tid</threshold-id>"
    "$cos_values_block"
    "</cos-map></rcv-queue>"
)
RCV_QUEUE_COS_MAP_REMOVE_1612 = (
    '<rcv-queue><cos-map nc:operation="remove">'
    '<queue-id>$qid</queue-id><threshold-id>$tid</threshold-id>'
    '</cos-map></rcv-queue>'
)

# --- flowcontrol / hold-queue ---
FLOWCONTROL_1612 = (
    "<flowcontrol>"
    "<receive>$rx</receive>"
    "<send>$tx</send>"
    "</flowcontrol>"
)
FLOWCONTROL_REMOVE_1612 = '<flowcontrol nc:operation="remove"/>'
HOLD_QUEUE_1612 = (
    "<hold-queue>"
    "<direction>$direction</direction>"
    "<queue-length>$qlen</queue-length>"
    "</hold-queue>"
)
# FIXED vs 1715: hold-queue is a list keyed by <direction>; remove by key.
HOLD_QUEUE_REMOVE_1612 = (
    '<hold-queue nc:operation="remove"><direction>$direction</direction></hold-queue>'
)

# --- bandwidth ---
LINK_BANDWIDTH_1612        = "<bandwidth><kilobits>$kbps</kilobits></bandwidth>"
LINK_BANDWIDTH_REMOVE_1612 = '<bandwidth nc:operation="remove"/>'
LINK_BANDWIDTH_QOS_REF_1612 = (
    "<bandwidth><qos-reference>$kbps</qos-reference></bandwidth>"
)
LINK_BANDWIDTH_QOS_REF_REMOVE_1612 = (
    '<bandwidth><qos-reference nc:operation="remove"/></bandwidth>'
)

# --- dampening ---
DAMPENING_FULL_1612 = (
    "<dampening>"
    "<dampening-time>$half_life</dampening-time>"
    "<start-reusing-time>$reuse</start-reusing-time>"
    "<start-supressing-time>$suppress</start-supressing-time>"
    "<maximum-supressing-time>$max_suppress</maximum-supressing-time>"
    "</dampening>"
)
DAMPENING_DEFAULT_1612 = "<dampening/>"
DAMPENING_REMOVE_1612  = '<dampening nc:operation="remove"/>'

# --- srlg -> NOT PRESENT in 16.12 ---

# --- domain ---
DOMAIN_NAME_1612        = "<domain><name>$domain</name></domain>"
DOMAIN_NAME_REMOVE_1612 = '<domain><name nc:operation="remove"/></domain>'
DOMAIN_PATH_1612 = (
    "<domain>"
    "<path>$sp_path</path>"
    "<path-id>$path_id</path-id>"
    "</domain>"
)
DOMAIN_PATH_REMOVE_1612 = (
    '<domain><path nc:operation="remove">$sp_path</path></domain>'
)

# --- keepalive ---
# 1612-ADAPTED: 17.3 has a choice:
#   leaf keepalive (boolean)  |  keepalive-settings/keepalive (presence){period,retries}
# There is no <keepalive-config> wrapper.
KEEPALIVE_TIMERS_1612 = (
    "<keepalive-settings><keepalive>"
    "<period>$period</period>"
    "<retries>$retries</retries>"
    "</keepalive></keepalive-settings>"
)
KEEPALIVE_DISABLE_1612 = "<keepalive>false</keepalive>"

# --- logging ---
# link-status-enable is not in the 16.12 catalogue: use LINK_LOGGING_EVENT with
# $event = link-status instead.
# $event: bundle-status | link-status | trunk-status | nfas-status | power-inline-status | status
LINK_LOGGING_EVENT_1612 = (
    "<logging><event><$event/></event></logging>"
)
LINK_LOGGING_EVENT_REMOVE_1612 = (
    '<logging><event><$event nc:operation="remove"/></event></logging>'
)
LINK_LOGGING_EVENTS_BLOCK_1612 = (
    "<logging><event>$events_block</event></logging>"
)
LINK_LOGGING_EVENTS_BLOCK_REMOVE_1612 = (
    '<logging><event nc:operation="remove"/></logging>'
)
LINK_LOGGING_SPANNING_TREE_1612 = (
    "<logging><event><spanning-tree><status/></spanning-tree></event></logging>"
)
LINK_LOGGING_SPANNING_TREE_REMOVE_1612 = (
    '<logging><event><spanning-tree nc:operation="remove"/></event></logging>'
)
LINK_LOGGING_SUBIF_1612 = (
    "<logging><event><subif-link-status>$ignore_bulk_block</subif-link-status></event></logging>"
)
LINK_LOGGING_SUBIF_REMOVE_1612 = (
    '<logging><event><subif-link-status nc:operation="remove"/></event></logging>'
)

# --- fair queue ---
FAIR_QUEUE_1612        = "<fair-queue><incomplete/></fair-queue>"
FAIR_QUEUE_REMOVE_1612 = '<fair-queue nc:operation="remove"/>'
FAIR_QUEUE_CONF_1612   = (
    "<fair-queue-conf><fair-queue>$flag</fair-queue></fair-queue-conf>"
)


# ============================================================
# 4. IPv4
# ============================================================

IP4_PRIMARY_1612 = (
    "<ip><address><primary>"
    "<address>$ip</address><mask>$mask</mask>"
    "</primary></address></ip>"
)
IP4_PRIMARY_REMOVE_1612 = (
    '<ip><address><primary nc:operation="remove"/></address></ip>'
)
IP4_SECONDARY_1612 = (
    "<ip><address><secondary>"
    "<address>$ip</address><mask>$mask</mask>"
    "<secondary/>"
    "</secondary></address></ip>"
)
IP4_SECONDARY_REMOVE_1612 = (
    '<ip><address><secondary nc:operation="remove">'
    '<address>$ip</address><mask>$mask</mask>'
    '</secondary></address></ip>'
)
IP4_DHCP_1612        = "<ip><address><dhcp/></address></ip>"
IP4_DHCP_REMOVE_1612 = '<ip><address><dhcp nc:operation="remove"/></address></ip>'
IP4_NEGOTIATED_1612        = "<ip><address><negotiated/></address></ip>"
IP4_NEGOTIATED_REMOVE_1612 = '<ip><address><negotiated nc:operation="remove"/></address></ip>'
IP4_DHCP_OPTIONS_1612 = (
    "<ip><address><dhcp>"
    "$client_id_block"
    "$hostname_block"
    "</dhcp></address></ip>"
)
IP4_UNNUMBERED_1612        = "<ip><unnumbered>$src_if</unnumbered></ip>"
IP4_UNNUMBERED_REMOVE_1612 = '<ip><unnumbered nc:operation="remove"/></ip>'
IP4_ACCESS_GROUP_IN_1612 = (
    "<ip><access-group><in><acl>"
    "<acl-name>$acl</acl-name><in/>"
    "</acl></in></access-group></ip>"
)
IP4_ACCESS_GROUP_IN_REMOVE_1612 = (
    '<ip><access-group><in nc:operation="remove"/></access-group></ip>'
)
IP4_ACCESS_GROUP_OUT_1612 = (
    "<ip><access-group><out><acl>"
    "<acl-name>$acl</acl-name><out/>"
    "</acl></out></access-group></ip>"
)
IP4_ACCESS_GROUP_OUT_REMOVE_1612 = (
    '<ip><access-group><out nc:operation="remove"/></access-group></ip>'
)
# 1612-ADAPTED: common-acl has only <common> + <in|out>; no <acl-name> child.
IP4_ACCESS_GROUP_COMMON_IN_1612 = (
    "<ip><access-group><in><common-acl>"
    "<common>$common_acl</common><in/>"
    "</common-acl></in></access-group></ip>"
)
IP4_ACCESS_GROUP_COMMON_IN_REMOVE_1612 = (
    '<ip><access-group><in><common-acl nc:operation="remove"/></in></access-group></ip>'
)
IP4_ACCESS_GROUP_COMMON_OUT_1612 = (
    "<ip><access-group><out><common-acl>"
    "<common>$common_acl</common><out/>"
    "</common-acl></out></access-group></ip>"
)
IP4_ACCESS_GROUP_COMMON_OUT_REMOVE_1612 = (
    '<ip><access-group><out><common-acl nc:operation="remove"/></out></access-group></ip>'
)
IP4_VRF_FORWARDING_1612 = "<vrf><forwarding>$vrf</forwarding></vrf>"
IP4_VRF_FORWARDING_REMOVE_1612 = (
    '<vrf><forwarding nc:operation="remove">$vrf</forwarding></vrf>'
)
IP4_VRF_RECEIVE_1612 = "<ip><vrf><receive>$vrf</receive></vrf></ip>"
IP4_VRF_RECEIVE_REMOVE_1612 = (
    '<ip><vrf><receive nc:operation="remove">$vrf</receive></vrf></ip>'
)
IP4_VRF_SITEMAP_1612 = "<ip><vrf><sitemap>$route_map</sitemap></vrf></ip>"
IP4_VRF_SITEMAP_REMOVE_1612 = (
    '<ip><vrf><sitemap nc:operation="remove">$route_map</sitemap></vrf></ip>'
)
IP4_HELPER_1612 = (
    "<ip><helper-address><address>$helper</address></helper-address></ip>"
)
IP4_HELPER_REMOVE_1612 = (
    '<ip><helper-address nc:operation="remove"><address>$helper</address></helper-address></ip>'
)
IP4_HELPER_GLOBAL_1612 = (
    "<ip><helper-address><address>$helper</address><global/>"
    "</helper-address></ip>"
)
IP4_HELPER_GLOBAL_REMOVE_1612 = (
    '<ip><helper-address nc:operation="remove"><address>$helper</address><global/></helper-address></ip>'
)
IP4_HELPER_VRF_1612 = (
    "<ip><helper-address><address>$helper</address><vrf>$vrf</vrf>"
    "</helper-address></ip>"
)
IP4_HELPER_VRF_REMOVE_1612 = (
    '<ip><helper-address nc:operation="remove"><address>$helper</address><vrf>$vrf</vrf></helper-address></ip>'
)
IP4_POLICY_ROUTE_MAP_1612 = (
    "<ip><policy><route-map>$route_map</route-map></policy></ip>"
)
IP4_POLICY_ROUTE_MAP_REMOVE_1612 = (
    '<ip><policy><route-map nc:operation="remove"/></policy></ip>'
)
# FIXED vs 1715: closing </ip> was missing
IP4_PROXY_ARP_1612 = "<ip><proxy-arp>$flag</proxy-arp></ip>"
IP4_LOCAL_PROXY_ARP_1612        = "<ip><local-proxy-arp/></ip>"
IP4_LOCAL_PROXY_ARP_REMOVE_1612 = '<ip><local-proxy-arp nc:operation="remove"/></ip>'
# FIXED vs 1715: closing </ip> was missing
IP4_REDIRECTS_1612 = "<ip><redirects>$flag</redirects></ip>"
# IP4_CLEAR_DF -> NOT PRESENT in 16.12
IP4_TCP_MSS_1612        = "<ip><tcp><adjust-mss>$mss</adjust-mss></tcp></ip>"      # 500..1460
IP4_TCP_MSS_REMOVE_1612 = '<ip><tcp><adjust-mss nc:operation="remove"/></tcp></ip>'
IP4_MTU_1612            = "<ip><mtu>$ip_mtu</mtu></ip>"                            # 68..9976
IP4_MTU_REMOVE_1612     = '<ip><mtu nc:operation="remove"/></ip>'
# 1612-ADAPTED: no ACL leaf under verify/unicast/source in 17.3 -> $acl_block dropped.
#              Only reachable-via (any|rx), allow-self-ping, allow-default exist.
IP4_URPF_1612 = (
    "<ip><verify><unicast><source>"
    "<reachable-via>$via</reachable-via>"
    "$allow_block"
    "</source></unicast></verify></ip>"
)
IP4_URPF_REMOVE_1612 = '<ip><verify nc:operation="remove"/></ip>'
IP4_ARP_INSPECT_TRUST_1612 = (
    '<ip><arp><inspection><trust/></inspection></arp></ip>'
)
IP4_ARP_INSPECT_TRUST_REMOVE_1612 = (
    '<ip><arp><inspection><trust nc:operation="remove"/></inspection></arp></ip>'
)
# 1612-ADAPTED: limit has only <rate> and <none>; no burst leaf -> $burst_block dropped.
IP4_ARP_INSPECT_RATE_1612 = (
    "<ip><arp><inspection><limit>"
    "<rate>$pps</rate>"
    "</limit></inspection></arp></ip>"
)
IP4_ARP_INSPECT_RATE_REMOVE_1612 = (
    '<ip><arp><inspection><limit nc:operation="remove"/></inspection></arp></ip>'
)
IP4_ARP_INSPECT_RATE_NONE_1612 = (
    "<ip><arp><inspection><limit><none/></limit></inspection></arp></ip>"
)
IP4_DIRECTED_BROADCAST_1612        = "<ip><directed-broadcast/></ip>"
IP4_DIRECTED_BROADCAST_REMOVE_1612 = (
    '<ip><directed-broadcast nc:operation="remove"/></ip>'
)
IP4_DIRECTED_BROADCAST_ACL_1612 = (
    "<ip><directed-broadcast>"
    "<direct-broadcast>$acl</direct-broadcast>"
    "</directed-broadcast></ip>"
)


# ============================================================
# 5. IPv6
# ============================================================

IP6_ENABLE_1612        = "<ipv6><enable/></ipv6>"
IP6_ENABLE_REMOVE_1612 = '<ipv6><enable nc:operation="remove"/></ipv6>'

IP6_ADDRESS_PREFIX_1612 = (
    "<ipv6><address><prefix-list><prefix>$ipv6</prefix></prefix-list></address></ipv6>"
)
IP6_ADDRESS_PREFIX_REMOVE_1612 = (
    '<ipv6><address><prefix-list nc:operation="remove"><prefix>$ipv6</prefix></prefix-list></address></ipv6>'
)
IP6_ADDRESS_EUI64_1612 = (
    "<ipv6><address><prefix-list><prefix>$ipv6</prefix><eui-64/></prefix-list></address></ipv6>"
)
IP6_ADDRESS_EUI64_REMOVE_1612 = (
    '<ipv6><address><prefix-list nc:operation="remove"><prefix>$ipv6</prefix><eui-64/></prefix-list></address></ipv6>'
)
IP6_ADDRESS_ANYCAST_1612 = (
    "<ipv6><address><prefix-list><prefix>$ipv6</prefix><anycast/></prefix-list></address></ipv6>"
)
IP6_ADDRESS_ANYCAST_REMOVE_1612 = (
    '<ipv6><address><prefix-list nc:operation="remove"><prefix>$ipv6</prefix><anycast/></prefix-list></address></ipv6>'
)
IP6_ADDRESS_LINK_LOCAL_1612 = (
    "<ipv6><address><link-local-address><address>$ll</address><link-local/>"
    "</link-local-address></address></ipv6>"
)
IP6_ADDRESS_LINK_LOCAL_REMOVE_1612 = (
    '<ipv6><address><link-local-address nc:operation="remove"><address>$ll</address><link-local/></link-local-address></address></ipv6>'
)
IP6_ADDRESS_AUTOCONFIG_1612        = "<ipv6><address><autoconfig/></address></ipv6>"
IP6_ADDRESS_AUTOCONFIG_REMOVE_1612 = (
    '<ipv6><address><autoconfig nc:operation="remove"/></address></ipv6>'
)
IP6_ADDRESS_AUTOCONFIG_DEFAULT_1612 = (
    "<ipv6><address><autoconfig><default/></autoconfig></address></ipv6>"
)
IP6_ADDRESS_AUTOCONFIG_DEFAULT_REMOVE_1612 = (
    '<ipv6><address><autoconfig nc:operation="remove"><default/></autoconfig></address></ipv6>'
)
IP6_ADDRESS_DHCP_1612        = "<ipv6><address><dhcp/></address></ipv6>"
IP6_ADDRESS_DHCP_REMOVE_1612 = (
    '<ipv6><address><dhcp nc:operation="remove"/></address></ipv6>'
)
IP6_ADDRESS_DHCP_RAPID_COMMIT_1612 = (
    "<ipv6><address><dhcp><rapid-commit/></dhcp></address></ipv6>"
)
IP6_ADDRESS_DHCP_RAPID_COMMIT_REMOVE_1612 = (
    '<ipv6><address><dhcp nc:operation="remove"><rapid-commit/></dhcp></address></ipv6>'
)
# IP6_ADDRESS_PREFIX_NAME -> NOT PRESENT in 16.12

IP6_UNNUMBERED_1612        = "<ipv6><unnumbered>$src_if</unnumbered></ipv6>"
IP6_UNNUMBERED_REMOVE_1612 = '<ipv6><unnumbered nc:operation="remove"/></ipv6>'
IP6_MTU_1612               = "<ipv6><mtu>$ip6_mtu</mtu></ipv6>"                    # 1280..9976
IP6_MTU_REMOVE_1612        = '<ipv6><mtu nc:operation="remove"/></ipv6>'
# IP6_ND_DAD_ATTEMPTS / IP6_ND_NUD_IGP -> NOT PRESENT (ipv6/nd is an empty container)
IP6_TCP_ADJUST_MSS_1612        = "<ipv6><tcp><adjust-mss>$mss</adjust-mss></tcp></ipv6>"   # 40..1454
IP6_TCP_ADJUST_MSS_REMOVE_1612 = (
    '<ipv6><tcp><adjust-mss nc:operation="remove"/></tcp></ipv6>'
)
IP6_TRAFFIC_FILTER_1612 = (
    "<ipv6><traffic-filter><direction>$direction</direction>"
    "<access-list>$acl</access-list></traffic-filter></ipv6>"
)
IP6_TRAFFIC_FILTER_REMOVE_1612 = (
    '<ipv6><traffic-filter nc:operation="remove">'
    '<direction>$direction</direction><access-list>$acl</access-list>'
    '</traffic-filter></ipv6>'
)
IP6_SOURCE_GUARD_1612 = (
    "<ipv6><source-guard>$policy_block</source-guard></ipv6>"
)
IP6_SOURCE_GUARD_REMOVE_1612 = '<ipv6><source-guard nc:operation="remove"/></ipv6>'
# IP6_VERIFY_UNICAST_REVERSE_PATH -> NOT PRESENT in 16.12 (no ipv6/verify)


# ============================================================
# 6. ACCESS-SESSION
# ============================================================

AS_PORT_CONTROL_1612 = (
    "<access-session><port-control-config>$pc</port-control-config></access-session>"
)
AS_PORT_CONTROL_REMOVE_1612 = (
    '<access-session><port-control-config nc:operation="remove"/></access-session>'
)
# 1612-ADAPTED: plain <control-direction><in/> container (17.15: control-direction-config).
# 'both' = node absent -> use *_REMOVE to go back to both. $dir = in
AS_CONTROL_DIRECTION_1612 = (
    "<access-session><control-direction><$dir/></control-direction></access-session>"
)
AS_CONTROL_DIRECTION_REMOVE_1612 = (
    '<access-session><control-direction nc:operation="remove"/></access-session>'
)
# 1612-ADAPTED: 17.3 uses leaf <host-mode> (multi-auth|multi-domain|multi-host|single-host),
#              not host-mode-config/modes.
AS_HOST_MODE_1612 = (
    "<access-session><host-mode>$hm</host-mode></access-session>"
)
AS_HOST_MODE_REMOVE_1612 = (
    '<access-session><host-mode nc:operation="remove"/></access-session>'
)
# AS_HOST_MODE_PEER -> NOT PRESENT in 16.12
AS_MONITOR_1612 = "<access-session><monitor>$flag</monitor></access-session>"


# ============================================================
# 7. STORM-CONTROL
# ============================================================

SC_ACTION_LEVEL_1612 = (
    "<storm-control><action><level>$pct</level></action></storm-control>"
)
SC_ACTION_SHUTDOWN_1612 = "<storm-control><action><shutdown/></action></storm-control>"
SC_ACTION_TRAP_1612     = "<storm-control><action><trap/></action></storm-control>"
SC_ACTION_REMOVE_1612   = '<storm-control><action nc:operation="remove"/></storm-control>'

# $sc_type: broadcast | multicast | unicast | unknown-unicast
SC_THRESHOLD_PERCENT_1612 = (
    "<storm-control><$sc_type><level><threshold>"
    "<rising-threshold>$rise</rising-threshold>"
    "<falling-threshold>$fall</falling-threshold>"
    "</threshold></level></$sc_type></storm-control>"
)
SC_THRESHOLD_REMOVE_1612 = (
    '<storm-control><$sc_type nc:operation="remove"/></storm-control>'
)
SC_BROADCAST_INCLUDE_MULTICAST_1612 = (
    "<storm-control><broadcast><include><multicast/></include></broadcast></storm-control>"
)
SC_BROADCAST_INCLUDE_MULTICAST_REMOVE_1612 = (
    '<storm-control><broadcast><include nc:operation="remove"/></broadcast></storm-control>'
)


# ============================================================
# 8. MACSEC  (Cisco-IOS-XE-switch, augments the interface directly - not switchport)
# ============================================================
# 1612-ADAPTED: nodes live in the $SW namespace, so each top node carries xmlns="$SW".
#   enable : empty leaf <macsec/>
#   option : <macsec-option><macsec>...  (replay-protection/window-size, network-link)
# Present on: Fast/Gig/2.5G/5G/AppGig/10G/25G/40G/100G Ethernet and Port-channel.

MSEC_ENABLE_1612 = '<macsec xmlns="$SW"/>'
MSEC_ENABLE_REMOVE_1612 = '<macsec xmlns="$SW" nc:operation="remove"/>'
MSEC_REPLAY_PROTECTION_1612 = (
    '<macsec-option xmlns="$SW"><macsec><replay-protection>'
    '<window-size>$window</window-size>'
    '</replay-protection></macsec></macsec-option>'
)
MSEC_REPLAY_PROTECTION_REMOVE_1612 = (
    '<macsec-option xmlns="$SW"><macsec><replay-protection nc:operation="remove"/></macsec></macsec-option>'
)


# ============================================================
# 9. MISC — SUBSCRIBER  -> NOT PRESENT in 16.12 catalogue
# ============================================================


# ============================================================
# 10. PHYSICAL LAYER
# ============================================================
# media-type : only on GigabitEthernet, TwoGigabitEthernet, FiveGigabitEthernet,
#              AppGigabitEthernet, TenGigabitEthernet, TwentyFiveGigE,
#              FortyGigabitEthernet (NOT HundredGigE)
# fec        : only on TwentyFiveGigE (auto|cl108|cl74|cl91|off)

PHY_MEDIA_TYPE_1612        = "<media-type>$media</media-type>"
PHY_MEDIA_TYPE_REMOVE_1612 = '<media-type nc:operation="remove"/>'
PHY_FEC_1612               = "<fec>$fec</fec>"
PHY_FEC_REMOVE_1612        = '<fec nc:operation="remove"/>'


# ============================================================
# 11. PORT-CHANNEL
# ============================================================
# PO_LOAD_BALANCE_HASH_ALGO -> NOT PRESENT in 16.12
#   (17.3 has a different leaf <load-balancing> = vlan|flow directly on list Port-channel)

PO_MIN_LINKS_1612 = (
    "<port-channel><min-links>$min_links</min-links></port-channel>"       # 2..8
)
PO_MIN_LINKS_REMOVE_1612 = (
    '<port-channel><min-links nc:operation="remove"/></port-channel>'
)
PO_STANDALONE_DISABLE_1612 = (
    "<port-channel><standalone-disable/></port-channel>"
)
PO_STANDALONE_DISABLE_REMOVE_1612 = (
    '<port-channel><standalone-disable nc:operation="remove"/></port-channel>'
)


# ============================================================
# 12. OTHER TYPE LEAVES
# ============================================================
# TYPE_VLAN_AUTOSTATE -> NOT PRESENT in 16.12 (list Vlan has no autostate leaf)

# list Tunnel only
TYPE_TUNNEL_QOS_PRE_CLASSIFY_1612 = "<qos><pre-classify/></qos>"
TYPE_TUNNEL_QOS_PRE_CLASSIFY_REMOVE_1612 = (
    '<qos><pre-classify nc:operation="remove"/></qos>'
)


# ============================================================
# 13. NVE / VXLAN   (list nve only)
# ============================================================

NVE_HOST_REACHABILITY_BGP_1612 = (
    "<host-reachability><protocol><bgp/></protocol></host-reachability>"
)
NVE_HOST_REACHABILITY_BGP_REMOVE_1612 = (
    '<host-reachability nc:operation="remove"/>'
)
# source-interface body comes from ios-ifc:interface-grouping (other module);
# container exists in 17.3, leaf names under it are not verifiable from this YANG.
NVE_SOURCE_INTERFACE_1612 = (
    "<source-interface><$src_type>$src_name</$src_type></source-interface>"
)
NVE_SOURCE_INTERFACE_REMOVE_1612 = '<source-interface nc:operation="remove"/>'
NVE_MEMBER_VNI_VRF_1612 = (
    "<member-in-one-line><member><vni>"
    "<vni-range>$vni</vni-range><vrf>$vrf</vrf>"
    "</vni></member></member-in-one-line>"
)
NVE_MEMBER_VNI_VRF_REMOVE_1612 = (
    '<member-in-one-line><member nc:operation="remove"><vni><vni-range>$vni</vni-range></vni></member></member-in-one-line>'
)
NVE_MEMBER_VNI_MCAST_GROUP_1612 = (
    "<member><vni><vni-range>$vni</vni-range><mcast-group>"
    "<multicast-group-min>$mc_min</multicast-group-min>"
    "$mc_max_block"
    "</mcast-group></vni></member>"
)
NVE_MEMBER_VNI_MCAST_GROUP_REMOVE_1612 = (
    '<member><vni nc:operation="remove"><vni-range>$vni</vni-range></vni></member>'
)


# ============================================================
# NOT PRESENT IN 16.12
# ============================================================
# base label -> reason. Families in the 1715 catalogue with no 16.12 equivalent.

_R_ARP = "arp snap/entries/packet-priority arrived with the 'arp model gaps' fix (interfaces rev 2019-11-01, 17.1+)"
_R_L2F = "l2protocol forward arrived in interfaces rev 2020-03-01 (17.3); not in 16.12"
_R_SUB = "subscriber aging/inactivity-timer is not in the 16.12 catalogue"
_R_ND  = "ipv6/nd children come from Cisco-IOS-XE-nd (not supplied); not in the 16.12 catalogue"

NOT_PRESENT_1612 = {
    "EXPORT_NAME":            "no export-name leaf in 16.12 (also absent in 17.3)",
    "EXPORT_NAME_REMOVE":     "no export-name leaf in 16.12 (also absent in 17.3)",

    "L2_PORTSEC_VIOLATION_SHUTDOWN_VLAN": "16.12 violation is a plain enum leaf; 'shutdown vlan' only exists in the newer port-security-conf model",

    "L2PT_FORWARD_PROTOCOL":        _R_L2F,
    "L2PT_FORWARD_PROTOCOL_REMOVE": _R_L2F,
    "L2PT_FORWARD_BLOCK":           _R_L2F,
    "L2PT_FORWARD_BLOCK_REMOVE":    _R_L2F,
    "L2PT_FORWARD_DROP":            _R_L2F,
    "L2PT_FORWARD_DROP_REMOVE":     _R_L2F,
    "L2PT_FORWARD_SHUTDOWN":        _R_L2F,
    "L2PT_FORWARD_SHUTDOWN_REMOVE": _R_L2F,

    "ARP_SNAP_TRUE":            _R_ARP,
    "ARP_SNAP_FALSE":           _R_ARP,
    "ARP_ENTRY_LIMIT":          _R_ARP,
    "ARP_ENTRY_LIMIT_REMOVE":   _R_ARP,
    "ARP_PACKET_PRIORITY":      _R_ARP,
    "ARP_PACKET_PRIORITY_REMOVE": _R_ARP,

    "SRLG":                   "no srlg container in 16.12",
    "SRLG_REMOVE":            "no srlg container in 16.12",

    "LINK_LOGGING_LINK_STATUS":        "link-status-enable not in 16.12 catalogue; use LINK_LOGGING_EVENT with event=link-status",
    "LINK_LOGGING_LINK_STATUS_REMOVE": "link-status-enable not in 16.12 catalogue; use LINK_LOGGING_EVENT_REMOVE with event=link-status",

    "IP4_CLEAR_DF":           "no ip/clear-dont-fragment leaf in 16.12",

    "IP6_ADDRESS_PREFIX_NAME":        "no ipv6/address/prefix-name in 16.12",
    "IP6_ADDRESS_PREFIX_NAME_REMOVE": "no ipv6/address/prefix-name in 16.12",
    "IP6_ND_DAD_ATTEMPTS":            _R_ND,
    "IP6_ND_DAD_ATTEMPTS_REMOVE":     _R_ND,
    "IP6_ND_NUD_IGP":                 _R_ND,
    "IP6_VERIFY_UNICAST_REVERSE_PATH":        "no ipv6/verify in 16.12",
    "IP6_VERIFY_UNICAST_REVERSE_PATH_REMOVE": "no ipv6/verify in 16.12",

    "AS_HOST_MODE_PEER":        "no peer option on access-session host-mode in 16.12",
    "AS_HOST_MODE_PEER_REMOVE": "no peer option on access-session host-mode in 16.12",

    "MISC_SUBSCRIBER_INACTIVITY":        _R_SUB,
    "MISC_SUBSCRIBER_INACTIVITY_REMOVE": _R_SUB,
    "MISC_SUBSCRIBER_PROBE":             _R_SUB,
    "MISC_SUBSCRIBER_PROBE_REMOVE":      _R_SUB,

    "PO_LOAD_BALANCE_HASH_ALGO":        "no load-balance-hash-algo in 16.12",
    "PO_LOAD_BALANCE_HASH_ALGO_REMOVE": "no load-balance-hash-algo in 16.12",

    "TYPE_VLAN_AUTOSTATE": "CONFIRMED: the 16.12 Cisco-IOS-XE-vlan Vlan-interface augment has no autostate leaf",
}

# ============================================================
# UNVERIFIED (present, but shape rests on inference — see header)
# ============================================================
# family -> why it is not backed by a supplied 16.12 YANG
_U_MSEC = ("switch-module revision history shows macsec added 2017-09 (before 16.12), so the leaf "
           "is inferred present; shape copied from the 17.3 switch module. Existing 1612 catalogue "
           "had it as absent.")
_U_L2PT = ("17.3 interfaces models this flat (<proto>$pps</proto>); the nested <packet-rate> form is "
           "the existing 1612 catalogue shape. Confirm against the 16.12 interfaces YANG.")
_U_PSEC = ("Matches the single <port-security> container that 17.3 marks deprecated; 16.12 switch "
           "module not supplied to confirm.")

UNVERIFIED_1612 = {
    "MSEC_ENABLE":                   _U_MSEC,
    "MSEC_ENABLE_REMOVE":            _U_MSEC,
    "MSEC_REPLAY_PROTECTION":        _U_MSEC,
    "MSEC_REPLAY_PROTECTION_REMOVE": _U_MSEC,
    "L2PT_DROP_THRESHOLD":              _U_L2PT,
    "L2PT_DROP_THRESHOLD_REMOVE":       _U_L2PT,
    "L2PT_DROP_THRESHOLD_RATE":         _U_L2PT,
    "L2PT_DROP_THRESHOLD_RATE_REMOVE":  _U_L2PT,
    "L2PT_SHUTDOWN_THRESHOLD":          _U_L2PT,
    "L2PT_SHUTDOWN_THRESHOLD_REMOVE":   _U_L2PT,
    "L2PT_SHUTDOWN_THRESHOLD_RATE":     _U_L2PT,
    "L2PT_SHUTDOWN_THRESHOLD_RATE_REMOVE": _U_L2PT,
    "L2_PORTSEC_ENABLE":            _U_PSEC,
    "L2_PORTSEC_ENABLE_REMOVE":     _U_PSEC,
    "L2_PORTSEC_MAX":               _U_PSEC,
    "L2_PORTSEC_MAX_REMOVE":        _U_PSEC,
    "L2_PORTSEC_MAX_VLAN":          _U_PSEC,
    "L2_PORTSEC_VIOLATION":         _U_PSEC,
    "L2_PORTSEC_VIOLATION_REMOVE":  _U_PSEC,
    "L2_PORTSEC_STICKY":            _U_PSEC,
    "L2_PORTSEC_STICKY_REMOVE":     _U_PSEC,
    "L2_PORTSEC_AGING":             _U_PSEC,
    "L2_PORTSEC_AGING_REMOVE":      _U_PSEC,
    "L2_PORTSEC_MAC_ACCESS":        _U_PSEC,
    "L2_PORTSEC_MAC_ACCESS_REMOVE": _U_PSEC,
    "L2_PORTSEC_MAC_STICKY":        _U_PSEC,
    "L2_PORTSEC_MAC_STICKY_REMOVE": _U_PSEC,
    "AS_CONTROL_DIRECTION":        "Matches the control-direction container 17.3 marks deprecated; 16.12 interfaces YANG not supplied.",
    "AS_CONTROL_DIRECTION_REMOVE": "Matches the control-direction container 17.3 marks deprecated; 16.12 interfaces YANG not supplied.",
}


# ================================================================
# PLACEHOLDER VALIDATION
# ================================================================

_ALLOWED = {
    # scaffolding
    "parent", "name",
    # text / labels
    "desc", "export", "mac",
    # timers / mtu
    "mtu", "delay", "seconds", "percent",
    # media / negotiation
    "flag",
    # service / qos
    "svc", "device",
    # voice / vlan
    "voice_vlan", "access_vlan", "vlans",
    "primary_vlan", "secondary_vlan", "secondary_vlans",
    "pvlan_type", "action", "vlan_kind",
    # port-security
        # port-security
    "max", "violation", "minutes", "aging_type", "hwaddr",
    # l2pt
    "proto", "p2p_proto", "pps", "core_block", "p2p_block", "proto_block",
    # arp / queues
    "secs", "count", "log_secs", "qid", "tid", "cos_values_block",
    "direction", "qlen", "rx", "tx", "kbps",
    # dampening / srlg / domain
    "half_life", "reuse", "suppress", "max_suppress",
    "srlg_values_block", "domain", "sp_path", "path_id",
    # keepalive
    "period", "retries",
    # logging
    "event", "events_block", "ignore_bulk_block",
    # ipv4
    "ip", "mask", "src_if", "acl", "common_acl", "vrf", "route_map",
    "helper", "via", "allow_block", "acl_block",
    "burst_block", "ip_mtu", "mss",
    "client_id_block", "hostname_block",
    # ipv6
    "ipv6", "ll", "pfx_name", "attempts", "ip6_mtu", "policy_block",
    # access-session
    "pc", "dir", "hm",
    # storm-control
    "pct", "sc_type", "rise", "fall",
    # macsec
    "window",
    # subscriber
    "probe_block",
    # phy / po
    "media", "fec", "algo", "min_links",
    # nve
    "src_type", "src_name", "vni", "mc_min", "mc_max_block",
    # namespace slots carried in templates
    "N", "NC", "SW", "ST", "VLAN",
}

_PLACEHOLDER_RE = re.compile(r"\$([A-Za-z_][A-Za-z0-9_]*)")


# ================================================================
# TEMPLATE REGISTRY  (base label -> {train: template})
# ================================================================
# Explicit dict — same style as 17.3/17.9/17.15. NOT_PRESENT families are
# registered by the trailing guard with a None slot so resolve() reports the
# reason instead of "unknown family".

_TRAINS = ("1612",)

def _t(**kw):
    """Expand a per-train dict to every train slot (None for missing)."""
    return {v: kw.get(v) for v in _TRAINS}


TEMPLATES = {
    # §1 general attributes
    "DESCRIPTION":                     _t(**{"1612": DESCRIPTION_1612}),
    "DESCRIPTION_REMOVE":              _t(**{"1612": DESCRIPTION_REMOVE_1612}),
    "MAC_ADDRESS":                     _t(**{"1612": MAC_ADDRESS_1612}),
    "MAC_ADDRESS_REMOVE":              _t(**{"1612": MAC_ADDRESS_REMOVE_1612}),
    "SHUTDOWN":                        _t(**{"1612": SHUTDOWN_1612}),
    "SHUTDOWN_REMOVE":                 _t(**{"1612": SHUTDOWN_REMOVE_1612}),
    "MTU":                             _t(**{"1612": MTU_1612}),
    "MTU_REMOVE":                      _t(**{"1612": MTU_REMOVE_1612}),
    "DELAY":                           _t(**{"1612": DELAY_1612}),
    "DELAY_REMOVE":                    _t(**{"1612": DELAY_REMOVE_1612}),
    "LOAD_INTERVAL":                   _t(**{"1612": LOAD_INTERVAL_1612}),
    "LOAD_INTERVAL_REMOVE":            _t(**{"1612": LOAD_INTERVAL_REMOVE_1612}),
    "MAX_BANDWIDTH":                   _t(**{"1612": MAX_BANDWIDTH_1612}),
    "MAX_BANDWIDTH_REMOVE":            _t(**{"1612": MAX_BANDWIDTH_REMOVE_1612}),
    "NEGOTIATION":                     _t(**{"1612": NEGOTIATION_1612}),
    "GEN_MDIX":                        _t(**{"1612": GEN_MDIX_1612}),
    "SERVICE_INSERTION":               _t(**{"1612": SERVICE_INSERTION_1612}),
    "SERVICE_INSERTION_REMOVE":        _t(**{"1612": SERVICE_INSERTION_REMOVE_1612}),
    "QOS_TRUST":                       _t(**{"1612": QOS_TRUST_1612}),
    "QOS_TRUST_REMOVE":                _t(**{"1612": QOS_TRUST_REMOVE_1612}),

    # §2 L2 switching
    "L2_SWITCHPORT_TRUE":              _t(**{"1612": L2_SWITCHPORT_TRUE_1612}),
    "L2_SWITCHPORT_FALSE":             _t(**{"1612": L2_SWITCHPORT_FALSE_1612}),
    "L2_DTP_DISABLE_TRUE":             _t(**{"1612": L2_DTP_DISABLE_TRUE_1612}),
    "L2_DTP_DISABLE_FALSE":            _t(**{"1612": L2_DTP_DISABLE_FALSE_1612}),
    "L2_VOICE_FULL":                   _t(**{"1612": L2_VOICE_FULL_1612}),
    "L2_VOICE_FULL_REMOVE":            _t(**{"1612": L2_VOICE_FULL_REMOVE_1612}),
    "L2_VOICE_VLAN_ID":                _t(**{"1612": L2_VOICE_VLAN_ID_1612}),
    "L2_VOICE_VLAN_DOT1P":             _t(**{"1612": L2_VOICE_VLAN_DOT1P_1612}),
    "L2_VOICE_VLAN_NONE":              _t(**{"1612": L2_VOICE_VLAN_NONE_1612}),
    "L2_VOICE_VLAN_UNTAGGED":          _t(**{"1612": L2_VOICE_VLAN_UNTAGGED_1612}),
    "L2_VOICE_VLAN_REMOVE":            _t(**{"1612": L2_VOICE_VLAN_REMOVE_1612}),
    "L2_VOICE_DETECT":                 _t(**{"1612": L2_VOICE_DETECT_1612}),
    "L2_VOICE_DETECT_REMOVE":          _t(**{"1612": L2_VOICE_DETECT_REMOVE_1612}),
    "L2_ACCESS_VLAN":                  _t(**{"1612": L2_ACCESS_VLAN_1612}),
    "L2_ACCESS_VLAN_REMOVE":           _t(**{"1612": L2_ACCESS_VLAN_REMOVE_1612}),
    "L2_TRUNK_PRUNING_ADD":            _t(**{"1612": L2_TRUNK_PRUNING_ADD_1612}),
    "L2_TRUNK_PRUNING_REMOVE":         _t(**{"1612": L2_TRUNK_PRUNING_REMOVE_1612}),
    "L2_TRUNK_PRUNING_REPLACE":        _t(**{"1612": L2_TRUNK_PRUNING_REPLACE_1612}),
    "L2_TRUNK_PRUNING_NONE":           _t(**{"1612": L2_TRUNK_PRUNING_NONE_1612}),
    "L2_TRUNK_PRUNING_REMOVE_ALL":     _t(**{"1612": L2_TRUNK_PRUNING_REMOVE_ALL_1612}),
    "PVLAN_GLOBAL":                    _t(**{"1612": PVLAN_GLOBAL_1612}),
    "PVLAN_GLOBAL_PRIMARY":            _t(**{"1612": PVLAN_GLOBAL_PRIMARY_1612}),
    "PVLAN_GLOBAL_ASSOC":              _t(**{"1612": PVLAN_GLOBAL_ASSOC_1612}),
    "PVLAN_GLOBAL_REMOVE":             _t(**{"1612": PVLAN_GLOBAL_REMOVE_1612}),
    "PVLAN_SECONDARY":                 _t(**{"1612": PVLAN_SECONDARY_1612}),
    "PVLAN_SECONDARY_REMOVE":          _t(**{"1612": PVLAN_SECONDARY_REMOVE_1612}),
    "PVLAN_HOST_ASSOC":                _t(**{"1612": PVLAN_HOST_ASSOC_1612}),
    "PVLAN_HOST_ASSOC_REMOVE":         _t(**{"1612": PVLAN_HOST_ASSOC_REMOVE_1612}),
    "PVLAN_PROMISCUOUS_MAP":           _t(**{"1612": PVLAN_PROMISCUOUS_MAP_1612}),
    "PVLAN_PROMISCUOUS_MAP_REMOVE":    _t(**{"1612": PVLAN_PROMISCUOUS_MAP_REMOVE_1612}),
    "L2_PORTSEC_ENABLE":               _t(**{"1612": L2_PORTSEC_ENABLE_1612}),
    "L2_PORTSEC_ENABLE_REMOVE":        _t(**{"1612": L2_PORTSEC_ENABLE_REMOVE_1612}),
    "L2_PORTSEC_MAX":                  _t(**{"1612": L2_PORTSEC_MAX_1612}),
    "L2_PORTSEC_MAX_VLAN":             _t(**{"1612": L2_PORTSEC_MAX_VLAN_1612}),
    "L2_PORTSEC_MAX_REMOVE":           _t(**{"1612": L2_PORTSEC_MAX_REMOVE_1612}),
    "L2_PORTSEC_VIOLATION":            _t(**{"1612": L2_PORTSEC_VIOLATION_1612}),
    "L2_PORTSEC_VIOLATION_REMOVE":     _t(**{"1612": L2_PORTSEC_VIOLATION_REMOVE_1612}),
    "L2_PORTSEC_STICKY":               _t(**{"1612": L2_PORTSEC_STICKY_1612}),
    "L2_PORTSEC_STICKY_REMOVE":        _t(**{"1612": L2_PORTSEC_STICKY_REMOVE_1612}),
    "L2_PORTSEC_AGING":                _t(**{"1612": L2_PORTSEC_AGING_1612}),
    "L2_PORTSEC_AGING_REMOVE":         _t(**{"1612": L2_PORTSEC_AGING_REMOVE_1612}),
    "L2_PORTSEC_MAC_ACCESS":           _t(**{"1612": L2_PORTSEC_MAC_ACCESS_1612}),
    "L2_PORTSEC_MAC_ACCESS_REMOVE":    _t(**{"1612": L2_PORTSEC_MAC_ACCESS_REMOVE_1612}),
    "L2_PORTSEC_MAC_STICKY":           _t(**{"1612": L2_PORTSEC_MAC_STICKY_1612}),
    "L2_PORTSEC_MAC_STICKY_REMOVE":    _t(**{"1612": L2_PORTSEC_MAC_STICKY_REMOVE_1612}),
    "L2_PROTECTED":                    _t(**{"1612": L2_PROTECTED_1612}),
    "L2_PROTECTED_REMOVE":             _t(**{"1612": L2_PROTECTED_REMOVE_1612}),
    "L2_HOST":                         _t(**{"1612": L2_HOST_1612}),
    "L2_HOST_REMOVE":                  _t(**{"1612": L2_HOST_REMOVE_1612}),
    "L2_BLOCK_MULTICAST":              _t(**{"1612": L2_BLOCK_MULTICAST_1612}),
    "L2_BLOCK_MULTICAST_REMOVE":       _t(**{"1612": L2_BLOCK_MULTICAST_REMOVE_1612}),
    "L2_BLOCK_UNICAST":                _t(**{"1612": L2_BLOCK_UNICAST_1612}),
    "L2_BLOCK_UNICAST_REMOVE":         _t(**{"1612": L2_BLOCK_UNICAST_REMOVE_1612}),
    "L2_VEPA":                         _t(**{"1612": L2_VEPA_1612}),
    "L2_VEPA_REMOVE":                  _t(**{"1612": L2_VEPA_REMOVE_1612}),
    "L2PT_TUNNEL_CORE":                _t(**{"1612": L2PT_TUNNEL_CORE_1612}),
    "L2PT_TUNNEL_CORE_REMOVE":         _t(**{"1612": L2PT_TUNNEL_CORE_REMOVE_1612}),
    "L2PT_TUNNEL_P2P":                 _t(**{"1612": L2PT_TUNNEL_P2P_1612}),
    "L2PT_TUNNEL_P2P_REMOVE":          _t(**{"1612": L2PT_TUNNEL_P2P_REMOVE_1612}),
    "L2PT_TUNNEL_CORE_BLOCK":          _t(**{"1612": L2PT_TUNNEL_CORE_BLOCK_1612}),
    "L2PT_TUNNEL_CORE_BLOCK_REMOVE":   _t(**{"1612": L2PT_TUNNEL_CORE_BLOCK_REMOVE_1612}),
    "L2PT_TUNNEL_P2P_BLOCK":           _t(**{"1612": L2PT_TUNNEL_P2P_BLOCK_1612}),
    "L2PT_TUNNEL_P2P_BLOCK_REMOVE":    _t(**{"1612": L2PT_TUNNEL_P2P_BLOCK_REMOVE_1612}),
    "L2PT_DROP_THRESHOLD":             _t(**{"1612": L2PT_DROP_THRESHOLD_1612}),
    "L2PT_DROP_THRESHOLD_REMOVE":      _t(**{"1612": L2PT_DROP_THRESHOLD_REMOVE_1612}),
    "L2PT_DROP_THRESHOLD_RATE":        _t(**{"1612": L2PT_DROP_THRESHOLD_RATE_1612}),
    "L2PT_DROP_THRESHOLD_RATE_REMOVE": _t(**{"1612": L2PT_DROP_THRESHOLD_RATE_REMOVE_1612}),
    "L2PT_DROP_THRESHOLD_P2P":         _t(**{"1612": L2PT_DROP_THRESHOLD_P2P_1612}),
    "L2PT_DROP_THRESHOLD_P2P_REMOVE":  _t(**{"1612": L2PT_DROP_THRESHOLD_P2P_REMOVE_1612}),
    "L2PT_SHUTDOWN_THRESHOLD":         _t(**{"1612": L2PT_SHUTDOWN_THRESHOLD_1612}),
    "L2PT_SHUTDOWN_THRESHOLD_REMOVE":  _t(**{"1612": L2PT_SHUTDOWN_THRESHOLD_REMOVE_1612}),
    "L2PT_SHUTDOWN_THRESHOLD_RATE":    _t(**{"1612": L2PT_SHUTDOWN_THRESHOLD_RATE_1612}),
    "L2PT_SHUTDOWN_THRESHOLD_RATE_REMOVE": _t(**{"1612": L2PT_SHUTDOWN_THRESHOLD_RATE_REMOVE_1612}),
    "L2PT_SHUTDOWN_THRESHOLD_P2P":     _t(**{"1612": L2PT_SHUTDOWN_THRESHOLD_P2P_1612}),
    "L2PT_SHUTDOWN_THRESHOLD_P2P_REMOVE": _t(**{"1612": L2PT_SHUTDOWN_THRESHOLD_P2P_REMOVE_1612}),

    # §3 ARP + link tuning
    "ARP_TIMEOUT":                     _t(**{"1612": ARP_TIMEOUT_1612}),
    "ARP_TIMEOUT_REMOVE":              _t(**{"1612": ARP_TIMEOUT_REMOVE_1612}),
    "PQ_OUT_ENABLE":                   _t(**{"1612": PQ_OUT_ENABLE_1612}),
    "PQ_OUT_ENABLE_REMOVE":            _t(**{"1612": PQ_OUT_ENABLE_REMOVE_1612}),
    "PQ_COS_MAP":                      _t(**{"1612": PQ_COS_MAP_1612}),
    "PQ_COS_MAP_REMOVE":               _t(**{"1612": PQ_COS_MAP_REMOVE_1612}),
    "RCV_QUEUE_COS_MAP":               _t(**{"1612": RCV_QUEUE_COS_MAP_1612}),
    "RCV_QUEUE_COS_MAP_REMOVE":        _t(**{"1612": RCV_QUEUE_COS_MAP_REMOVE_1612}),
    "FLOWCONTROL":                     _t(**{"1612": FLOWCONTROL_1612}),
    "FLOWCONTROL_REMOVE":              _t(**{"1612": FLOWCONTROL_REMOVE_1612}),
    "HOLD_QUEUE":                      _t(**{"1612": HOLD_QUEUE_1612}),
    "HOLD_QUEUE_REMOVE":               _t(**{"1612": HOLD_QUEUE_REMOVE_1612}),
    "LINK_BANDWIDTH":                  _t(**{"1612": LINK_BANDWIDTH_1612}),
    "LINK_BANDWIDTH_REMOVE":           _t(**{"1612": LINK_BANDWIDTH_REMOVE_1612}),
    "LINK_BANDWIDTH_QOS_REF":          _t(**{"1612": LINK_BANDWIDTH_QOS_REF_1612}),
    "LINK_BANDWIDTH_QOS_REF_REMOVE":   _t(**{"1612": LINK_BANDWIDTH_QOS_REF_REMOVE_1612}),
    "DAMPENING_FULL":                  _t(**{"1612": DAMPENING_FULL_1612}),
    "DAMPENING_DEFAULT":               _t(**{"1612": DAMPENING_DEFAULT_1612}),
    "DAMPENING_REMOVE":                _t(**{"1612": DAMPENING_REMOVE_1612}),
    "DOMAIN_NAME":                     _t(**{"1612": DOMAIN_NAME_1612}),
    "DOMAIN_NAME_REMOVE":              _t(**{"1612": DOMAIN_NAME_REMOVE_1612}),
    "DOMAIN_PATH":                     _t(**{"1612": DOMAIN_PATH_1612}),
    "DOMAIN_PATH_REMOVE":              _t(**{"1612": DOMAIN_PATH_REMOVE_1612}),
    "KEEPALIVE_TIMERS":                _t(**{"1612": KEEPALIVE_TIMERS_1612}),
    "KEEPALIVE_DISABLE":               _t(**{"1612": KEEPALIVE_DISABLE_1612}),
    "LINK_LOGGING_EVENT":              _t(**{"1612": LINK_LOGGING_EVENT_1612}),
    "LINK_LOGGING_EVENT_REMOVE":       _t(**{"1612": LINK_LOGGING_EVENT_REMOVE_1612}),
    "LINK_LOGGING_EVENTS_BLOCK":       _t(**{"1612": LINK_LOGGING_EVENTS_BLOCK_1612}),
    "LINK_LOGGING_EVENTS_BLOCK_REMOVE":_t(**{"1612": LINK_LOGGING_EVENTS_BLOCK_REMOVE_1612}),
    "LINK_LOGGING_SPANNING_TREE":      _t(**{"1612": LINK_LOGGING_SPANNING_TREE_1612}),
    "LINK_LOGGING_SPANNING_TREE_REMOVE": _t(**{"1612": LINK_LOGGING_SPANNING_TREE_REMOVE_1612}),
    "LINK_LOGGING_SUBIF":              _t(**{"1612": LINK_LOGGING_SUBIF_1612}),
    "LINK_LOGGING_SUBIF_REMOVE":       _t(**{"1612": LINK_LOGGING_SUBIF_REMOVE_1612}),
    "FAIR_QUEUE":                      _t(**{"1612": FAIR_QUEUE_1612}),
    "FAIR_QUEUE_REMOVE":               _t(**{"1612": FAIR_QUEUE_REMOVE_1612}),
    "FAIR_QUEUE_CONF":                 _t(**{"1612": FAIR_QUEUE_CONF_1612}),

    # §4 IPv4
    "IP4_PRIMARY":                     _t(**{"1612": IP4_PRIMARY_1612}),
    "IP4_PRIMARY_REMOVE":              _t(**{"1612": IP4_PRIMARY_REMOVE_1612}),
    "IP4_SECONDARY":                   _t(**{"1612": IP4_SECONDARY_1612}),
    "IP4_SECONDARY_REMOVE":            _t(**{"1612": IP4_SECONDARY_REMOVE_1612}),
    "IP4_DHCP":                        _t(**{"1612": IP4_DHCP_1612}),
    "IP4_DHCP_REMOVE":                 _t(**{"1612": IP4_DHCP_REMOVE_1612}),
    "IP4_NEGOTIATED":                  _t(**{"1612": IP4_NEGOTIATED_1612}),
    "IP4_NEGOTIATED_REMOVE":           _t(**{"1612": IP4_NEGOTIATED_REMOVE_1612}),
    "IP4_DHCP_OPTIONS":                _t(**{"1612": IP4_DHCP_OPTIONS_1612}),
    "IP4_UNNUMBERED":                  _t(**{"1612": IP4_UNNUMBERED_1612}),
    "IP4_UNNUMBERED_REMOVE":           _t(**{"1612": IP4_UNNUMBERED_REMOVE_1612}),
    "IP4_ACCESS_GROUP_IN":             _t(**{"1612": IP4_ACCESS_GROUP_IN_1612}),
    "IP4_ACCESS_GROUP_IN_REMOVE":      _t(**{"1612": IP4_ACCESS_GROUP_IN_REMOVE_1612}),
    "IP4_ACCESS_GROUP_OUT":            _t(**{"1612": IP4_ACCESS_GROUP_OUT_1612}),
    "IP4_ACCESS_GROUP_OUT_REMOVE":     _t(**{"1612": IP4_ACCESS_GROUP_OUT_REMOVE_1612}),
    "IP4_ACCESS_GROUP_COMMON_IN":      _t(**{"1612": IP4_ACCESS_GROUP_COMMON_IN_1612}),
    "IP4_ACCESS_GROUP_COMMON_IN_REMOVE": _t(**{"1612": IP4_ACCESS_GROUP_COMMON_IN_REMOVE_1612}),
    "IP4_ACCESS_GROUP_COMMON_OUT":     _t(**{"1612": IP4_ACCESS_GROUP_COMMON_OUT_1612}),
    "IP4_ACCESS_GROUP_COMMON_OUT_REMOVE": _t(**{"1612": IP4_ACCESS_GROUP_COMMON_OUT_REMOVE_1612}),
    "IP4_VRF_FORWARDING":              _t(**{"1612": IP4_VRF_FORWARDING_1612}),
    "IP4_VRF_FORWARDING_REMOVE":       _t(**{"1612": IP4_VRF_FORWARDING_REMOVE_1612}),
    "IP4_VRF_RECEIVE":                 _t(**{"1612": IP4_VRF_RECEIVE_1612}),
    "IP4_VRF_RECEIVE_REMOVE":          _t(**{"1612": IP4_VRF_RECEIVE_REMOVE_1612}),
    "IP4_VRF_SITEMAP":                 _t(**{"1612": IP4_VRF_SITEMAP_1612}),
    "IP4_VRF_SITEMAP_REMOVE":          _t(**{"1612": IP4_VRF_SITEMAP_REMOVE_1612}),
    "IP4_HELPER":                      _t(**{"1612": IP4_HELPER_1612}),
    "IP4_HELPER_REMOVE":               _t(**{"1612": IP4_HELPER_REMOVE_1612}),
    "IP4_HELPER_GLOBAL":               _t(**{"1612": IP4_HELPER_GLOBAL_1612}),
    "IP4_HELPER_GLOBAL_REMOVE":        _t(**{"1612": IP4_HELPER_GLOBAL_REMOVE_1612}),
    "IP4_HELPER_VRF":                  _t(**{"1612": IP4_HELPER_VRF_1612}),
    "IP4_HELPER_VRF_REMOVE":           _t(**{"1612": IP4_HELPER_VRF_REMOVE_1612}),
    "IP4_POLICY_ROUTE_MAP":            _t(**{"1612": IP4_POLICY_ROUTE_MAP_1612}),
    "IP4_POLICY_ROUTE_MAP_REMOVE":     _t(**{"1612": IP4_POLICY_ROUTE_MAP_REMOVE_1612}),
    "IP4_PROXY_ARP":                   _t(**{"1612": IP4_PROXY_ARP_1612}),
    "IP4_LOCAL_PROXY_ARP":             _t(**{"1612": IP4_LOCAL_PROXY_ARP_1612}),
    "IP4_LOCAL_PROXY_ARP_REMOVE":      _t(**{"1612": IP4_LOCAL_PROXY_ARP_REMOVE_1612}),
    "IP4_REDIRECTS":                   _t(**{"1612": IP4_REDIRECTS_1612}),
    "IP4_TCP_MSS":                     _t(**{"1612": IP4_TCP_MSS_1612}),
    "IP4_TCP_MSS_REMOVE":              _t(**{"1612": IP4_TCP_MSS_REMOVE_1612}),
    "IP4_MTU":                         _t(**{"1612": IP4_MTU_1612}),
    "IP4_MTU_REMOVE":                  _t(**{"1612": IP4_MTU_REMOVE_1612}),
    "IP4_URPF":                        _t(**{"1612": IP4_URPF_1612}),
    "IP4_URPF_REMOVE":                 _t(**{"1612": IP4_URPF_REMOVE_1612}),
    "IP4_ARP_INSPECT_TRUST":           _t(**{"1612": IP4_ARP_INSPECT_TRUST_1612}),
    "IP4_ARP_INSPECT_TRUST_REMOVE":    _t(**{"1612": IP4_ARP_INSPECT_TRUST_REMOVE_1612}),
    "IP4_ARP_INSPECT_RATE":            _t(**{"1612": IP4_ARP_INSPECT_RATE_1612}),
    "IP4_ARP_INSPECT_RATE_REMOVE":     _t(**{"1612": IP4_ARP_INSPECT_RATE_REMOVE_1612}),
    "IP4_ARP_INSPECT_RATE_NONE":       _t(**{"1612": IP4_ARP_INSPECT_RATE_NONE_1612}),
    "IP4_DIRECTED_BROADCAST":          _t(**{"1612": IP4_DIRECTED_BROADCAST_1612}),
    "IP4_DIRECTED_BROADCAST_REMOVE":   _t(**{"1612": IP4_DIRECTED_BROADCAST_REMOVE_1612}),
    "IP4_DIRECTED_BROADCAST_ACL":      _t(**{"1612": IP4_DIRECTED_BROADCAST_ACL_1612}),

    # §5 IPv6
    "IP6_ENABLE":                      _t(**{"1612": IP6_ENABLE_1612}),
    "IP6_ENABLE_REMOVE":               _t(**{"1612": IP6_ENABLE_REMOVE_1612}),
    "IP6_ADDRESS_PREFIX":              _t(**{"1612": IP6_ADDRESS_PREFIX_1612}),
    "IP6_ADDRESS_PREFIX_REMOVE":       _t(**{"1612": IP6_ADDRESS_PREFIX_REMOVE_1612}),
    "IP6_ADDRESS_EUI64":               _t(**{"1612": IP6_ADDRESS_EUI64_1612}),
    "IP6_ADDRESS_EUI64_REMOVE":        _t(**{"1612": IP6_ADDRESS_EUI64_REMOVE_1612}),
    "IP6_ADDRESS_ANYCAST":             _t(**{"1612": IP6_ADDRESS_ANYCAST_1612}),
    "IP6_ADDRESS_ANYCAST_REMOVE":      _t(**{"1612": IP6_ADDRESS_ANYCAST_REMOVE_1612}),
    "IP6_ADDRESS_LINK_LOCAL":          _t(**{"1612": IP6_ADDRESS_LINK_LOCAL_1612}),
    "IP6_ADDRESS_LINK_LOCAL_REMOVE":   _t(**{"1612": IP6_ADDRESS_LINK_LOCAL_REMOVE_1612}),
    "IP6_ADDRESS_AUTOCONFIG":          _t(**{"1612": IP6_ADDRESS_AUTOCONFIG_1612}),
    "IP6_ADDRESS_AUTOCONFIG_REMOVE":   _t(**{"1612": IP6_ADDRESS_AUTOCONFIG_REMOVE_1612}),
    "IP6_ADDRESS_AUTOCONFIG_DEFAULT":  _t(**{"1612": IP6_ADDRESS_AUTOCONFIG_DEFAULT_1612}),
    "IP6_ADDRESS_AUTOCONFIG_DEFAULT_REMOVE": _t(**{"1612": IP6_ADDRESS_AUTOCONFIG_DEFAULT_REMOVE_1612}),
    "IP6_ADDRESS_DHCP":                _t(**{"1612": IP6_ADDRESS_DHCP_1612}),
    "IP6_ADDRESS_DHCP_REMOVE":         _t(**{"1612": IP6_ADDRESS_DHCP_REMOVE_1612}),
    "IP6_ADDRESS_DHCP_RAPID_COMMIT":   _t(**{"1612": IP6_ADDRESS_DHCP_RAPID_COMMIT_1612}),
    "IP6_ADDRESS_DHCP_RAPID_COMMIT_REMOVE": _t(**{"1612": IP6_ADDRESS_DHCP_RAPID_COMMIT_REMOVE_1612}),
    "IP6_UNNUMBERED":                  _t(**{"1612": IP6_UNNUMBERED_1612}),
    "IP6_UNNUMBERED_REMOVE":           _t(**{"1612": IP6_UNNUMBERED_REMOVE_1612}),
    "IP6_MTU":                         _t(**{"1612": IP6_MTU_1612}),
    "IP6_MTU_REMOVE":                  _t(**{"1612": IP6_MTU_REMOVE_1612}),
    "IP6_TCP_ADJUST_MSS":              _t(**{"1612": IP6_TCP_ADJUST_MSS_1612}),
    "IP6_TCP_ADJUST_MSS_REMOVE":       _t(**{"1612": IP6_TCP_ADJUST_MSS_REMOVE_1612}),
    "IP6_TRAFFIC_FILTER":              _t(**{"1612": IP6_TRAFFIC_FILTER_1612}),
    "IP6_TRAFFIC_FILTER_REMOVE":       _t(**{"1612": IP6_TRAFFIC_FILTER_REMOVE_1612}),
    "IP6_SOURCE_GUARD":                _t(**{"1612": IP6_SOURCE_GUARD_1612}),
    "IP6_SOURCE_GUARD_REMOVE":         _t(**{"1612": IP6_SOURCE_GUARD_REMOVE_1612}),

    # §6 access-session
    "AS_PORT_CONTROL":                 _t(**{"1612": AS_PORT_CONTROL_1612}),
    "AS_PORT_CONTROL_REMOVE":          _t(**{"1612": AS_PORT_CONTROL_REMOVE_1612}),
    "AS_CONTROL_DIRECTION":            _t(**{"1612": AS_CONTROL_DIRECTION_1612}),
    "AS_CONTROL_DIRECTION_REMOVE":     _t(**{"1612": AS_CONTROL_DIRECTION_REMOVE_1612}),
    "AS_HOST_MODE":                    _t(**{"1612": AS_HOST_MODE_1612}),
    "AS_HOST_MODE_REMOVE":             _t(**{"1612": AS_HOST_MODE_REMOVE_1612}),
    "AS_MONITOR":                      _t(**{"1612": AS_MONITOR_1612}),

    # §7 storm-control
    "SC_ACTION_LEVEL":                 _t(**{"1612": SC_ACTION_LEVEL_1612}),
    "SC_ACTION_SHUTDOWN":              _t(**{"1612": SC_ACTION_SHUTDOWN_1612}),
    "SC_ACTION_TRAP":                  _t(**{"1612": SC_ACTION_TRAP_1612}),
    "SC_ACTION_REMOVE":                _t(**{"1612": SC_ACTION_REMOVE_1612}),
    "SC_THRESHOLD_PERCENT":            _t(**{"1612": SC_THRESHOLD_PERCENT_1612}),
    "SC_THRESHOLD_REMOVE":             _t(**{"1612": SC_THRESHOLD_REMOVE_1612}),
    "SC_BROADCAST_INCLUDE_MULTICAST":  _t(**{"1612": SC_BROADCAST_INCLUDE_MULTICAST_1612}),
    "SC_BROADCAST_INCLUDE_MULTICAST_REMOVE": _t(**{"1612": SC_BROADCAST_INCLUDE_MULTICAST_REMOVE_1612}),

    # §8 MACsec
    "MSEC_ENABLE":                     _t(**{"1612": MSEC_ENABLE_1612}),
    "MSEC_ENABLE_REMOVE":              _t(**{"1612": MSEC_ENABLE_REMOVE_1612}),
    "MSEC_REPLAY_PROTECTION":          _t(**{"1612": MSEC_REPLAY_PROTECTION_1612}),
    "MSEC_REPLAY_PROTECTION_REMOVE":   _t(**{"1612": MSEC_REPLAY_PROTECTION_REMOVE_1612}),

    # §10 physical layer
    "PHY_MEDIA_TYPE":                  _t(**{"1612": PHY_MEDIA_TYPE_1612}),
        "PHY_MEDIA_TYPE_REMOVE":           _t(**{"1612": PHY_MEDIA_TYPE_REMOVE_1612}),
    "PHY_FEC":                         _t(**{"1612": PHY_FEC_1612}),
    "PHY_FEC_REMOVE":                  _t(**{"1612": PHY_FEC_REMOVE_1612}),

    # §11 port-channel
    "PO_MIN_LINKS":                    _t(**{"1612": PO_MIN_LINKS_1612}),
    "PO_MIN_LINKS_REMOVE":             _t(**{"1612": PO_MIN_LINKS_REMOVE_1612}),
    "PO_STANDALONE_DISABLE":           _t(**{"1612": PO_STANDALONE_DISABLE_1612}),
    "PO_STANDALONE_DISABLE_REMOVE":    _t(**{"1612": PO_STANDALONE_DISABLE_REMOVE_1612}),

    # §12 other type leaves
    "TYPE_TUNNEL_QOS_PRE_CLASSIFY":    _t(**{"1612": TYPE_TUNNEL_QOS_PRE_CLASSIFY_1612}),
    "TYPE_TUNNEL_QOS_PRE_CLASSIFY_REMOVE": _t(**{"1612": TYPE_TUNNEL_QOS_PRE_CLASSIFY_REMOVE_1612}),

    # §13 NVE / VXLAN
    "NVE_HOST_REACHABILITY_BGP":        _t(**{"1612": NVE_HOST_REACHABILITY_BGP_1612}),
    "NVE_HOST_REACHABILITY_BGP_REMOVE": _t(**{"1612": NVE_HOST_REACHABILITY_BGP_REMOVE_1612}),
    "NVE_SOURCE_INTERFACE":             _t(**{"1612": NVE_SOURCE_INTERFACE_1612}),
    "NVE_SOURCE_INTERFACE_REMOVE":      _t(**{"1612": NVE_SOURCE_INTERFACE_REMOVE_1612}),
    "NVE_MEMBER_VNI_VRF":               _t(**{"1612": NVE_MEMBER_VNI_VRF_1612}),
    "NVE_MEMBER_VNI_VRF_REMOVE":        _t(**{"1612": NVE_MEMBER_VNI_VRF_REMOVE_1612}),
    "NVE_MEMBER_VNI_MCAST_GROUP":       _t(**{"1612": NVE_MEMBER_VNI_MCAST_GROUP_1612}),
    "NVE_MEMBER_VNI_MCAST_GROUP_REMOVE":_t(**{"1612": NVE_MEMBER_VNI_MCAST_GROUP_REMOVE_1612}),
}

import re
# Register NOT_PRESENT_1612 families with a None slot so resolve() reports the
# reason instead of "unknown family". Collision with an explicit entry is a
# programming error and must abort the import.
for _name in NOT_PRESENT_1612:
    if _name in TEMPLATES:
        raise ValueError(
            f"{_name} is both defined in TEMPLATES and listed in NOT_PRESENT_1612"
        )
    TEMPLATES[_name] = _t(**{"1612": None})


# ================================================================
# RESOLVERS
# ================================================================

def resolve(base, train="1612"):
    """Return the template for base/train. Raises with a clear message when missing."""
    if base not in TEMPLATES:
        raise KeyError(f"{base!r} not in 16.12 catalogue ({len(TEMPLATES)} families)")
    tpl = TEMPLATES[base].get(train)
    if tpl is None:
        reason = NOT_PRESENT_1612.get(base, "no template for this train")
        raise KeyError(f"{base!r} not available on train {train!r}: {reason}")
    return tpl


def families():
    """Yield every catalogue family name, sorted."""
    for name in sorted(TEMPLATES):
        yield name


def supported_on(train="1612"):
    """Yield every family available on the given train."""
    for name, slots in TEMPLATES.items():
        if slots.get(train) is not None:
            yield name


def not_present(train="1612"):
    """Yield (family, reason) for every family flagged not present on the train."""
    for name in sorted(NOT_PRESENT_1612):
        yield name, NOT_PRESENT_1612[name]


def unsupported_on(train="1612"):
    """Yield every family registered in the catalogue but absent on this train."""
    for name, slots in TEMPLATES.items():
        if slots.get(train) is None:
            yield name


def unverified(train="1612"):
    """Yield (family, note) for present families whose shape rests on inference."""
    for name in sorted(UNVERIFIED_1612):
        if TEMPLATES.get(name, {}).get(train) is not None:
            yield name, UNVERIFIED_1612[name]


def on_off_pairs(train="1612"):
    """Yield (on_base, off_base) for every family that has a _REMOVE twin."""
    for base in TEMPLATES:
        if base.endswith("_REMOVE"):
            continue
        twin = base + "_REMOVE"
        if twin in TEMPLATES and TEMPLATES[twin].get(train) is not None \
                and TEMPLATES[base].get(train) is not None:
            yield (base, twin)


def flag_symmetric(train="1612"):
    """Yield families whose template uses $flag — symmetric by construction."""
    for base, slots in TEMPLATES.items():
        tpl = slots.get(train)
        if tpl and "$flag" in tpl:
            yield base


# ================================================================
# STARTUP PLACEHOLDER VALIDATION
# ================================================================

def _validate_all():
    errors = []
    seen = set()
    for family, slots in TEMPLATES.items():
        for train, tpl in slots.items():
            if tpl is None or (family, train) in seen:
                continue
            seen.add((family, train))
            for ph in _PLACEHOLDER_RE.findall(tpl):
                if ph not in _ALLOWED:
                    errors.append(f"{family}[{train}] unknown placeholder ${ph}")
    if errors:
        raise ValueError(
            "interface_attrs_1612: placeholder validation failed:\n  "
            + "\n  ".join(errors)
        )

_validate_all()


# ================================================================
# RENDERING
# ================================================================
from string import Template as _Template

NS = {
    "N":    "http://cisco.com/ns/yang/Cisco-IOS-XE-native",
    "NC":   "urn:ietf:params:xml:ns:netconf:base:1.0",
    "SW":   "http://cisco.com/ns/yang/Cisco-IOS-XE-switch",
    "ST":   "http://cisco.com/ns/yang/Cisco-IOS-XE-spanning-tree",
    "VLAN": "http://cisco.com/ns/yang/Cisco-IOS-XE-vlan",
}

# bodies that sit directly under <native> (no interface scaffold)
NATIVE_SCOPED = frozenset(
    n for n in TEMPLATES if n.startswith(("PVLAN_GLOBAL", "PVLAN_SECONDARY"))
)


def render(base, train="1612", **kw):
    """Resolve base/train, fill namespaces + caller values, return the XML body.
    Raises KeyError naming any placeholder the caller did not supply."""
    tpl = resolve(base, train)
    try:
        return _Template(tpl).substitute({**NS, **kw})
    except KeyError as e:
        raise KeyError(f"{base}: missing value for placeholder ${e.args[0]}") from None


def wrap_native(*bodies):
    """<native> root. Use directly for NATIVE_SCOPED families (PVLAN_GLOBAL*, PVLAN_SECONDARY*)."""
    return f'<native xmlns="{NS["N"]}" xmlns:nc="{NS["NC"]}">{"".join(bodies)}</native>'


def wrap_interface(parent, name, *bodies):
    """<native><interface><TYPE><name>..bodies..</TYPE></interface></native>.
    parent is the list name ('GigabitEthernet') or a nested path for subinterfaces
    ('Port-channel-subinterface/Port-channel')."""
    parts = [p for p in parent.split("/") if p]
    if not parts:
        raise ValueError("parent is required")
    opening = "".join(f"<{p}>" for p in parts)
    closing = "".join(f"</{p}>" for p in reversed(parts))
    return wrap_native(f'<interface>{opening}<name>{name}</name>{"".join(bodies)}{closing}</interface>')


def build_config(base, parent=None, name=None, train="1612", **kw):
    """Complete NETCONF <config> payload for one family; picks the right scaffold automatically."""
    body = render(base, train, **kw)
    if base in NATIVE_SCOPED:
        inner = wrap_native(body)
    else:
        if not parent or name is None:
            raise ValueError(f"{base} is interface-scoped: parent and name are required")
        inner = wrap_interface(parent, name, body)
    return f'<config xmlns="{NS["NC"]}">{inner}</config>'


def _selftest():
    """Render every 16.12 template with dummy values and parse as XML."""
    import xml.etree.ElementTree as ET

    class _Dummy(dict):
        def __missing__(self, key):
            return "x"

    bad = []
    supported = list(supported_on("1612"))
    for name in supported:
        tpl = resolve(name)
        kw = {ph: "x" for ph in _PLACEHOLDER_RE.findall(tpl) if ph not in NS}
        xml = render(name, **kw)
        try:
            ET.fromstring('<r xmlns:nc="%s">%s</r>' % (NS["NC"], xml))
        except ET.ParseError as e:
            bad.append((name, str(e)))
    n_ok = len(supported) - len(bad)
    print(f"1612 selftest: {n_ok} templates OK, {len(bad)} malformed, "
          f"{len(NOT_PRESENT_1612)} flagged not present, "
          f"{sum(1 for _ in unverified())} present-but-unverified")
    for b in bad:
        print("  BAD", b)
    return not bad


if __name__ == "__main__":
    raise SystemExit(0 if _selftest() else 1)