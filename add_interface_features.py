# add_interface_features.py
# Nornir task + FastAPI endpoint for interface-feature configuration.
# Mirrors add_port_channels.py's structure:
#   - same auth/connection model (scrapli_netconf, port 830)
#   - same _try_edit() candidate/running handling
#   - same _has_candidate / _confirmed_commit / _reset_connection helpers
#   - same job status (set_job_status)
#   - same fallback pattern (_try_with_fallback -> _render_with_fallback)
#
# Difference from add_port_channels.py:
#   - the task is generic across every interface feature family (not just Po)
#   - the renderer is phase 3 (interface_features_engine.render_change)
#   - the mapper is phase 2 (interface_features_mapper.to_render_calls)
#   - the wire is phase 1 (interface_features_schemas.ConfigureFeaturesDetails)

import logging
import time
import re

from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional

from nornir import InitNornir
from nornir.core.filter import F
from nornir_scrapli.tasks import netconf_edit_config, netconf_get_config

# ---- shared with add_port_channels.py ----
from add_port_channels import (
    ConfigureRequest,
    Credentials,
    Device,
    MemberInt,
    Vlan,
    set_job_status,
    normalize_platform,
    _has_candidate,
    _confirmed_commit,
    _reset_connection,
    _try_edit,
    _version_family,
    _attempt_order,
    log,
    NATIVE_NS,
)

# ---- phase 1/2/3 stack ----
from interface_features_schemas import (
    ConfigureFeaturesDetails,
    FeatureChange,
    InterfaceConfig,
    NATIVE_SCOPED_FEATURES,
    is_native_scoped,
)
from interface_features_mapper import (
    RenderCall,
    to_render_calls,
)
from interface_features_engine import (
    validate_change,
    render_calls,
)

app = FastAPI()


# ================================================================
# TRAIN MAPPING  (feature trains vs port-channel trains)
# ================================================================
# The feature layer has: 1612, 173, 179, 1712, 1715
# The port-channel layer has: 1612, 173, 176, 179, 1712, 1715
# Feature trains skip "176" (there is no interfaces_176_xml.py).

_FEATURE_TRAINS = ("1612", "173", "179", "1712", "1715")


def _feature_train_for(version: Optional[str]) -> str:
    """Map an IOS XE version string to a feature-train key."""
    fam = _version_family(version)
    if fam in _FEATURE_TRAINS:
        return fam
    # 176 has no feature module; nearest neighbour is 179
    return {"176": "179", "unknown": "1715"}.get(fam, "1715")


def _feature_train_order(version: Optional[str]) -> List[str]:
    """Ordered trains to try for this version (primary first, then by proximity)."""
    primary = _feature_train_for(version)
    ordered = [primary]
    for t in _attempt_order(version):
        if t in _FEATURE_TRAINS and t not in ordered:
            ordered.append(t)
    for t in _FEATURE_TRAINS:
        if t not in ordered:
            ordered.append(t)
    return ordered


# ================================================================
# NETCONF SUBTREE FILTER  (per payload)
# ================================================================
# The filter just needs to be permissive enough to let the server see the
# full subtree. We reuse the same filter shape add_port_channels.py uses,
# but build it from the RenderCall so we don't guess interface types.

def _filter_for_call(call: RenderCall) -> str:
    if call.parent is None:
        # native-scoped: filter on <native> at top level
        return f'<native xmlns="{NATIVE_NS}"/>'
    return (
        f'<native xmlns="{NATIVE_NS}">'
        f'<interface><{call.parent}>'
        f'<name>{call.name}</name>'
        f'</{call.parent}></interface>'
        f'</native>'
    )


# ================================================================
# RENDER WITH FALLBACK
# ================================================================

def _render_with_fallback(change: FeatureChange, version: Optional[str]):
    """Render the whole change with the first train that succeeds.
    Returns ([(RenderCall, config), ...], train_used, errors)."""
    errors = []
    for train in _feature_train_order(version):
        try:
            validate_change(change, train=train)   # ← pass the loop's train
        except (ValueError, KeyError) as e:
            errors.append(f"train {train}: {e}")
            log.info("render fallback: train %s cannot validate: %s", train, e)
            continue

        try:
            calls = list(to_render_calls(change))
            configs = render_calls(train, calls)
            return list(zip(calls, configs)), train, errors
        except (ValueError, KeyError) as e:
            errors.append(f"train {train}: {e}")
            log.info("render fallback: train %s cannot render: %s", train, e)
        except Exception as e:
            errors.append(f"train {train}: {type(e).__name__}: {e}")
            log.warning("render fallback: train %s failed: %s", train, e)

    return [], None, errors

# ================================================================
# PUSH EACH PAYLOAD
# ================================================================

def _push_rendered(task, conn, rendered, has_candidate):
    """Push every (RenderCall, config) payload; raise on first failure."""
    for call, config in rendered:
        label = f"{call.base} on {call.parent or 'native'}{call.name or ''}"
        filter_xml = _filter_for_call(call)
        ok, err = _try_edit(task, conn, config, filter_xml, label, has_candidate)
        if not ok:
            raise RuntimeError(f"[{task.host.name}] {label} failed: {err}")
        log.info("[%s] %s OK", task.host.name, label)


# ================================================================
# NORNIR TASK
# ================================================================

def iosxe_interface_features_task(task):
    conn = task.host.get_connection("scrapli_netconf", task.nornir.config)
    has_candidate = _has_candidate(conn)
    log.info("[%s] candidate: %s", task.host.name,
             "YES" if has_candidate else "NO")

    change: FeatureChange = task.host["change"]
    version = task.host.get("version", "")

    # 1. fail-fast train gate — reject before any device contact
    #try:
     #   validate_change(change)
    #except (ValueError, KeyError) as e:
     #   raise RuntimeError(f"[{task.host.name}] change validation failed: {e}")

    # 2. render (with per-train fallback)
    rendered, train_used, errors = _render_with_fallback(change, version)
    if not rendered:
        raise RuntimeError(
            f"[{task.host.name}] could not render any feature payloads:\n"
            + "\n".join(errors)
        )
    log.info("[%s] rendered %d payload(s) on train %s",
             task.host.name, len(rendered), train_used)

    # 3. push each payload
    _push_rendered(task, conn, rendered, has_candidate)

    log.info("[%s] feature task done (%d payloads)", task.host.name, len(rendered))


# ================================================================
# HOST BUILDER
# ================================================================

def _build_hosts_data(payload: ConfigureRequest) -> list:
    """Build the Nornir inventory from the request, attaching the FeatureChange."""
    details = ConfigureFeaturesDetails.model_validate(payload.details)
    change = details.change

    # one entry per device; the change is shared
    hosts = []
    for dev in payload.devices:
        hosts.append({
            "name": str(dev.id),
            "hostname": dev.management_ip,
            "platform": normalize_platform(dev.platform),
            "username": payload.profile.username,
            "password": payload.profile.password_cipher,
            "port": 830,
            "connection_options": {
                "scrapli_netconf": {
                    "extras": {
                        "auth_strict_key": False,
                        "timeout_socket": 10.0,
                        "timeout_transport": 15.0,
                        "timeout_banner": 30,
                    }
                }
            },
            "device_id": dev.id,
            "version": dev.version or "",
            "family": dev.family or "",
            "interfaces": [i.model_dump() for i in (dev.interfaces or [])],
            "change": change,
        })
    return hosts


# ================================================================
# RUNNER
# ================================================================

def run_feature_job(payload: ConfigureRequest):
    set_job_status(payload.job_id, "running")
    log.info("job %s: feature start, %d devices", payload.job_id,
             len(payload.devices))

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
        result = filtered.run(task=iosxe_interface_features_task)

        failed = [
            f"{host}: {type(multi.exception).__name__}: {multi.exception}"
            for host, multi in result.items() if multi.failed
        ]
        if failed:
            raise RuntimeError("tasks failed:\n" + "\n".join(failed))

        set_job_status(payload.job_id, "done")
        log.info("job %s: feature done", payload.job_id)

    except Exception as e:
        log.exception("job %s: feature failed", payload.job_id)
        set_job_status(payload.job_id, "failed", str(e))


# ================================================================
# FASTAPI ENDPOINT
# ================================================================

class FeatureResponse(BaseModel):
    job_id: Optional[str] = None
    status: str
    message: Optional[str] = None


@app.post("/features/configure", response_model=FeatureResponse)
def configure_features(req: ConfigureRequest):
    """Configure interface features on one or more devices.

    Request `operation` must be "feature_add" or "feature_remove".
    Request `details` must be {"change": {"train": "...", "interfaces": [...],
    "native_features": [...]}} — see interface_features_schemas for the
    full schema.
    """
    if req.operation not in ("feature_add", "feature_remove"):
        return FeatureResponse(
            job_id=req.job_id,
            status="error",
            message=f"unsupported operation {req.operation!r}; "
                    f"expected feature_add or feature_remove",
        )

    # validate the details payload up front so a bad shape returns 400 fast
    try:
        ConfigureFeaturesDetails.model_validate(req.details)
    except Exception as e:
        return FeatureResponse(
            job_id=req.job_id,
            status="error",
            message=f"invalid details: {e}",
        )

    if req.async_:
        # fire-and-forget; job status is tracked in DB
        from threading import Thread
        Thread(target=run_feature_job, args=(req,), daemon=True).start()
        return FeatureResponse(
            job_id=req.job_id,
            status="accepted",
            message="job queued (async)",
        )

    run_feature_job(req)
    return FeatureResponse(job_id=req.job_id, status="done")