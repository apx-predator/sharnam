# interface_attrs_1715.py
# Modular interface XML bodies for Cisco-IOS-XE-native (IOS XE 17.15).
# Same conventions as interface_attrs_179.py. Suffix: _1715.
#
# Interface scaffolding is added by wrap_interface()/build_config(); bodies here are bare.

import re
from string import Template as _Template

# $N    = http://cisco.com/ns/yang/Cisco-IOS-XE-native
# $NC   = urn:ietf:params:xml:ns:netconf:base:1.0
# $SW   = http://cisco.com/ns/yang/Cisco-IOS-XE-switch
# $ST   = http://cisco.com/ns/yang/Cisco-IOS-XE-spanning-tree
# $VLAN = http://cisco.com/ns/yang/Cisco-IOS-XE-vlan


# ============================================================
# 1. GENERAL ATTRIBUTES
# ============================================================
DESCRIPTION_1715          = "<description>$desc</description>"
DESCRIPTION_REMOVE_1715   = '<description nc:operation="remove"/>'
EXPORT_NAME_1715          = "<export-name>$export</export-name>"
EXPORT_NAME_REMOVE_1715   = '<export-name nc:operation="remove"/>'
MAC_ADDRESS_1715          = "<mac-address>$mac</mac-address>"
MAC_ADDRESS_REMOVE_1715   = '<mac-address nc:operation="remove"/>'

SHUTDOWN_1715             = "<shutdown/>"
SHUTDOWN_REMOVE_1715      = '<shutdown nc:operation="remove"/>'

MTU_1715                  = "<mtu>$mtu</mtu>"
MTU_REMOVE_1715           = '<mtu nc:operation="remove"/>'
DELAY_1715                = "<delay>$delay</delay>"
DELAY_REMOVE_1715         = '<delay nc:operation="remove"/>'
LOAD_INTERVAL_1715        = "<load-interval>$seconds</load-interval>"
LOAD_INTERVAL_REMOVE_1715 = '<load-interval nc:operation="remove"/>'
MAX_BANDWIDTH_1715        = "<max-reserved-bandwidth>$percent</max-reserved-bandwidth>"
MAX_BANDWIDTH_REMOVE_1715 = '<max-reserved-bandwidth nc:operation="remove"/>'

NEGOTIATION_1715          = "<negotiation><auto>$flag</auto></negotiation>"
GEN_MDIX_1715             = "<mdix><auto>$flag</auto></mdix>"
NEGOTIATION_FULL_1715     = "<negotiation>$auto_block</negotiation>$speed_block$duplex_block"
GEN_MDIX_FULL_1715        = "<mdix>$auto_block$mode_block</mdix>"

SERVICE_INSERTION_1715        = "<service-insertion>$svc</service-insertion>"
SERVICE_INSERTION_REMOVE_1715 = '<service-insertion nc:operation="remove"/>'
QOS_TRUST_1715                = '<interface_qos><trust><device>$device</device></trust></interface_qos>'
QOS_TRUST_REMOVE_1715         = '<interface_qos nc:operation="remove"/>'


# ============================================================
# 2. L2 SWITCHING
# ============================================================
L2_SWITCHPORT_TRUE_1715  = "<switchport-conf><switchport>true</switchport></switchport-conf>"
L2_SWITCHPORT_FALSE_1715 = "<switchport-conf><switchport>false</switchport></switchport-conf>"

L2_DTP_DISABLE_TRUE_1715 = (
    '<switchport-config><switchport><nonegotiate xmlns="$SW"/></switchport></switchport-config>'
)
L2_DTP_DISABLE_FALSE_1715 = (
    '<switchport-config><switchport><nonegotiate xmlns="$SW" nc:operation="remove"/></switchport></switchport-config>'
)

L2_VOICE_FULL_1715 = (
    '<switchport-config><switchport>'
    '<voice xmlns="$SW">'
      '<vlan><vlan>$voice_vlan</vlan></vlan>'
      '<detect><cisco-phone><full-duplex/></cisco-phone></detect>'
    '</voice>'
    '<access xmlns="$SW"><vlan><vlan>$access_vlan</vlan></vlan></access>'
    '</switchport></switchport-config>'
)
L2_VOICE_FULL_REMOVE_1715 = (
    '<switchport-config><switchport>'
    '<voice xmlns="$SW" nc:operation="remove"/>'
    '<access xmlns="$SW" nc:operation="remove"/>'
    '</switchport></switchport-config>'
)
L2_VOICE_VLAN_ID_1715 = (
    '<switchport-config><switchport>'
    '<voice xmlns="$SW"><vlan><vlan>$voice_vlan</vlan></vlan></voice>'
    '</switchport></switchport-config>'
)
L2_VOICE_VLAN_DOT1P_1715 = (
    '<switchport-config><switchport>'
    '<voice xmlns="$SW"><vlan><vlan>dot1p</vlan></vlan></voice>'
    '</switchport></switchport-config>'
)
L2_VOICE_VLAN_NONE_1715 = (
    '<switchport-config><switchport>'
    '<voice xmlns="$SW"><vlan><vlan>none</vlan></vlan></voice>'
    '</switchport></switchport-config>'
)
L2_VOICE_VLAN_UNTAGGED_1715 = (
    '<switchport-config><switchport>'
    '<voice xmlns="$SW"><vlan><vlan>untagged</vlan></vlan></voice>'
    '</switchport></switchport-config>'
)
L2_VOICE_VLAN_REMOVE_1715 = (
    '<switchport-config><switchport>'
    '<voice xmlns="$SW"><vlan nc:operation="remove"/></voice>'
    '</switchport></switchport-config>'
)
L2_VOICE_DETECT_1715 = (
    '<switchport-config><switchport>'
    '<voice xmlns="$SW"><detect><cisco-phone><full-duplex/></cisco-phone></detect></voice>'
    '</switchport></switchport-config>'
)
L2_VOICE_DETECT_REMOVE_1715 = (
    '<switchport-config><switchport>'
    '<voice xmlns="$SW"><detect nc:operation="remove"/></voice>'
    '</switchport></switchport-config>'
)
L2_ACCESS_VLAN_1715 = (
    '<switchport-config><switchport>'
    '<access xmlns="$SW"><vlan><vlan>$access_vlan</vlan></vlan></access>'
    '</switchport></switchport-config>'
)
L2_ACCESS_VLAN_REMOVE_1715 = (
    '<switchport-config><switchport>'
    '<access xmlns="$SW"><vlan nc:operation="remove"/></access>'
    '</switchport></switchport-config>'
)

L2_TRUNK_PRUNING_ADD_1715 = (
    '<switchport-config><switchport>'
    '<trunk xmlns="$SW"><pruning><vlan><add>$vlans</add></vlan></pruning></trunk>'
    '</switchport></switchport-config>'
)
L2_TRUNK_PRUNING_REMOVE_1715 = (
    '<switchport-config><switchport>'
    '<trunk xmlns="$SW"><pruning><vlan><remove>$vlans</remove></vlan></pruning></trunk>'
    '</switchport></switchport-config>'
)
L2_TRUNK_PRUNING_REPLACE_1715 = (
    '<switchport-config><switchport>'
    '<trunk xmlns="$SW"><pruning><vlan><vlans nc:operation="replace">$vlans</vlans></vlan></pruning></trunk>'
    '</switchport></switchport-config>'
)
L2_TRUNK_PRUNING_NONE_1715 = (
    '<switchport-config><switchport>'
    '<trunk xmlns="$SW"><pruning><vlan><none/></vlan></pruning></trunk>'
    '</switchport></switchport-config>'
)
L2_TRUNK_PRUNING_REMOVE_ALL_1715 = (
    '<switchport-config><switchport>'
    '<trunk xmlns="$SW"><pruning nc:operation="remove"/></trunk>'
    '</switchport></switchport-config>'
)

PVLAN_HOST_ASSOC_1715 = (
    '<switchport-config><switchport>'
      '<mode xmlns="$SW"><private-vlan><host/></private-vlan></mode>'
      '<private-vlan xmlns="$SW"><host-association>'
        '<primary-range>$primary_vlan</primary-range>'
        '<secondary-range>$secondary_vlan</secondary-range>'
      '</host-association></private-vlan>'
    '</switchport></switchport-config>'
)
PVLAN_HOST_ASSOC_REMOVE_1715 = (
    '<switchport-config><switchport>'
      '<private-vlan xmlns="$SW"><host-association nc:operation="remove"/></private-vlan>'
    '</switchport></switchport-config>'
)
PVLAN_PROMISCUOUS_MAP_1715 = (
    '<switchport-config><switchport>'
      '<mode xmlns="$SW"><private-vlan><promiscuous/></private-vlan></mode>'
      '<private-vlan xmlns="$SW"><mapping>'
        '<primary-range>$primary_vlan</primary-range>'
        '<secondary-range>$secondary_vlans</secondary-range>'
      '</mapping></private-vlan>'
    '</switchport></switchport-config>'
)
PVLAN_PROMISCUOUS_MAP_REMOVE_1715 = (
    '<switchport-config><switchport>'
      '<private-vlan xmlns="$SW"><mapping nc:operation="remove"/></private-vlan>'
    '</switchport></switchport-config>'
)

PVLAN_GLOBAL_1715 = (
    '<vlan xmlns="$N"><vlan-list xmlns="$VLAN">'
      '<id>$primary_vlan</id>'
      '<private-vlan><primary/><association>$secondary_vlans</association></private-vlan>'
    '</vlan-list></vlan>'
)
PVLAN_GLOBAL_PRIMARY_1715 = (
    '<vlan xmlns="$N"><vlan-list xmlns="$VLAN">'
      '<id>$primary_vlan</id><private-vlan><primary/></private-vlan>'
    '</vlan-list></vlan>'
)
PVLAN_GLOBAL_ASSOC_1715 = (
    '<vlan xmlns="$N"><vlan-list xmlns="$VLAN">'
      '<id>$primary_vlan</id><private-vlan><association>$secondary_vlans</association></private-vlan>'
    '</vlan-list></vlan>'
)
PVLAN_GLOBAL_REMOVE_1715 = (
    '<vlan xmlns="$N"><vlan-list xmlns="$VLAN">'
      '<id>$primary_vlan</id><private-vlan nc:operation="remove"/>'
    '</vlan-list></vlan>'
)
PVLAN_SECONDARY_1715 = (
    '<vlan xmlns="$N"><vlan-list xmlns="$VLAN">'
      '<id>$secondary_vlan</id><private-vlan><$pvlan_type/></private-vlan>'
    '</vlan-list></vlan>'
)
PVLAN_SECONDARY_REMOVE_1715 = (
    '<vlan xmlns="$N"><vlan-list xmlns="$VLAN" nc:operation="remove"><id>$secondary_vlan</id></vlan-list></vlan>'
)

L2_PORTSEC_ENABLE_1715 = (
    '<switchport-config><switchport><port-security-conf xmlns="$SW"/></switchport></switchport-config>'
)
L2_PORTSEC_ENABLE_REMOVE_1715 = (
    '<switchport-config><switchport><port-security-conf xmlns="$SW" nc:operation="remove"/></switchport></switchport-config>'
)
L2_PORTSEC_MAX_1715 = (
    '<switchport-config><switchport><port-security-config xmlns="$SW"><port-security>'
      '<maximum-address-config><maximum><maximum>$max</maximum></maximum></maximum-address-config>'
    '</port-security></port-security-config></switchport></switchport-config>'
)
L2_PORTSEC_MAX_VLAN_1715 = (
    '<switchport-config><switchport><port-security-config xmlns="$SW"><port-security>'
      '<maximum-address-config><maximum><maximum>$max</maximum><vlan>$vlan_kind</vlan></maximum></maximum-address-config>'
    '</port-security></port-security-config></switchport></switchport-config>'
)
L2_PORTSEC_MAX_REMOVE_1715 = (
    '<switchport-config><switchport><port-security-config xmlns="$SW"><port-security>'
      '<maximum-address-config nc:operation="remove"/>'
    '</port-security></port-security-config></switchport></switchport-config>'
)
L2_PORTSEC_VIOLATION_1715 = (
    '<switchport-config><switchport><port-security-config xmlns="$SW"><port-security>'
      '<violation><$violation/></violation>'
    '</port-security></port-security-config></switchport></switchport-config>'
)
L2_PORTSEC_VIOLATION_SHUTDOWN_VLAN_1715 = (
    '<switchport-config><switchport><port-security-config xmlns="$SW"><port-security>'
      '<violation><shutdown><vlan/></shutdown></violation>'
    '</port-security></port-security-config></switchport></switchport-config>'
)
L2_PORTSEC_VIOLATION_REMOVE_1715 = (
    '<switchport-config><switchport><port-security-config xmlns="$SW"><port-security>'
      '<violation nc:operation="remove"/>'
    '</port-security></port-security-config></switchport></switchport-config>'
)
L2_PORTSEC_STICKY_1715 = (
    '<switchport-config><switchport><port-security-config xmlns="$SW"><port-security>'
      '<mac-address-sticky-on><mac-address><sticky/></mac-address></mac-address-sticky-on>'
    '</port-security></port-security-config></switchport></switchport-config>'
)
L2_PORTSEC_STICKY_REMOVE_1715 = (
    '<switchport-config><switchport><port-security-config xmlns="$SW"><port-security>'
      '<mac-address-sticky-on nc:operation="remove"/>'
    '</port-security></port-security-config></switchport></switchport-config>'
)
L2_PORTSEC_AGING_1715 = (
    '<switchport-config><switchport><port-security-config xmlns="$SW"><port-security>'
      '<aging><time>$minutes</time><type>$aging_type</type></aging>'
    '</port-security></port-security-config></switchport></switchport-config>'
)
L2_PORTSEC_AGING_REMOVE_1715 = (
    '<switchport-config><switchport><port-security-config xmlns="$SW"><port-security>'
      '<aging nc:operation="remove"/>'
    '</port-security></port-security-config></switchport></switchport-config>'
)
L2_PORTSEC_MAC_ACCESS_1715 = (
    '<switchport-config><switchport><port-security-config xmlns="$SW"><port-security>'
      '<mac-address-config><mac-address>'
        '<hw-address-access><hw-address>$hwaddr</hw-address></hw-address-access>'
      '</mac-address></mac-address-config>'
    '</port-security></port-security-config></switchport></switchport-config>'
)
L2_PORTSEC_MAC_ACCESS_REMOVE_1715 = (
    '<switchport-config><switchport><port-security-config xmlns="$SW"><port-security>'
      '<mac-address-config><mac-address>'
        '<hw-address-access nc:operation="remove"><hw-address>$hwaddr</hw-address></hw-address-access>'
      '</mac-address></mac-address-config>'
    '</port-security></port-security-config></switchport></switchport-config>'
)
L2_PORTSEC_MAC_STICKY_1715 = (
    '<switchport-config><switchport><port-security-config xmlns="$SW"><port-security>'
      '<mac-address-config><mac-address>'
        '<hw-address-sticky><hw-address>$hwaddr</hw-address></hw-address-sticky>'
      '</mac-address></mac-address-config>'
    '</port-security></port-security-config></switchport></switchport-config>'
)
L2_PORTSEC_MAC_STICKY_REMOVE_1715 = (
    '<switchport-config><switchport><port-security-config xmlns="$SW"><port-security>'
      '<mac-address-config><mac-address>'
        '<hw-address-sticky nc:operation="remove"><hw-address>$hwaddr</hw-address></hw-address-sticky>'
      '</mac-address></mac-address-config>'
    '</port-security></port-security-config></switchport></switchport-config>'
)

L2_PROTECTED_1715 = (
    '<switchport-config><switchport><protected xmlns="$SW"/></switchport></switchport-config>'
)
L2_PROTECTED_REMOVE_1715 = (
    '<switchport-config><switchport><protected xmlns="$SW" nc:operation="remove"/></switchport></switchport-config>'
)
L2_HOST_1715 = (
    '<switchport-config><switchport><host xmlns="$SW"/></switchport></switchport-config>'
)
L2_HOST_REMOVE_1715 = (
    '<switchport-config><switchport><host xmlns="$SW" nc:operation="remove"/></switchport></switchport-config>'
)
L2_BLOCK_MULTICAST_1715 = (
    '<switchport-config><switchport><block xmlns="$SW"><multicast/></block></switchport></switchport-config>'
)
L2_BLOCK_MULTICAST_REMOVE_1715 = (
    '<switchport-config><switchport><block xmlns="$SW"><multicast nc:operation="remove"/></block></switchport></switchport-config>'
)
L2_BLOCK_UNICAST_1715 = (
    '<switchport-config><switchport><block xmlns="$SW"><unicast/></block></switchport></switchport-config>'
)
L2_BLOCK_UNICAST_REMOVE_1715 = (
    '<switchport-config><switchport><block xmlns="$SW"><unicast nc:operation="remove"/></block></switchport></switchport-config>'
)
L2_VEPA_1715 = (
    '<switchport-config><switchport><vepa xmlns="$SW"><enabled/></vepa></switchport></switchport-config>'
)
L2_VEPA_REMOVE_1715 = (
    '<switchport-config><switchport><vepa xmlns="$SW"><enabled nc:operation="remove"/></vepa></switchport></switchport-config>'
)

L2PT_TUNNEL_CORE_1715            = '<l2protocol-tunnel><$proto/></l2protocol-tunnel>'
L2PT_TUNNEL_CORE_REMOVE_1715     = '<l2protocol-tunnel><$proto nc:operation="remove"/></l2protocol-tunnel>'
L2PT_TUNNEL_P2P_1715             = '<l2protocol-tunnel><point-to-point><$p2p_proto/></point-to-point></l2protocol-tunnel>'
L2PT_TUNNEL_P2P_REMOVE_1715      = '<l2protocol-tunnel><point-to-point><$p2p_proto nc:operation="remove"/></point-to-point></l2protocol-tunnel>'
L2PT_TUNNEL_CORE_BLOCK_1715      = '<l2protocol-tunnel>$core_block</l2protocol-tunnel>'
L2PT_TUNNEL_CORE_BLOCK_REMOVE_1715 = '<l2protocol-tunnel nc:operation="remove"/>'
L2PT_TUNNEL_P2P_BLOCK_1715       = '<l2protocol-tunnel><point-to-point>$p2p_block</point-to-point></l2protocol-tunnel>'
L2PT_TUNNEL_P2P_BLOCK_REMOVE_1715 = '<l2protocol-tunnel><point-to-point nc:operation="remove"/></l2protocol-tunnel>'

L2PT_DROP_THRESHOLD_1715 = (
    '<l2protocol-tunnel><drop-threshold>'
      '<$proto><packet-rate>$pps</packet-rate></$proto>'
    '</drop-threshold></l2protocol-tunnel>'
)
L2PT_DROP_THRESHOLD_REMOVE_1715 = (
    '<l2protocol-tunnel><drop-threshold><$proto nc:operation="remove"/></drop-threshold></l2protocol-tunnel>'
)
L2PT_DROP_THRESHOLD_RATE_1715 = (
    '<l2protocol-tunnel><drop-threshold><packet-rate>$pps</packet-rate></drop-threshold></l2protocol-tunnel>'
)
L2PT_DROP_THRESHOLD_RATE_REMOVE_1715 = (
    '<l2protocol-tunnel><drop-threshold><packet-rate nc:operation="remove"/></drop-threshold></l2protocol-tunnel>'
)
L2PT_DROP_THRESHOLD_P2P_1715 = (
    '<l2protocol-tunnel><drop-threshold><point-to-point>'
      '<$p2p_proto><packet-rate>$pps</packet-rate></$p2p_proto>'
    '</point-to-point></drop-threshold></l2protocol-tunnel>'
)
L2PT_DROP_THRESHOLD_P2P_REMOVE_1715 = (
    '<l2protocol-tunnel><drop-threshold><point-to-point><$p2p_proto nc:operation="remove"/>'
    '</point-to-point></drop-threshold></l2protocol-tunnel>'
)
L2PT_SHUTDOWN_THRESHOLD_1715 = (
    '<l2protocol-tunnel><shutdown-threshold>'
      '<$proto><packet-rate>$pps</packet-rate></$proto>'
    '</shutdown-threshold></l2protocol-tunnel>'
)
L2PT_SHUTDOWN_THRESHOLD_REMOVE_1715 = (
    '<l2protocol-tunnel><shutdown-threshold><$proto nc:operation="remove"/></shutdown-threshold></l2protocol-tunnel>'
)
L2PT_SHUTDOWN_THRESHOLD_RATE_1715 = (
    '<l2protocol-tunnel><shutdown-threshold><packet-rate>$pps</packet-rate></shutdown-threshold></l2protocol-tunnel>'
)
L2PT_SHUTDOWN_THRESHOLD_RATE_REMOVE_1715 = (
    '<l2protocol-tunnel><shutdown-threshold><packet-rate nc:operation="remove"/></shutdown-threshold></l2protocol-tunnel>'
)
L2PT_SHUTDOWN_THRESHOLD_P2P_1715 = (
    '<l2protocol-tunnel><shutdown-threshold><point-to-point>'
      '<$p2p_proto><packet-rate>$pps</packet-rate></$p2p_proto>'
    '</point-to-point></shutdown-threshold></l2protocol-tunnel>'
)
L2PT_SHUTDOWN_THRESHOLD_P2P_REMOVE_1715 = (
    '<l2protocol-tunnel><shutdown-threshold><point-to-point><$p2p_proto nc:operation="remove"/>'
    '</point-to-point></shutdown-threshold></l2protocol-tunnel>'
)

L2PT_FORWARD_PROTOCOL_1715        = '<l2protocol><forward><protocols>$proto</protocols></forward></l2protocol>'
L2PT_FORWARD_PROTOCOL_REMOVE_1715 = '<l2protocol><forward><protocols nc:operation="remove">$proto</protocols></forward></l2protocol>'
L2PT_FORWARD_BLOCK_1715           = '<l2protocol><forward>$proto_block</forward></l2protocol>'
L2PT_FORWARD_BLOCK_REMOVE_1715    = '<l2protocol><forward nc:operation="remove"/></l2protocol>'
L2PT_FORWARD_DROP_1715 = (
    '<l2protocol><forward><drop-threshold><threshold-list>'
    '<proto-type>$proto</proto-type><pps-num>$pps</pps-num>'
    '</threshold-list></drop-threshold></forward></l2protocol>'
)
L2PT_FORWARD_DROP_REMOVE_1715 = '<l2protocol><forward><drop-threshold nc:operation="remove"/></forward></l2protocol>'
L2PT_FORWARD_SHUTDOWN_1715 = (
    '<l2protocol><forward><shutdown-threshold><threshold-list>'
    '<proto-type>$proto</proto-type><pps-num>$pps</pps-num>'
    '</threshold-list></shutdown-threshold></forward></l2protocol>'
)
L2PT_FORWARD_SHUTDOWN_REMOVE_1715 = '<l2protocol><forward><shutdown-threshold nc:operation="remove"/></forward></l2protocol>'


# ============================================================
# 3. ARP + LINK TUNING
# ============================================================
ARP_TIMEOUT_1715         = "<arp><timeout>$secs</timeout></arp>"
ARP_TIMEOUT_REMOVE_1715  = '<arp><timeout nc:operation="remove"/></arp>'
ARP_SNAP_TRUE_1715       = "<arp><snap/></arp>"
ARP_SNAP_FALSE_1715      = '<arp><snap nc:operation="remove"/></arp>'
ARP_ENTRY_LIMIT_1715 = (
    "<arp><entries><interface-limit>"
    "<entry-count>$count</entry-count><log>$log_secs</log>"
    "</interface-limit></entries></arp>"
)
ARP_ENTRY_LIMIT_REMOVE_1715 = '<arp><entries><interface-limit nc:operation="remove"/></entries></arp>'
ARP_PACKET_PRIORITY_1715 = "<arp><packet-priority><enable/></packet-priority></arp>"
ARP_PACKET_PRIORITY_REMOVE_1715 = (
    '<arp><packet-priority><enable nc:operation="remove"/></packet-priority></arp>'
)

PQ_OUT_ENABLE_1715        = "<priority-queue><out/></priority-queue>"
PQ_OUT_ENABLE_REMOVE_1715 = '<priority-queue><out nc:operation="remove"/></priority-queue>'
PQ_COS_MAP_1715 = (
    "<priority-queue><cos-map><id>$qid</id>$cos_values_block</cos-map></priority-queue>"
)
PQ_COS_MAP_REMOVE_1715 = '<priority-queue><cos-map nc:operation="remove"/></priority-queue>'
RCV_QUEUE_COS_MAP_1715 = (
    "<rcv-queue><cos-map><queue-id>$qid</queue-id><threshold-id>$tid</threshold-id>"
    "$cos_values_block</cos-map></rcv-queue>"
)
RCV_QUEUE_COS_MAP_REMOVE_1715 = (
    '<rcv-queue><cos-map nc:operation="remove">'
    '<queue-id>$qid</queue-id><threshold-id>$tid</threshold-id></cos-map></rcv-queue>'
)

FLOWCONTROL_1715        = "<flowcontrol><receive>$rx</receive><send>$tx</send></flowcontrol>"
FLOWCONTROL_REMOVE_1715 = '<flowcontrol nc:operation="remove"/>'
HOLD_QUEUE_1715 = (
    "<hold-queue><direction>$direction</direction><queue-length>$qlen</queue-length></hold-queue>"
)
HOLD_QUEUE_REMOVE_1715 = (
    '<hold-queue nc:operation="remove"><direction>$direction</direction></hold-queue>'
)

LINK_BANDWIDTH_1715        = "<bandwidth><kilobits>$kbps</kilobits></bandwidth>"
LINK_BANDWIDTH_REMOVE_1715 = '<bandwidth nc:operation="remove"/>'
LINK_BANDWIDTH_QOS_REF_1715        = "<bandwidth><qos-reference>$kbps</qos-reference></bandwidth>"
LINK_BANDWIDTH_QOS_REF_REMOVE_1715 = '<bandwidth><qos-reference nc:operation="remove"/></bandwidth>'

DAMPENING_FULL_1715 = (
    "<dampening>"
    "<dampening-time>$half_life</dampening-time>"
    "<start-reusing-time>$reuse</start-reusing-time>"
    "<start-supressing-time>$suppress</start-supressing-time>"
    "<maximum-supressing-time>$max_suppress</maximum-supressing-time>"
    "</dampening>"
)
DAMPENING_DEFAULT_1715 = "<dampening/>"
DAMPENING_REMOVE_1715  = '<dampening nc:operation="remove"/>'

SRLG_1715        = "<srlg><gid>$srlg_values_block</gid></srlg>"
SRLG_REMOVE_1715 = '<srlg nc:operation="remove"/>'

DOMAIN_NAME_1715        = "<domain><name>$domain</name></domain>"
DOMAIN_NAME_REMOVE_1715 = '<domain><name nc:operation="remove"/></domain>'
DOMAIN_PATH_1715        = "<domain><path>$sp_path</path><path-id>$path_id</path-id></domain>"
DOMAIN_PATH_REMOVE_1715 = '<domain><path nc:operation="remove">$sp_path</path></domain>'

KEEPALIVE_TIMERS_1715 = (
    "<keepalive-config>"
    "<keepalive>true</keepalive>"
    "<period>$period</period>"
    "<retries>$retries</retries>"
    "</keepalive-config>"
)
KEEPALIVE_TIMERS_REMOVE_1715 = '<keepalive-config nc:operation="remove"/>'
KEEPALIVE_DISABLE_1715 = "<keepalive-config><keepalive>false</keepalive></keepalive-config>"

LINK_LOGGING_LINK_STATUS_1715 = (
    "<logging><event><link-status-enable>$flag</link-status-enable></event></logging>"
)
LINK_LOGGING_LINK_STATUS_REMOVE_1715 = (
    '<logging><event><link-status-enable nc:operation="remove"/></event></logging>'
)
LINK_LOGGING_EVENT_1715        = "<logging><event><$event/></event></logging>"
LINK_LOGGING_EVENT_REMOVE_1715 = '<logging><event><$event nc:operation="remove"/></event></logging>'
LINK_LOGGING_EVENTS_BLOCK_1715        = "<logging><event>$events_block</event></logging>"
LINK_LOGGING_EVENTS_BLOCK_REMOVE_1715 = '<logging><event nc:operation="remove"/></logging>'
LINK_LOGGING_SPANNING_TREE_1715 = (
    "<logging><event><spanning-tree><status/></spanning-tree></event></logging>"
)
LINK_LOGGING_SPANNING_TREE_REMOVE_1715 = (
    '<logging><event><spanning-tree nc:operation="remove"/></event></logging>'
)
LINK_LOGGING_SUBIF_1715 = (
    "<logging><event><subif-link-status>$ignore_bulk_block</subif-link-status></event></logging>"
)
LINK_LOGGING_SUBIF_REMOVE_1715 = (
    '<logging><event><subif-link-status nc:operation="remove"/></event></logging>'
)

FAIR_QUEUE_1715        = "<fair-queue><incomplete/></fair-queue>"
FAIR_QUEUE_REMOVE_1715 = '<fair-queue nc:operation="remove"/>'
FAIR_QUEUE_CONF_1715   = "<fair-queue-conf><fair-queue>$flag</fair-queue></fair-queue-conf>"


# ============================================================
# 4. IPv4
# ============================================================
IP4_PRIMARY_1715 = (
    "<ip><address><primary><address>$ip</address><mask>$mask</mask></primary></address></ip>"
)
IP4_PRIMARY_REMOVE_1715 = '<ip><address><primary nc:operation="remove"/></address></ip>'
IP4_SECONDARY_1715 = (
    "<ip><address><secondary><address>$ip</address><mask>$mask</mask><secondary/>"
    "</secondary></address></ip>"
)
IP4_SECONDARY_REMOVE_1715 = (
    '<ip><address><secondary nc:operation="remove">'
    '<address>$ip</address><mask>$mask</mask></secondary></address></ip>'
)
IP4_DHCP_1715               = "<ip><address><dhcp/></address></ip>"
IP4_DHCP_REMOVE_1715        = '<ip><address><dhcp nc:operation="remove"/></address></ip>'
IP4_NEGOTIATED_1715         = "<ip><address><negotiated/></address></ip>"
IP4_NEGOTIATED_REMOVE_1715  = '<ip><address><negotiated nc:operation="remove"/></address></ip>'
IP4_DHCP_OPTIONS_1715 = "<ip><address><dhcp>$client_id_block$hostname_block</dhcp></address></ip>"
IP4_UNNUMBERED_1715         = "<ip><unnumbered>$src_if</unnumbered></ip>"
IP4_UNNUMBERED_REMOVE_1715  = '<ip><unnumbered nc:operation="remove"/></ip>'

IP4_ACCESS_GROUP_IN_1715 = (
    "<ip><access-group><in><acl><acl-name>$acl</acl-name><in/></acl></in></access-group></ip>"
)
IP4_ACCESS_GROUP_IN_REMOVE_1715 = '<ip><access-group><in nc:operation="remove"/></access-group></ip>'
IP4_ACCESS_GROUP_OUT_1715 = (
    "<ip><access-group><out><acl><acl-name>$acl</acl-name><out/></acl></out></access-group></ip>"
)
IP4_ACCESS_GROUP_OUT_REMOVE_1715 = '<ip><access-group><out nc:operation="remove"/></access-group></ip>'
IP4_ACCESS_GROUP_COMMON_IN_1715 = (
    "<ip><access-group><in><common-acl><common>$common_acl</common>"
    "<acl-name>$acl</acl-name><in/></common-acl></in></access-group></ip>"
)
IP4_ACCESS_GROUP_COMMON_IN_REMOVE_1715 = (
    '<ip><access-group><in><common-acl nc:operation="remove"/></in></access-group></ip>'
)
IP4_ACCESS_GROUP_COMMON_OUT_1715 = (
    "<ip><access-group><out><common-acl><common>$common_acl</common>"
    "<acl-name>$acl</acl-name><out/></common-acl></out></access-group></ip>"
)
IP4_ACCESS_GROUP_COMMON_OUT_REMOVE_1715 = (
    '<ip><access-group><out><common-acl nc:operation="remove"/></out></access-group></ip>'
)

IP4_VRF_FORWARDING_1715        = "<vrf><forwarding>$vrf</forwarding></vrf>"
IP4_VRF_FORWARDING_REMOVE_1715 = '<vrf><forwarding nc:operation="remove">$vrf</forwarding></vrf>'
IP4_VRF_RECEIVE_1715           = "<ip><vrf><receive>$vrf</receive></vrf></ip>"
IP4_VRF_RECEIVE_REMOVE_1715    = '<ip><vrf><receive nc:operation="remove">$vrf</receive></vrf></ip>'
IP4_VRF_SITEMAP_1715           = "<ip><vrf><sitemap>$route_map</sitemap></vrf></ip>"
IP4_VRF_SITEMAP_REMOVE_1715    = '<ip><vrf><sitemap nc:operation="remove">$route_map</sitemap></vrf></ip>'

IP4_HELPER_1715        = "<ip><helper-address><address>$helper</address></helper-address></ip>"
IP4_HELPER_REMOVE_1715 = (
    '<ip><helper-address nc:operation="remove"><address>$helper</address></helper-address></ip>'
)
IP4_HELPER_GLOBAL_1715 = (
    "<ip><helper-address><address>$helper</address><global/></helper-address></ip>"
)
IP4_HELPER_GLOBAL_REMOVE_1715 = (
    '<ip><helper-address nc:operation="remove"><address>$helper</address><global/></helper-address></ip>'
)
IP4_HELPER_VRF_1715 = (
    "<ip><helper-address><address>$helper</address><vrf>$vrf</vrf></helper-address></ip>"
)
IP4_HELPER_VRF_REMOVE_1715 = (
    '<ip><helper-address nc:operation="remove"><address>$helper</address><vrf>$vrf</vrf></helper-address></ip>'
)

IP4_POLICY_ROUTE_MAP_1715        = "<ip><policy><route-map>$route_map</route-map></policy></ip>"
IP4_POLICY_ROUTE_MAP_REMOVE_1715 = '<ip><policy><route-map nc:operation="remove"/></policy></ip>'

IP4_PROXY_ARP_1715              = "<ip><proxy-arp>$flag</proxy-arp></ip>"
IP4_LOCAL_PROXY_ARP_1715        = "<ip><local-proxy-arp/></ip>"
IP4_LOCAL_PROXY_ARP_REMOVE_1715 = '<ip><local-proxy-arp nc:operation="remove"/></ip>'
IP4_REDIRECTS_1715              = "<ip><redirects>$flag</redirects></ip>"
IP4_CLEAR_DF_1715               = "<ip><clear-dont-fragment>$flag</clear-dont-fragment></ip>"
IP4_TCP_MSS_1715                = "<ip><tcp><adjust-mss>$mss</adjust-mss></tcp></ip>"
IP4_TCP_MSS_REMOVE_1715         = '<ip><tcp><adjust-mss nc:operation="remove"/></tcp></ip>'
IP4_MTU_1715                    = "<ip><mtu>$ip_mtu</mtu></ip>"
IP4_MTU_REMOVE_1715             = '<ip><mtu nc:operation="remove"/></ip>'

IP4_URPF_1715 = (
    "<ip><verify><unicast><source>"
    "<reachable-via>$via</reachable-via>"
    "$allow_block"
    "$acl_block"
    "</source></unicast></verify></ip>"
)
IP4_URPF_REMOVE_1715 = '<ip><verify nc:operation="remove"/></ip>'

IP4_ARP_INSPECT_TRUST_1715 = "<ip><arp><inspection><trust/></inspection></arp></ip>"
IP4_ARP_INSPECT_TRUST_REMOVE_1715 = (
    '<ip><arp><inspection><trust nc:operation="remove"/></inspection></arp></ip>'
)
IP4_ARP_INSPECT_RATE_1715 = (
    "<ip><arp><inspection><limit>"
    "<rate>$pps</rate>"
    "$burst_block"
    "</limit></inspection></arp></ip>"
)
IP4_ARP_INSPECT_RATE_REMOVE_1715 = (
    '<ip><arp><inspection><limit nc:operation="remove"/></inspection></arp></ip>'
)
IP4_ARP_INSPECT_RATE_NONE_1715 = "<ip><arp><inspection><limit><none/></limit></inspection></arp></ip>"

IP4_DIRECTED_BROADCAST_1715        = "<ip><directed-broadcast/></ip>"
IP4_DIRECTED_BROADCAST_REMOVE_1715 = '<ip><directed-broadcast nc:operation="remove"/></ip>'
IP4_DIRECTED_BROADCAST_ACL_1715 = (
    "<ip><directed-broadcast><direct-broadcast>$acl</direct-broadcast></directed-broadcast></ip>"
)


# ============================================================
# 5. IPv6
# ============================================================
IP6_ENABLE_1715        = "<ipv6><enable/></ipv6>"
IP6_ENABLE_REMOVE_1715 = '<ipv6><enable nc:operation="remove"/></ipv6>'

IP6_ADDRESS_PREFIX_1715 = "<ipv6><address><prefix-list><prefix>$ipv6</prefix></prefix-list></address></ipv6>"
IP6_ADDRESS_PREFIX_REMOVE_1715 = (
    '<ipv6><address><prefix-list nc:operation="remove"><prefix>$ipv6</prefix></prefix-list></address></ipv6>'
)
IP6_ADDRESS_EUI64_1715 = (
    "<ipv6><address><prefix-list><prefix>$ipv6</prefix><eui-64/></prefix-list></address></ipv6>"
)
IP6_ADDRESS_EUI64_REMOVE_1715 = (
    '<ipv6><address><prefix-list nc:operation="remove"><prefix>$ipv6</prefix><eui-64/></prefix-list></address></ipv6>'
)
IP6_ADDRESS_ANYCAST_1715 = (
    "<ipv6><address><prefix-list><prefix>$ipv6</prefix><anycast/></prefix-list></address></ipv6>"
)
IP6_ADDRESS_ANYCAST_REMOVE_1715 = (
    '<ipv6><address><prefix-list nc:operation="remove"><prefix>$ipv6</prefix><anycast/></prefix-list></address></ipv6>'
)
IP6_ADDRESS_LINK_LOCAL_1715 = (
    "<ipv6><address><link-local-address><address>$ll</address><link-local/>"
    "</link-local-address></address></ipv6>"
)
IP6_ADDRESS_LINK_LOCAL_REMOVE_1715 = (
    '<ipv6><address><link-local-address nc:operation="remove"><address>$ll</address><link-local/>'
    '</link-local-address></address></ipv6>'
)
IP6_ADDRESS_AUTOCONFIG_1715        = "<ipv6><address><autoconfig/></address></ipv6>"
IP6_ADDRESS_AUTOCONFIG_REMOVE_1715 = '<ipv6><address><autoconfig nc:operation="remove"/></address></ipv6>'
IP6_ADDRESS_AUTOCONFIG_DEFAULT_1715 = "<ipv6><address><autoconfig><default/></autoconfig></address></ipv6>"
IP6_ADDRESS_AUTOCONFIG_DEFAULT_REMOVE_1715 = (
    '<ipv6><address><autoconfig nc:operation="remove"><default/></autoconfig></address></ipv6>'
)
IP6_ADDRESS_DHCP_1715        = "<ipv6><address><dhcp/></address></ipv6>"
IP6_ADDRESS_DHCP_REMOVE_1715 = '<ipv6><address><dhcp nc:operation="remove"/></address></ipv6>'
IP6_ADDRESS_DHCP_RAPID_COMMIT_1715 = "<ipv6><address><dhcp><rapid-commit/></dhcp></address></ipv6>"
IP6_ADDRESS_DHCP_RAPID_COMMIT_REMOVE_1715 = (
    '<ipv6><address><dhcp nc:operation="remove"><rapid-commit/></dhcp></address></ipv6>'
)
IP6_ADDRESS_PREFIX_NAME_1715 = (
    "<ipv6><address><prefix-name><name>$pfx_name</name><prefix-options>"
    "<ipv6-prefix><prefix>$ipv6</prefix></ipv6-prefix></prefix-options></prefix-name></address></ipv6>"
)
IP6_ADDRESS_PREFIX_NAME_REMOVE_1715 = (
    '<ipv6><address><prefix-name nc:operation="remove"><name>$pfx_name</name></prefix-name></address></ipv6>'
)

IP6_UNNUMBERED_1715        = "<ipv6><unnumbered>$src_if</unnumbered></ipv6>"
IP6_UNNUMBERED_REMOVE_1715 = '<ipv6><unnumbered nc:operation="remove"/></ipv6>'
IP6_MTU_1715               = "<ipv6><mtu>$ip6_mtu</mtu></ipv6>"
IP6_MTU_REMOVE_1715        = '<ipv6><mtu nc:operation="remove"/></ipv6>'
IP6_TCP_ADJUST_MSS_1715        = "<ipv6><tcp><adjust-mss>$mss</adjust-mss></tcp></ipv6>"
IP6_TCP_ADJUST_MSS_REMOVE_1715 = '<ipv6><tcp><adjust-mss nc:operation="remove"/></tcp></ipv6>'
IP6_TRAFFIC_FILTER_1715 = (
    "<ipv6><traffic-filter><direction>$direction</direction>"
    "<access-list>$acl</access-list></traffic-filter></ipv6>"
)
IP6_TRAFFIC_FILTER_REMOVE_1715 = (
    '<ipv6><traffic-filter nc:operation="remove"><direction>$direction</direction>'
    '<access-list>$acl</access-list></traffic-filter></ipv6>'
)
IP6_SOURCE_GUARD_1715        = "<ipv6><source-guard>$policy_block</source-guard></ipv6>"
IP6_SOURCE_GUARD_REMOVE_1715 = '<ipv6><source-guard nc:operation="remove"/></ipv6>'

IP6_ND_DAD_ATTEMPTS_1715 = (
    "<ipv6><nd><dad><attempts>$attempts</attempts></dad></nd></ipv6>"
)
IP6_ND_DAD_ATTEMPTS_REMOVE_1715 = (
    '<ipv6><nd><dad><attempts nc:operation="remove"/></dad></nd></ipv6>'
)
IP6_ND_NUD_IGP_1715 = "<ipv6><nd><nud><igp>$flag</igp></nud></nd></ipv6>"
IP6_VERIFY_UNICAST_REVERSE_PATH_1715 = (
    "<ipv6><verify><unicast><reverse-path>$acl_block</reverse-path>"
    "</unicast></verify></ipv6>"
)
IP6_VERIFY_UNICAST_REVERSE_PATH_REMOVE_1715 = (
    '<ipv6><verify nc:operation="remove"/></ipv6>'
)


# ============================================================
# 6. ACCESS-SESSION
# ============================================================
AS_PORT_CONTROL_1715 = "<access-session><port-control-config>$pc</port-control-config></access-session>"
AS_PORT_CONTROL_REMOVE_1715 = '<access-session><port-control-config nc:operation="remove"/></access-session>'
AS_CONTROL_DIRECTION_1715 = (
    "<access-session><control-direction-config>$dir</control-direction-config></access-session>"
)
AS_CONTROL_DIRECTION_REMOVE_1715 = (
    '<access-session><control-direction-config nc:operation="remove"/></access-session>'
)
AS_HOST_MODE_1715 = (
    "<access-session><host-mode-config><modes>$hm</modes></host-mode-config></access-session>"
)
AS_HOST_MODE_REMOVE_1715 = '<access-session><host-mode-config nc:operation="remove"/></access-session>'
AS_HOST_MODE_PEER_1715 = (
    "<access-session><host-mode-config><modes>multi-host</modes><peer/></host-mode-config></access-session>"
)
AS_HOST_MODE_PEER_REMOVE_1715 = (
    '<access-session><host-mode-config nc:operation="remove"><peer/></host-mode-config></access-session>'
)
AS_MONITOR_1715 = "<access-session><monitor>$flag</monitor></access-session>"


# ============================================================
# 7. STORM-CONTROL
# ============================================================
SC_ACTION_LEVEL_1715    = "<storm-control><action><level>$pct</level></action></storm-control>"
SC_ACTION_SHUTDOWN_1715 = "<storm-control><action><shutdown/></action></storm-control>"
SC_ACTION_TRAP_1715     = "<storm-control><action><trap/></action></storm-control>"
SC_ACTION_REMOVE_1715   = '<storm-control><action nc:operation="remove"/></storm-control>'
SC_THRESHOLD_PERCENT_1715 = (
    "<storm-control><$sc_type><level><threshold>"
    "<rising-threshold>$rise</rising-threshold>"
    "<falling-threshold>$fall</falling-threshold>"
    "</threshold></level></$sc_type></storm-control>"
)
SC_THRESHOLD_REMOVE_1715 = '<storm-control><$sc_type nc:operation="remove"/></storm-control>'
SC_BROADCAST_INCLUDE_MULTICAST_1715 = (
    "<storm-control><broadcast><include><multicast/></include></broadcast></storm-control>"
)
SC_BROADCAST_INCLUDE_MULTICAST_REMOVE_1715 = (
    '<storm-control><broadcast><include nc:operation="remove"/></broadcast></storm-control>'
)


# ============================================================
# 8. MACSEC
# ============================================================
MSEC_ENABLE_1715        = "<macsec-enable><macsec/></macsec-enable>"
MSEC_ENABLE_REMOVE_1715 = '<macsec-enable><macsec nc:operation="remove"/></macsec-enable>'
MSEC_REPLAY_PROTECTION_1715 = (
    "<macsec-option><macsec><replay-protection>"
    "<window-size>$window</window-size>"
    "</replay-protection></macsec></macsec-option>"
)
MSEC_REPLAY_PROTECTION_REMOVE_1715 = (
    '<macsec-option><macsec><replay-protection nc:operation="remove"/></macsec></macsec-option>'
)


# ============================================================
# 9. MISC — SUBSCRIBER
# ============================================================
MISC_SUBSCRIBER_INACTIVITY_1715 = (
    "<subscriber><aging><inactivity-timer><value>$secs</value>$probe_block"
    "</inactivity-timer></aging></subscriber>"
)
MISC_SUBSCRIBER_INACTIVITY_REMOVE_1715 = (
    '<subscriber><aging><inactivity-timer nc:operation="remove"/></aging></subscriber>'
)
MISC_SUBSCRIBER_PROBE_1715 = "<subscriber><aging><probe/></aging></subscriber>"
MISC_SUBSCRIBER_PROBE_REMOVE_1715 = '<subscriber><aging><probe nc:operation="remove"/></aging></subscriber>'


# ============================================================
# 10. PHYSICAL LAYER
# ============================================================
PHY_MEDIA_TYPE_1715        = "<media-type>$media</media-type>"
PHY_MEDIA_TYPE_REMOVE_1715 = '<media-type nc:operation="remove"/>'
PHY_FEC_1715               = "<fec>$fec</fec>"
PHY_FEC_REMOVE_1715        = '<fec nc:operation="remove"/>'


# ============================================================
# 11. PORT-CHANNEL
# ============================================================
PO_LOAD_BALANCE_HASH_ALGO_1715        = "<load-balance-hash-algo>$algo</load-balance-hash-algo>"
PO_LOAD_BALANCE_HASH_ALGO_REMOVE_1715 = '<load-balance-hash-algo nc:operation="remove"/>'
PO_MIN_LINKS_1715             = "<port-channel><min-links>$min_links</min-links></port-channel>"
PO_MIN_LINKS_REMOVE_1715      = '<port-channel><min-links nc:operation="remove"/></port-channel>'
PO_STANDALONE_DISABLE_1715        = "<port-channel><standalone-disable/></port-channel>"
PO_STANDALONE_DISABLE_REMOVE_1715 = '<port-channel><standalone-disable nc:operation="remove"/></port-channel>'


# ============================================================
# 12. OTHER TYPE LEAVES
# ============================================================
TYPE_VLAN_AUTOSTATE_1715 = "<autostate>$flag</autostate>"
TYPE_TUNNEL_QOS_PRE_CLASSIFY_1715 = "<qos><pre-classify/></qos>"
TYPE_TUNNEL_QOS_PRE_CLASSIFY_REMOVE_1715 = '<qos><pre-classify nc:operation="remove"/></qos>'


# ============================================================
# 13. NVE / VXLAN
# ============================================================
NVE_HOST_REACHABILITY_BGP_1715 = "<host-reachability><protocol><bgp/></protocol></host-reachability>"
NVE_HOST_REACHABILITY_BGP_REMOVE_1715 = '<host-reachability nc:operation="remove"/>'
NVE_SOURCE_INTERFACE_1715 = "<source-interface><$src_type>$src_name</$src_type></source-interface>"
NVE_SOURCE_INTERFACE_REMOVE_1715 = '<source-interface nc:operation="remove"/>'
NVE_MEMBER_VNI_VRF_1715 = (
    "<member-in-one-line><member><vni><vni-range>$vni</vni-range><vrf>$vrf</vrf>"
    "</vni></member></member-in-one-line>"
)
NVE_MEMBER_VNI_VRF_REMOVE_1715 = (
    '<member-in-one-line><member nc:operation="remove"><vni><vni-range>$vni</vni-range></vni>'
    '</member></member-in-one-line>'
)
NVE_MEMBER_VNI_MCAST_GROUP_1715 = (
    "<member><vni><vni-range>$vni</vni-range><mcast-group>"
    "<multicast-group-min>$mc_min</multicast-group-min>$mc_max_block"
    "</mcast-group></vni></member>"
)
NVE_MEMBER_VNI_MCAST_GROUP_REMOVE_1715 = (
    '<member><vni nc:operation="remove"><vni-range>$vni</vni-range></vni></member>'
)


# ============================================================
# 14. VLAN DATABASE + SVI
# ============================================================
VLAN_CREATE_1715 = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN"><id>$vlan_id</id></vlan-list></vlan>'
VLAN_DELETE_1715 = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN" nc:operation="remove"><id>$vlan_id</id></vlan-list></vlan>'

VLAN_NAME_1715        = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN"><id>$vlan_id</id><name>$vlan_name</name></vlan-list></vlan>'
VLAN_NAME_REMOVE_1715 = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN"><id>$vlan_id</id><name nc:operation="remove"/></vlan-list></vlan>'
VLAN_STATE_1715        = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN"><id>$vlan_id</id><state>$vlan_state</state></vlan-list></vlan>'
VLAN_STATE_REMOVE_1715 = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN"><id>$vlan_id</id><state nc:operation="remove"/></vlan-list></vlan>'
VLAN_SHUTDOWN_1715        = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN"><id>$vlan_id</id><shutdown/></vlan-list></vlan>'
VLAN_SHUTDOWN_REMOVE_1715 = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN"><id>$vlan_id</id><shutdown nc:operation="remove"/></vlan-list></vlan>'
VLAN_REMOTE_SPAN_1715        = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN"><id>$vlan_id</id><remote-span/></vlan-list></vlan>'
VLAN_REMOTE_SPAN_REMOVE_1715 = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN"><id>$vlan_id</id><remote-span nc:operation="remove"/></vlan-list></vlan>'
VLAN_UNI_1715        = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN"><id>$vlan_id</id><uni-vlan>$uni_type</uni-vlan></vlan-list></vlan>'
VLAN_UNI_REMOVE_1715 = '<vlan xmlns="$N"><vlan-list xmlns="$VLAN"><id>$vlan_id</id><uni-vlan nc:operation="remove"/></vlan-list></vlan>'

VLAN_GROUP_1715 = (
    '<vlan xmlns="$N"><group xmlns="$VLAN"><name>$group_name</name><vlan-lists>$vlan_id</vlan-lists></group></vlan>'
)
VLAN_GROUP_REMOVE_1715 = (
    '<vlan xmlns="$N"><group xmlns="$VLAN" nc:operation="remove"><name>$group_name</name></group></vlan>'
)
VLAN_GROUP_MEMBER_REMOVE_1715 = (
    '<vlan xmlns="$N"><group xmlns="$VLAN"><name>$group_name</name>'
    '<vlan-lists nc:operation="remove">$vlan_id</vlan-lists></group></vlan>'
)

VLAN_FILTER_1715 = (
    '<vlan xmlns="$N"><filter xmlns="$VLAN"><word>$map_name</word><vlan-lists>$vlan_id</vlan-lists></filter></vlan>'
)
VLAN_FILTER_REMOVE_1715 = (
    '<vlan xmlns="$N"><filter xmlns="$VLAN" nc:operation="remove"><word>$map_name</word></filter></vlan>'
)

VLAN_DOT1Q_TAG_NATIVE_1715 = '<vlan xmlns="$N"><dot1q xmlns="$VLAN"><tag><native/></tag></dot1q></vlan>'
VLAN_DOT1Q_TAG_NATIVE_REMOVE_1715 = (
    '<vlan xmlns="$N"><dot1q xmlns="$VLAN"><tag><native nc:operation="remove"/></tag></dot1q></vlan>'
)
VLAN_INTERNAL_ALLOCATION_1715 = (
    '<vlan xmlns="$N"><internal xmlns="$VLAN"><allocation><policy>$policy</policy></allocation></internal></vlan>'
)
VLAN_INTERNAL_ALLOCATION_REMOVE_1715 = (
    '<vlan xmlns="$N"><internal xmlns="$VLAN"><allocation nc:operation="remove"/></internal></vlan>'
)
VLAN_ACCOUNTING_1715 = '<vlan xmlns="$N"><accounting xmlns="$VLAN">$accounting_block</accounting></vlan>'
VLAN_ACCOUNTING_REMOVE_1715 = '<vlan xmlns="$N"><accounting xmlns="$VLAN" nc:operation="remove"/></vlan>'

SVI_PRIVATE_VLAN_MAPPING_1715 = '<private-vlan xmlns="$VLAN"><mapping>$mapping</mapping></private-vlan>'
SVI_PRIVATE_VLAN_MAPPING_REMOVE_1715 = '<private-vlan xmlns="$VLAN"><mapping nc:operation="remove"/></private-vlan>'


# ================================================================
# NOT_PRESENT  (kept for engine parity; 17.15 has a template for every family)
# ================================================================
NOT_PRESENT = {
    "ARP_INSPECT_RATE": 'not modelled on train 1715',
    "ARP_INSPECT_RATE_REMOVE": 'not modelled on train 1715',
    "ARP_INSPECT_TRUST": 'not modelled on train 1715',
    "ARP_INSPECT_TRUST_REMOVE": 'not modelled on train 1715',
    "ARP_SNAP": 'not modelled on train 1715',
    "ARP_SNAP_REMOVE": 'not modelled on train 1715',
    "AS_MONITOR_REMOVE": 'not modelled on train 1715',
    "CLEAR_DF": 'not modelled on train 1715',
    "CLEAR_DF_REMOVE": 'not modelled on train 1715',
    "DAMPENING": 'not modelled on train 1715',
    "DIRECTED_BROADCAST": 'not modelled on train 1715',
    "DIRECTED_BROADCAST_REMOVE": 'not modelled on train 1715',
    "FEC": 'not modelled on train 1715',
    "FEC_REMOVE": 'not modelled on train 1715',
    "HELPER_ADDRESS": 'not modelled on train 1715',
    "HELPER_ADDRESS_REMOVE": 'not modelled on train 1715',
    "IPV4_ACCESS_GROUP": 'not modelled on train 1715',
    "IPV4_ACCESS_GROUP_REMOVE": 'not modelled on train 1715',
    "IPV4_ADDRESS": 'not modelled on train 1715',
    "IPV4_ADDRESS_REMOVE": 'not modelled on train 1715',
    "IPV4_DHCP": 'not modelled on train 1715',
    "IPV4_DHCP_REMOVE": 'not modelled on train 1715',
    "IPV4_UNNUMBERED": 'not modelled on train 1715',
    "IPV4_UNNUMBERED_REMOVE": 'not modelled on train 1715',
    "IPV4_VRF_RECEIVE": 'not modelled on train 1715',
    "IPV4_VRF_RECEIVE_REMOVE": 'not modelled on train 1715',
    "IPV4_VRF_SITEMAP": 'not modelled on train 1715',
    "IPV4_VRF_SITEMAP_REMOVE": 'not modelled on train 1715',
    "IPV6_ADDRESS": 'not modelled on train 1715',
    "IPV6_ADDRESS_REMOVE": 'not modelled on train 1715',
    "IPV6_AUTOCONFIG": 'not modelled on train 1715',
    "IPV6_AUTOCONFIG_REMOVE": 'not modelled on train 1715',
    "IPV6_DHCP": 'not modelled on train 1715',
    "IPV6_DHCP_REMOVE": 'not modelled on train 1715',
    "IPV6_ENABLE": 'not modelled on train 1715',
    "IPV6_ENABLE_REMOVE": 'not modelled on train 1715',
    "IPV6_MTU": 'not modelled on train 1715',
    "IPV6_MTU_REMOVE": 'not modelled on train 1715',
    "IPV6_ND_DAD_ATTEMPTS": 'not modelled on train 1715',
    "IPV6_ND_DAD_ATTEMPTS_REMOVE": 'not modelled on train 1715',
    "IPV6_ND_NUD_IGP": 'not modelled on train 1715',
    "IPV6_ND_NUD_IGP_REMOVE": 'not modelled on train 1715',
    "IPV6_SOURCE_GUARD": 'not modelled on train 1715',
    "IPV6_SOURCE_GUARD_REMOVE": 'not modelled on train 1715',
    "IPV6_TCP_ADJUST_MSS": 'not modelled on train 1715',
    "IPV6_TCP_ADJUST_MSS_REMOVE": 'not modelled on train 1715',
    "IPV6_TRAFFIC_FILTER": 'not modelled on train 1715',
    "IPV6_TRAFFIC_FILTER_REMOVE": 'not modelled on train 1715',
    "IPV6_UNNUMBERED": 'not modelled on train 1715',
    "IPV6_UNNUMBERED_REMOVE": 'not modelled on train 1715',
    "IPV6_VERIFY_REVERSE_PATH": 'not modelled on train 1715',
    "IPV6_VERIFY_REVERSE_PATH_REMOVE": 'not modelled on train 1715',
    "IP_MTU": 'not modelled on train 1715',
    "IP_MTU_REMOVE": 'not modelled on train 1715',
    "KEEPALIVE": 'not modelled on train 1715',
    "KEEPALIVE_REMOVE": 'not modelled on train 1715',
    "L2PT_THRESHOLD": 'not modelled on train 1715',
    "L2PT_THRESHOLD_REMOVE": 'not modelled on train 1715',
    "L2_PORT_SECURITY_AGING": 'not modelled on train 1715',
    "L2_PORT_SECURITY_AGING_REMOVE": 'not modelled on train 1715',
    "L2_PORT_SECURITY_ENABLE": 'not modelled on train 1715',
    "L2_PORT_SECURITY_ENABLE_REMOVE": 'not modelled on train 1715',
    "L2_PORT_SECURITY_MAC": 'not modelled on train 1715',
    "L2_PORT_SECURITY_MAC_REMOVE": 'not modelled on train 1715',
    "L2_PORT_SECURITY_MAX": 'not modelled on train 1715',
    "L2_PORT_SECURITY_MAX_REMOVE": 'not modelled on train 1715',
    "L2_PORT_SECURITY_STICKY": 'not modelled on train 1715',
    "L2_PORT_SECURITY_STICKY_REMOVE": 'not modelled on train 1715',
    "L2_PORT_SECURITY_VIOLATION": 'not modelled on train 1715',
    "L2_PORT_SECURITY_VIOLATION_REMOVE": 'not modelled on train 1715',
    "L2_TRUNK_ALLOWED": 'not modelled on train 1715',
    "L2_TRUNK_ALLOWED_REMOVE": 'not modelled on train 1715',
    "L2_TRUNK_ENCAPSULATION": 'not modelled on train 1715',
    "L2_TRUNK_ENCAPSULATION_REMOVE": 'not modelled on train 1715',
    "L2_TRUNK_NATIVE_VLAN": 'not modelled on train 1715',
    "L2_TRUNK_NATIVE_VLAN_REMOVE": 'not modelled on train 1715',
    "L2_TRUNK_PRUNING": 'not modelled on train 1715',
    "L2_VOICE_VLAN": 'not modelled on train 1715',
    "L2_VOICE_VLAN_NAME": 'not modelled on train 1715',
    "LOCAL_PROXY_ARP": 'not modelled on train 1715',
    "LOCAL_PROXY_ARP_REMOVE": 'not modelled on train 1715',
    "LOGGING_EVENT": 'not modelled on train 1715',
    "LOGGING_EVENT_REMOVE": 'not modelled on train 1715',
    "LOGGING_LINK_STATUS": 'not modelled on train 1715',
    "LOGGING_LINK_STATUS_REMOVE": 'not modelled on train 1715',
    "LOGGING_SPANNING_TREE": 'not modelled on train 1715',
    "LOGGING_SPANNING_TREE_REMOVE": 'not modelled on train 1715',
    "LOGGING_SUBIF": 'not modelled on train 1715',
    "LOGGING_SUBIF_REMOVE": 'not modelled on train 1715',
    "MACSEC_ENABLE": 'not modelled on train 1715',
    "MACSEC_ENABLE_REMOVE": 'not modelled on train 1715',
    "MACSEC_REPLAY_PROTECTION": 'not modelled on train 1715',
    "MACSEC_REPLAY_PROTECTION_REMOVE": 'not modelled on train 1715',
    "MDIX": 'not modelled on train 1715',
    "MDIX_REMOVE": 'not modelled on train 1715',
    "MEDIA_TYPE": 'not modelled on train 1715',
    "MEDIA_TYPE_REMOVE": 'not modelled on train 1715',
    "NEGOTIATION_REMOVE": 'not modelled on train 1715',
    "POLICY_ROUTE_MAP": 'not modelled on train 1715',
    "POLICY_ROUTE_MAP_REMOVE": 'not modelled on train 1715',
    "PO_LOAD_BALANCE": 'not modelled on train 1715',
    "PO_LOAD_BALANCE_REMOVE": 'not modelled on train 1715',
    "PQ_OUT": 'not modelled on train 1715',
    "PQ_OUT_REMOVE": 'not modelled on train 1715',
    "PROXY_ARP": 'not modelled on train 1715',
    "PROXY_ARP_REMOVE": 'not modelled on train 1715',
    "REDIRECTS": 'not modelled on train 1715',
    "REDIRECTS_REMOVE": 'not modelled on train 1715',
    "STORM_CONTROL_ACTION": 'not modelled on train 1715',
    "STORM_CONTROL_ACTION_REMOVE": 'not modelled on train 1715',
    "STORM_CONTROL_BCAST_INCLUDE_MCAST": 'not modelled on train 1715',
    "STORM_CONTROL_BCAST_INCLUDE_MCAST_REMOVE": 'not modelled on train 1715',
    "STORM_CONTROL_THRESHOLD": 'not modelled on train 1715',
    "STORM_CONTROL_THRESHOLD_REMOVE": 'not modelled on train 1715',
    "SUBSCRIBER_INACTIVITY": 'not modelled on train 1715',
    "SUBSCRIBER_INACTIVITY_REMOVE": 'not modelled on train 1715',
    "SUBSCRIBER_PROBE": 'not modelled on train 1715',
    "SUBSCRIBER_PROBE_REMOVE": 'not modelled on train 1715',
    "TCP_ADJUST_MSS": 'not modelled on train 1715',
    "TCP_ADJUST_MSS_REMOVE": 'not modelled on train 1715',
    "TUNNEL_QOS_PRE_CLASSIFY": 'not modelled on train 1715',
    "TUNNEL_QOS_PRE_CLASSIFY_REMOVE": 'not modelled on train 1715',
    "URPF": 'not modelled on train 1715',
    "URPF_REMOVE": 'not modelled on train 1715',
    "VLAN_AUTOSTATE": 'not modelled on train 1715',
    "VLAN_AUTOSTATE_REMOVE": 'not modelled on train 1715',
    "VLAN_CREATE_REMOVE": 'not modelled on train 1715',
    "VLAN_DELETE_REMOVE": 'not modelled on train 1715',
    "VRF_FORWARDING": 'not modelled on train 1715',
    "VRF_FORWARDING_REMOVE": 'not modelled on train 1715',
}
DIFFS_VS_179 = {
    "L2PT_DROP_THRESHOLD":              "17.9: <$proto>$pps</$proto>; packet-rate is a sibling leaf",
    "L2PT_DROP_THRESHOLD_P2P":          "17.9: <$p2p_proto>$pps</$p2p_proto>",
    "L2PT_DROP_THRESHOLD_RATE":         "17.9 has sibling <packet-rate>; 17.15 switch YANG needs check",
    "L2PT_SHUTDOWN_THRESHOLD":          "17.9: <$proto>$pps</$proto>; packet-rate is a sibling leaf",
    "L2PT_SHUTDOWN_THRESHOLD_P2P":      "17.9: <$p2p_proto>$pps</$p2p_proto>",
    "L2PT_SHUTDOWN_THRESHOLD_RATE":     "17.9 has sibling <packet-rate>; 17.15 switch YANG needs check",
    "L2_PORTSEC_MAX":       "17.9: list maxcount (key max-addresses, leaf vlan)",
    "L2_PORTSEC_MAX_VLAN":  "17.9: list maxcount (key max-addresses, leaf vlan)",
    "L2_PORTSEC_MAC_STICKY": "17.9: hw-address-access + <sticky>sticky</sticky>",
    "KEEPALIVE_TIMERS":     "17.9: keepalive-settings/keepalive/{period,retries}",
    "KEEPALIVE_DISABLE":    "17.9: <keepalive>false</keepalive>",
    "IP4_URPF":             "17.9: no ACL leaf under verify/unicast/source",
    "IP4_ARP_INSPECT_RATE": "17.9: no burst leaf",
    "IP6_ND_DAD_ATTEMPTS":  "17.9: ipv6/nd children live in Cisco-IOS-XE-nd (unverified)",
    "IP6_ND_NUD_IGP":       "17.9: ipv6/nd children live in Cisco-IOS-XE-nd (unverified)",
    "IP6_VERIFY_UNICAST_REVERSE_PATH": "17.9: no verify node under ipv6",
    "MSEC_ENABLE":          "17.9: plain <macsec xmlns=SW/> leaf in the switch module",
    "MSEC_REPLAY_PROTECTION": "17.9: <macsec-option xmlns=SW> in the switch module",
    "PO_LOAD_BALANCE_HASH_ALGO": "17.9: <load-balancing> vlan|flow; no hash-algo leaf",
    "NEGOTIATION_FULL":     "17.9 negotiation has only <auto>",
    "GEN_MDIX_FULL":        "17.9 mdix has only <auto>",
}


# ================================================================
# TEMPLATE REGISTRY
# ================================================================
_TRAINS = ("1715",)

def _t(**kw):
    return {v: kw.get(v) for v in _TRAINS}


TEMPLATES = {
    # §1
    "DESCRIPTION":                     _t(**{"1715": DESCRIPTION_1715}),
    "DESCRIPTION_REMOVE":              _t(**{"1715": DESCRIPTION_REMOVE_1715}),
    "EXPORT_NAME":                     _t(**{"1715": EXPORT_NAME_1715}),
    "EXPORT_NAME_REMOVE":              _t(**{"1715": EXPORT_NAME_REMOVE_1715}),
    "MAC_ADDRESS":                     _t(**{"1715": MAC_ADDRESS_1715}),
    "MAC_ADDRESS_REMOVE":              _t(**{"1715": MAC_ADDRESS_REMOVE_1715}),
    "SHUTDOWN":                        _t(**{"1715": SHUTDOWN_1715}),
    "SHUTDOWN_REMOVE":                 _t(**{"1715": SHUTDOWN_REMOVE_1715}),
    "MTU":                             _t(**{"1715": MTU_1715}),
    "MTU_REMOVE":                      _t(**{"1715": MTU_REMOVE_1715}),
    "DELAY":                           _t(**{"1715": DELAY_1715}),
    "DELAY_REMOVE":                    _t(**{"1715": DELAY_REMOVE_1715}),
    "LOAD_INTERVAL":                   _t(**{"1715": LOAD_INTERVAL_1715}),
    "LOAD_INTERVAL_REMOVE":            _t(**{"1715": LOAD_INTERVAL_REMOVE_1715}),
    "MAX_BANDWIDTH":                   _t(**{"1715": MAX_BANDWIDTH_1715}),
    "MAX_BANDWIDTH_REMOVE":            _t(**{"1715": MAX_BANDWIDTH_REMOVE_1715}),
    "NEGOTIATION":                     _t(**{"1715": NEGOTIATION_1715}),
    "NEGOTIATION_FULL":                _t(**{"1715": NEGOTIATION_FULL_1715}),
    "GEN_MDIX":                        _t(**{"1715": GEN_MDIX_1715}),
    "GEN_MDIX_FULL":                   _t(**{"1715": GEN_MDIX_FULL_1715}),
    "SERVICE_INSERTION":               _t(**{"1715": SERVICE_INSERTION_1715}),
    "SERVICE_INSERTION_REMOVE":        _t(**{"1715": SERVICE_INSERTION_REMOVE_1715}),
    "QOS_TRUST":                       _t(**{"1715": QOS_TRUST_1715}),
    "QOS_TRUST_REMOVE":                _t(**{"1715": QOS_TRUST_REMOVE_1715}),

    # §2
    "L2_SWITCHPORT_TRUE":              _t(**{"1715": L2_SWITCHPORT_TRUE_1715}),
    "L2_SWITCHPORT_FALSE":             _t(**{"1715": L2_SWITCHPORT_FALSE_1715}),
    "L2_DTP_DISABLE_TRUE":             _t(**{"1715": L2_DTP_DISABLE_TRUE_1715}),
    "L2_DTP_DISABLE_FALSE":            _t(**{"1715": L2_DTP_DISABLE_FALSE_1715}),
    "L2_VOICE_FULL":                   _t(**{"1715": L2_VOICE_FULL_1715}),
    "L2_VOICE_FULL_REMOVE":            _t(**{"1715": L2_VOICE_FULL_REMOVE_1715}),
    "L2_VOICE_VLAN_ID":                _t(**{"1715": L2_VOICE_VLAN_ID_1715}),
    "L2_VOICE_VLAN_DOT1P":             _t(**{"1715": L2_VOICE_VLAN_DOT1P_1715}),
    "L2_VOICE_VLAN_NONE":              _t(**{"1715": L2_VOICE_VLAN_NONE_1715}),
    "L2_VOICE_VLAN_UNTAGGED":          _t(**{"1715": L2_VOICE_VLAN_UNTAGGED_1715}),
    "L2_VOICE_VLAN_REMOVE":            _t(**{"1715": L2_VOICE_VLAN_REMOVE_1715}),
    "L2_VOICE_DETECT":                 _t(**{"1715": L2_VOICE_DETECT_1715}),
    "L2_VOICE_DETECT_REMOVE":          _t(**{"1715": L2_VOICE_DETECT_REMOVE_1715}),
    "L2_ACCESS_VLAN":                  _t(**{"1715": L2_ACCESS_VLAN_1715}),
    "L2_ACCESS_VLAN_REMOVE":           _t(**{"1715": L2_ACCESS_VLAN_REMOVE_1715}),
    "L2_TRUNK_PRUNING_ADD":            _t(**{"1715": L2_TRUNK_PRUNING_ADD_1715}),
    "L2_TRUNK_PRUNING_REMOVE":         _t(**{"1715": L2_TRUNK_PRUNING_REMOVE_1715}),
    "L2_TRUNK_PRUNING_REPLACE":        _t(**{"1715": L2_TRUNK_PRUNING_REPLACE_1715}),
    "L2_TRUNK_PRUNING_NONE":           _t(**{"1715": L2_TRUNK_PRUNING_NONE_1715}),
    "L2_TRUNK_PRUNING_REMOVE_ALL":     _t(**{"1715": L2_TRUNK_PRUNING_REMOVE_ALL_1715}),
    "PVLAN_GLOBAL":                    _t(**{"1715": PVLAN_GLOBAL_1715}),
    "PVLAN_GLOBAL_PRIMARY":            _t(**{"1715": PVLAN_GLOBAL_PRIMARY_1715}),
    "PVLAN_GLOBAL_ASSOC":              _t(**{"1715": PVLAN_GLOBAL_ASSOC_1715}),
    "PVLAN_GLOBAL_REMOVE":             _t(**{"1715": PVLAN_GLOBAL_REMOVE_1715}),
    "PVLAN_SECONDARY":                 _t(**{"1715": PVLAN_SECONDARY_1715}),
    "PVLAN_SECONDARY_REMOVE":          _t(**{"1715": PVLAN_SECONDARY_REMOVE_1715}),
    "PVLAN_HOST_ASSOC":                _t(**{"1715": PVLAN_HOST_ASSOC_1715}),
    "PVLAN_HOST_ASSOC_REMOVE":         _t(**{"1715": PVLAN_HOST_ASSOC_REMOVE_1715}),
    "PVLAN_PROMISCUOUS_MAP":           _t(**{"1715": PVLAN_PROMISCUOUS_MAP_1715}),
    "PVLAN_PROMISCUOUS_MAP_REMOVE":    _t(**{"1715": PVLAN_PROMISCUOUS_MAP_REMOVE_1715}),
        "L2_PORTSEC_ENABLE":               _t(**{"1715": L2_PORTSEC_ENABLE_1715}),
    "L2_PORTSEC_ENABLE_REMOVE":        _t(**{"1715": L2_PORTSEC_ENABLE_REMOVE_1715}),
    "L2_PORTSEC_MAX":                  _t(**{"1715": L2_PORTSEC_MAX_1715}),
    "L2_PORTSEC_MAX_VLAN":             _t(**{"1715": L2_PORTSEC_MAX_VLAN_1715}),
    "L2_PORTSEC_MAX_REMOVE":           _t(**{"1715": L2_PORTSEC_MAX_REMOVE_1715}),
    "L2_PORTSEC_VIOLATION":            _t(**{"1715": L2_PORTSEC_VIOLATION_1715}),
    "L2_PORTSEC_VIOLATION_SHUTDOWN_VLAN": _t(**{"1715": L2_PORTSEC_VIOLATION_SHUTDOWN_VLAN_1715}),
    "L2_PORTSEC_VIOLATION_REMOVE":     _t(**{"1715": L2_PORTSEC_VIOLATION_REMOVE_1715}),
    "L2_PORTSEC_STICKY":               _t(**{"1715": L2_PORTSEC_STICKY_1715}),
    "L2_PORTSEC_STICKY_REMOVE":        _t(**{"1715": L2_PORTSEC_STICKY_REMOVE_1715}),
    "L2_PORTSEC_AGING":                _t(**{"1715": L2_PORTSEC_AGING_1715}),
    "L2_PORTSEC_AGING_REMOVE":         _t(**{"1715": L2_PORTSEC_AGING_REMOVE_1715}),
    "L2_PORTSEC_MAC_ACCESS":           _t(**{"1715": L2_PORTSEC_MAC_ACCESS_1715}),
    "L2_PORTSEC_MAC_ACCESS_REMOVE":    _t(**{"1715": L2_PORTSEC_MAC_ACCESS_REMOVE_1715}),
    "L2_PORTSEC_MAC_STICKY":           _t(**{"1715": L2_PORTSEC_MAC_STICKY_1715}),
    "L2_PORTSEC_MAC_STICKY_REMOVE":    _t(**{"1715": L2_PORTSEC_MAC_STICKY_REMOVE_1715}),
    "L2_PROTECTED":                    _t(**{"1715": L2_PROTECTED_1715}),
    "L2_PROTECTED_REMOVE":             _t(**{"1715": L2_PROTECTED_REMOVE_1715}),
    "L2_HOST":                         _t(**{"1715": L2_HOST_1715}),
    "L2_HOST_REMOVE":                  _t(**{"1715": L2_HOST_REMOVE_1715}),
    "L2_BLOCK_MULTICAST":              _t(**{"1715": L2_BLOCK_MULTICAST_1715}),
    "L2_BLOCK_MULTICAST_REMOVE":       _t(**{"1715": L2_BLOCK_MULTICAST_REMOVE_1715}),
    "L2_BLOCK_UNICAST":                _t(**{"1715": L2_BLOCK_UNICAST_1715}),
    "L2_BLOCK_UNICAST_REMOVE":         _t(**{"1715": L2_BLOCK_UNICAST_REMOVE_1715}),
    "L2_VEPA":                         _t(**{"1715": L2_VEPA_1715}),
    "L2_VEPA_REMOVE":                  _t(**{"1715": L2_VEPA_REMOVE_1715}),
    "L2PT_TUNNEL_CORE":                _t(**{"1715": L2PT_TUNNEL_CORE_1715}),
    "L2PT_TUNNEL_CORE_REMOVE":         _t(**{"1715": L2PT_TUNNEL_CORE_REMOVE_1715}),
    "L2PT_TUNNEL_P2P":                 _t(**{"1715": L2PT_TUNNEL_P2P_1715}),
    "L2PT_TUNNEL_P2P_REMOVE":          _t(**{"1715": L2PT_TUNNEL_P2P_REMOVE_1715}),
    "L2PT_TUNNEL_CORE_BLOCK":          _t(**{"1715": L2PT_TUNNEL_CORE_BLOCK_1715}),
    "L2PT_TUNNEL_CORE_BLOCK_REMOVE":   _t(**{"1715": L2PT_TUNNEL_CORE_BLOCK_REMOVE_1715}),
    "L2PT_TUNNEL_P2P_BLOCK":           _t(**{"1715": L2PT_TUNNEL_P2P_BLOCK_1715}),
    "L2PT_TUNNEL_P2P_BLOCK_REMOVE":    _t(**{"1715": L2PT_TUNNEL_P2P_BLOCK_REMOVE_1715}),
    "L2PT_DROP_THRESHOLD":             _t(**{"1715": L2PT_DROP_THRESHOLD_1715}),
    "L2PT_DROP_THRESHOLD_REMOVE":      _t(**{"1715": L2PT_DROP_THRESHOLD_REMOVE_1715}),
    "L2PT_DROP_THRESHOLD_RATE":        _t(**{"1715": L2PT_DROP_THRESHOLD_RATE_1715}),
    "L2PT_DROP_THRESHOLD_RATE_REMOVE": _t(**{"1715": L2PT_DROP_THRESHOLD_RATE_REMOVE_1715}),
    "L2PT_DROP_THRESHOLD_P2P":         _t(**{"1715": L2PT_DROP_THRESHOLD_P2P_1715}),
    "L2PT_DROP_THRESHOLD_P2P_REMOVE":  _t(**{"1715": L2PT_DROP_THRESHOLD_P2P_REMOVE_1715}),
    "L2PT_SHUTDOWN_THRESHOLD":         _t(**{"1715": L2PT_SHUTDOWN_THRESHOLD_1715}),
    "L2PT_SHUTDOWN_THRESHOLD_REMOVE":  _t(**{"1715": L2PT_SHUTDOWN_THRESHOLD_REMOVE_1715}),
    "L2PT_SHUTDOWN_THRESHOLD_RATE":    _t(**{"1715": L2PT_SHUTDOWN_THRESHOLD_RATE_1715}),
    "L2PT_SHUTDOWN_THRESHOLD_RATE_REMOVE": _t(**{"1715": L2PT_SHUTDOWN_THRESHOLD_RATE_REMOVE_1715}),
    "L2PT_SHUTDOWN_THRESHOLD_P2P":     _t(**{"1715": L2PT_SHUTDOWN_THRESHOLD_P2P_1715}),
    "L2PT_SHUTDOWN_THRESHOLD_P2P_REMOVE": _t(**{"1715": L2PT_SHUTDOWN_THRESHOLD_P2P_REMOVE_1715}),
    "L2PT_FORWARD_PROTOCOL":           _t(**{"1715": L2PT_FORWARD_PROTOCOL_1715}),
    "L2PT_FORWARD_PROTOCOL_REMOVE":    _t(**{"1715": L2PT_FORWARD_PROTOCOL_REMOVE_1715}),
    "L2PT_FORWARD_BLOCK":              _t(**{"1715": L2PT_FORWARD_BLOCK_1715}),
    "L2PT_FORWARD_BLOCK_REMOVE":       _t(**{"1715": L2PT_FORWARD_BLOCK_REMOVE_1715}),
    "L2PT_FORWARD_DROP":               _t(**{"1715": L2PT_FORWARD_DROP_1715}),
    "L2PT_FORWARD_DROP_REMOVE":        _t(**{"1715": L2PT_FORWARD_DROP_REMOVE_1715}),
    "L2PT_FORWARD_SHUTDOWN":           _t(**{"1715": L2PT_FORWARD_SHUTDOWN_1715}),
    "L2PT_FORWARD_SHUTDOWN_REMOVE":    _t(**{"1715": L2PT_FORWARD_SHUTDOWN_REMOVE_1715}),

    # §3
    "ARP_TIMEOUT":                     _t(**{"1715": ARP_TIMEOUT_1715}),
    "ARP_TIMEOUT_REMOVE":              _t(**{"1715": ARP_TIMEOUT_REMOVE_1715}),
    "ARP_SNAP_TRUE":                   _t(**{"1715": ARP_SNAP_TRUE_1715}),
    "ARP_SNAP_FALSE":                  _t(**{"1715": ARP_SNAP_FALSE_1715}),
    "ARP_ENTRY_LIMIT":                 _t(**{"1715": ARP_ENTRY_LIMIT_1715}),
    "ARP_ENTRY_LIMIT_REMOVE":          _t(**{"1715": ARP_ENTRY_LIMIT_REMOVE_1715}),
    "ARP_PACKET_PRIORITY":             _t(**{"1715": ARP_PACKET_PRIORITY_1715}),
    "ARP_PACKET_PRIORITY_REMOVE":      _t(**{"1715": ARP_PACKET_PRIORITY_REMOVE_1715}),
    "PQ_OUT_ENABLE":                   _t(**{"1715": PQ_OUT_ENABLE_1715}),
    "PQ_OUT_ENABLE_REMOVE":            _t(**{"1715": PQ_OUT_ENABLE_REMOVE_1715}),
    "PQ_COS_MAP":                      _t(**{"1715": PQ_COS_MAP_1715}),
    "PQ_COS_MAP_REMOVE":               _t(**{"1715": PQ_COS_MAP_REMOVE_1715}),
    "RCV_QUEUE_COS_MAP":               _t(**{"1715": RCV_QUEUE_COS_MAP_1715}),
    "RCV_QUEUE_COS_MAP_REMOVE":        _t(**{"1715": RCV_QUEUE_COS_MAP_REMOVE_1715}),
    "FLOWCONTROL":                     _t(**{"1715": FLOWCONTROL_1715}),
    "FLOWCONTROL_REMOVE":              _t(**{"1715": FLOWCONTROL_REMOVE_1715}),
    "HOLD_QUEUE":                      _t(**{"1715": HOLD_QUEUE_1715}),
    "HOLD_QUEUE_REMOVE":               _t(**{"1715": HOLD_QUEUE_REMOVE_1715}),
    "LINK_BANDWIDTH":                  _t(**{"1715": LINK_BANDWIDTH_1715}),
    "LINK_BANDWIDTH_REMOVE":           _t(**{"1715": LINK_BANDWIDTH_REMOVE_1715}),
    "LINK_BANDWIDTH_QOS_REF":          _t(**{"1715": LINK_BANDWIDTH_QOS_REF_1715}),
    "LINK_BANDWIDTH_QOS_REF_REMOVE":   _t(**{"1715": LINK_BANDWIDTH_QOS_REF_REMOVE_1715}),
    "DAMPENING_FULL":                  _t(**{"1715": DAMPENING_FULL_1715}),
    "DAMPENING_DEFAULT":               _t(**{"1715": DAMPENING_DEFAULT_1715}),
    "DAMPENING_REMOVE":                _t(**{"1715": DAMPENING_REMOVE_1715}),
    "SRLG":                            _t(**{"1715": SRLG_1715}),
    "SRLG_REMOVE":                     _t(**{"1715": SRLG_REMOVE_1715}),
    "DOMAIN_NAME":                     _t(**{"1715": DOMAIN_NAME_1715}),
    "DOMAIN_NAME_REMOVE":              _t(**{"1715": DOMAIN_NAME_REMOVE_1715}),
    "DOMAIN_PATH":                     _t(**{"1715": DOMAIN_PATH_1715}),
    "DOMAIN_PATH_REMOVE":              _t(**{"1715": DOMAIN_PATH_REMOVE_1715}),
    "KEEPALIVE_TIMERS":                _t(**{"1715": KEEPALIVE_TIMERS_1715}),
    "KEEPALIVE_TIMERS_REMOVE":         _t(**{"1715": KEEPALIVE_TIMERS_REMOVE_1715}),
    "KEEPALIVE_DISABLE":               _t(**{"1715": KEEPALIVE_DISABLE_1715}),
    "LINK_LOGGING_LINK_STATUS":        _t(**{"1715": LINK_LOGGING_LINK_STATUS_1715}),
    "LINK_LOGGING_LINK_STATUS_REMOVE": _t(**{"1715": LINK_LOGGING_LINK_STATUS_REMOVE_1715}),
    "LINK_LOGGING_EVENT":              _t(**{"1715": LINK_LOGGING_EVENT_1715}),
    "LINK_LOGGING_EVENT_REMOVE":       _t(**{"1715": LINK_LOGGING_EVENT_REMOVE_1715}),
    "LINK_LOGGING_EVENTS_BLOCK":       _t(**{"1715": LINK_LOGGING_EVENTS_BLOCK_1715}),
    "LINK_LOGGING_EVENTS_BLOCK_REMOVE":_t(**{"1715": LINK_LOGGING_EVENTS_BLOCK_REMOVE_1715}),
    "LINK_LOGGING_SPANNING_TREE":      _t(**{"1715": LINK_LOGGING_SPANNING_TREE_1715}),
    "LINK_LOGGING_SPANNING_TREE_REMOVE": _t(**{"1715": LINK_LOGGING_SPANNING_TREE_REMOVE_1715}),
    "LINK_LOGGING_SUBIF":              _t(**{"1715": LINK_LOGGING_SUBIF_1715}),
    "LINK_LOGGING_SUBIF_REMOVE":       _t(**{"1715": LINK_LOGGING_SUBIF_REMOVE_1715}),
    "FAIR_QUEUE":                      _t(**{"1715": FAIR_QUEUE_1715}),
    "FAIR_QUEUE_REMOVE":               _t(**{"1715": FAIR_QUEUE_REMOVE_1715}),
    "FAIR_QUEUE_CONF":                 _t(**{"1715": FAIR_QUEUE_CONF_1715}),

    # §4
    "IP4_PRIMARY":                     _t(**{"1715": IP4_PRIMARY_1715}),
    "IP4_PRIMARY_REMOVE":              _t(**{"1715": IP4_PRIMARY_REMOVE_1715}),
    "IP4_SECONDARY":                   _t(**{"1715": IP4_SECONDARY_1715}),
    "IP4_SECONDARY_REMOVE":            _t(**{"1715": IP4_SECONDARY_REMOVE_1715}),
    "IP4_DHCP":                        _t(**{"1715": IP4_DHCP_1715}),
    "IP4_DHCP_REMOVE":                 _t(**{"1715": IP4_DHCP_REMOVE_1715}),
    "IP4_NEGOTIATED":                  _t(**{"1715": IP4_NEGOTIATED_1715}),
    "IP4_NEGOTIATED_REMOVE":           _t(**{"1715": IP4_NEGOTIATED_REMOVE_1715}),
    "IP4_DHCP_OPTIONS":                _t(**{"1715": IP4_DHCP_OPTIONS_1715}),
    "IP4_UNNUMBERED":                  _t(**{"1715": IP4_UNNUMBERED_1715}),
    "IP4_UNNUMBERED_REMOVE":           _t(**{"1715": IP4_UNNUMBERED_REMOVE_1715}),
    "IP4_ACCESS_GROUP_IN":             _t(**{"1715": IP4_ACCESS_GROUP_IN_1715}),
    "IP4_ACCESS_GROUP_IN_REMOVE":      _t(**{"1715": IP4_ACCESS_GROUP_IN_REMOVE_1715}),
    "IP4_ACCESS_GROUP_OUT":            _t(**{"1715": IP4_ACCESS_GROUP_OUT_1715}),
    "IP4_ACCESS_GROUP_OUT_REMOVE":     _t(**{"1715": IP4_ACCESS_GROUP_OUT_REMOVE_1715}),
    "IP4_ACCESS_GROUP_COMMON_IN":      _t(**{"1715": IP4_ACCESS_GROUP_COMMON_IN_1715}),
    "IP4_ACCESS_GROUP_COMMON_IN_REMOVE": _t(**{"1715": IP4_ACCESS_GROUP_COMMON_IN_REMOVE_1715}),
    "IP4_ACCESS_GROUP_COMMON_OUT":     _t(**{"1715": IP4_ACCESS_GROUP_COMMON_OUT_1715}),
    "IP4_ACCESS_GROUP_COMMON_OUT_REMOVE": _t(**{"1715": IP4_ACCESS_GROUP_COMMON_OUT_REMOVE_1715}),
    "IP4_VRF_FORWARDING":              _t(**{"1715": IP4_VRF_FORWARDING_1715}),
    "IP4_VRF_FORWARDING_REMOVE":       _t(**{"1715": IP4_VRF_FORWARDING_REMOVE_1715}),
    "IP4_VRF_RECEIVE":                 _t(**{"1715": IP4_VRF_RECEIVE_1715}),
    "IP4_VRF_RECEIVE_REMOVE":          _t(**{"1715": IP4_VRF_RECEIVE_REMOVE_1715}),
    "IP4_VRF_SITEMAP":                 _t(**{"1715": IP4_VRF_SITEMAP_1715}),
    "IP4_VRF_SITEMAP_REMOVE":          _t(**{"1715": IP4_VRF_SITEMAP_REMOVE_1715}),
    "IP4_HELPER":                      _t(**{"1715": IP4_HELPER_1715}),
    "IP4_HELPER_REMOVE":               _t(**{"1715": IP4_HELPER_REMOVE_1715}),
    "IP4_HELPER_GLOBAL":               _t(**{"1715": IP4_HELPER_GLOBAL_1715}),
    "IP4_HELPER_GLOBAL_REMOVE":        _t(**{"1715": IP4_HELPER_GLOBAL_REMOVE_1715}),
    "IP4_HELPER_VRF":                  _t(**{"1715": IP4_HELPER_VRF_1715}),
    "IP4_HELPER_VRF_REMOVE":           _t(**{"1715": IP4_HELPER_VRF_REMOVE_1715}),
    "IP4_POLICY_ROUTE_MAP":            _t(**{"1715": IP4_POLICY_ROUTE_MAP_1715}),
    "IP4_POLICY_ROUTE_MAP_REMOVE":     _t(**{"1715": IP4_POLICY_ROUTE_MAP_REMOVE_1715}),
    "IP4_PROXY_ARP":                   _t(**{"1715": IP4_PROXY_ARP_1715}),
    "IP4_LOCAL_PROXY_ARP":             _t(**{"1715": IP4_LOCAL_PROXY_ARP_1715}),
    "IP4_LOCAL_PROXY_ARP_REMOVE":      _t(**{"1715": IP4_LOCAL_PROXY_ARP_REMOVE_1715}),
    "IP4_REDIRECTS":                   _t(**{"1715": IP4_REDIRECTS_1715}),
    "IP4_CLEAR_DF":                    _t(**{"1715": IP4_CLEAR_DF_1715}),
    "IP4_TCP_MSS":                     _t(**{"1715": IP4_TCP_MSS_1715}),
    "IP4_TCP_MSS_REMOVE":              _t(**{"1715": IP4_TCP_MSS_REMOVE_1715}),
    "IP4_MTU":                         _t(**{"1715": IP4_MTU_1715}),
    "IP4_MTU_REMOVE":                  _t(**{"1715": IP4_MTU_REMOVE_1715}),
    "IP4_URPF":                        _t(**{"1715": IP4_URPF_1715}),
    "IP4_URPF_REMOVE":                 _t(**{"1715": IP4_URPF_REMOVE_1715}),
    "IP4_ARP_INSPECT_TRUST":           _t(**{"1715": IP4_ARP_INSPECT_TRUST_1715}),
    "IP4_ARP_INSPECT_TRUST_REMOVE":    _t(**{"1715": IP4_ARP_INSPECT_TRUST_REMOVE_1715}),
    "IP4_ARP_INSPECT_RATE":            _t(**{"1715": IP4_ARP_INSPECT_RATE_1715}),
    "IP4_ARP_INSPECT_RATE_REMOVE":     _t(**{"1715": IP4_ARP_INSPECT_RATE_REMOVE_1715}),
    "IP4_ARP_INSPECT_RATE_NONE":       _t(**{"1715": IP4_ARP_INSPECT_RATE_NONE_1715}),
    "IP4_DIRECTED_BROADCAST":          _t(**{"1715": IP4_DIRECTED_BROADCAST_1715}),
    "IP4_DIRECTED_BROADCAST_REMOVE":   _t(**{"1715": IP4_DIRECTED_BROADCAST_REMOVE_1715}),
    "IP4_DIRECTED_BROADCAST_ACL":      _t(**{"1715": IP4_DIRECTED_BROADCAST_ACL_1715}),

    # §5
    "IP6_ENABLE":                      _t(**{"1715": IP6_ENABLE_1715}),
    "IP6_ENABLE_REMOVE":               _t(**{"1715": IP6_ENABLE_REMOVE_1715}),
    "IP6_ADDRESS_PREFIX":              _t(**{"1715": IP6_ADDRESS_PREFIX_1715}),
    "IP6_ADDRESS_PREFIX_REMOVE":       _t(**{"1715": IP6_ADDRESS_PREFIX_REMOVE_1715}),
    "IP6_ADDRESS_EUI64":               _t(**{"1715": IP6_ADDRESS_EUI64_1715}),
    "IP6_ADDRESS_EUI64_REMOVE":        _t(**{"1715": IP6_ADDRESS_EUI64_REMOVE_1715}),
    "IP6_ADDRESS_ANYCAST":             _t(**{"1715": IP6_ADDRESS_ANYCAST_1715}),
    "IP6_ADDRESS_ANYCAST_REMOVE":      _t(**{"1715": IP6_ADDRESS_ANYCAST_REMOVE_1715}),
    "IP6_ADDRESS_LINK_LOCAL":          _t(**{"1715": IP6_ADDRESS_LINK_LOCAL_1715}),
    "IP6_ADDRESS_LINK_LOCAL_REMOVE":   _t(**{"1715": IP6_ADDRESS_LINK_LOCAL_REMOVE_1715}),
    "IP6_ADDRESS_AUTOCONFIG":          _t(**{"1715": IP6_ADDRESS_AUTOCONFIG_1715}),
    "IP6_ADDRESS_AUTOCONFIG_REMOVE":   _t(**{"1715": IP6_ADDRESS_AUTOCONFIG_REMOVE_1715}),
    "IP6_ADDRESS_AUTOCONFIG_DEFAULT":  _t(**{"1715": IP6_ADDRESS_AUTOCONFIG_DEFAULT_1715}),
    "IP6_ADDRESS_AUTOCONFIG_DEFAULT_REMOVE": _t(**{"1715": IP6_ADDRESS_AUTOCONFIG_DEFAULT_REMOVE_1715}),
    "IP6_ADDRESS_DHCP":                _t(**{"1715": IP6_ADDRESS_DHCP_1715}),
    "IP6_ADDRESS_DHCP_REMOVE":         _t(**{"1715": IP6_ADDRESS_DHCP_REMOVE_1715}),
    "IP6_ADDRESS_DHCP_RAPID_COMMIT":   _t(**{"1715": IP6_ADDRESS_DHCP_RAPID_COMMIT_1715}),
    "IP6_ADDRESS_DHCP_RAPID_COMMIT_REMOVE": _t(**{"1715": IP6_ADDRESS_DHCP_RAPID_COMMIT_REMOVE_1715}),
    "IP6_ADDRESS_PREFIX_NAME":         _t(**{"1715": IP6_ADDRESS_PREFIX_NAME_1715}),
    "IP6_ADDRESS_PREFIX_NAME_REMOVE":  _t(**{"1715": IP6_ADDRESS_PREFIX_NAME_REMOVE_1715}),
    "IP6_UNNUMBERED":                  _t(**{"1715": IP6_UNNUMBERED_1715}),
    "IP6_UNNUMBERED_REMOVE":           _t(**{"1715": IP6_UNNUMBERED_REMOVE_1715}),
    "IP6_MTU":                         _t(**{"1715": IP6_MTU_1715}),
    "IP6_MTU_REMOVE":                  _t(**{"1715": IP6_MTU_REMOVE_1715}),
    "IP6_ND_DAD_ATTEMPTS":             _t(**{"1715": IP6_ND_DAD_ATTEMPTS_1715}),
    "IP6_ND_DAD_ATTEMPTS_REMOVE":      _t(**{"1715": IP6_ND_DAD_ATTEMPTS_REMOVE_1715}),
    "IP6_ND_NUD_IGP":                  _t(**{"1715": IP6_ND_NUD_IGP_1715}),
    "IP6_TCP_ADJUST_MSS":              _t(**{"1715": IP6_TCP_ADJUST_MSS_1715}),
    "IP6_TCP_ADJUST_MSS_REMOVE":       _t(**{"1715": IP6_TCP_ADJUST_MSS_REMOVE_1715}),
    "IP6_TRAFFIC_FILTER":              _t(**{"1715": IP6_TRAFFIC_FILTER_1715}),
    "IP6_TRAFFIC_FILTER_REMOVE":       _t(**{"1715": IP6_TRAFFIC_FILTER_REMOVE_1715}),
    "IP6_SOURCE_GUARD":                _t(**{"1715": IP6_SOURCE_GUARD_1715}),
    "IP6_SOURCE_GUARD_REMOVE":         _t(**{"1715": IP6_SOURCE_GUARD_REMOVE_1715}),
    "IP6_VERIFY_UNICAST_REVERSE_PATH": _t(**{"1715": IP6_VERIFY_UNICAST_REVERSE_PATH_1715}),
    "IP6_VERIFY_UNICAST_REVERSE_PATH_REMOVE": _t(**{"1715": IP6_VERIFY_UNICAST_REVERSE_PATH_REMOVE_1715}),

    # §6
    "AS_PORT_CONTROL":                 _t(**{"1715": AS_PORT_CONTROL_1715}),
    "AS_PORT_CONTROL_REMOVE":          _t(**{"1715": AS_PORT_CONTROL_REMOVE_1715}),
    "AS_CONTROL_DIRECTION":            _t(**{"1715": AS_CONTROL_DIRECTION_1715}),
    "AS_CONTROL_DIRECTION_REMOVE":     _t(**{"1715": AS_CONTROL_DIRECTION_REMOVE_1715}),
    "AS_HOST_MODE":                    _t(**{"1715": AS_HOST_MODE_1715}),
    "AS_HOST_MODE_REMOVE":             _t(**{"1715": AS_HOST_MODE_REMOVE_1715}),
    "AS_HOST_MODE_PEER":               _t(**{"1715": AS_HOST_MODE_PEER_1715}),
    "AS_HOST_MODE_PEER_REMOVE":        _t(**{"1715": AS_HOST_MODE_PEER_REMOVE_1715}),
    "AS_MONITOR":                      _t(**{"1715": AS_MONITOR_1715}),

    # §7
    "SC_ACTION_LEVEL":                 _t(**{"1715": SC_ACTION_LEVEL_1715}),
    "SC_ACTION_SHUTDOWN":              _t(**{"1715": SC_ACTION_SHUTDOWN_1715}),
    "SC_ACTION_TRAP":                  _t(**{"1715": SC_ACTION_TRAP_1715}),
    "SC_ACTION_REMOVE":                _t(**{"1715": SC_ACTION_REMOVE_1715}),
    "SC_THRESHOLD_PERCENT":            _t(**{"1715": SC_THRESHOLD_PERCENT_1715}),
    "SC_THRESHOLD_REMOVE":             _t(**{"1715": SC_THRESHOLD_REMOVE_1715}),
    "SC_BROADCAST_INCLUDE_MULTICAST":  _t(**{"1715": SC_BROADCAST_INCLUDE_MULTICAST_1715}),
    "SC_BROADCAST_INCLUDE_MULTICAST_REMOVE": _t(**{"1715": SC_BROADCAST_INCLUDE_MULTICAST_REMOVE_1715}),

    # §8
    "MSEC_ENABLE":                     _t(**{"1715": MSEC_ENABLE_1715}),
    "MSEC_ENABLE_REMOVE":              _t(**{"1715": MSEC_ENABLE_REMOVE_1715}),
    "MSEC_REPLAY_PROTECTION":          _t(**{"1715": MSEC_REPLAY_PROTECTION_1715}),
    "MSEC_REPLAY_PROTECTION_REMOVE":   _t(**{"1715": MSEC_REPLAY_PROTECTION_REMOVE_1715}),

    # §9
    "MISC_SUBSCRIBER_INACTIVITY":        _t(**{"1715": MISC_SUBSCRIBER_INACTIVITY_1715}),
    "MISC_SUBSCRIBER_INACTIVITY_REMOVE": _t(**{"1715": MISC_SUBSCRIBER_INACTIVITY_REMOVE_1715}),
    "MISC_SUBSCRIBER_PROBE":             _t(**{"1715": MISC_SUBSCRIBER_PROBE_1715}),
    "MISC_SUBSCRIBER_PROBE_REMOVE":      _t(**{"1715": MISC_SUBSCRIBER_PROBE_REMOVE_1715}),

    # §10
    "PHY_MEDIA_TYPE":                  _t(**{"1715": PHY_MEDIA_TYPE_1715}),
    "PHY_MEDIA_TYPE_REMOVE":           _t(**{"1715": PHY_MEDIA_TYPE_REMOVE_1715}),
    "PHY_FEC":                         _t(**{"1715": PHY_FEC_1715}),
    "PHY_FEC_REMOVE":                  _t(**{"1715": PHY_FEC_REMOVE_1715}),

    # §11
    "PO_LOAD_BALANCE_HASH_ALGO":       _t(**{"1715": PO_LOAD_BALANCE_HASH_ALGO_1715}),
    "PO_LOAD_BALANCE_HASH_ALGO_REMOVE":_t(**{"1715": PO_LOAD_BALANCE_HASH_ALGO_REMOVE_1715}),
    "PO_MIN_LINKS":                    _t(**{"1715": PO_MIN_LINKS_1715}),
    "PO_MIN_LINKS_REMOVE":             _t(**{"1715": PO_MIN_LINKS_REMOVE_1715}),
    "PO_STANDALONE_DISABLE":           _t(**{"1715": PO_STANDALONE_DISABLE_1715}),
    "PO_STANDALONE_DISABLE_REMOVE":    _t(**{"1715": PO_STANDALONE_DISABLE_REMOVE_1715}),

    # §12
    "TYPE_VLAN_AUTOSTATE":             _t(**{"1715": TYPE_VLAN_AUTOSTATE_1715}),
    "TYPE_TUNNEL_QOS_PRE_CLASSIFY":    _t(**{"1715": TYPE_TUNNEL_QOS_PRE_CLASSIFY_1715}),
    "TYPE_TUNNEL_QOS_PRE_CLASSIFY_REMOVE": _t(**{"1715": TYPE_TUNNEL_QOS_PRE_CLASSIFY_REMOVE_1715}),

    # §13
    "NVE_HOST_REACHABILITY_BGP":        _t(**{"1715": NVE_HOST_REACHABILITY_BGP_1715}),
    "NVE_HOST_REACHABILITY_BGP_REMOVE": _t(**{"1715": NVE_HOST_REACHABILITY_BGP_REMOVE_1715}),
    "NVE_SOURCE_INTERFACE":             _t(**{"1715": NVE_SOURCE_INTERFACE_1715}),
    "NVE_SOURCE_INTERFACE_REMOVE":      _t(**{"1715": NVE_SOURCE_INTERFACE_REMOVE_1715}),
    "NVE_MEMBER_VNI_VRF":               _t(**{"1715": NVE_MEMBER_VNI_VRF_1715}),
    "NVE_MEMBER_VNI_VRF_REMOVE":        _t(**{"1715": NVE_MEMBER_VNI_VRF_REMOVE_1715}),
    "NVE_MEMBER_VNI_MCAST_GROUP":       _t(**{"1715": NVE_MEMBER_VNI_MCAST_GROUP_1715}),
    "NVE_MEMBER_VNI_MCAST_GROUP_REMOVE":_t(**{"1715": NVE_MEMBER_VNI_MCAST_GROUP_REMOVE_1715}),

    # §14
    "VLAN_CREATE":                      _t(**{"1715": VLAN_CREATE_1715}),
    "VLAN_DELETE":                      _t(**{"1715": VLAN_DELETE_1715}),
    "VLAN_NAME":                        _t(**{"1715": VLAN_NAME_1715}),
    "VLAN_NAME_REMOVE":                 _t(**{"1715": VLAN_NAME_REMOVE_1715}),
    "VLAN_STATE":                       _t(**{"1715": VLAN_STATE_1715}),
    "VLAN_STATE_REMOVE":                _t(**{"1715": VLAN_STATE_REMOVE_1715}),
    "VLAN_SHUTDOWN":                    _t(**{"1715": VLAN_SHUTDOWN_1715}),
    "VLAN_SHUTDOWN_REMOVE":             _t(**{"1715": VLAN_SHUTDOWN_REMOVE_1715}),
    "VLAN_REMOTE_SPAN":                 _t(**{"1715": VLAN_REMOTE_SPAN_1715}),
        "VLAN_REMOTE_SPAN":                 _t(**{"1715": VLAN_REMOTE_SPAN_1715}),
    "VLAN_REMOTE_SPAN_REMOVE":          _t(**{"1715": VLAN_REMOTE_SPAN_REMOVE_1715}),
    "VLAN_UNI":                         _t(**{"1715": VLAN_UNI_1715}),
    "VLAN_UNI_REMOVE":                  _t(**{"1715": VLAN_UNI_REMOVE_1715}),
    "VLAN_GROUP":                       _t(**{"1715": VLAN_GROUP_1715}),
    "VLAN_GROUP_REMOVE":                _t(**{"1715": VLAN_GROUP_REMOVE_1715}),
    "VLAN_GROUP_MEMBER_REMOVE":         _t(**{"1715": VLAN_GROUP_MEMBER_REMOVE_1715}),
    "VLAN_FILTER":                      _t(**{"1715": VLAN_FILTER_1715}),
    "VLAN_FILTER_REMOVE":               _t(**{"1715": VLAN_FILTER_REMOVE_1715}),
    "VLAN_DOT1Q_TAG_NATIVE":            _t(**{"1715": VLAN_DOT1Q_TAG_NATIVE_1715}),
    "VLAN_DOT1Q_TAG_NATIVE_REMOVE":     _t(**{"1715": VLAN_DOT1Q_TAG_NATIVE_REMOVE_1715}),
    "VLAN_INTERNAL_ALLOCATION":         _t(**{"1715": VLAN_INTERNAL_ALLOCATION_1715}),
    "VLAN_INTERNAL_ALLOCATION_REMOVE":  _t(**{"1715": VLAN_INTERNAL_ALLOCATION_REMOVE_1715}),
    "VLAN_ACCOUNTING":                  _t(**{"1715": VLAN_ACCOUNTING_1715}),
    "VLAN_ACCOUNTING_REMOVE":           _t(**{"1715": VLAN_ACCOUNTING_REMOVE_1715}),
    "SVI_PRIVATE_VLAN_MAPPING":         _t(**{"1715": SVI_PRIVATE_VLAN_MAPPING_1715}),
    "SVI_PRIVATE_VLAN_MAPPING_REMOVE":  _t(**{"1715": SVI_PRIVATE_VLAN_MAPPING_REMOVE_1715}),
}


# Register NOT_PRESENT families with a None slot so resolve() reports the reason
# rather than "unknown family". Collision with an explicit entry aborts the import.
for _name in NOT_PRESENT:
    if _name in TEMPLATES:
        raise ValueError(
            f"{_name} is both defined in TEMPLATES and listed in NOT_PRESENT"
        )
    TEMPLATES[_name] = _t()


# ================================================================
# RESOLVERS
# ================================================================

def resolve(base, train="1715"):
    """Return the template for base/train. Raises with status + reason when unavailable."""
    if base not in TEMPLATES:
        raise KeyError(f"{base!r} not in 17.15 catalogue ({len(TEMPLATES)} families)")
    tpl = TEMPLATES[base].get(train)
    if tpl is None:
        entry = NOT_PRESENT.get(base, ("ABSENT", "no template"))
        status, why = entry if isinstance(entry, tuple) else ("ABSENT", str(entry))
        raise KeyError(f"{base!r} not available on train {train!r} [{status}]: {why}")
    return tpl


def families():
    for name in sorted(TEMPLATES):
        yield name


def supported_on(train="1715"):
    for name, slots in TEMPLATES.items():
        if slots.get(train) is not None:
            yield name


def not_present(status=None):
    """Yield (family, status, reason); defensive against non-tuple entries."""
    for name in sorted(NOT_PRESENT):
        entry = NOT_PRESENT[name]
        if isinstance(entry, tuple) and len(entry) == 2:
            st, why = entry
        else:
            st, why = "ABSENT", str(entry)
        if status is None or st == status:
            yield name, st, why


def on_off_pairs(train="1715"):
    for base in TEMPLATES:
        if base.endswith("_REMOVE"):
            continue
        twin = base + "_REMOVE"
        if twin in TEMPLATES and TEMPLATES[twin].get(train) is not None \
                and TEMPLATES[base].get(train) is not None:
            yield (base, twin)


def flag_symmetric(train="1715"):
    for base, slots in TEMPLATES.items():
        tpl = slots.get(train)
        if tpl and "$flag" in tpl:
            yield base


# ================================================================
# PLACEHOLDER VALIDATION
# ================================================================
_ALLOWED = {
    "parent", "name", "desc", "export", "mac",
    "voice_vlan", "access_vlan", "vlans", "primary_vlan", "secondary_vlan", "secondary_vlans",
    "vlan_kind", "pvlan_type", "max", "violation", "minutes", "aging_type", "hwaddr", "window",
    "mtu", "delay", "seconds", "percent", "flag", "svc", "device",
    "auto_block", "speed_block", "duplex_block", "mode_block",
    "proto", "p2p_proto", "pps", "core_block", "p2p_block", "proto_block",
    "secs", "count", "log_secs", "qid", "tid", "cos_values_block",
    "direction", "qlen", "rx", "tx", "kbps",
    "half_life", "reuse", "suppress", "max_suppress",
    "srlg_values_block", "domain", "sp_path", "path_id",
    "period", "retries",
    "event", "events_block", "ignore_bulk_block",
    "ip", "mask", "src_if", "acl", "common_acl", "vrf", "route_map",
    "helper", "via", "allow_block", "acl_block", "burst_block", "ip_mtu", "mss",
    "client_id_block", "hostname_block",
    "ipv6", "ll", "pfx_name", "attempts", "ip6_mtu", "policy_block",
    "pc", "dir", "hm",
    "pct", "sc_type", "rise", "fall",
    "probe_block",
    "media", "fec", "algo", "min_links",
    "src_type", "src_name", "vni", "mc_min", "mc_max_block",
    "vlan_id", "vlan_name", "vlan_state", "uni_type", "group_name", "map_name",
    "policy", "accounting_block", "mapping",
    "N", "NC", "SW", "ST", "VLAN",
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
        raise ValueError(
            "interfaces_1715_xml: placeholder validation failed:\n  "
            + "\n  ".join(errors)
        )


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
}

_TYPES_VERIFIED = (
    "AppNav-Compress", "AppNav-UnCompress", "ATM-ACR", "ATM-ACRsubinterface", "BDI", "CEM",
    "CEM-ACR", "Embedded-Service-Engine", "Ethernet", "FastEthernet", "GigabitEthernet",
    "FiveGigabitEthernet", "AppGigabitEthernet", "TwentyFiveGigE", "TwoGigabitEthernet",
    "FortyGigabitEthernet", "FiftyGigabitEthernet", "HundredGigE", "TwoHundredGigE",
    "FourHundredGigE", "L2LISP", "L2LISP-subinterface", "LISP", "LISP-subinterface",
    "Loopback", "LORAWAN", "WPAN", "Virtual-WPAN", "Multilink", "nve", "overlay",
    "Port-channel", "Port-channel-subinterface", "PRP-channel", "pseudowire", "SM",
    "Cellular", "Dialer", "Serial", "Async", "TenGigabitEthernet", "Tunnel",
    "Virtual-Template", "Vlan", "VirtualPortGroup", "vasileft", "vasiright", "BD-VIF",
    "MFR", "Serial-subinterface", "Bundle",
)
_TYPES_EXTRA = (
    "ATM", "ATM-subinterface", "MFR-subinterface", "ucse", "Ethernet-Internal",
    "Service-Engine", "GMPLS", "Group-Async", "Vif", "vmi", "Virtual-PPP",
    "Wlan-GigabitEthernet", "TwentyFiveGigabitEthernet",
)
KNOWN_INTERFACE_TYPES = frozenset(_TYPES_VERIFIED + _TYPES_EXTRA)

NATIVE_SCOPED = frozenset(
    n for n in TEMPLATES
    if n.startswith(("PVLAN_GLOBAL", "PVLAN_SECONDARY", "VLAN_"))
)


def render(base, train="1715", **kw):
    return _Template(resolve(base, train)).substitute({**NS, **kw})


def wrap_native(*bodies):
    return f'<native xmlns="{NS["N"]}" xmlns:nc="{NS["NC"]}">{"".join(bodies)}</native>'


def wrap_interface(parent, name, *bodies, strict=False):
    parts = [p for p in parent.split("/") if p]
    if not parts:
        raise ValueError("parent is required")
    if strict and parts[0] not in KNOWN_INTERFACE_TYPES:
        raise ValueError(f"unknown interface type {parts[0]!r}")
    opening = "".join(f"<{p}>" for p in parts)
    closing = "".join(f"</{p}>" for p in reversed(parts))
    return wrap_native(
        f'<interface>{opening}<name>{name}</name>{"".join(bodies)}{closing}</interface>'
    )


def build_config(base, parent=None, name=None, train="1715", strict=False, **kw):
    """Complete NETCONF <config> payload for one family; picks the right scaffold automatically.
    strict=True additionally enforces interface-type applicability via applies_to()."""
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
                raise ValueError(f"{base} is not defined on {path!r} in 17.15")
        inner = wrap_interface(parent, name, body, strict=strict)
    return f'<config xmlns="{NS["NC"]}">{inner}</config>'
def diff_vs_179():
    for fam in sorted(DIFFS_VS_179):
        yield fam, DIFFS_VS_179[fam]


def _selftest():
    import xml.dom.minidom as md

    class _Dummy(dict):
        def __missing__(self, key):
            return "x"

    ok = 0
    for fam in supported_on():
        xml = _Template(resolve(fam)).substitute(_Dummy(NS))
        md.parseString(f'<r xmlns:nc="{NS["NC"]}">{xml}</r>')
        ok += 1
    md.parseString(build_config("DESCRIPTION", "GigabitEthernet", "1/0/1", desc="uplink"))
    md.parseString(build_config("L2_VEPA", "Port-channel-subinterface/Port-channel", "1.100"))
    md.parseString(build_config("VLAN_NAME", vlan_id=10, vlan_name="users"))
    md.parseString(build_config("PVLAN_GLOBAL", primary_vlan=100, secondary_vlans="101,102"))
    assert "VLAN_NAME" in NATIVE_SCOPED and "DESCRIPTION" not in NATIVE_SCOPED
    for fam in DIFFS_VS_179:
        assert fam in TEMPLATES, fam
    print(f"selftest OK: {ok} families render to well-formed XML; "
          f"{len(NATIVE_SCOPED)} native-scoped; {len(DIFFS_VS_179)} flagged vs 17.9; "
          f"{len(list(on_off_pairs()))} on/off pairs")


if __name__ == "__main__":
    _selftest()


# ================================================================
# APPLICABILITY  (interface-type gates used by build_config(strict=True))
# ================================================================
SWITCHPORT_TYPES = frozenset({
    "FastEthernet", "GigabitEthernet", "TwoGigabitEthernet", "FiveGigabitEthernet",
    "AppGigabitEthernet", "TenGigabitEthernet", "TwentyFiveGigE", "FortyGigabitEthernet",
    "HundredGigE", "Port-channel", "Port-channel-subinterface/Port-channel",
    "ucse", "Ethernet-Internal", "Wlan-GigabitEthernet",
})

_COMMON_PATHS = frozenset(KNOWN_INTERFACE_TYPES)

_APPLICABILITY = (
    (("L2_", "PVLAN_HOST_ASSOC", "PVLAN_PROMISCUOUS_MAP"), SWITCHPORT_TYPES),
    (("MSEC_",), frozenset({
        "FastEthernet", "GigabitEthernet", "TwoGigabitEthernet", "FiveGigabitEthernet",
        "AppGigabitEthernet", "TenGigabitEthernet", "TwentyFiveGigE", "FortyGigabitEthernet",
        "FiftyGigabitEthernet", "HundredGigE", "TwoHundredGigE", "FourHundredGigE",
        "Port-channel", "Port-channel-subinterface/Port-channel",
    })),
    (("PHY_FEC",), frozenset({"TwentyFiveGigE"})),
    (("PHY_",), frozenset({
        "GigabitEthernet", "TwoGigabitEthernet", "FiveGigabitEthernet",
        "AppGigabitEthernet", "TenGigabitEthernet", "TwentyFiveGigE",
        "FortyGigabitEthernet", "FiftyGigabitEthernet",
    })),
    (("NEGOTIATION",), frozenset({"ucse", "Ethernet-Internal"})),
    (("PO_MIN_LINKS", "PO_STANDALONE_DISABLE",
      "PO_LOAD_BALANCE_HASH_ALGO"), frozenset({"Port-channel"})),
    (("TYPE_VLAN_", "SVI_"), frozenset({"Vlan"})),
    (("TYPE_TUNNEL_",), frozenset({"Tunnel"})),
    (("NVE_",), frozenset({"nve"})),
)


def applies_to(base):
    """Set of interface paths the family is valid on, or None for native-scoped."""
    if base in NATIVE_SCOPED:
        return None
    for prefixes, allowed in _APPLICABILITY:
        if base.startswith(prefixes):
            return allowed
    return _COMMON_PATHS


