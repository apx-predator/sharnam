# interface_attrs_173.py
# Consolidated modular interface XML bodies for Cisco-IOS-XE-native (IOS XE 17.3)
# Derived from interface_attrs_1715.py and checked against
# Cisco-IOS-XE-interfaces.yang (submodule, rev 2020-07-01, semver 4.0.0) and
# Cisco-IOS-XE-switch.yang (module, rev 2020-07-01, semver 2.2.0),
# Cisco-IOS-XE-vlan.yang (module, rev 2020-03-01, semver 2.0.0) and
# Cisco-IOS-XE-native.yang (module, rev 2020-07-01, semver 4.0.0).
# Placeholders use $…; NS dict supplies $N, $NC, $SW, $ST.
#
# SCOPE RULES
#   * Only features that exist in the 17.3 interfaces submodule are templated.
#   * Features absent from 17.3 are listed in NOT_PRESENT_173 with the reason,
#     and registered with a None slot so resolve() raises a clear error.
#   * Where 17.3 models a feature with a DIFFERENT shape than 17.15, the body
#     is rewritten for 17.3 and marked "# 173-ADAPTED".
#   * Same placeholder vocabulary as 1715, so the two files merge cleanly.
#
# DESIGN RULES (unchanged from 1715):
#   * Valued leaves (true|false) are symmetric: caller passes $flag.
#   * Every presence leaf has a matching *_REMOVE_173 twin.
#   * Every additive/list feature has a *_REMOVE_173 (remove-by-key) twin.
#   * Bulk forms accept $*_block fragments so the engine controls contents.
#   * Interface scaffolding (<interfaces><$parent><$name>) is owned by
#     the caller's wrapper — bodies here are bare interface-scoped nodes.

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
DESCRIPTION_173        = "<description>$desc</description>"
DESCRIPTION_REMOVE_173 = '<description nc:operation="remove"/>'
MAC_ADDRESS_173        = "<mac-address>$mac</mac-address>"
MAC_ADDRESS_REMOVE_173 = '<mac-address nc:operation="remove"/>'
# EXPORT_NAME            -> NOT PRESENT in 17.3

# --- admin state ---
SHUTDOWN_173           = "<shutdown/>"
SHUTDOWN_REMOVE_173    = '<shutdown nc:operation="remove"/>'

# --- L2 / MTU / timers ---
MTU_173                = "<mtu>$mtu</mtu>"                           # 64..18000
MTU_REMOVE_173         = '<mtu nc:operation="remove"/>'
DELAY_173              = "<delay>$delay</delay>"
DELAY_REMOVE_173       = '<delay nc:operation="remove"/>'
LOAD_INTERVAL_173      = "<load-interval>$seconds</load-interval>"
LOAD_INTERVAL_REMOVE_173 = '<load-interval nc:operation="remove"/>'

# --- bandwidth ---
MAX_BANDWIDTH_173        = "<max-reserved-bandwidth>$percent</max-reserved-bandwidth>"
MAX_BANDWIDTH_REMOVE_173 = '<max-reserved-bandwidth nc:operation="remove"/>'

# --- media / negotiation ---
# NOTE: in 17.3 <negotiation> exists ONLY on list ucse and list Ethernet-Internal
#       (interface-negotiation-grouping). It is not on GigabitEthernet etc.
NEGOTIATION_173        = "<negotiation><auto>$flag</auto></negotiation>"
GEN_MDIX_173           = "<mdix><auto>$flag</auto></mdix>"

# --- service / qos ---
SERVICE_INSERTION_173        = "<service-insertion>$svc</service-insertion>"   # waas|appqoe
SERVICE_INSERTION_REMOVE_173 = '<service-insertion nc:operation="remove"/>'
QOS_TRUST_173          = '<interface_qos><trust><device>$device</device></trust></interface_qos>'
QOS_TRUST_REMOVE_173   = '<interface_qos nc:operation="remove"/>'


# ============================================================
# 2. L2 SWITCHING
# ============================================================

# --- switchport (switchport-conf is in the interfaces submodule) ---
L2_SWITCHPORT_TRUE_173  = "<switchport-conf><switchport>true</switchport></switchport-conf>"
L2_SWITCHPORT_FALSE_173 = "<switchport-conf><switchport>false</switchport></switchport-conf>"

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
L2_DTP_DISABLE_TRUE_173  = '<switchport><nonegotiate xmlns="$SW"/></switchport>'
L2_DTP_DISABLE_FALSE_173 = '<switchport><nonegotiate xmlns="$SW" nc:operation="remove"/></switchport>'

# --- voice vlan ---
L2_VOICE_FULL_173 = (
    '<switchport>'
    '<voice xmlns="$SW">'
      '<vlan><vlan>$voice_vlan</vlan></vlan>'
      '<detect><cisco-phone><full-duplex/></cisco-phone></detect>'
    '</voice>'
    '<access xmlns="$SW"><vlan><vlan>$access_vlan</vlan></vlan></access>'
    '</switchport>'
)
L2_VOICE_FULL_REMOVE_173 = (
    '<switchport>'
    '<voice xmlns="$SW" nc:operation="remove"/>'
    '<access xmlns="$SW" nc:operation="remove"/>'
    '</switchport>'
)
L2_VOICE_VLAN_ID_173 = (
    '<switchport><voice xmlns="$SW"><vlan><vlan>$voice_vlan</vlan></vlan></voice></switchport>'
)
L2_VOICE_VLAN_DOT1P_173 = (
    '<switchport><voice xmlns="$SW"><vlan><vlan>dot1p</vlan></vlan></voice></switchport>'
)
L2_VOICE_VLAN_NONE_173 = (
    '<switchport><voice xmlns="$SW"><vlan><vlan>none</vlan></vlan></voice></switchport>'
)
L2_VOICE_VLAN_UNTAGGED_173 = (
    '<switchport><voice xmlns="$SW"><vlan><vlan>untagged</vlan></vlan></voice></switchport>'
)
L2_VOICE_VLAN_REMOVE_173 = (
    '<switchport><voice xmlns="$SW"><vlan nc:operation="remove"/></voice></switchport>'
)
L2_VOICE_DETECT_173 = (
    '<switchport><voice xmlns="$SW"><detect><cisco-phone><full-duplex/></cisco-phone></detect></voice></switchport>'
)
L2_VOICE_DETECT_REMOVE_173 = (
    '<switchport><voice xmlns="$SW"><detect nc:operation="remove"/></voice></switchport>'
)
# access vlan: 1..4094 | dynamic
L2_ACCESS_VLAN_173 = (
    '<switchport><access xmlns="$SW"><vlan><vlan>$access_vlan</vlan></vlan></access></switchport>'
)
L2_ACCESS_VLAN_REMOVE_173 = (
    '<switchport><access xmlns="$SW"><vlan nc:operation="remove"/></access></switchport>'
)

# --- trunk pruning ---
# NOTE: in 17.3 <vlans> and <except> are LEAF-LISTS (repeat the element per value);
#       <add> and <remove> are single leaves taking a range string.
L2_TRUNK_PRUNING_ADD_173 = (
    '<switchport><trunk xmlns="$SW"><pruning><vlan><add>$vlans</add></vlan></pruning></trunk></switchport>'
)
L2_TRUNK_PRUNING_REMOVE_173 = (
    '<switchport><trunk xmlns="$SW"><pruning><vlan><remove>$vlans</remove></vlan></pruning></trunk></switchport>'
)
L2_TRUNK_PRUNING_REPLACE_173 = (
    '<switchport><trunk xmlns="$SW"><pruning><vlan><vlans nc:operation="replace">$vlans</vlans></vlan></pruning></trunk></switchport>'
)
L2_TRUNK_PRUNING_NONE_173 = (
    '<switchport><trunk xmlns="$SW"><pruning><vlan><none/></vlan></pruning></trunk></switchport>'
)
L2_TRUNK_PRUNING_REMOVE_ALL_173 = (
    '<switchport><trunk xmlns="$SW"><pruning nc:operation="remove"/></trunk></switchport>'
)

# --- PVLAN global (GLOBAL scope, not interface-scoped) ---
# <vlan> is a native container; <vlan-list> is augmented in by Cisco-IOS-XE-vlan,
# so it carries xmlns="$VLAN". Requires feature ios-features:private-vlan.
# 173-ADAPTED: in 17.3 <primary/> and <association> are SIBLING leaves, and
# <association> is one string (e.g. "101,102"). There is no add/remove action
# leaf as in 17.15, so $action is no longer used here.
PVLAN_GLOBAL_173 = (
    '<vlan xmlns="$N"><vlan-list xmlns="$VLAN">'
      '<id>$primary_vlan</id>'
      '<private-vlan><primary/><association>$secondary_vlans</association></private-vlan>'
    '</vlan-list></vlan>'
)
PVLAN_GLOBAL_REMOVE_173 = (
    '<vlan xmlns="$N"><vlan-list xmlns="$VLAN">'
      '<id>$primary_vlan</id>'
      '<private-vlan nc:operation="remove"/>'
    '</vlan-list></vlan>'
)
# $pvlan_type: community | isolated
PVLAN_SECONDARY_173 = (
    '<vlan xmlns="$N"><vlan-list xmlns="$VLAN">'
      '<id>$secondary_vlan</id>'
      '<private-vlan><$pvlan_type/></private-vlan>'
    '</vlan-list></vlan>'
)
PVLAN_SECONDARY_REMOVE_173 = (
    '<vlan xmlns="$N"><vlan-list xmlns="$VLAN" nc:operation="remove">'
      '<id>$secondary_vlan</id>'
    '</vlan-list></vlan>'
)

# --- PVLAN interface bindings ---
PVLAN_HOST_ASSOC_173 = (
    '<switchport>'
      '<mode xmlns="$SW"><private-vlan><host/></private-vlan></mode>'
      '<private-vlan xmlns="$SW"><host-association>'
        '<primary-range>$primary_vlan</primary-range>'
        '<secondary-range>$secondary_vlan</secondary-range>'
      '</host-association></private-vlan>'
    '</switchport>'
)
PVLAN_HOST_ASSOC_REMOVE_173 = (
    '<switchport>'
      '<private-vlan xmlns="$SW"><host-association nc:operation="remove"/></private-vlan>'
    '</switchport>'
)
PVLAN_PROMISCUOUS_MAP_173 = (
    '<switchport>'
      '<mode xmlns="$SW"><private-vlan><promiscuous/></private-vlan></mode>'
      '<private-vlan xmlns="$SW"><mapping>'
        '<primary-range>$primary_vlan</primary-range>'
        '<secondary-range>$secondary_vlans</secondary-range>'
      '</mapping></private-vlan>'
    '</switchport>'
)
PVLAN_PROMISCUOUS_MAP_REMOVE_173 = (
    '<switchport>'
      '<private-vlan xmlns="$SW"><mapping nc:operation="remove"/></private-vlan>'
    '</switchport>'
)

# --- port-security ---
# 173-ADAPTED vs 17.15:
#   enable      : empty leaf <port-security-cfg>  (not a <port-security-conf> presence)
#   config tree : <port-security-conf><port-security>...  (not port-security-config)
#   maximum     : list <maxcount> keyed by <max-addresses>, optional <vlan>
#   sticky      : <mac-address><sticky/>          (not mac-address-sticky-on)
#   static MAC  : <mac-address><hw-address>       (single container, not a list;
#                 add <sticky/> beside it for a sticky-learned static entry)
L2_PORTSEC_ENABLE_173 = (
    '<switchport><port-security-cfg xmlns="$SW"/></switchport>'
)
L2_PORTSEC_ENABLE_REMOVE_173 = (
    '<switchport><port-security-cfg xmlns="$SW" nc:operation="remove"/></switchport>'
)
L2_PORTSEC_MAX_173 = (
    '<switchport><port-security-conf xmlns="$SW"><port-security>'
      '<maxcount><max-addresses>$max</max-addresses></maxcount>'
    '</port-security></port-security-conf></switchport>'
)
L2_PORTSEC_MAX_VLAN_173 = (
    '<switchport><port-security-conf xmlns="$SW"><port-security>'
      '<maxcount><max-addresses>$max</max-addresses><vlan>$vlan_kind</vlan></maxcount>'
    '</port-security></port-security-conf></switchport>'
)
# ADDED: remove a single <maxcount> entry by its key <max-addresses>.
L2_PORTSEC_MAX_REMOVE_173 = (
    '<switchport><port-security-conf xmlns="$SW"><port-security>'
      '<maxcount nc:operation="remove"><max-addresses>$max</max-addresses></maxcount>'
    '</port-security></port-security-conf></switchport>'
)
# $violation: protect | restrict | shutdown
L2_PORTSEC_VIOLATION_173 = (
    '<switchport><port-security-conf xmlns="$SW"><port-security>'
      '<violation><$violation/></violation>'
    '</port-security></port-security-conf></switchport>'
)
L2_PORTSEC_VIOLATION_SHUTDOWN_VLAN_173 = (
    '<switchport><port-security-conf xmlns="$SW"><port-security>'
      '<violation><shutdown><vlan/></shutdown></violation>'
    '</port-security></port-security-conf></switchport>'
)
# ADDED: remove the violation leaf.
L2_PORTSEC_VIOLATION_REMOVE_173 = (
    '<switchport><port-security-conf xmlns="$SW"><port-security>'
      '<violation nc:operation="remove"/>'
    '</port-security></port-security-conf></switchport>'
)
L2_PORTSEC_STICKY_173 = (
    '<switchport><port-security-conf xmlns="$SW"><port-security>'
      '<mac-address><sticky/></mac-address>'
    '</port-security></port-security-conf></switchport>'
)
L2_PORTSEC_STICKY_REMOVE_173 = (
    '<switchport><port-security-conf xmlns="$SW"><port-security>'
      '<mac-address><sticky nc:operation="remove"/></mac-address>'
    '</port-security></port-security-conf></switchport>'
)
L2_PORTSEC_AGING_173 = (
    '<switchport><port-security-conf xmlns="$SW"><port-security>'
      '<aging><time>$minutes</time><type>$aging_type</type></aging>'
    '</port-security></port-security-conf></switchport>'
)
L2_PORTSEC_AGING_REMOVE_173 = (
    '<switchport><port-security-conf xmlns="$SW"><port-security>'
      '<aging nc:operation="remove"/>'
    '</port-security></port-security-conf></switchport>'
)
L2_PORTSEC_MAC_ACCESS_173 = (
    '<switchport><port-security-conf xmlns="$SW"><port-security>'
      '<mac-address><hw-address>$hwaddr</hw-address></mac-address>'
    '</port-security></port-security-conf></switchport>'
)
# ADDED: remove a single static MAC by its <hw-address>.
L2_PORTSEC_MAC_ACCESS_REMOVE_173 = (
    '<switchport><port-security-conf xmlns="$SW"><port-security>'
      '<mac-address nc:operation="remove"><hw-address>$hwaddr</hw-address></mac-address>'
    '</port-security></port-security-conf></switchport>'
)
L2_PORTSEC_MAC_STICKY_173 = (
    '<switchport><port-security-conf xmlns="$SW"><port-security>'
      '<mac-address><sticky/><hw-address>$hwaddr</hw-address></mac-address>'
    '</port-security></port-security-conf></switchport>'
)
# ADDED: remove a single sticky MAC by its <hw-address>.
L2_PORTSEC_MAC_STICKY_REMOVE_173 = (
    '<switchport><port-security-conf xmlns="$SW"><port-security>'
      '<mac-address nc:operation="remove"><hw-address>$hwaddr</hw-address><sticky/></mac-address>'
    '</port-security></port-security-conf></switchport>'
)

# --- protected / host / block / vepa ---
L2_PROTECTED_173        = '<switchport><protected xmlns="$SW"/></switchport>'
L2_PROTECTED_REMOVE_173 = '<switchport><protected xmlns="$SW" nc:operation="remove"/></switchport>'
L2_HOST_173             = '<switchport><host xmlns="$SW"/></switchport>'
L2_HOST_REMOVE_173      = '<switchport><host xmlns="$SW" nc:operation="remove"/></switchport>'
L2_BLOCK_MULTICAST_173  = '<switchport><block xmlns="$SW"><multicast/></block></switchport>'
L2_BLOCK_MULTICAST_REMOVE_173 = (
    '<switchport><block xmlns="$SW"><multicast nc:operation="remove"/></block></switchport>'
)
L2_BLOCK_UNICAST_173    = '<switchport><block xmlns="$SW"><unicast/></block></switchport>'
L2_BLOCK_UNICAST_REMOVE_173 = (
    '<switchport><block xmlns="$SW"><unicast nc:operation="remove"/></block></switchport>'
)
L2_VEPA_173        = '<switchport><vepa xmlns="$SW"><enabled/></vepa></switchport>'
L2_VEPA_REMOVE_173 = '<switchport><vepa xmlns="$SW"><enabled nc:operation="remove"/></vepa></switchport>'

# --- L2PT (l2protocol-tunnel) ---
# 17.3 shape: protocol thresholds are plain uint16 leaves (1..4096) directly
# under drop-threshold / shutdown-threshold. There is NO <proto><packet-rate>
# nesting as in 17.15.
# $proto     : cdp | stp | vtp | lldp   (+ mvrp dtp ptppd mmrp elmi link-oam esmc
#              only when feature ios-features:l2pt-more-protocols is on)
# $p2p_proto : lacp | pagp | udld
L2PT_TUNNEL_CORE_173 = (
    '<l2protocol-tunnel><$proto/></l2protocol-tunnel>'
)
L2PT_TUNNEL_CORE_REMOVE_173 = (
    '<l2protocol-tunnel><$proto nc:operation="remove"/></l2protocol-tunnel>'
)
L2PT_TUNNEL_P2P_173 = (
    '<l2protocol-tunnel><point-to-point><$p2p_proto/></point-to-point></l2protocol-tunnel>'
)
L2PT_TUNNEL_P2P_REMOVE_173 = (
    '<l2protocol-tunnel><point-to-point><$p2p_proto nc:operation="remove"/></point-to-point></l2protocol-tunnel>'
)
L2PT_TUNNEL_CORE_BLOCK_173 = (
    '<l2protocol-tunnel>$core_block</l2protocol-tunnel>'
)
L2PT_TUNNEL_CORE_BLOCK_REMOVE_173 = (
    '<l2protocol-tunnel nc:operation="remove"/>'
)
L2PT_TUNNEL_P2P_BLOCK_173 = (
    '<l2protocol-tunnel><point-to-point>$p2p_block</point-to-point></l2protocol-tunnel>'
)
L2PT_TUNNEL_P2P_BLOCK_REMOVE_173 = (
    '<l2protocol-tunnel><point-to-point nc:operation="remove"/></l2protocol-tunnel>'
)
# 173-ADAPTED: leaf value is the pps directly
L2PT_DROP_THRESHOLD_173 = (
    '<l2protocol-tunnel><drop-threshold>'
      '<$proto>$pps</$proto>'
    '</drop-threshold></l2protocol-tunnel>'
)
L2PT_DROP_THRESHOLD_REMOVE_173 = (
    '<l2protocol-tunnel><drop-threshold><$proto nc:operation="remove"/></drop-threshold></l2protocol-tunnel>'
)
# 173-ADAPTED
L2PT_DROP_THRESHOLD_P2P_173 = (
    '<l2protocol-tunnel><drop-threshold><point-to-point>'
      '<$p2p_proto>$pps</$p2p_proto>'
    '</point-to-point></drop-threshold></l2protocol-tunnel>'
)
L2PT_DROP_THRESHOLD_P2P_REMOVE_173 = (
    '<l2protocol-tunnel><drop-threshold><point-to-point><$p2p_proto nc:operation="remove"/></point-to-point></drop-threshold></l2protocol-tunnel>'
)
# 173-ADAPTED
L2PT_SHUTDOWN_THRESHOLD_173 = (
    '<l2protocol-tunnel><shutdown-threshold>'
      '<$proto>$pps</$proto>'
    '</shutdown-threshold></l2protocol-tunnel>'
)
L2PT_SHUTDOWN_THRESHOLD_REMOVE_173 = (
    '<l2protocol-tunnel><shutdown-threshold><$proto nc:operation="remove"/></shutdown-threshold></l2protocol-tunnel>'
)
# 173-ADAPTED
L2PT_SHUTDOWN_THRESHOLD_P2P_173 = (
    '<l2protocol-tunnel><shutdown-threshold><point-to-point>'
      '<$p2p_proto>$pps</$p2p_proto>'
    '</point-to-point></shutdown-threshold></l2protocol-tunnel>'
)
L2PT_SHUTDOWN_THRESHOLD_P2P_REMOVE_173 = (
    '<l2protocol-tunnel><shutdown-threshold><point-to-point><$p2p_proto nc:operation="remove"/></point-to-point></shutdown-threshold></l2protocol-tunnel>'
)

# --- l2protocol forward (requires feature ios-features:l2cp-fwd) ---
L2PT_FORWARD_PROTOCOL_173 = (
    '<l2protocol><forward><protocols>$proto</protocols></forward></l2protocol>'
)
L2PT_FORWARD_PROTOCOL_REMOVE_173 = (
    '<l2protocol><forward><protocols nc:operation="remove">$proto</protocols></forward></l2protocol>'
)
L2PT_FORWARD_BLOCK_173 = (
    '<l2protocol><forward>$proto_block</forward></l2protocol>'
)
L2PT_FORWARD_BLOCK_REMOVE_173 = (
    '<l2protocol><forward nc:operation="remove"/></l2protocol>'
)
L2PT_FORWARD_DROP_173 = (
    '<l2protocol><forward><drop-threshold><threshold-list>'
      '<proto-type>$proto</proto-type><pps-num>$pps</pps-num>'
    '</threshold-list></drop-threshold></forward></l2protocol>'
)
L2PT_FORWARD_DROP_REMOVE_173 = (
    '<l2protocol><forward><drop-threshold nc:operation="remove"/></forward></l2protocol>'
)
L2PT_FORWARD_SHUTDOWN_173 = (
    '<l2protocol><forward><shutdown-threshold><threshold-list>'
      '<proto-type>$proto</proto-type><pps-num>$pps</pps-num>'
    '</threshold-list></shutdown-threshold></forward></l2protocol>'
)
L2PT_FORWARD_SHUTDOWN_REMOVE_173 = (
    '<l2protocol><forward><shutdown-threshold nc:operation="remove"/></forward></l2protocol>'
)


# ============================================================
# 3. ARP + LINK TUNING
# ============================================================

# --- ARP ---
ARP_TIMEOUT_173        = "<arp><timeout>$secs</timeout></arp>"
ARP_TIMEOUT_REMOVE_173 = '<arp><timeout nc:operation="remove"/></arp>'
ARP_SNAP_TRUE_173      = "<arp><snap/></arp>"
ARP_SNAP_FALSE_173     = '<arp><snap nc:operation="remove"/></arp>'
ARP_ENTRY_LIMIT_173 = (
    "<arp><entries><interface-limit>"
    "<entry-count>$count</entry-count><log>$log_secs</log>"
    "</interface-limit></entries></arp>"
)
ARP_ENTRY_LIMIT_REMOVE_173 = (
    '<arp><entries><interface-limit nc:operation="remove"/></entries></arp>'
)
ARP_PACKET_PRIORITY_173 = "<arp><packet-priority><enable/></packet-priority></arp>"
ARP_PACKET_PRIORITY_REMOVE_173 = (
    '<arp><packet-priority><enable nc:operation="remove"/></packet-priority></arp>'
)

# --- priority-queue / rcv-queue ---
PQ_OUT_ENABLE_173        = "<priority-queue><out/></priority-queue>"
PQ_OUT_ENABLE_REMOVE_173 = '<priority-queue><out nc:operation="remove"/></priority-queue>'
PQ_COS_MAP_173 = (
    "<priority-queue><cos-map>"
    "<id>$qid</id>"
    "$cos_values_block"
    "</cos-map></priority-queue>"
)
PQ_COS_MAP_REMOVE_173 = (
    '<priority-queue><cos-map nc:operation="remove"><id>$qid</id></cos-map></priority-queue>'
)
RCV_QUEUE_COS_MAP_173 = (
    "<rcv-queue><cos-map>"
    "<queue-id>$qid</queue-id>"
    "<threshold-id>$tid</threshold-id>"
    "$cos_values_block"
    "</cos-map></rcv-queue>"
)
RCV_QUEUE_COS_MAP_REMOVE_173 = (
    '<rcv-queue><cos-map nc:operation="remove">'
    '<queue-id>$qid</queue-id><threshold-id>$tid</threshold-id>'
    '</cos-map></rcv-queue>'
)

# --- flowcontrol / hold-queue ---
FLOWCONTROL_173 = (
    "<flowcontrol>"
    "<receive>$rx</receive>"
    "<send>$tx</send>"
    "</flowcontrol>"
)
FLOWCONTROL_REMOVE_173 = '<flowcontrol nc:operation="remove"/>'
HOLD_QUEUE_173 = (
    "<hold-queue>"
    "<direction>$direction</direction>"
    "<queue-length>$qlen</queue-length>"
    "</hold-queue>"
)
# FIXED vs 1715: hold-queue is a list keyed by <direction>; remove by key.
HOLD_QUEUE_REMOVE_173 = (
    '<hold-queue nc:operation="remove"><direction>$direction</direction></hold-queue>'
)

# --- bandwidth ---
LINK_BANDWIDTH_173        = "<bandwidth><kilobits>$kbps</kilobits></bandwidth>"
LINK_BANDWIDTH_REMOVE_173 = '<bandwidth nc:operation="remove"/>'
LINK_BANDWIDTH_QOS_REF_173 = (
    "<bandwidth><qos-reference>$kbps</qos-reference></bandwidth>"
)
LINK_BANDWIDTH_QOS_REF_REMOVE_173 = (
    '<bandwidth><qos-reference nc:operation="remove"/></bandwidth>'
)

# --- dampening ---
DAMPENING_FULL_173 = (
    "<dampening>"
    "<dampening-time>$half_life</dampening-time>"
    "<start-reusing-time>$reuse</start-reusing-time>"
    "<start-supressing-time>$suppress</start-supressing-time>"
    "<maximum-supressing-time>$max_suppress</maximum-supressing-time>"
    "</dampening>"
)
DAMPENING_DEFAULT_173 = "<dampening/>"
DAMPENING_REMOVE_173  = '<dampening nc:operation="remove"/>'

# --- srlg -> NOT PRESENT in 17.3 ---

# --- domain ---
DOMAIN_NAME_173        = "<domain><name>$domain</name></domain>"
DOMAIN_NAME_REMOVE_173 = '<domain><name nc:operation="remove"/></domain>'
DOMAIN_PATH_173 = (
    "<domain>"
    "<path>$sp_path</path>"
    "<path-id>$path_id</path-id>"
    "</domain>"
)
DOMAIN_PATH_REMOVE_173 = (
    '<domain><path nc:operation="remove">$sp_path</path></domain>'
)

# --- keepalive ---
# 173-ADAPTED: 17.3 has a choice:
#   leaf keepalive (boolean)  |  keepalive-settings/keepalive (presence){period,retries}
# There is no <keepalive-config> wrapper.
KEEPALIVE_TIMERS_173 = (
    "<keepalive-settings><keepalive>"
    "<period>$period</period>"
    "<retries>$retries</retries>"
    "</keepalive></keepalive-settings>"
)
KEEPALIVE_DISABLE_173 = "<keepalive>false</keepalive>"

# --- logging ---
LINK_LOGGING_LINK_STATUS_173 = (
    "<logging><event><link-status-enable>$flag</link-status-enable></event></logging>"
)
LINK_LOGGING_LINK_STATUS_REMOVE_173 = (
    '<logging><event><link-status-enable nc:operation="remove"/></event></logging>'
)
# $event: bundle-status | trunk-status | nfas-status | power-inline-status | status
LINK_LOGGING_EVENT_173 = (
    "<logging><event><$event/></event></logging>"
)
LINK_LOGGING_EVENT_REMOVE_173 = (
    '<logging><event><$event nc:operation="remove"/></event></logging>'
)
LINK_LOGGING_EVENTS_BLOCK_173 = (
    "<logging><event>$events_block</event></logging>"
)
LINK_LOGGING_EVENTS_BLOCK_REMOVE_173 = (
    '<logging><event nc:operation="remove"/></logging>'
)
LINK_LOGGING_SPANNING_TREE_173 = (
    "<logging><event><spanning-tree><status/></spanning-tree></event></logging>"
)
LINK_LOGGING_SPANNING_TREE_REMOVE_173 = (
    '<logging><event><spanning-tree nc:operation="remove"/></event></logging>'
)
LINK_LOGGING_SUBIF_173 = (
    "<logging><event><subif-link-status>$ignore_bulk_block</subif-link-status></event></logging>"
)
LINK_LOGGING_SUBIF_REMOVE_173 = (
    '<logging><event><subif-link-status nc:operation="remove"/></event></logging>'
)

# --- fair queue ---
FAIR_QUEUE_173        = "<fair-queue><incomplete/></fair-queue>"
FAIR_QUEUE_REMOVE_173 = '<fair-queue nc:operation="remove"/>'
FAIR_QUEUE_CONF_173   = (
    "<fair-queue-conf><fair-queue>$flag</fair-queue></fair-queue-conf>"
)


# ============================================================
# 4. IPv4
# ============================================================

IP4_PRIMARY_173 = (
    "<ip><address><primary>"
    "<address>$ip</address><mask>$mask</mask>"
    "</primary></address></ip>"
)
IP4_PRIMARY_REMOVE_173 = (
    '<ip><address><primary nc:operation="remove"/></address></ip>'
)
IP4_SECONDARY_173 = (
    "<ip><address><secondary>"
    "<address>$ip</address><mask>$mask</mask>"
    "<secondary/>"
    "</secondary></address></ip>"
)
IP4_SECONDARY_REMOVE_173 = (
    '<ip><address><secondary nc:operation="remove">'
    '<address>$ip</address><mask>$mask</mask>'
    '</secondary></address></ip>'
)
IP4_DHCP_173        = "<ip><address><dhcp/></address></ip>"
IP4_DHCP_REMOVE_173 = '<ip><address><dhcp nc:operation="remove"/></address></ip>'
IP4_NEGOTIATED_173        = "<ip><address><negotiated/></address></ip>"
IP4_NEGOTIATED_REMOVE_173 = '<ip><address><negotiated nc:operation="remove"/></address></ip>'
IP4_DHCP_OPTIONS_173 = (
    "<ip><address><dhcp>"
    "$client_id_block"
    "$hostname_block"
    "</dhcp></address></ip>"
)
IP4_UNNUMBERED_173        = "<ip><unnumbered>$src_if</unnumbered></ip>"
IP4_UNNUMBERED_REMOVE_173 = '<ip><unnumbered nc:operation="remove"/></ip>'
IP4_ACCESS_GROUP_IN_173 = (
    "<ip><access-group><in><acl>"
    "<acl-name>$acl</acl-name><in/>"
    "</acl></in></access-group></ip>"
)
IP4_ACCESS_GROUP_IN_REMOVE_173 = (
    '<ip><access-group><in nc:operation="remove"/></access-group></ip>'
)
IP4_ACCESS_GROUP_OUT_173 = (
    "<ip><access-group><out><acl>"
    "<acl-name>$acl</acl-name><out/>"
    "</acl></out></access-group></ip>"
)
IP4_ACCESS_GROUP_OUT_REMOVE_173 = (
    '<ip><access-group><out nc:operation="remove"/></access-group></ip>'
)
# 173-ADAPTED: common-acl has only <common> + <in|out>; no <acl-name> child.
IP4_ACCESS_GROUP_COMMON_IN_173 = (
    "<ip><access-group><in><common-acl>"
    "<common>$common_acl</common><in/>"
    "</common-acl></in></access-group></ip>"
)
IP4_ACCESS_GROUP_COMMON_IN_REMOVE_173 = (
    '<ip><access-group><in><common-acl nc:operation="remove"/></in></access-group></ip>'
)
IP4_ACCESS_GROUP_COMMON_OUT_173 = (
    "<ip><access-group><out><common-acl>"
    "<common>$common_acl</common><out/>"
    "</common-acl></out></access-group></ip>"
)
IP4_ACCESS_GROUP_COMMON_OUT_REMOVE_173 = (
    '<ip><access-group><out><common-acl nc:operation="remove"/></out></access-group></ip>'
)
IP4_VRF_FORWARDING_173 = "<vrf><forwarding>$vrf</forwarding></vrf>"
IP4_VRF_FORWARDING_REMOVE_173 = (
    '<vrf><forwarding nc:operation="remove">$vrf</forwarding></vrf>'
)
IP4_VRF_RECEIVE_173 = "<ip><vrf><receive>$vrf</receive></vrf></ip>"
IP4_VRF_RECEIVE_REMOVE_173 = (
    '<ip><vrf><receive nc:operation="remove">$vrf</receive></vrf></ip>'
)
IP4_VRF_SITEMAP_173 = "<ip><vrf><sitemap>$route_map</sitemap></vrf></ip>"
IP4_VRF_SITEMAP_REMOVE_173 = (
    '<ip><vrf><sitemap nc:operation="remove">$route_map</sitemap></vrf></ip>'
)
IP4_HELPER_173 = (
    "<ip><helper-address><address>$helper</address></helper-address></ip>"
)
IP4_HELPER_REMOVE_173 = (
    '<ip><helper-address nc:operation="remove"><address>$helper</address></helper-address></ip>'
)
IP4_HELPER_GLOBAL_173 = (
    "<ip><helper-address><address>$helper</address><global/>"
    "</helper-address></ip>"
)
IP4_HELPER_GLOBAL_REMOVE_173 = (
    '<ip><helper-address nc:operation="remove"><address>$helper</address><global/></helper-address></ip>'
)
IP4_HELPER_VRF_173 = (
    "<ip><helper-address><address>$helper</address><vrf>$vrf</vrf>"
    "</helper-address></ip>"
)
IP4_HELPER_VRF_REMOVE_173 = (
    '<ip><helper-address nc:operation="remove"><address>$helper</address><vrf>$vrf</vrf></helper-address></ip>'
)
IP4_POLICY_ROUTE_MAP_173 = (
    "<ip><policy><route-map>$route_map</route-map></policy></ip>"
)
IP4_POLICY_ROUTE_MAP_REMOVE_173 = (
    '<ip><policy><route-map nc:operation="remove"/></policy></ip>'
)
# FIXED vs 1715: closing </ip> was missing
IP4_PROXY_ARP_173 = "<ip><proxy-arp>$flag</proxy-arp></ip>"
IP4_LOCAL_PROXY_ARP_173        = "<ip><local-proxy-arp/></ip>"
IP4_LOCAL_PROXY_ARP_REMOVE_173 = '<ip><local-proxy-arp nc:operation="remove"/></ip>'
# FIXED vs 1715: closing </ip> was missing
IP4_REDIRECTS_173 = "<ip><redirects>$flag</redirects></ip>"
# IP4_CLEAR_DF -> NOT PRESENT in 17.3
IP4_TCP_MSS_173        = "<ip><tcp><adjust-mss>$mss</adjust-mss></tcp></ip>"      # 500..1460
IP4_TCP_MSS_REMOVE_173 = '<ip><tcp><adjust-mss nc:operation="remove"/></tcp></ip>'
IP4_MTU_173            = "<ip><mtu>$ip_mtu</mtu></ip>"                            # 68..9976
IP4_MTU_REMOVE_173     = '<ip><mtu nc:operation="remove"/></ip>'
# 173-ADAPTED: no ACL leaf under verify/unicast/source in 17.3 -> $acl_block dropped.
#              Only reachable-via (any|rx), allow-self-ping, allow-default exist.
IP4_URPF_173 = (
    "<ip><verify><unicast><source>"
    "<reachable-via>$via</reachable-via>"
    "$allow_block"
    "</source></unicast></verify></ip>"
)
IP4_URPF_REMOVE_173 = '<ip><verify nc:operation="remove"/></ip>'
IP4_ARP_INSPECT_TRUST_173 = (
    '<ip><arp><inspection><trust/></inspection></arp></ip>'
)
IP4_ARP_INSPECT_TRUST_REMOVE_173 = (
    '<ip><arp><inspection><trust nc:operation="remove"/></inspection></arp></ip>'
)
# 173-ADAPTED: limit has only <rate> and <none>; no burst leaf -> $burst_block dropped.
IP4_ARP_INSPECT_RATE_173 = (
    "<ip><arp><inspection><limit>"
    "<rate>$pps</rate>"
    "</limit></inspection></arp></ip>"
)
IP4_ARP_INSPECT_RATE_REMOVE_173 = (
    '<ip><arp><inspection><limit nc:operation="remove"/></inspection></arp></ip>'
)
IP4_ARP_INSPECT_RATE_NONE_173 = (
    "<ip><arp><inspection><limit><none/></limit></inspection></arp></ip>"
)
IP4_DIRECTED_BROADCAST_173        = "<ip><directed-broadcast/></ip>"
IP4_DIRECTED_BROADCAST_REMOVE_173 = (
    '<ip><directed-broadcast nc:operation="remove"/></ip>'
)
IP4_DIRECTED_BROADCAST_ACL_173 = (
    "<ip><directed-broadcast>"
    "<direct-broadcast>$acl</direct-broadcast>"
    "</directed-broadcast></ip>"
)


# ============================================================
# 5. IPv6
# ============================================================

IP6_ENABLE_173        = "<ipv6><enable/></ipv6>"
IP6_ENABLE_REMOVE_173 = '<ipv6><enable nc:operation="remove"/></ipv6>'

IP6_ADDRESS_PREFIX_173 = (
    "<ipv6><address><prefix-list><prefix>$ipv6</prefix></prefix-list></address></ipv6>"
)
IP6_ADDRESS_PREFIX_REMOVE_173 = (
    '<ipv6><address><prefix-list nc:operation="remove"><prefix>$ipv6</prefix></prefix-list></address></ipv6>'
)
IP6_ADDRESS_EUI64_173 = (
    "<ipv6><address><prefix-list><prefix>$ipv6</prefix><eui-64/></prefix-list></address></ipv6>"
)
IP6_ADDRESS_EUI64_REMOVE_173 = (
    '<ipv6><address><prefix-list nc:operation="remove"><prefix>$ipv6</prefix><eui-64/></prefix-list></address></ipv6>'
)
IP6_ADDRESS_ANYCAST_173 = (
    "<ipv6><address><prefix-list><prefix>$ipv6</prefix><anycast/></prefix-list></address></ipv6>"
)
IP6_ADDRESS_ANYCAST_REMOVE_173 = (
    '<ipv6><address><prefix-list nc:operation="remove"><prefix>$ipv6</prefix><anycast/></prefix-list></address></ipv6>'
)
IP6_ADDRESS_LINK_LOCAL_173 = (
    "<ipv6><address><link-local-address><address>$ll</address><link-local/>"
    "</link-local-address></address></ipv6>"
)
IP6_ADDRESS_LINK_LOCAL_REMOVE_173 = (
    '<ipv6><address><link-local-address nc:operation="remove"><address>$ll</address><link-local/></link-local-address></address></ipv6>'
)
IP6_ADDRESS_AUTOCONFIG_173        = "<ipv6><address><autoconfig/></address></ipv6>"
IP6_ADDRESS_AUTOCONFIG_REMOVE_173 = (
    '<ipv6><address><autoconfig nc:operation="remove"/></address></ipv6>'
)
IP6_ADDRESS_AUTOCONFIG_DEFAULT_173 = (
    "<ipv6><address><autoconfig><default/></autoconfig></address></ipv6>"
)
IP6_ADDRESS_AUTOCONFIG_DEFAULT_REMOVE_173 = (
    '<ipv6><address><autoconfig nc:operation="remove"><default/></autoconfig></address></ipv6>'
)
IP6_ADDRESS_DHCP_173        = "<ipv6><address><dhcp/></address></ipv6>"
IP6_ADDRESS_DHCP_REMOVE_173 = (
    '<ipv6><address><dhcp nc:operation="remove"/></address></ipv6>'
)
IP6_ADDRESS_DHCP_RAPID_COMMIT_173 = (
    "<ipv6><address><dhcp><rapid-commit/></dhcp></address></ipv6>"
)
IP6_ADDRESS_DHCP_RAPID_COMMIT_REMOVE_173 = (
    '<ipv6><address><dhcp nc:operation="remove"><rapid-commit/></dhcp></address></ipv6>'
)
# IP6_ADDRESS_PREFIX_NAME -> NOT PRESENT in 17.3

IP6_UNNUMBERED_173        = "<ipv6><unnumbered>$src_if</unnumbered></ipv6>"
IP6_UNNUMBERED_REMOVE_173 = '<ipv6><unnumbered nc:operation="remove"/></ipv6>'
IP6_MTU_173               = "<ipv6><mtu>$ip6_mtu</mtu></ipv6>"                    # 1280..9976
IP6_MTU_REMOVE_173        = '<ipv6><mtu nc:operation="remove"/></ipv6>'
# IP6_ND_DAD_ATTEMPTS / IP6_ND_NUD_IGP -> NOT PRESENT (ipv6/nd is an empty container)
IP6_TCP_ADJUST_MSS_173        = "<ipv6><tcp><adjust-mss>$mss</adjust-mss></tcp></ipv6>"   # 40..1454
IP6_TCP_ADJUST_MSS_REMOVE_173 = (
    '<ipv6><tcp><adjust-mss nc:operation="remove"/></tcp></ipv6>'
)
IP6_TRAFFIC_FILTER_173 = (
    "<ipv6><traffic-filter><direction>$direction</direction>"
    "<access-list>$acl</access-list></traffic-filter></ipv6>"
)
IP6_TRAFFIC_FILTER_REMOVE_173 = (
    '<ipv6><traffic-filter nc:operation="remove">'
    '<direction>$direction</direction><access-list>$acl</access-list>'
    '</traffic-filter></ipv6>'
)
IP6_SOURCE_GUARD_173 = (
    "<ipv6><source-guard>$policy_block</source-guard></ipv6>"
)
IP6_SOURCE_GUARD_REMOVE_173 = '<ipv6><source-guard nc:operation="remove"/></ipv6>'
# IP6_VERIFY_UNICAST_REVERSE_PATH -> NOT PRESENT in 17.3 (no ipv6/verify)


# ============================================================
# 6. ACCESS-SESSION
# ============================================================

AS_PORT_CONTROL_173 = (
    "<access-session><port-control-config>$pc</port-control-config></access-session>"
)
AS_PORT_CONTROL_REMOVE_173 = (
    '<access-session><port-control-config nc:operation="remove"/></access-session>'
)
AS_CONTROL_DIRECTION_173 = (
    "<access-session><control-direction-config>$dir</control-direction-config></access-session>"
)
AS_CONTROL_DIRECTION_REMOVE_173 = (
    '<access-session><control-direction-config nc:operation="remove"/></access-session>'
)
# 173-ADAPTED: 17.3 uses leaf <host-mode> (multi-auth|multi-domain|multi-host|single-host),
#              not host-mode-config/modes.
AS_HOST_MODE_173 = (
    "<access-session><host-mode>$hm</host-mode></access-session>"
)
AS_HOST_MODE_REMOVE_173 = (
    '<access-session><host-mode nc:operation="remove"/></access-session>'
)
# AS_HOST_MODE_PEER -> NOT PRESENT in 17.3
AS_MONITOR_173 = "<access-session><monitor>$flag</monitor></access-session>"


# ============================================================
# 7. STORM-CONTROL
# ============================================================

SC_ACTION_LEVEL_173 = (
    "<storm-control><action><level>$pct</level></action></storm-control>"
)
SC_ACTION_SHUTDOWN_173 = "<storm-control><action><shutdown/></action></storm-control>"
SC_ACTION_TRAP_173     = "<storm-control><action><trap/></action></storm-control>"
SC_ACTION_REMOVE_173   = '<storm-control><action nc:operation="remove"/></storm-control>'

# $sc_type: broadcast | multicast | unicast | unknown-unicast
SC_THRESHOLD_PERCENT_173 = (
    "<storm-control><$sc_type><level><threshold>"
    "<rising-threshold>$rise</rising-threshold>"
    "<falling-threshold>$fall</falling-threshold>"
    "</threshold></level></$sc_type></storm-control>"
)
SC_THRESHOLD_REMOVE_173 = (
    '<storm-control><$sc_type nc:operation="remove"/></storm-control>'
)
SC_BROADCAST_INCLUDE_MULTICAST_173 = (
    "<storm-control><broadcast><include><multicast/></include></broadcast></storm-control>"
)
SC_BROADCAST_INCLUDE_MULTICAST_REMOVE_173 = (
    '<storm-control><broadcast><include nc:operation="remove"/></broadcast></storm-control>'
)


# ============================================================
# 8. MACSEC  (Cisco-IOS-XE-switch, augments the interface directly - not switchport)
# ============================================================
# 173-ADAPTED: nodes live in the $SW namespace, so each top node carries xmlns="$SW".
#   enable : empty leaf <macsec/>
#   option : <macsec-option><macsec>...  (replay-protection/window-size, network-link)
# Present on: Fast/Gig/2.5G/5G/AppGig/10G/25G/40G/100G Ethernet and Port-channel.

MSEC_ENABLE_173 = '<macsec xmlns="$SW"/>'
MSEC_ENABLE_REMOVE_173 = '<macsec xmlns="$SW" nc:operation="remove"/>'
MSEC_REPLAY_PROTECTION_173 = (
    '<macsec-option xmlns="$SW"><macsec><replay-protection>'
    '<window-size>$window</window-size>'
    '</replay-protection></macsec></macsec-option>'
)
MSEC_REPLAY_PROTECTION_REMOVE_173 = (
    '<macsec-option xmlns="$SW"><macsec><replay-protection nc:operation="remove"/></macsec></macsec-option>'
)


# ============================================================
# 9. MISC — SUBSCRIBER
# ============================================================

MISC_SUBSCRIBER_INACTIVITY_173 = (
    "<subscriber><aging><inactivity-timer>"
    "<value>$secs</value>"
    "$probe_block"
    "</inactivity-timer></aging></subscriber>"
)
MISC_SUBSCRIBER_INACTIVITY_REMOVE_173 = (
    '<subscriber><aging><inactivity-timer nc:operation="remove"/></aging></subscriber>'
)
MISC_SUBSCRIBER_PROBE_173        = "<subscriber><aging><probe/></aging></subscriber>"
MISC_SUBSCRIBER_PROBE_REMOVE_173 = (
    '<subscriber><aging><probe nc:operation="remove"/></aging></subscriber>'
)


# ============================================================
# 10. PHYSICAL LAYER
# ============================================================
# media-type : only on GigabitEthernet, TwoGigabitEthernet, FiveGigabitEthernet,
#              AppGigabitEthernet, TenGigabitEthernet, TwentyFiveGigE,
#              FortyGigabitEthernet (NOT HundredGigE)
# fec        : only on TwentyFiveGigE (auto|cl108|cl74|cl91|off)

PHY_MEDIA_TYPE_173        = "<media-type>$media</media-type>"
PHY_MEDIA_TYPE_REMOVE_173 = '<media-type nc:operation="remove"/>'
PHY_FEC_173               = "<fec>$fec</fec>"
PHY_FEC_REMOVE_173        = '<fec nc:operation="remove"/>'


# ============================================================
# 11. PORT-CHANNEL
# ============================================================
# PO_LOAD_BALANCE_HASH_ALGO -> NOT PRESENT in 17.3
#   (17.3 has a different leaf <load-balancing> = vlan|flow directly on list Port-channel)

PO_MIN_LINKS_173 = (
    "<port-channel><min-links>$min_links</min-links></port-channel>"       # 2..8
)
PO_MIN_LINKS_REMOVE_173 = (
    '<port-channel><min-links nc:operation="remove"/></port-channel>'
)
PO_STANDALONE_DISABLE_173 = (
    "<port-channel><standalone-disable/></port-channel>"
)
PO_STANDALONE_DISABLE_REMOVE_173 = (
    '<port-channel><standalone-disable nc:operation="remove"/></port-channel>'
)


# ============================================================
# 12. OTHER TYPE LEAVES
# ============================================================
# TYPE_VLAN_AUTOSTATE -> NOT PRESENT in 17.3 (list Vlan has no autostate leaf)

# list Tunnel only
TYPE_TUNNEL_QOS_PRE_CLASSIFY_173 = "<qos><pre-classify/></qos>"
TYPE_TUNNEL_QOS_PRE_CLASSIFY_REMOVE_173 = (
    '<qos><pre-classify nc:operation="remove"/></qos>'
)


# ============================================================
# 13. NVE / VXLAN   (list nve only)
# ============================================================

NVE_HOST_REACHABILITY_BGP_173 = (
    "<host-reachability><protocol><bgp/></protocol></host-reachability>"
)
NVE_HOST_REACHABILITY_BGP_REMOVE_173 = (
    '<host-reachability nc:operation="remove"/>'
)
# source-interface body comes from ios-ifc:interface-grouping (other module);
# container exists in 17.3, leaf names under it are not verifiable from this YANG.
NVE_SOURCE_INTERFACE_173 = (
    "<source-interface><$src_type>$src_name</$src_type></source-interface>"
)
NVE_SOURCE_INTERFACE_REMOVE_173 = '<source-interface nc:operation="remove"/>'
NVE_MEMBER_VNI_VRF_173 = (
    "<member-in-one-line><member><vni>"
    "<vni-range>$vni</vni-range><vrf>$vrf</vrf>"
    "</vni></member></member-in-one-line>"
)
NVE_MEMBER_VNI_VRF_REMOVE_173 = (
    '<member-in-one-line><member nc:operation="remove"><vni><vni-range>$vni</vni-range></vni></member></member-in-one-line>'
)
NVE_MEMBER_VNI_MCAST_GROUP_173 = (
    "<member><vni><vni-range>$vni</vni-range><mcast-group>"
    "<multicast-group-min>$mc_min</multicast-group-min>"
    "$mc_max_block"
    "</mcast-group></vni></member>"
)
NVE_MEMBER_VNI_MCAST_GROUP_REMOVE_173 = (
    '<member><vni nc:operation="remove"><vni-range>$vni</vni-range></vni></member>'
)


# ================================================================
# TEMPLATE REGISTRY  (base label -> {version: template})
# ================================================================
# Engine imports TEMPLATES, looks up TEMPLATES[base][version].
# Families in NOT_PRESENT_173 are registered with a None slot so resolve()
# reports the reason instead of raising "unknown family".

_TRAINS = ("173",)

def _t(**kw):
    """Expand a per-train dict to every train slot (None for missing)."""
    return {v: kw.get(v) for v in _TRAINS}


TEMPLATES = {
    # §1 general attributes
    "DESCRIPTION":                     _t(**{"173": DESCRIPTION_173}),
    "DESCRIPTION_REMOVE":              _t(**{"173": DESCRIPTION_REMOVE_173}),
    "MAC_ADDRESS":                     _t(**{"173": MAC_ADDRESS_173}),
    "MAC_ADDRESS_REMOVE":              _t(**{"173": MAC_ADDRESS_REMOVE_173}),
    # "EXPORT_NAME" / "EXPORT_NAME_REMOVE": NOT PRESENT in 17.3
    "SHUTDOWN":                        _t(**{"173": SHUTDOWN_173}),
    "SHUTDOWN_REMOVE":                 _t(**{"173": SHUTDOWN_REMOVE_173}),
    "MTU":                             _t(**{"173": MTU_173}),
    "MTU_REMOVE":                      _t(**{"173": MTU_REMOVE_173}),
    "DELAY":                           _t(**{"173": DELAY_173}),
    "DELAY_REMOVE":                    _t(**{"173": DELAY_REMOVE_173}),
    "LOAD_INTERVAL":                   _t(**{"173": LOAD_INTERVAL_173}),
    "LOAD_INTERVAL_REMOVE":            _t(**{"173": LOAD_INTERVAL_REMOVE_173}),
    "MAX_BANDWIDTH":                   _t(**{"173": MAX_BANDWIDTH_173}),
    "MAX_BANDWIDTH_REMOVE":            _t(**{"173": MAX_BANDWIDTH_REMOVE_173}),
    "NEGOTIATION":                     _t(**{"173": NEGOTIATION_173}),
    "GEN_MDIX":                        _t(**{"173": GEN_MDIX_173}),
    "SERVICE_INSERTION":               _t(**{"173": SERVICE_INSERTION_173}),
    "SERVICE_INSERTION_REMOVE":        _t(**{"173": SERVICE_INSERTION_REMOVE_173}),
    "QOS_TRUST":                       _t(**{"173": QOS_TRUST_173}),
    "QOS_TRUST_REMOVE":                _t(**{"173": QOS_TRUST_REMOVE_173}),

    # §2 L2 switching
    "L2_SWITCHPORT_TRUE":              _t(**{"173": L2_SWITCHPORT_TRUE_173}),
    "L2_SWITCHPORT_FALSE":             _t(**{"173": L2_SWITCHPORT_FALSE_173}),
    "L2_DTP_DISABLE_TRUE":             _t(**{"173": L2_DTP_DISABLE_TRUE_173}),
    "L2_DTP_DISABLE_FALSE":            _t(**{"173": L2_DTP_DISABLE_FALSE_173}),
    "L2_VOICE_FULL":                   _t(**{"173": L2_VOICE_FULL_173}),
    "L2_VOICE_FULL_REMOVE":            _t(**{"173": L2_VOICE_FULL_REMOVE_173}),
    "L2_VOICE_VLAN_ID":                _t(**{"173": L2_VOICE_VLAN_ID_173}),
    "L2_VOICE_VLAN_DOT1P":             _t(**{"173": L2_VOICE_VLAN_DOT1P_173}),
    "L2_VOICE_VLAN_NONE":              _t(**{"173": L2_VOICE_VLAN_NONE_173}),
    "L2_VOICE_VLAN_UNTAGGED":          _t(**{"173": L2_VOICE_VLAN_UNTAGGED_173}),
    "L2_VOICE_VLAN_REMOVE":            _t(**{"173": L2_VOICE_VLAN_REMOVE_173}),
    "L2_VOICE_DETECT":                 _t(**{"173": L2_VOICE_DETECT_173}),
    "L2_VOICE_DETECT_REMOVE":          _t(**{"173": L2_VOICE_DETECT_REMOVE_173}),
    "L2_ACCESS_VLAN":                  _t(**{"173": L2_ACCESS_VLAN_173}),
    "L2_ACCESS_VLAN_REMOVE":           _t(**{"173": L2_ACCESS_VLAN_REMOVE_173}),
    "L2_TRUNK_PRUNING_ADD":            _t(**{"173": L2_TRUNK_PRUNING_ADD_173}),
    "L2_TRUNK_PRUNING_REMOVE":         _t(**{"173": L2_TRUNK_PRUNING_REMOVE_173}),
    "L2_TRUNK_PRUNING_REPLACE":        _t(**{"173": L2_TRUNK_PRUNING_REPLACE_173}),
    "L2_TRUNK_PRUNING_NONE":           _t(**{"173": L2_TRUNK_PRUNING_NONE_173}),
    "L2_TRUNK_PRUNING_REMOVE_ALL":     _t(**{"173": L2_TRUNK_PRUNING_REMOVE_ALL_173}),
    "PVLAN_GLOBAL":                    _t(**{"173": PVLAN_GLOBAL_173}),
    "PVLAN_GLOBAL_REMOVE":             _t(**{"173": PVLAN_GLOBAL_REMOVE_173}),
    "PVLAN_SECONDARY":                 _t(**{"173": PVLAN_SECONDARY_173}),
    "PVLAN_SECONDARY_REMOVE":          _t(**{"173": PVLAN_SECONDARY_REMOVE_173}),
    "PVLAN_HOST_ASSOC":                _t(**{"173": PVLAN_HOST_ASSOC_173}),
    "PVLAN_HOST_ASSOC_REMOVE":         _t(**{"173": PVLAN_HOST_ASSOC_REMOVE_173}),
    "PVLAN_PROMISCUOUS_MAP":           _t(**{"173": PVLAN_PROMISCUOUS_MAP_173}),
    "PVLAN_PROMISCUOUS_MAP_REMOVE":    _t(**{"173": PVLAN_PROMISCUOUS_MAP_REMOVE_173}),
    "L2_PORTSEC_ENABLE":               _t(**{"173": L2_PORTSEC_ENABLE_173}),
    "L2_PORTSEC_ENABLE_REMOVE":        _t(**{"173": L2_PORTSEC_ENABLE_REMOVE_173}),
    "L2_PORTSEC_MAX":                  _t(**{"173": L2_PORTSEC_MAX_173}),
    "L2_PORTSEC_MAX_VLAN":             _t(**{"173": L2_PORTSEC_MAX_VLAN_173}),
    "L2_PORTSEC_MAX_REMOVE":           _t(**{"173": L2_PORTSEC_MAX_REMOVE_173}),
    "L2_PORTSEC_VIOLATION":            _t(**{"173": L2_PORTSEC_VIOLATION_173}),
    "L2_PORTSEC_VIOLATION_SHUTDOWN_VLAN": _t(**{"173": L2_PORTSEC_VIOLATION_SHUTDOWN_VLAN_173}),
    "L2_PORTSEC_VIOLATION_REMOVE":     _t(**{"173": L2_PORTSEC_VIOLATION_REMOVE_173}),
    "L2_PORTSEC_STICKY":               _t(**{"173": L2_PORTSEC_STICKY_173}),
    "L2_PORTSEC_STICKY_REMOVE":        _t(**{"173": L2_PORTSEC_STICKY_REMOVE_173}),
    "L2_PORTSEC_AGING":                _t(**{"173": L2_PORTSEC_AGING_173}),
    "L2_PORTSEC_AGING_REMOVE":         _t(**{"173": L2_PORTSEC_AGING_REMOVE_173}),
    "L2_PORTSEC_MAC_ACCESS":           _t(**{"173": L2_PORTSEC_MAC_ACCESS_173}),
    "L2_PORTSEC_MAC_ACCESS_REMOVE":    _t(**{"173": L2_PORTSEC_MAC_ACCESS_REMOVE_173}),
    "L2_PORTSEC_MAC_STICKY":           _t(**{"173": L2_PORTSEC_MAC_STICKY_173}),
    "L2_PORTSEC_MAC_STICKY_REMOVE":    _t(**{"173": L2_PORTSEC_MAC_STICKY_REMOVE_173}),
    "L2_PROTECTED":                    _t(**{"173": L2_PROTECTED_173}),
    "L2_PROTECTED_REMOVE":             _t(**{"173": L2_PROTECTED_REMOVE_173}),
    "L2_HOST":                         _t(**{"173": L2_HOST_173}),
    "L2_HOST_REMOVE":                  _t(**{"173": L2_HOST_REMOVE_173}),
    "L2_BLOCK_MULTICAST":              _t(**{"173": L2_BLOCK_MULTICAST_173}),
    "L2_BLOCK_MULTICAST_REMOVE":       _t(**{"173": L2_BLOCK_MULTICAST_REMOVE_173}),
    "L2_BLOCK_UNICAST":                _t(**{"173": L2_BLOCK_UNICAST_173}),
    "L2_BLOCK_UNICAST_REMOVE":         _t(**{"173": L2_BLOCK_UNICAST_REMOVE_173}),
    "L2_VEPA":                         _t(**{"173": L2_VEPA_173}),
    "L2_VEPA_REMOVE":                  _t(**{"173": L2_VEPA_REMOVE_173}),
    "L2PT_TUNNEL_CORE":                _t(**{"173": L2PT_TUNNEL_CORE_173}),
    "L2PT_TUNNEL_CORE_REMOVE":         _t(**{"173": L2PT_TUNNEL_CORE_REMOVE_173}),
    "L2PT_TUNNEL_P2P":                 _t(**{"173": L2PT_TUNNEL_P2P_173}),
    "L2PT_TUNNEL_P2P_REMOVE":          _t(**{"173": L2PT_TUNNEL_P2P_REMOVE_173}),
    "L2PT_TUNNEL_CORE_BLOCK":          _t(**{"173": L2PT_TUNNEL_CORE_BLOCK_173}),
    "L2PT_TUNNEL_CORE_BLOCK_REMOVE":   _t(**{"173": L2PT_TUNNEL_CORE_BLOCK_REMOVE_173}),
    "L2PT_TUNNEL_P2P_BLOCK":           _t(**{"173": L2PT_TUNNEL_P2P_BLOCK_173}),
    "L2PT_TUNNEL_P2P_BLOCK_REMOVE":    _t(**{"173": L2PT_TUNNEL_P2P_BLOCK_REMOVE_173}),
    "L2PT_DROP_THRESHOLD":             _t(**{"173": L2PT_DROP_THRESHOLD_173}),
    "L2PT_DROP_THRESHOLD_REMOVE":      _t(**{"173": L2PT_DROP_THRESHOLD_REMOVE_173}),
    "L2PT_DROP_THRESHOLD_P2P":         _t(**{"173": L2PT_DROP_THRESHOLD_P2P_173}),
    "L2PT_DROP_THRESHOLD_P2P_REMOVE":  _t(**{"173": L2PT_DROP_THRESHOLD_P2P_REMOVE_173}),
    "L2PT_SHUTDOWN_THRESHOLD":         _t(**{"173": L2PT_SHUTDOWN_THRESHOLD_173}),
    "L2PT_SHUTDOWN_THRESHOLD_REMOVE":  _t(**{"173": L2PT_SHUTDOWN_THRESHOLD_REMOVE_173}),
    "L2PT_SHUTDOWN_THRESHOLD_P2P":     _t(**{"173": L2PT_SHUTDOWN_THRESHOLD_P2P_173}),
    "L2PT_SHUTDOWN_THRESHOLD_P2P_REMOVE": _t(**{"173": L2PT_SHUTDOWN_THRESHOLD_P2P_REMOVE_173}),
    "L2PT_FORWARD_PROTOCOL":           _t(**{"173": L2PT_FORWARD_PROTOCOL_173}),
    "L2PT_FORWARD_PROTOCOL_REMOVE":    _t(**{"173": L2PT_FORWARD_PROTOCOL_REMOVE_173}),
    "L2PT_FORWARD_BLOCK":              _t(**{"173": L2PT_FORWARD_BLOCK_173}),
    "L2PT_FORWARD_BLOCK_REMOVE":       _t(**{"173": L2PT_FORWARD_BLOCK_REMOVE_173}),
    "L2PT_FORWARD_DROP":               _t(**{"173": L2PT_FORWARD_DROP_173}),
    "L2PT_FORWARD_DROP_REMOVE":        _t(**{"173": L2PT_FORWARD_DROP_REMOVE_173}),
    "L2PT_FORWARD_SHUTDOWN":           _t(**{"173": L2PT_FORWARD_SHUTDOWN_173}),
    "L2PT_FORWARD_SHUTDOWN_REMOVE":    _t(**{"173": L2PT_FORWARD_SHUTDOWN_REMOVE_173}),

    # §3 ARP + link tuning
    "ARP_TIMEOUT":                     _t(**{"173": ARP_TIMEOUT_173}),
    "ARP_TIMEOUT_REMOVE":              _t(**{"173": ARP_TIMEOUT_REMOVE_173}),
    "ARP_SNAP_TRUE":                   _t(**{"173": ARP_SNAP_TRUE_173}),
    "ARP_SNAP_FALSE":                  _t(**{"173": ARP_SNAP_FALSE_173}),
    "ARP_ENTRY_LIMIT":                 _t(**{"173": ARP_ENTRY_LIMIT_173}),
    "ARP_ENTRY_LIMIT_REMOVE":          _t(**{"173": ARP_ENTRY_LIMIT_REMOVE_173}),
    "ARP_PACKET_PRIORITY":             _t(**{"173": ARP_PACKET_PRIORITY_173}),
    "ARP_PACKET_PRIORITY_REMOVE":      _t(**{"173": ARP_PACKET_PRIORITY_REMOVE_173}),
    "PQ_OUT_ENABLE":                   _t(**{"173": PQ_OUT_ENABLE_173}),
    "PQ_OUT_ENABLE_REMOVE":            _t(**{"173": PQ_OUT_ENABLE_REMOVE_173}),
    "PQ_COS_MAP":                      _t(**{"173": PQ_COS_MAP_173}),
    "PQ_COS_MAP_REMOVE":               _t(**{"173": PQ_COS_MAP_REMOVE_173}),
    "RCV_QUEUE_COS_MAP":               _t(**{"173": RCV_QUEUE_COS_MAP_173}),
    "RCV_QUEUE_COS_MAP_REMOVE":        _t(**{"173": RCV_QUEUE_COS_MAP_REMOVE_173}),
    "FLOWCONTROL":                     _t(**{"173": FLOWCONTROL_173}),
    "FLOWCONTROL_REMOVE":              _t(**{"173": FLOWCONTROL_REMOVE_173}),
    "HOLD_QUEUE":                      _t(**{"173": HOLD_QUEUE_173}),
    "HOLD_QUEUE_REMOVE":               _t(**{"173": HOLD_QUEUE_REMOVE_173}),
    "LINK_BANDWIDTH":                  _t(**{"173": LINK_BANDWIDTH_173}),
    "LINK_BANDWIDTH_REMOVE":           _t(**{"173": LINK_BANDWIDTH_REMOVE_173}),
    "LINK_BANDWIDTH_QOS_REF":          _t(**{"173": LINK_BANDWIDTH_QOS_REF_173}),
    "LINK_BANDWIDTH_QOS_REF_REMOVE":   _t(**{"173": LINK_BANDWIDTH_QOS_REF_REMOVE_173}),
    "DAMPENING_FULL":                  _t(**{"173": DAMPENING_FULL_173}),
    "DAMPENING_DEFAULT":               _t(**{"173": DAMPENING_DEFAULT_173}),
    "DAMPENING_REMOVE":                _t(**{"173": DAMPENING_REMOVE_173}),
    # "SRLG" / "SRLG_REMOVE": NOT PRESENT in 17.3
    "DOMAIN_NAME":                     _t(**{"173": DOMAIN_NAME_173}),
    "DOMAIN_NAME_REMOVE":              _t(**{"173": DOMAIN_NAME_REMOVE_173}),
    "DOMAIN_PATH":                     _t(**{"173": DOMAIN_PATH_173}),
    "DOMAIN_PATH_REMOVE":              _t(**{"173": DOMAIN_PATH_REMOVE_173}),
    "KEEPALIVE_TIMERS":                _t(**{"173": KEEPALIVE_TIMERS_173}),
    "KEEPALIVE_DISABLE":               _t(**{"173": KEEPALIVE_DISABLE_173}),
    "LINK_LOGGING_LINK_STATUS":        _t(**{"173": LINK_LOGGING_LINK_STATUS_173}),
    "LINK_LOGGING_LINK_STATUS_REMOVE": _t(**{"173": LINK_LOGGING_LINK_STATUS_REMOVE_173}),
    "LINK_LOGGING_EVENT":              _t(**{"173": LINK_LOGGING_EVENT_173}),
    "LINK_LOGGING_EVENT_REMOVE":       _t(**{"173": LINK_LOGGING_EVENT_REMOVE_173}),
    "LINK_LOGGING_EVENTS_BLOCK":       _t(**{"173": LINK_LOGGING_EVENTS_BLOCK_173}),
    "LINK_LOGGING_EVENTS_BLOCK_REMOVE":_t(**{"173": LINK_LOGGING_EVENTS_BLOCK_REMOVE_173}),
    "LINK_LOGGING_SPANNING_TREE":      _t(**{"173": LINK_LOGGING_SPANNING_TREE_173}),
    "LINK_LOGGING_SPANNING_TREE_REMOVE": _t(**{"173": LINK_LOGGING_SPANNING_TREE_REMOVE_173}),
    "LINK_LOGGING_SUBIF":              _t(**{"173": LINK_LOGGING_SUBIF_173}),
    "LINK_LOGGING_SUBIF_REMOVE":       _t(**{"173": LINK_LOGGING_SUBIF_REMOVE_173}),
    "FAIR_QUEUE":                      _t(**{"173": FAIR_QUEUE_173}),
    "FAIR_QUEUE_REMOVE":               _t(**{"173": FAIR_QUEUE_REMOVE_173}),
    "FAIR_QUEUE_CONF":                 _t(**{"173": FAIR_QUEUE_CONF_173}),

    # §4 IPv4
    "IP4_PRIMARY":                     _t(**{"173": IP4_PRIMARY_173}),
    "IP4_PRIMARY_REMOVE":              _t(**{"173": IP4_PRIMARY_REMOVE_173}),
    "IP4_SECONDARY":                   _t(**{"173": IP4_SECONDARY_173}),
    "IP4_SECONDARY_REMOVE":            _t(**{"173": IP4_SECONDARY_REMOVE_173}),
    "IP4_DHCP":                        _t(**{"173": IP4_DHCP_173}),
    "IP4_DHCP_REMOVE":                 _t(**{"173": IP4_DHCP_REMOVE_173}),
    "IP4_NEGOTIATED":                  _t(**{"173": IP4_NEGOTIATED_173}),
    "IP4_NEGOTIATED_REMOVE":           _t(**{"173": IP4_NEGOTIATED_REMOVE_173}),
    "IP4_DHCP_OPTIONS":                _t(**{"173": IP4_DHCP_OPTIONS_173}),
    "IP4_UNNUMBERED":                  _t(**{"173": IP4_UNNUMBERED_173}),
    "IP4_UNNUMBERED_REMOVE":           _t(**{"173": IP4_UNNUMBERED_REMOVE_173}),
    "IP4_ACCESS_GROUP_IN":             _t(**{"173": IP4_ACCESS_GROUP_IN_173}),
    "IP4_ACCESS_GROUP_IN_REMOVE":      _t(**{"173": IP4_ACCESS_GROUP_IN_REMOVE_173}),
    "IP4_ACCESS_GROUP_OUT":            _t(**{"173": IP4_ACCESS_GROUP_OUT_173}),
    "IP4_ACCESS_GROUP_OUT_REMOVE":     _t(**{"173": IP4_ACCESS_GROUP_OUT_REMOVE_173}),
    "IP4_ACCESS_GROUP_COMMON_IN":      _t(**{"173": IP4_ACCESS_GROUP_COMMON_IN_173}),
    "IP4_ACCESS_GROUP_COMMON_IN_REMOVE": _t(**{"173": IP4_ACCESS_GROUP_COMMON_IN_REMOVE_173}),
    "IP4_ACCESS_GROUP_COMMON_OUT":     _t(**{"173": IP4_ACCESS_GROUP_COMMON_OUT_173}),
    "IP4_ACCESS_GROUP_COMMON_OUT_REMOVE": _t(**{"173": IP4_ACCESS_GROUP_COMMON_OUT_REMOVE_173}),
    "IP4_VRF_FORWARDING":              _t(**{"173": IP4_VRF_FORWARDING_173}),
    "IP4_VRF_FORWARDING_REMOVE":       _t(**{"173": IP4_VRF_FORWARDING_REMOVE_173}),
    "IP4_VRF_RECEIVE":                 _t(**{"173": IP4_VRF_RECEIVE_173}),
    "IP4_VRF_RECEIVE_REMOVE":          _t(**{"173": IP4_VRF_RECEIVE_REMOVE_173}),
    "IP4_VRF_SITEMAP":                 _t(**{"173": IP4_VRF_SITEMAP_173}),
    "IP4_VRF_SITEMAP_REMOVE":          _t(**{"173": IP4_VRF_SITEMAP_REMOVE_173}),
    "IP4_HELPER":                      _t(**{"173": IP4_HELPER_173}),
    "IP4_HELPER_REMOVE":               _t(**{"173": IP4_HELPER_REMOVE_173}),
    "IP4_HELPER_GLOBAL":               _t(**{"173": IP4_HELPER_GLOBAL_173}),
    "IP4_HELPER_GLOBAL_REMOVE":        _t(**{"173": IP4_HELPER_GLOBAL_REMOVE_173}),
    "IP4_HELPER_VRF":                  _t(**{"173": IP4_HELPER_VRF_173}),
    "IP4_HELPER_VRF_REMOVE":           _t(**{"173": IP4_HELPER_VRF_REMOVE_173}),
    "IP4_POLICY_ROUTE_MAP":            _t(**{"173": IP4_POLICY_ROUTE_MAP_173}),
    "IP4_POLICY_ROUTE_MAP_REMOVE":     _t(**{"173": IP4_POLICY_ROUTE_MAP_REMOVE_173}),
    "IP4_PROXY_ARP":                   _t(**{"173": IP4_PROXY_ARP_173}),
    "IP4_LOCAL_PROXY_ARP":             _t(**{"173": IP4_LOCAL_PROXY_ARP_173}),
    "IP4_LOCAL_PROXY_ARP_REMOVE":      _t(**{"173": IP4_LOCAL_PROXY_ARP_REMOVE_173}),
    "IP4_REDIRECTS":                   _t(**{"173": IP4_REDIRECTS_173}),
    # "IP4_CLEAR_DF": NOT PRESENT in 17.3
    "IP4_TCP_MSS":                     _t(**{"173": IP4_TCP_MSS_173}),
    "IP4_TCP_MSS_REMOVE":              _t(**{"173": IP4_TCP_MSS_REMOVE_173}),
    "IP4_MTU":                         _t(**{"173": IP4_MTU_173}),
    "IP4_MTU_REMOVE":                  _t(**{"173": IP4_MTU_REMOVE_173}),
    "IP4_URPF":                        _t(**{"173": IP4_URPF_173}),
    "IP4_URPF_REMOVE":                 _t(**{"173": IP4_URPF_REMOVE_173}),
    "IP4_ARP_INSPECT_TRUST":           _t(**{"173": IP4_ARP_INSPECT_TRUST_173}),
    "IP4_ARP_INSPECT_TRUST_REMOVE":    _t(**{"173": IP4_ARP_INSPECT_TRUST_REMOVE_173}),
    "IP4_ARP_INSPECT_RATE":            _t(**{"173": IP4_ARP_INSPECT_RATE_173}),
    "IP4_ARP_INSPECT_RATE_REMOVE":     _t(**{"173": IP4_ARP_INSPECT_RATE_REMOVE_173}),
    "IP4_ARP_INSPECT_RATE_NONE":       _t(**{"173": IP4_ARP_INSPECT_RATE_NONE_173}),
    "IP4_DIRECTED_BROADCAST":          _t(**{"173": IP4_DIRECTED_BROADCAST_173}),
    "IP4_DIRECTED_BROADCAST_REMOVE":   _t(**{"173": IP4_DIRECTED_BROADCAST_REMOVE_173}),
    "IP4_DIRECTED_BROADCAST_ACL":      _t(**{"173": IP4_DIRECTED_BROADCAST_ACL_173}),

    # §5 IPv6
    "IP6_ENABLE":                      _t(**{"173": IP6_ENABLE_173}),
    "IP6_ENABLE_REMOVE":               _t(**{"173": IP6_ENABLE_REMOVE_173}),
    "IP6_ADDRESS_PREFIX":              _t(**{"173": IP6_ADDRESS_PREFIX_173}),
    "IP6_ADDRESS_PREFIX_REMOVE":       _t(**{"173": IP6_ADDRESS_PREFIX_REMOVE_173}),
    "IP6_ADDRESS_EUI64":               _t(**{"173": IP6_ADDRESS_EUI64_173}),
    "IP6_ADDRESS_EUI64_REMOVE":        _t(**{"173": IP6_ADDRESS_EUI64_REMOVE_173}),
    "IP6_ADDRESS_ANYCAST":             _t(**{"173": IP6_ADDRESS_ANYCAST_173}),
    "IP6_ADDRESS_ANYCAST_REMOVE":      _t(**{"173": IP6_ADDRESS_ANYCAST_REMOVE_173}),
    "IP6_ADDRESS_LINK_LOCAL":          _t(**{"173": IP6_ADDRESS_LINK_LOCAL_173}),
    "IP6_ADDRESS_LINK_LOCAL_REMOVE":   _t(**{"173": IP6_ADDRESS_LINK_LOCAL_REMOVE_173}),
    "IP6_ADDRESS_AUTOCONFIG":          _t(**{"173": IP6_ADDRESS_AUTOCONFIG_173}),
    "IP6_ADDRESS_AUTOCONFIG_REMOVE":   _t(**{"173": IP6_ADDRESS_AUTOCONFIG_REMOVE_173}),
    "IP6_ADDRESS_AUTOCONFIG_DEFAULT":  _t(**{"173": IP6_ADDRESS_AUTOCONFIG_DEFAULT_173}),
    "IP6_ADDRESS_AUTOCONFIG_DEFAULT_REMOVE": _t(**{"173": IP6_ADDRESS_AUTOCONFIG_DEFAULT_REMOVE_173}),
    "IP6_ADDRESS_DHCP":                _t(**{"173": IP6_ADDRESS_DHCP_173}),
    "IP6_ADDRESS_DHCP_REMOVE":         _t(**{"173": IP6_ADDRESS_DHCP_REMOVE_173}),
    "IP6_ADDRESS_DHCP_RAPID_COMMIT":   _t(**{"173": IP6_ADDRESS_DHCP_RAPID_COMMIT_173}),
    "IP6_ADDRESS_DHCP_RAPID_COMMIT_REMOVE": _t(**{"173": IP6_ADDRESS_DHCP_RAPID_COMMIT_REMOVE_173}),
    # "IP6_ADDRESS_PREFIX_NAME" / "_REMOVE": NOT PRESENT in 17.3
    "IP6_UNNUMBERED":                  _t(**{"173": IP6_UNNUMBERED_173}),
    "IP6_UNNUMBERED_REMOVE":           _t(**{"173": IP6_UNNUMBERED_REMOVE_173}),
    "IP6_MTU":                         _t(**{"173": IP6_MTU_173}),
    "IP6_MTU_REMOVE":                  _t(**{"173": IP6_MTU_REMOVE_173}),
    # "IP6_ND_DAD_ATTEMPTS" / "_REMOVE" / "IP6_ND_NUD_IGP": NOT PRESENT in 17.3
    "IP6_TCP_ADJUST_MSS":              _t(**{"173": IP6_TCP_ADJUST_MSS_173}),
    "IP6_TCP_ADJUST_MSS_REMOVE":       _t(**{"173": IP6_TCP_ADJUST_MSS_REMOVE_173}),
    "IP6_TRAFFIC_FILTER":              _t(**{"173": IP6_TRAFFIC_FILTER_173}),
    "IP6_TRAFFIC_FILTER_REMOVE":       _t(**{"173": IP6_TRAFFIC_FILTER_REMOVE_173}),
    "IP6_SOURCE_GUARD":                _t(**{"173": IP6_SOURCE_GUARD_173}),
    "IP6_SOURCE_GUARD_REMOVE":         _t(**{"173": IP6_SOURCE_GUARD_REMOVE_173}),
    # "IP6_VERIFY_UNICAST_REVERSE_PATH" / "_REMOVE": NOT PRESENT in 17.3

    # §6 access-session
    "AS_PORT_CONTROL":                 _t(**{"173": AS_PORT_CONTROL_173}),
    "AS_PORT_CONTROL_REMOVE":          _t(**{"173": AS_PORT_CONTROL_REMOVE_173}),
    "AS_CONTROL_DIRECTION":            _t(**{"173": AS_CONTROL_DIRECTION_173}),
    "AS_CONTROL_DIRECTION_REMOVE":     _t(**{"173": AS_CONTROL_DIRECTION_REMOVE_173}),
    "AS_HOST_MODE":                    _t(**{"173": AS_HOST_MODE_173}),
    "AS_HOST_MODE_REMOVE":             _t(**{"173": AS_HOST_MODE_REMOVE_173}),
    # "AS_HOST_MODE_PEER" / "_REMOVE": NOT PRESENT in 17.3
    "AS_MONITOR":                      _t(**{"173": AS_MONITOR_173}),

    # §7 storm-control
    "SC_ACTION_LEVEL":                 _t(**{"173": SC_ACTION_LEVEL_173}),
    "SC_ACTION_SHUTDOWN":              _t(**{"173": SC_ACTION_SHUTDOWN_173}),
    "SC_ACTION_TRAP":                  _t(**{"173": SC_ACTION_TRAP_173}),
    "SC_ACTION_REMOVE":                _t(**{"173": SC_ACTION_REMOVE_173}),
    "SC_THRESHOLD_PERCENT":            _t(**{"173": SC_THRESHOLD_PERCENT_173}),
    "SC_THRESHOLD_REMOVE":             _t(**{"173": SC_THRESHOLD_REMOVE_173}),
    "SC_BROADCAST_INCLUDE_MULTICAST":  _t(**{"173": SC_BROADCAST_INCLUDE_MULTICAST_173}),
    "SC_BROADCAST_INCLUDE_MULTICAST_REMOVE": _t(**{"173": SC_BROADCAST_INCLUDE_MULTICAST_REMOVE_173}),

    # §8 MACsec
    "MSEC_ENABLE":                     _t(**{"173": MSEC_ENABLE_173}),
    "MSEC_ENABLE_REMOVE":              _t(**{"173": MSEC_ENABLE_REMOVE_173}),
    "MSEC_REPLAY_PROTECTION":          _t(**{"173": MSEC_REPLAY_PROTECTION_173}),
    "MSEC_REPLAY_PROTECTION_REMOVE":   _t(**{"173": MSEC_REPLAY_PROTECTION_REMOVE_173}),

    # §9 subscriber
    "MISC_SUBSCRIBER_INACTIVITY":        _t(**{"173": MISC_SUBSCRIBER_INACTIVITY_173}),
    "MISC_SUBSCRIBER_INACTIVITY_REMOVE": _t(**{"173": MISC_SUBSCRIBER_INACTIVITY_REMOVE_173}),
    "MISC_SUBSCRIBER_PROBE":             _t(**{"173": MISC_SUBSCRIBER_PROBE_173}),
    "MISC_SUBSCRIBER_PROBE_REMOVE":      _t(**{"173": MISC_SUBSCRIBER_PROBE_REMOVE_173}),

    # §10 physical layer
    "PHY_MEDIA_TYPE":                  _t(**{"173": PHY_MEDIA_TYPE_173}),
    "PHY_MEDIA_TYPE_REMOVE":           _t(**{"173": PHY_MEDIA_TYPE_REMOVE_173}),
    "PHY_FEC":                         _t(**{"173": PHY_FEC_173}),
	    "PHY_FEC":                         _t(**{"173": PHY_FEC_173}),
    "PHY_FEC_REMOVE":                  _t(**{"173": PHY_FEC_REMOVE_173}),

    # §11 port-channel
    "PO_MIN_LINKS":                    _t(**{"173": PO_MIN_LINKS_173}),
    "PO_MIN_LINKS_REMOVE":             _t(**{"173": PO_MIN_LINKS_REMOVE_173}),
    "PO_STANDALONE_DISABLE":           _t(**{"173": PO_STANDALONE_DISABLE_173}),
    "PO_STANDALONE_DISABLE_REMOVE":    _t(**{"173": PO_STANDALONE_DISABLE_REMOVE_173}),
    # "PO_LOAD_BALANCE_HASH_ALGO" / "_REMOVE": NOT PRESENT in 17.3

    # §12 type leaves
    # "TYPE_VLAN_AUTOSTATE": NOT PRESENT in 17.3
    "TYPE_TUNNEL_QOS_PRE_CLASSIFY":         _t(**{"173": TYPE_TUNNEL_QOS_PRE_CLASSIFY_173}),
    "TYPE_TUNNEL_QOS_PRE_CLASSIFY_REMOVE":  _t(**{"173": TYPE_TUNNEL_QOS_PRE_CLASSIFY_REMOVE_173}),

    # §13 NVE
    "NVE_HOST_REACHABILITY_BGP":        _t(**{"173": NVE_HOST_REACHABILITY_BGP_173}),
    "NVE_HOST_REACHABILITY_BGP_REMOVE": _t(**{"173": NVE_HOST_REACHABILITY_BGP_REMOVE_173}),
    "NVE_SOURCE_INTERFACE":             _t(**{"173": NVE_SOURCE_INTERFACE_173}),
    "NVE_SOURCE_INTERFACE_REMOVE":      _t(**{"173": NVE_SOURCE_INTERFACE_REMOVE_173}),
    "NVE_MEMBER_VNI_VRF":               _t(**{"173": NVE_MEMBER_VNI_VRF_173}),
    "NVE_MEMBER_VNI_VRF_REMOVE":        _t(**{"173": NVE_MEMBER_VNI_VRF_REMOVE_173}),
    "NVE_MEMBER_VNI_MCAST_GROUP":       _t(**{"173": NVE_MEMBER_VNI_MCAST_GROUP_173}),
    "NVE_MEMBER_VNI_MCAST_GROUP_REMOVE":_t(**{"173": NVE_MEMBER_VNI_MCAST_GROUP_REMOVE_173}),
}
# 

NOT_PRESENT_173 = {
    "EXPORT_NAME":            "no export-name leaf in 17.3",
    "EXPORT_NAME_REMOVE":     "no export-name leaf in 17.3",
    "SRLG":                   "no srlg container in 17.3",
    "SRLG_REMOVE":            "no srlg container in 17.3",
    "IP4_CLEAR_DF":           "no ip/clear-dont-fragment leaf in 17.3",
    "IP6_ADDRESS_PREFIX_NAME":        "no ipv6/address/prefix-name in 17.3 …",
    "IP6_ADDRESS_PREFIX_NAME_REMOVE": "no ipv6/address/prefix-name in 17.3",
    "IP6_ND_DAD_ATTEMPTS":            "ipv6/nd is an empty container …",
    "IP6_ND_DAD_ATTEMPTS_REMOVE":     "ipv6/nd is an empty container …",
    "IP6_ND_NUD_IGP":                 "ipv6/nd is an empty container …",
    "IP6_VERIFY_UNICAST_REVERSE_PATH":        "no ipv6/verify in 17.3",
    "IP6_VERIFY_UNICAST_REVERSE_PATH_REMOVE": "no ipv6/verify in 17.3",
    "AS_HOST_MODE_PEER":        "no peer option on access-session host-mode in 17.3",
    "AS_HOST_MODE_PEER_REMOVE": "no peer option on access-session host-mode in 17.3",
    "PO_LOAD_BALANCE_HASH_ALGO":        "no load-balance-hash-algo in 17.3 …",
    "PO_LOAD_BALANCE_HASH_ALGO_REMOVE": "no load-balance-hash-algo in 17.3",
    "TYPE_VLAN_AUTOSTATE": ("list Vlan has no autostate leaf in 17.3 …"),
}


for _name in NOT_PRESENT_173:
    if _name in TEMPLATES:
        raise ValueError(
            f"{_name} is both defined in TEMPLATES and listed in NOT_PRESENT_173"
        )
    TEMPLATES[_name] = _t(**{"173": None})
	
# ================================================================
# STARTUP PLACEHOLDER VALIDATION
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
    # namespace slots
    "N", "NC", "SW", "ST", "VLAN",
}


_PLACEHOLDER_RE = re.compile(r"\$([A-Za-z_][A-Za-z0-9_]*)")


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
            "interface_attrs_173: placeholder validation failed:\n  "
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


def render(base, train="173", **kw):
    """Resolve base/train, fill namespaces + caller values, return the XML body.
    Raises KeyError naming any placeholder the caller did not supply."""
    tpl = resolve(base, train)
    try:
        return _Template(tpl).substitute({**NS, **kw})
    except KeyError as e:
        raise KeyError(f"{base}: missing value for placeholder ${e.args[0]}") from None


def _selftest():
    """Render every 17.3 template with dummy values and parse as XML."""
    import xml.etree.ElementTree as ET
    bad = []
    for name in supported_on("173"):
        tpl = resolve(name)
        kw = {ph: "x" for ph in _PLACEHOLDER_RE.findall(tpl) if ph not in NS}
        xml = render(name, **kw)
        try:
            ET.fromstring('<r xmlns:nc="%s">%s</r>' % (NS["NC"], xml))
        except ET.ParseError as e:
            bad.append((name, str(e)))
    n_ok = sum(1 for _ in supported_on("173")) - len(bad)
    print(f"173 selftest: {n_ok} templates OK, {len(bad)} malformed, "
          f"{len(NOT_PRESENT_173)} flagged not present")
    for b in bad:
        print("  BAD", b)
    return not bad

# ================================================================
# RESOLVERS
# ================================================================

def resolve(base, train="173"):
    """Return the template for base/train. Raises with a clear message when missing."""
    if base not in TEMPLATES:
        raise KeyError(f"{base!r} not in 17.3 catalogue ({len(TEMPLATES)} families)")
    tpl = TEMPLATES[base].get(train)
    if tpl is None:
        reason = NOT_PRESENT_173.get(base, "no template for this train")
        raise KeyError(f"{base!r} not available on train {train!r}: {reason}")
    return tpl


def families():
    """Yield every catalogue family name, sorted."""
    for name in sorted(TEMPLATES):
        yield name


def supported_on(train="173"):
    """Yield every family available on the given train."""
    for name, slots in TEMPLATES.items():
        if slots.get(train) is not None:
            yield name


def not_present(train="173"):
    """Yield (family, reason) for every family flagged not present on the train."""
    for name in sorted(NOT_PRESENT_173):
        yield name, NOT_PRESENT_173[name]


def on_off_pairs(train="173"):
    """Yield (on_base, off_base) for every family that has a _REMOVE twin."""
    for base in TEMPLATES:
        if base.endswith("_REMOVE"):
            continue
        twin = base + "_REMOVE"
        if twin in TEMPLATES and TEMPLATES[twin].get(train) is not None:
            yield (base, twin)


def flag_symmetric(train="173"):
    """Yield families whose template uses $flag — symmetric by construction."""
    for base, slots in TEMPLATES.items():
        tpl = slots.get(train)
        if tpl and "$flag" in tpl:
            yield base


if __name__ == "__main__":
    raise SystemExit(0 if _selftest() else 1)