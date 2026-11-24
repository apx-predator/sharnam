# interface_features_engine.py
# Phase 3 — train gate + renderer.
#
# Two public functions:
#   validate_change(change)       -> None | raises ValueError
#   render_calls(train, calls)    -> list[str]  (NETCONF <config> payloads)
#
# Pure Python. No Nornir, no ncclient, no HTTP, no DB.
# The only import that touches the outside world is importlib for the train module.
#
# What this phase owns that phases 1/2 do not:
#   * train availability  — rejects families the target train does not ship
#   * strict applicability — via build_config(strict=True) inside the train module
#   * the concrete XML      — the only layer that produces <config> strings

from __future__ import annotations

import importlib
from typing import Iterable, List, Optional

from interface_features_mapper import RenderCall
from interface_features_schemas import FeatureChange


# ================================================================
# TRAIN MODULE LOADER
# ================================================================

_TRAIN_MODULE_CACHE: dict[str, object] = {}


def _module_for(train: str):
    """Import (and cache) interface_attrs_<train>."""
    if train not in _TRAIN_MODULE_CACHE:
        _TRAIN_MODULE_CACHE[train] = importlib.import_module(f"interfaces_{train}_xml")
    return _TRAIN_MODULE_CACHE[train]


# ================================================================
# VALIDATION
# ================================================================

#def validate_change(change: FeatureChange) -> None:
    """Reject the change before rendering if any family is not on the train.

    Rules:
      * base label must exist in TEMPLATES of the target train
      * base label must not be a NOT_PRESENT family on that train
      * family must resolve (i.e. have a non-None template)

    Called from the Nornir task, not the endpoint, so a misconfigured train
    fails on the device that is actually wrong, not on every device in the fleet.
    """
  #  module = _module_for(change.train.value)
 #  supported = set(module.supported_on(change.train.value))
def validate_change(change: FeatureChange, train: Optional[str] = None) -> None:
    train = train or change.train.value
    module = _module_for(train)
    supported = set(module.supported_on(train))
    try:
        not_present = dict(module.not_present())
    except (TypeError, ValueError):
        # not_present() may yield tuples or plain strings depending on train;
        # normalise to a dict of {family: reason}
        not_present = {}
        try:
            for entry in module.not_present():
                if isinstance(entry, tuple) and len(entry) == 2:
                    name, reason = entry
                else:
                    name, reason = entry, "not present"
                not_present[name] = reason
        except TypeError:
            pass

    # Import here, not at module top, to avoid a cycle in the selftest
    from interface_features_mapper import to_render_calls

    for call in to_render_calls(change):
        _validate_one(call.base, supported, not_present, change.train.value)


def _validate_one(base: str, supported: set, not_present: dict, train: str) -> None:
    if base in supported:
        return
    if base in not_present:
        raise ValueError(
            f"{base!r} is flagged NOT PRESENT on train {train}: {not_present[base]}"
        )
    raise ValueError(f"{base!r} is not in the {train} catalogue")


# ================================================================
# RENDERER
# ================================================================

def render_calls(train: str, calls: Iterable[RenderCall]) -> List[str]:
    """Turn each RenderCall into a full NETCONF <config> payload.

    Uses the train module's build_config():
      * native-scoped families (parent is None)  -> wrap_native()
      * interface-scoped families                -> wrap_interface()
      * strict=True                              -> applies_to() gate per family

    Raises KeyError (from resolve) or ValueError (from strict) on any problem.
    """
    module = _module_for(train)
    out: List[str] = []
    for call in calls:
        out.append(_render_one(module, train, call))
    return out


def _render_one(module, train: str, call: RenderCall) -> str:
    try:
        return module.build_config(
            call.base,
            parent=call.parent,
            name=call.name,
            train=train,
            strict=True,
            **call.kwargs,
        )
    except KeyError as e:
        raise KeyError(
            f"{call.base} on {call.parent or 'native'}{call.name or ''} "
            f"(train {train}): {e}"
        ) from e
    except ValueError as e:
        raise ValueError(
            f"{call.base} on {call.parent or 'native'}{call.name or ''} "
            f"(train {train}): {e}"
        ) from e


# ================================================================
# CONVENIENCE
# ================================================================

def render_change(change: FeatureChange) -> List[str]:
    """Validate + render in one call. This is what the task uses."""
    validate_change(change)
    from interface_features_mapper import to_render_calls
    return render_calls(change.train.value, to_render_calls(change))


def labelled_render_change(change: FeatureChange) -> List[tuple[RenderCall, str]]:
    """Same as render_change but pairs each payload with its originating call.
    The task uses this to log 'family on interface OK/FAIL' per line."""
    validate_change(change)
    from interface_features_mapper import to_render_calls
    calls = list(to_render_calls(change))
    configs = render_calls(change.train.value, calls)
    return list(zip(calls, configs))


# ================================================================
# SELFTEST  (python interface_features_engine.py)
# ================================================================
if __name__ == "__main__":
    import xml.etree.ElementTree as ET

    from interface_features_schemas import FeatureChange

    def _ok(label, change):
        try:
            configs = render_change(change)
            for cfg in configs:
                ET.fromstring(cfg)                      # must be well-formed XML
            print(f"  OK    {label}  ({len(configs)} payload(s))")
        except Exception as e:
            print(f"  FAIL  {label}: {type(e).__name__}: {e}")
            raise

    def _bad(label, change, *expected_substrings):
        try:
            render_change(change)
        except (ValueError, KeyError) as e:
            msg = str(e)
            for sub in expected_substrings:
                assert sub in msg, f"{label}: expected {sub!r} in error, got {msg!r}"
            print(f"  OK    {label}  -> rejected: {msg[:70]}")
            return
        raise AssertionError(f"{label}: should have been rejected")

    def _iface(parent, name, *features):
        return {"interface": {"parent": parent, "name": name}, "features": list(features)}

    # ---------- positive ----------
    _ok("description on 1715", FeatureChange.model_validate({
        "train": "1715",
        "interfaces": [_iface("GigabitEthernet", "1/0/1",
                              {"feature": "description", "value": "uplink"})],
    }))

    _ok("mtu + load_interval on 1712", FeatureChange.model_validate({
        "train": "1712",
        "interfaces": [_iface("GigabitEthernet", "1/0/1",
                              {"feature": "mtu", "value": 9000},
                              {"feature": "load_interval", "value": 300})],
    }))

    _ok("l2_switchport True on 179", FeatureChange.model_validate({
        "train": "179",
        "interfaces": [_iface("GigabitEthernet", "1/0/1",
                              {"feature": "l2_switchport", "value": True})],
    }))

    _ok("vlan_create native on 1715", FeatureChange.model_validate({
        "train": "1715",
        "native_features": [{"feature": "vlan_create", "vlan_id": 10}],
    }))

    _ok("ipv6 eui64 on 1712", FeatureChange.model_validate({
        "train": "1712",
        "interfaces": [_iface("GigabitEthernet", "1/0/1",
                              {"feature": "ipv6_address",
                               "prefix": "2001:db8::/64", "kind": "eui64"})],
    }))

    # ---------- negative: train gate ----------
    # ipv6_nd_dad_attempts is NOT PRESENT on 1612 and 1712 (17.12 has no dad node)
    _bad("ipv6_nd_dad_attempts on 1712",
         FeatureChange.model_validate({
             "train": "1712",
             "interfaces": [_iface("GigabitEthernet", "1/0/1",
                                   {"feature": "ipv6_nd_dad_attempts", "attempts": 3})],
         }),
         "IPV6_ND_DAD_ATTEMPTS")

    _bad("ipv6_nd_dad_attempts on 1612",
         FeatureChange.model_validate({
             "train": "1612",
             "interfaces": [_iface("GigabitEthernet", "1/0/1",
                                   {"feature": "ipv6_nd_dad_attempts", "attempts": 3})],
         }),
         "IPV6_ND_DAD_ATTEMPTS")

    # srlq is NOT PRESENT on 1612
    _bad("srlg on 1612",
         FeatureChange.model_validate({
             "train": "1612",
             "interfaces": [_iface("GigabitEthernet", "1/0/1",
                                   {"feature": "srlg", "values": [100, 200]})],
         }),
         "SRLG")

    # ---------- negative: strict applicability ----------
    # l2_vepa is switchport-scoped; Loopback is not in SWITCHPORT_TYPES
    _bad("l2_vepa on Loopback",
         FeatureChange.model_validate({
             "train": "1715",
             "interfaces": [_iface("Loopback", "0",
                                   {"feature": "l2_vepa", "value": True})],
         }),
         "L2_VEPA", "Loopback")

    # po_min_links only on Port-channel
    _bad("po_min_links on GigabitEthernet",
         FeatureChange.model_validate({
             "train": "1715",
             "interfaces": [_iface("GigabitEthernet", "1/0/1",
                                   {"feature": "po_min_links", "value": 3})],
         }),
         "PO_MIN_LINKS", "GigabitEthernet")

    print("\nengine selftest: all checks passed")