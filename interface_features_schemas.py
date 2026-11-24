# interface_features_schemas.py
# Phase 1 — wire models for the interface-features API.
# Pydantic v2 only. No train awareness, no I/O, no XML, no importlib.
# Everything downstream (mapper, engine, Nornir task) consumes these models.
#
# Design rules:
#   * One model per feature family. `feature` is a Literal that MUST equal
#     the lowercase form of the corresponding template base label in
#     interface_attrs_<train>.py. The engine's mapper enforces the mapping.
#   * `remove: bool = False` on every family that has a *_REMOVE_ twin.
#   * `value: bool` on families that are a single on/off toggle.
#   * Optional inputs use Optional[T] = None. Pair-required inputs are enforced
#     by model_validator, not by the caller.
#   * Native-scoped families (VLAN_*, PVLAN_GLOBAL*, PVLAN_SECONDARY*, SVI_*)
#     live in their own list on FeatureChange. The validator rejects mixing.

from __future__ import annotations

import ipaddress
from enum import Enum
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, Field, field_validator, model_validator


# ================================================================
# ENUMS
# ================================================================

class Train(str, Enum):
    xe_1612 = "1612"
    xe_173  = "173"
    xe_179  = "179"
    xe_1712 = "1712"
    xe_1715 = "1715"


class InterfaceType(str, Enum):
    gigabit_ethernet          = "GigabitEthernet"
    ten_gigabit_ethernet      = "TenGigabitEthernet"
    twenty_five_gig_e         = "TwentyFiveGigE"
    forty_gigabit_ethernet    = "FortyGigabitEthernet"
    fifty_gigabit_ethernet    = "FiftyGigabitEthernet"
    hundred_gig_e             = "HundredGigE"
    two_hundred_gig_e         = "TwoHundredGigE"
    four_hundred_gig_e        = "FourHundredGigE"
    app_gigabit_ethernet      = "AppGigabitEthernet"
    two_gigabit_ethernet      = "TwoGigabitEthernet"
    five_gigabit_ethernet     = "FiveGigabitEthernet"
    port_channel              = "Port-channel"
    port_channel_subinterface = "Port-channel-subinterface/Port-channel"
    loopback                  = "Loopback"
    tunnel                    = "Tunnel"
    vlan                      = "Vlan"
    nve                       = "nve"
    ucse                      = "ucse"
    ethernet_internal         = "Ethernet-Internal"
    wlan_gigabit_ethernet     = "Wlan-GigabitEthernet"


class FlowMode(str, Enum):
    desired = "desired"
    on      = "on"
    off     = "off"


class VoiceVlanKind(str, Enum):
    id       = "id"
    dot1p    = "dot1p"
    none     = "none"
    untagged = "untagged"
    name     = "name"


class TrunkEncap(str, Enum):
    dot1q     = "dot1q"
    isl       = "isl"
    negotiate = "negotiate"


class PortSecViolation(str, Enum):
    protect  = "protect"
    restrict = "restrict"
    shutdown = "shutdown"


class PortSecAgingType(str, Enum):
    absolute   = "absolute"
    inactivity = "inactivity"


class AccessSessionHostMode(str, Enum):
    single_host  = "single-host"
    multi_host   = "multi-host"
    multi_domain = "multi-domain"
    multi_auth   = "multi-auth"


class AccessSessionPortControl(str, Enum):
    auto               = "auto"
    force_authorized   = "force-authorized"
    force_unauthorized = "force-unauthorized"


class AccessSessionControlDir(str, Enum):
    both = "both"
    in_  = "in"


class StormControlType(str, Enum):
    broadcast       = "broadcast"
    multicast       = "multicast"
    unicast         = "unicast"
    unknown_unicast = "unknown-unicast"


class StormControlAction(str, Enum):
    level    = "level"
    shutdown = "shutdown"
    trap     = "trap"


class UrpfMode(str, Enum):
    rx  = "rx"
    any = "any"


class MediaType(str, Enum):
    auto_select = "auto-select"
    rj45        = "rj45"
    sfp         = "sfp"


class FecMode(str, Enum):
    auto  = "auto"
    cl108 = "cl108"
    cl74  = "cl74"
    cl91  = "cl91"
    off   = "off"


class PvlanType(str, Enum):
    community = "community"
    isolated  = "isolated"


class ServiceInsertion(str, Enum):
    waas   = "waas"
    appqoe = "appqoe"


class VlanState(str, Enum):
    active  = "active"
    suspend = "suspend"


class UniVlanType(str, Enum):
    community = "community"
    isolated  = "isolated"


class L2ptCoreProto(str, Enum):
    cdp  = "cdp"
    stp  = "stp"
    vtp  = "vtp"
    lldp = "lldp"


class L2ptP2pProto(str, Enum):
    lacp = "lacp"
    pagp = "pagp"
    udld = "udld"


# ================================================================
# INTERFACE REFERENCE
# ================================================================

class InterfaceRef(BaseModel):
    parent: InterfaceType
    name: str = Field(..., pattern=r"^\d+([/.]\d+)*$")


# ================================================================
# §1 GENERAL ATTRIBUTES
# ================================================================

class DescriptionFeature(BaseModel):
    feature: Literal["description"]
    value: Optional[str] = Field(None, max_length=200)
    remove: bool = False


class ExportNameFeature(BaseModel):
    feature: Literal["export_name"]
    value: Optional[str] = Field(None, min_length=1, max_length=128)
    remove: bool = False


class MacAddressFeature(BaseModel):
    feature: Literal["mac_address"]
    value: Optional[str] = Field(
        None, pattern=r"^[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}\.[0-9a-fA-F]{4}$"
    )
    remove: bool = False


class ShutdownFeature(BaseModel):
    feature: Literal["shutdown"]
    value: bool


class MtuFeature(BaseModel):
    feature: Literal["mtu"]
    value: Optional[int] = Field(None, ge=64, le=18000)
    remove: bool = False


class DelayFeature(BaseModel):
    feature: Literal["delay"]
    value: Optional[int] = Field(None, ge=1, le=16777215)
    remove: bool = False


class LoadIntervalFeature(BaseModel):
    feature: Literal["load_interval"]
    value: Optional[int] = Field(None, ge=30, le=600)
    remove: bool = False

    @field_validator("value")
    @classmethod
    def _multiple_of_30(cls, v):
        if v is not None and v % 30 != 0:
            raise ValueError("load_interval must be a multiple of 30")
        return v


class MaxBandwidthFeature(BaseModel):
    feature: Literal["max_bandwidth"]
    value: Optional[int] = Field(None, ge=1, le=100)
    remove: bool = False


class NegotiationFeature(BaseModel):
    feature: Literal["negotiation"]
    value: bool


class MdixFeature(BaseModel):
    feature: Literal["mdix"]
    value: bool


class ServiceInsertionFeature(BaseModel):
    feature: Literal["service_insertion"]
    value: Optional[ServiceInsertion] = None
    remove: bool = False


class QosTrustFeature(BaseModel):
    feature: Literal["qos_trust"]
    device: Literal["cisco-phone"] = "cisco-phone"
    remove: bool = False


# ================================================================
# §2 L2 SWITCHING
# ================================================================

class SwitchportModeFeature(BaseModel):
    """True -> L2_SWITCHPORT_TRUE; False -> L2_SWITCHPORT_FALSE."""
    feature: Literal["l2_switchport"]
    value: bool


class DtpDisableFeature(BaseModel):
    """True -> L2_DTP_DISABLE_TRUE (nonegotiate on); False -> L2_DTP_DISABLE_FALSE."""
    feature: Literal["l2_dtp_nonegotiate"]
    value: bool


class VoiceVlanFeature(BaseModel):
    feature: Literal["l2_voice_vlan"]
    kind: VoiceVlanKind
    vlan: Optional[int] = Field(None, ge=1, le=4094)
    vlan_name: Optional[str] = None
    remove: bool = False

    @model_validator(mode="after")
    def _kind_requires_field(self):
        if self.remove:
            return self
        if self.kind == VoiceVlanKind.id and self.vlan is None:
            raise ValueError("voice_vlan kind='id' requires vlan")
        if self.kind == VoiceVlanKind.name and not self.vlan_name:
            raise ValueError("voice_vlan kind='name' requires vlan_name")
        return self


class VoiceDetectFeature(BaseModel):
    feature: Literal["l2_voice_detect"]
    value: bool


class AccessVlanFeature(BaseModel):
    feature: Literal["l2_access_vlan"]
    vlan: Optional[int] = Field(None, ge=1, le=4094)
    remove: bool = False


class TrunkAllowedFeature(BaseModel):
    feature: Literal["l2_trunk_allowed"]
    vlans: Optional[str] = Field(None, description="e.g. '10-20,30', 'all', 'none'")
    remove: bool = False


class TrunkEncapFeature(BaseModel):
    feature: Literal["l2_trunk_encapsulation"]
    value: Optional[TrunkEncap] = None
    remove: bool = False


class TrunkNativeVlanFeature(BaseModel):
    feature: Literal["l2_trunk_native_vlan"]
    vlan: Optional[int] = Field(None, ge=1, le=4094)
    tag: Optional[bool] = None
    remove: bool = False


class TrunkPruningFeature(BaseModel):
    feature: Literal["l2_trunk_pruning"]
    op: Literal["add", "remove", "replace", "none"]
    vlans: Optional[str] = None
    remove_all: bool = False

    @model_validator(mode="after")
    def _op_requires_vlans(self):
        if self.op in ("add", "remove", "replace") and not self.vlans:
            raise ValueError(f"l2_trunk_pruning op={self.op} requires vlans")
        return self


class PortSecurityEnableFeature(BaseModel):
    feature: Literal["l2_port_security_enable"]
    value: bool


class PortSecurityMaxFeature(BaseModel):
    feature: Literal["l2_port_security_max"]
    max_addresses: Optional[int] = Field(None, ge=1, le=4097)
    vlan: Optional[str] = None
    remove: bool = False


class PortSecurityViolationFeature(BaseModel):
    feature: Literal["l2_port_security_violation"]
    violation: Optional[PortSecViolation] = None
    remove: bool = False


class PortSecurityStickyFeature(BaseModel):
    feature: Literal["l2_port_security_sticky"]
    value: bool


class PortSecurityAgingFeature(BaseModel):
    feature: Literal["l2_port_security_aging"]
    minutes: Optional[int] = Field(None, ge=1, le=1440)
    aging_type: Optional[PortSecAgingType] = None
    static: bool = False
    remove: bool = False


class PortSecurityMacFeature(BaseModel):
    feature: Literal["l2_port_security_mac"]
    hw_address: Optional[str] = Field(None, pattern=r"^([0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}$")
    vlan: Optional[int] = Field(None, ge=1, le=4094)
    remove: bool = False


class ProtectedFeature(BaseModel):
    feature: Literal["l2_protected"]
    value: bool


class HostFeature(BaseModel):
    feature: Literal["l2_host"]
    value: bool


class BlockMulticastFeature(BaseModel):
    feature: Literal["l2_block_multicast"]
    value: bool


class BlockUnicastFeature(BaseModel):
    feature: Literal["l2_block_unicast"]
    value: bool


class VepaFeature(BaseModel):
    feature: Literal["l2_vepa"]
    value: bool


class PvlanHostAssocFeature(BaseModel):
    feature: Literal["pvlan_host_assoc"]
    primary_vlan: int = Field(..., ge=1, le=4094)
    secondary_vlan: int = Field(..., ge=1, le=4094)
    remove: bool = False


class PvlanPromiscuousMapFeature(BaseModel):
    feature: Literal["pvlan_promiscuous_map"]
    primary_vlan: int = Field(..., ge=1, le=4094)
    secondary_vlans: str = Field(..., description="e.g. '101,102' or '101-105'")
    remove: bool = False


class L2ptTunnelCoreFeature(BaseModel):
    feature: Literal["l2pt_tunnel_core"]
    proto: L2ptCoreProto
    remove: bool = False


class L2ptTunnelP2pFeature(BaseModel):
    feature: Literal["l2pt_tunnel_p2p"]
    proto: L2ptP2pProto
    remove: bool = False


class L2ptThresholdFeature(BaseModel):
    feature: Literal["l2pt_threshold"]
    kind: Literal["drop", "shutdown"]
    proto: Optional[L2ptCoreProto] = None
    p2p_proto: Optional[L2ptP2pProto] = None
    pps: int = Field(..., ge=1, le=4096)
    remove: bool = False

    @model_validator(mode="after")
    def _exactly_one_proto(self):
        if (self.proto is None) == (self.p2p_proto is None):
            raise ValueError("l2pt_threshold requires exactly one of proto / p2p_proto")
        return self


# ================================================================
# §3 ARP + LINK TUNING
# ================================================================

class ArpTimeoutFeature(BaseModel):
    feature: Literal["arp_timeout"]
    seconds: Optional[int] = Field(None, ge=60, le=2147483)
    remove: bool = False


class ArpSnapFeature(BaseModel):
    """True -> ARP_SNAP_TRUE (snap on); False -> ARP_SNAP_FALSE (snap removed)."""
    feature: Literal["arp_snap"]
    value: bool


class ArpEntryLimitFeature(BaseModel):
    feature: Literal["arp_entry_limit"]
    count: Optional[int] = Field(None, ge=1)
    log_seconds: Optional[int] = Field(None, ge=0)
    remove: bool = False


class ArpPacketPriorityFeature(BaseModel):
    feature: Literal["arp_packet_priority"]
    value: bool


class PriorityQueueOutFeature(BaseModel):
    feature: Literal["pq_out"]
    value: bool


class PriorityQueueCosMapFeature(BaseModel):
    feature: Literal["pq_cos_map"]
    qid: int = Field(..., ge=0, le=7)
    cos_values: List[int] = Field(..., min_length=1, max_length=8)
    remove: bool = False

    @field_validator("cos_values")
    @classmethod
    def _cos_range(cls, v):
        for c in v:
            if not 0 <= c <= 7:
                raise ValueError("cos values must be 0..7")
        return v


class RcvQueueCosMapFeature(BaseModel):
    feature: Literal["rcv_queue_cos_map"]
    qid: int = Field(..., ge=0, le=7)
    tid: int = Field(..., ge=0, le=7)
    cos_values: List[int] = Field(..., min_length=1, max_length=8)
    remove: bool = False


class FlowcontrolFeature(BaseModel):
    feature: Literal["flowcontrol"]
    rx: Optional[FlowMode] = None
    tx: Optional[FlowMode] = None
    remove: bool = False


class HoldQueueFeature(BaseModel):
    feature: Literal["hold_queue"]
    direction: Literal["in", "out"]
    qlen: Optional[int] = Field(None, ge=1)
    remove: bool = False


class LinkBandwidthFeature(BaseModel):
    feature: Literal["link_bandwidth"]
    kbps: Optional[int] = Field(None, ge=1, le=200_000_000)
    qos_reference: bool = False
    remove: bool = False


class DampeningFeature(BaseModel):
    feature: Literal["dampening"]
    half_life: Optional[int] = Field(None, ge=1, le=30)
    reuse: Optional[int] = Field(None, ge=1)
    suppress: Optional[int] = Field(None, ge=1)
    max_suppress: Optional[int] = Field(None, ge=1, le=255)
    defaults: bool = False
    remove: bool = False


class SrlgFeature(BaseModel):
    feature: Literal["srlg"]
    values: Optional[List[int]] = Field(None, min_length=1)
    remove: bool = False


class DomainNameFeature(BaseModel):
    feature: Literal["domain_name"]
    name: Optional[str] = None
    remove: bool = False


class DomainPathFeature(BaseModel):
    feature: Literal["domain_path"]
    path: Optional[str] = None
    path_id: Optional[int] = Field(None, ge=1, le=65535)
    remove: bool = False


class KeepaliveFeature(BaseModel):
    feature: Literal["keepalive"]
    enabled: bool
    period: Optional[int] = Field(None, ge=1, le=32767)
    retries: Optional[int] = Field(None, ge=1, le=255)


class LoggingLinkStatusFeature(BaseModel):
    feature: Literal["logging_link_status"]
    value: bool


class LoggingEventFeature(BaseModel):
    feature: Literal["logging_event"]
    event: Literal[
        "bundle-status", "link-status", "trunk-status",
        "nfas-status", "power-inline-status", "status",
    ]
    remove: bool = False


class LoggingSpanningTreeFeature(BaseModel):
    feature: Literal["logging_spanning_tree"]
    value: bool


class LoggingSubifFeature(BaseModel):
    feature: Literal["logging_subif"]
    ignore_bulk: bool = False
    remove: bool = False


class FairQueueFeature(BaseModel):
    feature: Literal["fair_queue"]
    enabled: Optional[bool] = None       # None = default fair-queue incomplete form
    remove: bool = False


# ================================================================
# §4 IPv4
# ================================================================

class Ipv4AddressFeature(BaseModel):
    feature: Literal["ipv4_address"]
    ip: Optional[ipaddress.IPv4Address] = None
    mask: Optional[ipaddress.IPv4Address] = None
    secondary: bool = False
    remove: bool = False

    @model_validator(mode="after")
    def _pair_required(self):
        if not self.remove and (self.ip is None or self.mask is None):
            raise ValueError("ipv4_address requires ip and mask unless remove=True")
        return self


class Ipv4DhcpFeature(BaseModel):
    feature: Literal["ipv4_dhcp"]
    mode: Literal["dhcp", "negotiated"]
    client_id_interface: Optional[InterfaceRef] = None
    hostname: Optional[str] = None
    remove: bool = False


class Ipv4UnnumberedFeature(BaseModel):
    feature: Literal["ipv4_unnumbered"]
    source_interface: Optional[InterfaceRef] = None
    remove: bool = False


class Ipv4AccessGroupFeature(BaseModel):
    feature: Literal["ipv4_access_group"]
    direction: Literal["in", "out"]
    acl: Optional[str] = None
    common_acl: Optional[str] = None
    remove: bool = False


class VrfForwardingFeature(BaseModel):
    feature: Literal["vrf_forwarding"]
    vrf: Optional[str] = None
    remove: bool = False


class Ipv4VrfReceiveFeature(BaseModel):
    feature: Literal["ipv4_vrf_receive"]
    vrf: Optional[str] = None
    remove: bool = False


class Ipv4VrfSitemapFeature(BaseModel):
    feature: Literal["ipv4_vrf_sitemap"]
    route_map: Optional[str] = None
    remove: bool = False


class HelperAddressFeature(BaseModel):
    feature: Literal["helper_address"]
    helper: Optional[ipaddress.IPv4Address] = None
    global_: bool = False
    vrf: Optional[str] = None
    remove: bool = False


class PolicyRouteMapFeature(BaseModel):
    feature: Literal["policy_route_map"]
    route_map: Optional[str] = None
    remove: bool = False


class ProxyArpFeature(BaseModel):
    feature: Literal["proxy_arp"]
    value: bool


class LocalProxyArpFeature(BaseModel):
    feature: Literal["local_proxy_arp"]
    value: bool


class RedirectsFeature(BaseModel):
    feature: Literal["redirects"]
    value: bool


class ClearDfFeature(BaseModel):
    feature: Literal["clear_df"]
    value: bool


class TcpAdjustMssFeature(BaseModel):
    feature: Literal["tcp_adjust_mss"]
    mss: Optional[int] = Field(None, ge=500, le=1460)
    remove: bool = False


class IpMtuFeature(BaseModel):
    feature: Literal["ip_mtu"]
    value: Optional[int] = Field(None, ge=68, le=18000)
    remove: bool = False


class UrpfFeature(BaseModel):
    feature: Literal["urpf"]
    via: Optional[UrpfMode] = None
    allow_default: bool = False
    allow_self_ping: bool = False
    acl: Optional[str] = None
    remove: bool = False


class ArpInspectTrustFeature(BaseModel):
    feature: Literal["arp_inspect_trust"]
    value: bool


class ArpInspectRateFeature(BaseModel):
    feature: Literal["arp_inspect_rate"]
    pps: Optional[int] = Field(None, ge=0, le=2048)
    burst: Optional[int] = Field(None, ge=1, le=15)
    unlimited: bool = False
    remove: bool = False


class DirectedBroadcastFeature(BaseModel):
    feature: Literal["directed_broadcast"]
    acl: Optional[str] = None
    remove: bool = False


# ================================================================
# §5 IPv6
# ================================================================

class Ipv6EnableFeature(BaseModel):
    feature: Literal["ipv6_enable"]
    value: bool


class Ipv6AddressFeature(BaseModel):
    feature: Literal["ipv6_address"]
    prefix: Optional[ipaddress.IPv6Network] = None
    kind: Literal["plain", "eui64", "anycast", "link_local", "prefix_name"] = "plain"
    link_local: Optional[ipaddress.IPv6Address] = None
    prefix_name: Optional[str] = None
    remove: bool = False


class Ipv6AutoconfigFeature(BaseModel):
    feature: Literal["ipv6_autoconfig"]
    default: bool = False
    remove: bool = False


class Ipv6DhcpFeature(BaseModel):
    feature: Literal["ipv6_dhcp"]
    rapid_commit: bool = False
    remove: bool = False


class Ipv6UnnumberedFeature(BaseModel):
    feature: Literal["ipv6_unnumbered"]
    source_interface: Optional[InterfaceRef] = None
    remove: bool = False


class Ipv6MtuFeature(BaseModel):
    feature: Literal["ipv6_mtu"]
    value: Optional[int] = Field(None, ge=1280, le=9976)
    remove: bool = False


class Ipv6TcpAdjustMssFeature(BaseModel):
    feature: Literal["ipv6_tcp_adjust_mss"]
    mss: Optional[int] = Field(None, ge=40, le=1454)
    remove: bool = False


class Ipv6TrafficFilterFeature(BaseModel):
    feature: Literal["ipv6_traffic_filter"]
    direction: Literal["in", "out"]
    acl: Optional[str] = None
    remove: bool = False


class Ipv6SourceGuardFeature(BaseModel):
    feature: Literal["ipv6_source_guard"]
    policy: Optional[str] = None
    remove: bool = False


class Ipv6NdDadAttemptsFeature(BaseModel):
    feature: Literal["ipv6_nd_dad_attempts"]
    attempts: Optional[int] = Field(None, ge=0, le=600)
    remove: bool = False


class Ipv6NdNudIgpFeature(BaseModel):
    feature: Literal["ipv6_nd_nud_igp"]
    value: bool


class Ipv6VerifyReversePathFeature(BaseModel):
    feature: Literal["ipv6_verify_reverse_path"]
    acl: Optional[str] = None
    remove: bool = False


# ================================================================
# §6 ACCESS-SESSION
# ================================================================

class AccessSessionPortControlFeature(BaseModel):
    feature: Literal["as_port_control"]
    value: Optional[AccessSessionPortControl] = None
    remove: bool = False


class AccessSessionControlDirectionFeature(BaseModel):
    feature: Literal["as_control_direction"]
    value: Optional[AccessSessionControlDir] = None
    remove: bool = False


class AccessSessionHostModeFeature(BaseModel):
    feature: Literal["as_host_mode"]
    value: Optional[AccessSessionHostMode] = None
    peer: bool = False
    remove: bool = False


class AccessSessionMonitorFeature(BaseModel):
    feature: Literal["as_monitor"]
    value: bool


# ================================================================
# §7 STORM-CONTROL
# ================================================================

class StormControlActionFeature(BaseModel):
    feature: Literal["storm_control_action"]
    action: StormControlAction
    level_pct: Optional[int] = Field(None, ge=0, le=100)
    remove: bool = False


class StormControlThresholdFeature(BaseModel):
    feature: Literal["storm_control_threshold"]
    sc_type: StormControlType
    rise: Optional[int] = Field(None, ge=0, le=100)
    fall: Optional[int] = Field(None, ge=0, le=100)
    remove: bool = False


class StormControlBroadcastIncludeMulticastFeature(BaseModel):
    feature: Literal["storm_control_bcast_include_mcast"]
    value: bool


# ================================================================
# §8 MACSEC
# ================================================================

class MacsecEnableFeature(BaseModel):
    feature: Literal["macsec_enable"]
    value: bool


class MacsecReplayProtectionFeature(BaseModel):
    feature: Literal["macsec_replay_protection"]
    window: Optional[int] = Field(None, ge=0, le=4_294_967_295)
    remove: bool = False


# ================================================================
# §9 SUBSCRIBER
# ================================================================

class SubscriberInactivityFeature(BaseModel):
    feature: Literal["subscriber_inactivity"]
    seconds: Optional[int] = Field(None, ge=1)
    probe: bool = False
    remove: bool = False


class SubscriberProbeFeature(BaseModel):
    feature: Literal["subscriber_probe"]
    value: bool


# ================================================================
# §10 PHYSICAL LAYER
# ================================================================

class MediaTypeFeature(BaseModel):
    feature: Literal["media_type"]
    value: Optional[MediaType] = None
    remove: bool = False


class FecFeature(BaseModel):
    feature: Literal["fec"]
    value: Optional[FecMode] = None
    remove: bool = False


# ================================================================
# §11 PORT-CHANNEL
# ================================================================

class PoLoadBalanceFeature(BaseModel):
    feature: Literal["po_load_balance"]
    algo: Optional[str] = None
    balancing: Optional[Literal["vlan", "flow"]] = None
    remove: bool = False


class PoMinLinksFeature(BaseModel):
    feature: Literal["po_min_links"]
    value: Optional[int] = Field(None, ge=2, le=8)
    remove: bool = False


class PoStandaloneDisableFeature(BaseModel):
    feature: Literal["po_standalone_disable"]
    value: bool


# ================================================================
# §12 OTHER TYPE LEAVES
# ================================================================

class VlanAutostateFeature(BaseModel):
    feature: Literal["vlan_autostate"]
    value: bool


class TunnelQosPreClassifyFeature(BaseModel):
    feature: Literal["tunnel_qos_pre_classify"]
    value: bool


# ================================================================
# §13 NVE / VXLAN
# ================================================================

class NveHostReachabilityBgpFeature(BaseModel):
    feature: Literal["nve_host_reachability_bgp"]
    value: bool


class NveSourceInterfaceFeature(BaseModel):
    feature: Literal["nve_source_interface"]
    source_interface: Optional[InterfaceRef] = None
    remove: bool = False


class NveMemberVniVrfFeature(BaseModel):
    feature: Literal["nve_member_vni_vrf"]
    vni: Optional[int] = Field(None, ge=1, le=16777215)
    vrf: Optional[str] = None
    remove: bool = False


class NveMemberVniMcastGroupFeature(BaseModel):
    feature: Literal["nve_member_vni_mcast_group"]
    vni: Optional[int] = Field(None, ge=1, le=16777215)
    mc_min: Optional[ipaddress.IPv4Address] = None
    mc_max: Optional[ipaddress.IPv4Address] = None
    remove: bool = False


# ================================================================
# §14 VLAN DB + SVI  (native-scoped)
# ================================================================

class VlanCreateFeature(BaseModel):
    feature: Literal["vlan_create"]
    vlan_id: int = Field(..., ge=1, le=4094)


class VlanDeleteFeature(BaseModel):
    feature: Literal["vlan_delete"]
    vlan_id: int = Field(..., ge=1, le=4094)


class VlanNameFeature(BaseModel):
    feature: Literal["vlan_name"]
    vlan_id: int = Field(..., ge=1, le=4094)
    name: Optional[str] = None
    remove: bool = False


class VlanStateFeature(BaseModel):
    feature: Literal["vlan_state"]
    vlan_id: int = Field(..., ge=1, le=4094)
    state: Optional[VlanState] = None
    remove: bool = False


class VlanRemoteSpanFeature(BaseModel):
    feature: Literal["vlan_remote_span"]
    vlan_id: int = Field(..., ge=1, le=4094)
    value: bool


class VlanUniFeature(BaseModel):
    feature: Literal["vlan_uni"]
    vlan_id: int = Field(..., ge=1, le=4094)
    uni_type: Optional[UniVlanType] = None
    remove: bool = False


class PvlanGlobalFeature(BaseModel):
    feature: Literal["pvlan_global"]
    primary_vlan: int = Field(..., ge=1, le=4094)
    secondary_vlans: Optional[str] = None
    action: Optional[Literal["add", "remove", "all"]] = None
    remove: bool = False


class PvlanSecondaryFeature(BaseModel):
    feature: Literal["pvlan_secondary"]
    secondary_vlan: int = Field(..., ge=1, le=4094)
    pvlan_type: Optional[PvlanType] = None
    remove: bool = False


class SviPrivateVlanMappingFeature(BaseModel):
    feature: Literal["svi_private_vlan_mapping"]
    mapping: Optional[str] = None
    remove: bool = False


# ================================================================
# FEATURE UNION
# ================================================================

FeatureModel = Union[
    # §1
    DescriptionFeature, ExportNameFeature, MacAddressFeature, ShutdownFeature,
    MtuFeature, DelayFeature, LoadIntervalFeature, MaxBandwidthFeature,
    NegotiationFeature, MdixFeature, ServiceInsertionFeature, QosTrustFeature,
    # §2
    SwitchportModeFeature, DtpDisableFeature, VoiceVlanFeature, VoiceDetectFeature,
    AccessVlanFeature, TrunkAllowedFeature, TrunkEncapFeature, TrunkNativeVlanFeature,
    TrunkPruningFeature, PortSecurityEnableFeature, PortSecurityMaxFeature,
    PortSecurityViolationFeature, PortSecurityStickyFeature, PortSecurityAgingFeature,
    PortSecurityMacFeature, ProtectedFeature, HostFeature, BlockMulticastFeature,
    BlockUnicastFeature, VepaFeature, PvlanHostAssocFeature, PvlanPromiscuousMapFeature,
    L2ptTunnelCoreFeature, L2ptTunnelP2pFeature, L2ptThresholdFeature,
    # §3
    ArpTimeoutFeature, ArpSnapFeature, ArpEntryLimitFeature, ArpPacketPriorityFeature,
    PriorityQueueOutFeature, PriorityQueueCosMapFeature, RcvQueueCosMapFeature,
    FlowcontrolFeature, HoldQueueFeature, LinkBandwidthFeature, DampeningFeature,
    SrlgFeature, DomainNameFeature, DomainPathFeature, KeepaliveFeature,
    LoggingLinkStatusFeature, LoggingEventFeature, LoggingSpanningTreeFeature,
    LoggingSubifFeature, FairQueueFeature,
    # §4
    Ipv4AddressFeature, Ipv4DhcpFeature, Ipv4UnnumberedFeature, Ipv4AccessGroupFeature,
    VrfForwardingFeature, Ipv4VrfReceiveFeature, Ipv4VrfSitemapFeature, HelperAddressFeature,
    PolicyRouteMapFeature, ProxyArpFeature, LocalProxyArpFeature, RedirectsFeature,
    ClearDfFeature, TcpAdjustMssFeature, IpMtuFeature, UrpfFeature,
    ArpInspectTrustFeature, ArpInspectRateFeature, DirectedBroadcastFeature,
    # §5
    Ipv6EnableFeature, Ipv6AddressFeature, Ipv6AutoconfigFeature, Ipv6DhcpFeature,
    Ipv6UnnumberedFeature, Ipv6MtuFeature, 
        Ipv6UnnumberedFeature, Ipv6MtuFeature, Ipv6TcpAdjustMssFeature,
    Ipv6TrafficFilterFeature, Ipv6SourceGuardFeature, Ipv6NdDadAttemptsFeature,
    Ipv6NdNudIgpFeature, Ipv6VerifyReversePathFeature,
    # §6
    AccessSessionPortControlFeature, AccessSessionControlDirectionFeature,
    AccessSessionHostModeFeature, AccessSessionMonitorFeature,
    # §7
    StormControlActionFeature, StormControlThresholdFeature,
    StormControlBroadcastIncludeMulticastFeature,
    # §8
    MacsecEnableFeature, MacsecReplayProtectionFeature,
    # §9
    SubscriberInactivityFeature, SubscriberProbeFeature,
    # §10
    MediaTypeFeature, FecFeature,
    # §11
    PoLoadBalanceFeature, PoMinLinksFeature, PoStandaloneDisableFeature,
    # §12
    VlanAutostateFeature, TunnelQosPreClassifyFeature,
    # §13
    NveHostReachabilityBgpFeature, NveSourceInterfaceFeature,
    NveMemberVniVrfFeature, NveMemberVniMcastGroupFeature,
    # §14
    VlanCreateFeature, VlanDeleteFeature, VlanNameFeature, VlanStateFeature,
    VlanRemoteSpanFeature, VlanUniFeature,
    PvlanGlobalFeature, PvlanSecondaryFeature, SviPrivateVlanMappingFeature,
]


# ================================================================
# INTERFACE BUNDLE
# ================================================================

class InterfaceConfig(BaseModel):
    interface: InterfaceRef
    features: List[FeatureModel] = Field(..., min_length=1)


# ================================================================
# CHANGE  (the payload the endpoint validates against)
# ================================================================

_NATIVE_PREFIXES = ("vlan_", "pvlan_global", "pvlan_secondary", "svi_")


class FeatureChange(BaseModel):
    """
    Train-scoped batch of feature requests.

    `interfaces` carries interface-scoped bundles (each with a parent/name).
    `native_features` carries native-scoped families:
      vlan_*, pvlan_global, pvlan_secondary, svi_private_vlan_mapping.

    Cross-scope mixing is rejected here — plain Pydantic, no engine imports.
    Train availability is validated by the engine (phase 3), not this model.
    """
    train: Train
    interfaces: List[InterfaceConfig] = Field(default_factory=list)
    native_features: List[FeatureModel] = Field(default_factory=list)

    @model_validator(mode="after")
    def _not_empty(self):
        if not self.interfaces and not self.native_features:
            raise ValueError(
                "FeatureChange must contain at least one interface or native feature"
            )
        return self

    @model_validator(mode="after")
    def _no_native_in_interfaces(self):
        for i, bundle in enumerate(self.interfaces):
            for f in bundle.features:
                if f.feature.startswith(_NATIVE_PREFIXES):
                    raise ValueError(
                        f"interfaces[{i}]: native-scoped feature {f.feature!r} "
                        f"must be in native_features, not in interfaces[].features"
                    )
        return self

    @model_validator(mode="after")
    def _no_interface_in_native(self):
        for i, f in enumerate(self.native_features):
            if not f.feature.startswith(_NATIVE_PREFIXES):
                raise ValueError(
                    f"native_features[{i}]: interface-scoped feature {f.feature!r} "
                    f"must be in interfaces[].features, not in native_features"
                )
        return self


# ================================================================
# WIRE PAYLOAD  (details of ConfigureRequest for feature operations)
# ================================================================

class ConfigureFeaturesDetails(BaseModel):
    """
    `details` payload for ConfigureRequest when operation ∈ {feature_add, feature_remove}.

    Example:
        ConfigureRequest(
            profile=Credentials(...),
            operation="feature_add",
            devices=[...],
            details={
                "change": {
                    "train": "1715",
                    "interfaces": [
                        {
                            "interface": {"parent": "GigabitEthernet", "name": "1/0/1"},
                            "features": [
                                {"feature": "description", "value": "uplink to core"},
                                {"feature": "l2_switchport", "value": True},
                            ],
                        }
                    ],
                    "native_features": [
                        {"feature": "vlan_create", "vlan_id": 10},
                    ],
                }
            },
        )
    """
    change: FeatureChange


# ================================================================
# CONVENIENCE ALIASES  (used by tests and by the engine mapper)
# ================================================================

NATIVE_SCOPED_FEATURES = frozenset({
    "vlan_create", "vlan_delete", "vlan_name", "vlan_state", "vlan_remote_span",
    "vlan_uni", "pvlan_global", "pvlan_secondary", "svi_private_vlan_mapping",
})

def is_native_scoped(f: FeatureModel) -> bool:
    """True for families that emit under <native> without an interface scaffold."""
    return f.feature in NATIVE_SCOPED_FEATURES


# ================================================================
# SELFTEST  (python interface_features_schemas.py)
# ================================================================

if __name__ == "__main__":
    import json

    def _ok(label, value):
        try:
            FeatureChange.model_validate(value)
            print(f"  OK    {label}")
        except Exception as e:
            print(f"  FAIL  {label}: {e}")
            raise

    def _bad(label, value):
        try:
            FeatureChange.model_validate(value)
        except Exception:
            print(f"  OK    {label} (correctly rejected)")
            return
        raise AssertionError(f"{label}: should have been rejected but was accepted")

    # ---- positive ----
    _ok("interface-only", {
        "train": "1715",
        "interfaces": [{
            "interface": {"parent": "GigabitEthernet", "name": "1/0/1"},
            "features": [
                {"feature": "description", "value": "uplink"},
                {"feature": "mtu", "value": 9000},
                {"feature": "l2_switchport", "value": True},
            ],
        }],
    })
    _ok("native-only", {
        "train": "1715",
        "native_features": [
            {"feature": "vlan_create", "vlan_id": 10},
            {"feature": "vlan_name", "vlan_id": 10, "name": "users"},
        ],
    })
    _ok("mixed allowed when scoped correctly", {
        "train": "1712",
        "interfaces": [{
            "interface": {"parent": "Port-channel", "name": "1"},
            "features": [{"feature": "shutdown", "value": False}],
        }],
        "native_features": [{"feature": "pvlan_global",
                             "primary_vlan": 100, "secondary_vlans": "101,102"}],
    })

    # ---- negative ----
    _bad("empty", {"train": "1715"})
    _bad("native in interfaces[]", {
        "train": "1715",
        "interfaces": [{
            "interface": {"parent": "GigabitEthernet", "name": "1/0/1"},
            "features": [{"feature": "vlan_create", "vlan_id": 10}],
        }],
    })
    _bad("interface in native_features[]", {
        "train": "1715",
        "native_features": [{"feature": "mtu", "value": 9000}],
    })
    _bad("bad enum value", {
        "train": "1715",
        "native_features": [{"feature": "vlan_state", "vlan_id": 10, "state": "bogus"}],
    })
    _bad("ipv4 missing mask", {
        "train": "1715",
        "interfaces": [{
            "interface": {"parent": "GigabitEthernet", "name": "1/0/1"},
            "features": [{"feature": "ipv4_address", "ip": "10.0.0.1"}],
        }],
    })
    _bad("load_interval not multiple of 30", {
        "train": "1715",
        "interfaces": [{
            "interface": {"parent": "GigabitEthernet", "name": "1/0/1"},
            "features": [{"feature": "load_interval", "value": 45}],
        }],
    })
    _bad("l2pt_threshold both protos", {
        "train": "1715",
        "interfaces": [{
            "interface": {"parent": "GigabitEthernet", "name": "1/0/1"},
            "features": [{"feature": "l2pt_threshold", "kind": "drop",
                          "proto": "cdp", "p2p_proto": "lacp", "pps": 100}],
        }],
    })

    print("\nselftest: all checks passed")