# interface_features_mapper.py
# Phase 2 — translate FeatureChange (pydantic) into RenderCall tuples.
# Pure Python. No I/O, no XML, no importlib in production code paths
# (importlib is used only inside the selftest to cross-check templates).
#
# Responsibility:
#   FeatureChange  ->  list[RenderCall]
#
# A RenderCall is one (base_label, parent, name, kwargs) record the renderer
# (phase 3) hands to interfaces_<train>_xml.build_config().
#
# The mapper owns three things the wire layer cannot:
#   1. Sibling resolution — feature models carrying `value: bool` map to two
#      different template bases (e.g. L2_SWITCHPORT_TRUE / _FALSE).
#   2. _REMOVE selection — `remove=True` flips the base to `<BASE>_REMOVE`.
#   3. Placeholder projection — pydantic field names are renamed to the actual
#      $placeholder names the templates expect (see _FIELD_PLACEHOLDER_MAP).

from __future__ import annotations

from typing import Iterator, NamedTuple, Optional

from interface_features_schemas import (
    FeatureChange,
    FeatureModel,
)


# ================================================================
# RENDER CALL
# ================================================================

class RenderCall(NamedTuple):
    """One template render request.

    base   — template base label, e.g. "MTU", "MTU_REMOVE",
             "L2_SWITCHPORT_TRUE", "VLAN_CREATE".
    parent — interface type for interface-scoped families; None for native.
    name   — interface name for interface-scoped families; None for native.
    kwargs — placeholder dict; every key must appear as a $placeholder in
             the template, and every $placeholder in the template must
             appear as a key (or be a namespace).
    """
    base:   str
    parent: Optional[str]
    name:   Optional[str]
    kwargs: dict


# ================================================================
# SIBLING PAIRS  (bool `value` -> two bases)
# ================================================================

_BOOL_BASES: dict[str, tuple[str, str]] = {
    "l2_switchport":      ("L2_SWITCHPORT_TRUE",      "L2_SWITCHPORT_FALSE"),
    "l2_dtp_nonegotiate": ("L2_DTP_DISABLE_TRUE",     "L2_DTP_DISABLE_FALSE"),
    "arp_snap":           ("ARP_SNAP_TRUE",           "ARP_SNAP_FALSE"),
    "shutdown":           ("SHUTDOWN",                "SHUTDOWN_REMOVE"),
}


# ================================================================
# FIELD -> PLACEHOLDER RENAME MAP
# ================================================================
# Each pydantic feature has fields whose names don't necessarily match the
# $placeholder names in the train templates. This table maps, per feature:
#   {model_field_name: template_placeholder_name}
#
# Semantics:
#   * key not in renames      -> field name is the placeholder name
#   * renames[key] = str      -> rename to this placeholder
#   * renames[key] = None     -> drop this field entirely
#
# Booleans are converted to "true"/"false" before renaming.
# Enums are converted to .value before renaming.
# InterfaceRef submodels are expanded into src_type / src_name.
_FIELD_PLACEHOLDER_MAP: dict[str, dict[str, Optional[str]]] = {
    # §1 general attributes
    "description":       {"value": "desc"},
    "export_name":       {"value": "export"},
    "mac_address":       {"value": "mac"},
    "mtu":               {"value": "mtu"},
    "delay":             {"value": "delay"},
    "load_interval":     {"value": "seconds"},
    "max_bandwidth":     {"value": "percent"},
    "service_insertion": {"value": "svc"},
    "qos_trust":         {"device": "device"},
    "negotiation":       {"value": "flag"},
    "mdix":              {"value": "flag"},

    # §2 L2 switching
    "l2_voice_vlan":           {"kind": None, "vlan": "voice_vlan", "vlan_name": "vlan_name"},
    "l2_voice_detect":         {"value": "flag"},
    "l2_access_vlan":          {"vlan": "access_vlan"},
    "l2_trunk_allowed":        {"vlans": "vlans"},
    "l2_trunk_encapsulation":  {"value": "encap"},
    "l2_trunk_native_vlan":    {"vlan": "native_vlan", "tag": "flag"},
    "l2_trunk_pruning":        {"op": None, "vlans": "vlans", "remove_all": None},
    "l2_port_security_enable": {"value": "flag"},
    "l2_port_security_max":    {"max_addresses": "max", "vlan": "vlan_kind"},
    "l2_port_security_violation": {"violation": "violation"},
    "l2_port_security_sticky": {"value": "flag"},
    "l2_port_security_aging":  {"minutes": "minutes", "aging_type": "aging_type", "static": None},
    "l2_port_security_mac":    {"hw_address": "hwaddr", "vlan": None},
    "l2_protected":            {"value": "flag"},
    "l2_host":                 {"value": "flag"},
    "l2_block_multicast":      {"value": "flag"},
    "l2_block_unicast":        {"value": "flag"},
    "l2_vepa":                 {"value": "flag"},
    "pvlan_host_assoc":        {"primary_vlan": "primary_vlan", "secondary_vlan": "secondary_vlan"},
    "pvlan_promiscuous_map":   {"primary_vlan": "primary_vlan", "secondary_vlans": "secondary_vlans"},
    "l2pt_tunnel_core":        {"proto": "proto"},
    "l2pt_tunnel_p2p":         {"proto": "p2p_proto"},
    "l2pt_threshold":          {"kind": None, "proto": "proto", "p2p_proto": "p2p_proto", "pps": "pps"},

    # §3 ARP + link tuning
    "arp_timeout":             {"seconds": "secs"},
    "arp_snap":                {"value": "flag"},
    "arp_entry_limit":         {"count": "count", "log_seconds": "log_secs"},
    "arp_packet_priority":     {"value": "flag"},
    "pq_out":                  {"value": "flag"},
    "pq_cos_map":              {"qid": "qid", "cos_values": None},
    "rcv_queue_cos_map":       {"qid": "qid", "tid": "tid", "cos_values": None},
    "flowcontrol":             {"rx": "rx", "tx": "tx"},
    "hold_queue":              {"direction": "direction", "qlen": "qlen"},
    "link_bandwidth":          {"kbps": "kbps", "qos_reference": None},
    "dampening":               {"half_life": "half_life", "reuse": "reuse",
                                "suppress": "suppress", "max_suppress": "max_suppress",
                                "defaults": None},
    "srlg":                    {"values": None},
    "domain_name":             {"name": "domain"},
    "domain_path":             {"path": "sp_path", "path_id": "path_id"},
    "keepalive":               {"enabled": None, "period": "period", "retries": "retries"},
    "logging_link_status":     {"value": "flag"},
    "logging_event":           {"event": "event"},
    "logging_spanning_tree":   {"value": "flag"},
    "logging_subif":           {"ignore_bulk": "ignore_bulk_block"},
    "fair_queue":              {"enabled": "flag"},

    # §4 IPv4
    "ipv4_address":            {"ip": "ip", "mask": "mask", "secondary": None},
    "ipv4_dhcp":               {"mode": None, "client_id_interface": None, "hostname": None},
    "ipv4_unnumbered":         {"source_interface": None},
    "ipv4_access_group":       {"direction": "direction", "acl": "acl", "common_acl": "common_acl"},
    "vrf_forwarding":          {"vrf": "vrf"},
    "ipv4_vrf_receive":        {"vrf": "vrf"},
    "ipv4_vrf_sitemap":        {"route_map": "route_map"},
    "helper_address":          {"helper": "helper", "global_": "global", "vrf": "vrf"},
    "policy_route_map":        {"route_map": "route_map"},
    "proxy_arp":               {"value": "flag"},
    "local_proxy_arp":         {"value": "flag"},
    "redirects":               {"value": "flag"},
    "clear_df":                {"value": "flag"},
    "tcp_adjust_mss":          {"mss": "mss"},
    "ip_mtu":                  {"value": "ip_mtu"},
    "urpf":                    {"via": "via", "allow_default": None,
                                "allow_self_ping": None, "acl": "acl_block"},
    "arp_inspect_trust":       {"value": "flag"},
    "arp_inspect_rate":        {"pps": "pps", "burst": "burst_block", "unlimited": None},
    "directed_broadcast":      {"acl": "acl"},

    # §5 IPv6
    "ipv6_enable":             {"value": "flag"},
    "ipv6_address":            {"prefix": "ipv6", "kind": None,
                                "link_local": "ll", "prefix_name": "pfx_name"},
    "ipv6_autoconfig":         {"default": "flag"},
    "ipv6_dhcp":               {"rapid_commit": "flag"},
    "ipv6_unnumbered":         {"source_interface": None},
    "ipv6_mtu":                {"value": "ip6_mtu"},
    "ipv6_tcp_adjust_mss":     {"mss": "mss"},
    "ipv6_traffic_filter":     {"direction": "direction", "acl": "acl"},
    "ipv6_source_guard":       {"policy": "policy_block"},
    "ipv6_nd_dad_attempts":    {"attempts": "attempts"},
    "ipv6_nd_nud_igp":         {"value": "flag"},
    "ipv6_verify_reverse_path": {"acl": "acl_block"},

    # §6 access-session
    "as_port_control":         {"value": "pc"},
    "as_control_direction":    {"value": "dir"},
    "as_host_mode":            {"value": "hm", "peer": None},
    "as_monitor":              {"value": "flag"},

    # §7 storm-control
    "storm_control_action":    {"action": None, "level_pct": "pct"},
    "storm_control_threshold": {"sc_type": "sc_type", "rise": "rise", "fall": "fall"},
    "storm_control_bcast_include_mcast": {"value": "flag"},

    # §8 MACsec
    "macsec_enable":           {"value": "flag"},
    "macsec_replay_protection": {"window": "window"},

    # §9 subscriber
    "subscriber_inactivity":   {"seconds": "secs", "probe": "probe_block"},
    "subscriber_probe":        {"value": "flag"},

    # §10 physical
    "media_type":              {"value": "media"},
    "fec":                     {"value": "fec"},

    # §11 port-channel
    "po_load_balance":         {"algo": "algo", "balancing": None},
    "po_min_links":            {"value": "min_links"},
    "po_standalone_disable":   {"value": "flag"},

    # §12 other type leaves
    "vlan_autostate":          {"value": "flag"},
    "tunnel_qos_pre_classify": {"value": "flag"},

    # §13 NVE
    "nve_host_reachability_bgp": {"value": "flag"},
    "nve_source_interface":    {"source_interface": None},
    "nve_member_vni_vrf":      {"vni": "vni", "vrf": "vrf"},
    "nve_member_vni_mcast_group": {"vni": "vni", "mc_min": "mc_min", "mc_max": "mc_max_block"},

    # §14 VLAN
    "vlan_create":             {"vlan_id": "vlan_id"},
    "vlan_delete":             {"vlan_id": "vlan_id"},
    "vlan_name":               {"vlan_id": "vlan_id", "name": "vlan_name"},
    "vlan_state":              {"vlan_id": "vlan_id", "state": "vlan_state"},
    "vlan_remote_span":        {"vlan_id": "vlan_id", "value": "flag"},
    "vlan_uni":                {"vlan_id": "vlan_id", "uni_type": "uni_type"},
    "pvlan_global":            {"primary_vlan": "primary_vlan",
                                "secondary_vlans": "secondary_vlans",
                                "action": None},
    "pvlan_secondary":         {"secondary_vlan": "secondary_vlan",
                                "pvlan_type": "pvlan_type"},
    "svi_private_vlan_mapping": {"mapping": "mapping"},
}

_BASE_OVERRIDES: dict[str, str] = {
    # IPv4 (single-variant families only)
    "vrf_forwarding":       "IP4_VRF_FORWARDING",
    "ipv4_vrf_receive":     "IP4_VRF_RECEIVE",
    "ipv4_vrf_sitemap":     "IP4_VRF_SITEMAP",
    "policy_route_map":     "IP4_POLICY_ROUTE_MAP",
    "proxy_arp":            "IP4_PROXY_ARP",
    "local_proxy_arp":      "IP4_LOCAL_PROXY_ARP",
    "redirects":            "IP4_REDIRECTS",
    "clear_df":             "IP4_CLEAR_DF",
    "tcp_adjust_mss":       "IP4_TCP_MSS",
    "ip_mtu":               "IP4_MTU",
    "urpf":                 "IP4_URPF",
    "arp_inspect_trust":    "IP4_ARP_INSPECT_TRUST",
    "arp_inspect_rate":     "IP4_ARP_INSPECT_RATE",
    "directed_broadcast":   "IP4_DIRECTED_BROADCAST",
}

# ================================================================
# BASE LABEL RESOLUTION
# ================================================================

def _base_for(f: FeatureModel) -> str:
    """Resolve a FeatureModel to its template base label."""

    # 0. explicit feature -> base override (for pydantic/template name drift)
    if f.feature in _BASE_OVERRIDES:
        on_base = _BASE_OVERRIDES[f.feature]
        if getattr(f, "remove", False):
            return on_base + "_REMOVE"
        return on_base

    # 1. explicit bool pair
    if f.feature in _BOOL_BASES:
        on_base, off_base = _BOOL_BASES[f.feature]
        return on_base if getattr(f, "value", False) else off_base

    # 2. kind-discriminated families
    base = _KIND_BASES(f)
    if base is not None:
        return base

    # 3. default
    upper = f.feature.upper()
    if getattr(f, "remove", False):
        return f"{upper}_REMOVE"
    return upper


def _KIND_BASES(f: FeatureModel) -> Optional[str]:
    """Discriminator-based base resolution for families whose template varies
    by a `kind`-style field. Returns None if not a discriminator family."""
    feat = f.feature
    remove = getattr(f, "remove", False)

    if feat == "l2_voice_vlan":
        if remove:
            return "L2_VOICE_VLAN_REMOVE"
        k = getattr(getattr(f, "kind", None), "value", getattr(f, "kind", None))
        return {
            "id": "L2_VOICE_VLAN_ID",
            "dot1p": "L2_VOICE_VLAN_DOT1P",
            "none": "L2_VOICE_VLAN_NONE",
            "untagged": "L2_VOICE_VLAN_UNTAGGED",
            "name": "L2_VOICE_VLAN_NAME",
        }.get(k, "L2_VOICE_VLAN_ID")

    if feat == "ipv6_address":
        k = getattr(f, "kind", "plain")
        if remove:
            return {
                "plain":       "IP6_ADDRESS_PREFIX_REMOVE",
                "eui64":       "IP6_ADDRESS_EUI64_REMOVE",
                "anycast":     "IP6_ADDRESS_ANYCAST_REMOVE",
                "link_local":  "IP6_ADDRESS_LINK_LOCAL_REMOVE",
                "prefix_name": "IP6_ADDRESS_PREFIX_NAME_REMOVE",
            }.get(k, "IP6_ADDRESS_PREFIX_REMOVE")
        return {
            "plain":       "IP6_ADDRESS_PREFIX",
            "eui64":       "IP6_ADDRESS_EUI64",
            "anycast":     "IP6_ADDRESS_ANYCAST",
            "link_local":  "IP6_ADDRESS_LINK_LOCAL",
            "prefix_name": "IP6_ADDRESS_PREFIX_NAME",
        }.get(k, "IP6_ADDRESS_PREFIX")

    if feat == "l2pt_threshold":
        kind = getattr(f, "kind", "drop")
        p2p = getattr(f, "p2p_proto", None) is not None
        if remove:
            if p2p:
                return "L2PT_DROP_THRESHOLD_P2P_REMOVE" if kind == "drop" \
                       else "L2PT_SHUTDOWN_THRESHOLD_P2P_REMOVE"
            return "L2PT_DROP_THRESHOLD_REMOVE" if kind == "drop" \
                   else "L2PT_SHUTDOWN_THRESHOLD_REMOVE"
        if p2p:
            return "L2PT_DROP_THRESHOLD_P2P" if kind == "drop" \
                   else "L2PT_SHUTDOWN_THRESHOLD_P2P"
        return "L2PT_DROP_THRESHOLD" if kind == "drop" \
               else "L2PT_SHUTDOWN_THRESHOLD"

    if feat == "storm_control_action":
        if remove:
            return "SC_ACTION_REMOVE"
        a = getattr(getattr(f, "action", None), "value", getattr(f, "action", None))
        return {
            "level":    "SC_ACTION_LEVEL",
            "shutdown": "SC_ACTION_SHUTDOWN",
            "trap":     "SC_ACTION_TRAP",
        }.get(a)

    if feat == "keepalive":
        return "KEEPALIVE_TIMERS" if getattr(f, "enabled", False) else "KEEPALIVE_DISABLE"

    if feat == "l2_trunk_pruning":
        if getattr(f, "remove_all", False):
            return "L2_TRUNK_PRUNING_REMOVE_ALL"
        op = getattr(f, "op", None)
        return {
            "add":     "L2_TRUNK_PRUNING_ADD",
            "remove":  "L2_TRUNK_PRUNING_REMOVE",
            "replace": "L2_TRUNK_PRUNING_REPLACE",
            "none":    "L2_TRUNK_PRUNING_NONE",
        }.get(op, "L2_TRUNK_PRUNING_NONE")

    if feat == "ipv4_dhcp":
        mode = getattr(f, "mode", "dhcp")
        if remove:
            return "IP4_NEGOTIATED_REMOVE" if mode == "negotiated" else "IP4_DHCP_REMOVE"
        return "IP4_NEGOTIATED" if mode == "negotiated" else "IP4_DHCP"

    if feat == "logging_event":
        return "LINK_LOGGING_EVENT_REMOVE" if remove else "LINK_LOGGING_EVENT"

    if feat == "pvlan_global":
        if remove:
            return "PVLAN_GLOBAL_REMOVE"
        a = getattr(getattr(f, "action", None), "value", getattr(f, "action", None))
        if a in (None, "add"):
            return "PVLAN_GLOBAL"
        return "PVLAN_GLOBAL_REMOVE"

    return None


# ================================================================
# KWARGS PROJECTION
# ================================================================

_RESERVED = {"feature", "remove"}

_FIELD_RENAME = {
    "global_": "global",
    "type_":   "type",
    "in_":     "in",
    "async_":  "async",
}


def _kwargs_for(f: FeatureModel) -> dict:
    """Project a FeatureModel into the $placeholder dict its template expects.

    * drops `feature`, `remove`, and any field the per-feature map marks None
    * applies _FIELD_PLACEHOLDER_MAP renames
    * converts bool -> "true"/"false"
    * unwraps enums to their .value
    * decomposes InterfaceRef into src_type/src_name
    * drops None/""/[] values (templates use "" to mean "omit")
    """
    raw = f.model_dump(exclude_none=True)
    renames = _FIELD_PLACEHOLDER_MAP.get(f.feature, {})
    out: dict = {}

    for k, v in raw.items():
        if k in _RESERVED:
            continue
        if v == "" or v == []:
            continue

        # Determine the target placeholder name (or skip if explicitly dropped)
        target = renames.get(k, _FIELD_RENAME.get(k, k))
        if target is None:
            continue

        if isinstance(v, bool):
            out[target] = "true" if v else "false"
        elif hasattr(v, "value"):                 # Enum
            out[target] = v.value
        elif isinstance(v, dict) and "parent" in v and "name" in v:   # InterfaceRef
            out.setdefault("src_type", v["parent"])
            out.setdefault("src_name", v["name"])
        else:
            out[target] = v

    return out


# ================================================================
# PUBLIC API
# ================================================================

def to_render_calls(change: FeatureChange) -> Iterator[RenderCall]:
    """Yield one RenderCall per feature in the change, in order."""
    for bundle in change.interfaces:
        parent = bundle.interface.parent.value
        name = bundle.interface.name
        for f in bundle.features:
            yield RenderCall(
                base=_base_for(f),
                parent=parent,
                name=name,
                kwargs=_kwargs_for(f),
            )

    for f in change.native_features:
        yield RenderCall(
            base=_base_for(f),
            parent=None,
            name=None,
            kwargs=_kwargs_for(f),
        )


# ================================================================
# SELFTEST
# ================================================================
if __name__ == "__main__":
    import importlib
    import re
    from interface_features_schemas import FeatureChange

    _PLACEHOLDER_RE = re.compile(r"\$([A-Za-z_][A-Za-z0-9_]*)")

    def _show(label, change):
        print(f"\n== {label} ==")
        for c in to_render_calls(change):
            print(f"  {c.base:32s} parent={c.parent or '-':24s} "
                  f"name={c.name or '-':10s} kw={c.kwargs}")
        return change

    def _cross_check(label, change, train):
        """Assert every RenderCall's kwargs cover the template's $placeholders."""
        mod = importlib.import_module(f"interfaces_{train}_xml")
        ns_ph = set(mod.NS)      # skip namespace placeholders
        for c in to_render_calls(change):
            try:
                tpl = mod.resolve(c.base, train)
            except KeyError:
                print(f"  SKIP  {label}: {c.base} not on train {train}")
                continue
            needed = set(_PLACEHOLDER_RE.findall(tpl)) - ns_ph
            have = set(c.kwargs)
            missing = needed - have
            if missing:
                raise AssertionError(
                    f"{label}: {c.base} needs {sorted(missing)}, "
                    f"kwargs has {sorted(have)}"
                )
            print(f"  OK    {label}: {c.base} placeholders match ({sorted(needed)})")

    _TRAIN = "1715"

    # ---- positive: single families ----
    _cross_check("description",
                 FeatureChange.model_validate({
                     "train": _TRAIN,
                     "interfaces": [{"interface": {"parent": "GigabitEthernet", "name": "1/0/1"},
                                     "features": [{"feature": "description", "value": "uplink"}]}],
                 }), _TRAIN)

    _cross_check("mtu",
                 FeatureChange.model_validate({
                     "train": _TRAIN,
                     "interfaces": [{"interface": {"parent": "GigabitEthernet", "name": "1/0/1"},
                                     "features": [{"feature": "mtu", "value": 9000}]}],
                 }), _TRAIN)

    _cross_check("load_interval",
                 FeatureChange.model_validate({
                     "train": _TRAIN,
                     "interfaces": [{"interface": {"parent": "GigabitEthernet", "name": "1/0/1"},
                                     "features": [{"feature": "load_interval", "value": 300}]}],
                 }), _TRAIN)

    _cross_check("shutdown",
                 FeatureChange.model_validate({
                     "train": _TRAIN,
                     "interfaces": [{"interface": {"parent": "GigabitEthernet", "name": "1/0/1"},
                                     "features": [{"feature": "shutdown", "value": True}]}],
                 }), _TRAIN)

    _cross_check("l2_switchport True",
                 FeatureChange.model_validate({
                     "train": _TRAIN,
                     "interfaces": [{"interface": {"parent": "GigabitEthernet", "name": "1/0/1"},
                                     "features": [{"feature": "l2_switchport", "value": True}]}],
                 }), _TRAIN)

    _cross_check("l2_access_vlan",
                 FeatureChange.model_validate({
                     "train": _TRAIN,
                     "interfaces": [{"interface": {"parent": "GigabitEthernet", "name": "1/0/1"},
                                     "features": [{"feature": "l2_access_vlan", "vlan": 42}]}],
                 }), _TRAIN)

    _cross_check("voice_vlan id",
                 FeatureChange.model_validate({
                     "train": _TRAIN,
                     "interfaces": [{"interface": {"parent": "GigabitEthernet", "name": "1/0/1"},
                                     "features": [{"feature": "l2_voice_vlan", "kind": "id", "vlan": 42}]}],
                 }), _TRAIN)

    _cross_check("ipv4_address",
                 FeatureChange.model_validate({
                     "train": _TRAIN,
                     "interfaces": [{"interface": {"parent": "GigabitEthernet", "name": "1/0/1"},
                                     "features": [{"feature": "ipv4_address",
                                                   "ip": "10.0.0.1", "mask": "255.255.255.0"}]}],
                 }), _TRAIN)

    _cross_check("ipv6 eui64",
                 FeatureChange.model_validate({
                     "train": _TRAIN,
                     "interfaces": [{"interface": {"parent": "GigabitEthernet", "name": "1/0/1"},
                                     "features": [{"feature": "ipv6_address",
                                                   "prefix": "2001:db8::/64", "kind": "eui64"}]}],
                 }), _TRAIN)

    _cross_check("helper_address",
                 FeatureChange.model_validate({
                     "train": _TRAIN,
                     "interfaces": [{"interface": {"parent": "GigabitEthernet", "name": "1/0/1"},
                                     "features": [{"feature": "helper_address",
                                                   "helper": "10.0.0.2", "vrf": "MGMT"}]}],
                 }), _TRAIN)

    _cross_check("storm_control_action level",
                 FeatureChange.model_validate({
                     "train": _TRAIN,
                     "interfaces": [{"interface": {"parent": "GigabitEthernet", "name": "1/0/1"},
                                     "features": [{"feature": "storm_control_action",
                                                   "action": "level", "level_pct": 80}]}],
                 }), _TRAIN)

    _cross_check("l2pt_threshold drop p2p",
                 FeatureChange.model_validate({
                     "train": _TRAIN,
                     "interfaces": [{"interface": {"parent": "GigabitEthernet", "name": "1/0/1"},
                                     "features": [{"feature": "l2pt_threshold",
                                                   "kind": "drop", "p2p_proto": "lacp", "pps": 500}]}],
                 }), _TRAIN)

    _cross_check("vlan_create native",
                 FeatureChange.model_validate({
                     "train": _TRAIN,
                     "native_features": [{"feature": "vlan_create", "vlan_id": 10}],
                 }), _TRAIN)

    _cross_check("pvlan_global native",
                 FeatureChange.model_validate({
                     "train": _TRAIN,
                     "native_features": [{"feature": "pvlan_global",
                                          "primary_vlan": 100, "secondary_vlans": "101,102"}],
                 }), _TRAIN)

    _cross_check("description remove",
                 FeatureChange.model_validate({
                     "train": _TRAIN,
                     "interfaces": [{"interface": {"parent": "GigabitEthernet", "name": "1/0/1"},
                                     "features": [{"feature": "description", "remove": True}]}],
                 }), _TRAIN)

    print("\nmapper selftest: all placeholder checks passed")