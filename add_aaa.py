
import logging
import time
import re
from threading import Thread
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import List, Optional
import mysql.connector
from nornir import InitNornir
from nornir.core.filter import F
from nornir_scrapli.tasks import netconf_edit_config, netconf_get_config

from aaa_schemas import render, ConfigureFeature, ConfigureRequest

log = logging.getLogger(__name__)

_FEATURE_TRAINS = ("1612", "173", "179", "1712", "1715")


def _version_family(version: Optional[str]) -> str:
    """
    Turn an IOS XE version string like '17.15.1' or '16.12.4' into its
    feature-train family: '1715', '1712', '1612', ...
    """
    if not version:
        return ""
    m = re.match(r"^(\d+)\.(\d+)", version)   # '17.15.1' -> ('17','15')
    if not m:
        return ""
    major, minor = m.group(1), m.group(2)
    if major == "17":
        return f"17{int(minor):02d}"          # 17.15 -> '1715', 17.3 -> '1703'
    if major == "16":
        return f"16{int(minor):02d}"          # 16.12 -> '1612'
    return ""


def _feature_train_for(version: Optional[str]) -> str:
    fam = _version_family(version)
    if fam in _FEATURE_TRAINS:
        return fam
    if fam in ("1713", "1714"):
        return "1715"
    if fam in ("1710", "1711"):
        return "1712"
    if fam in ("177", "178"):
        return "179"
    if fam in ("174", "175"):
        return "176"
    if fam in ("171", "172"):
        return "173"
    if fam == "1611":
        return "1612"
    raise ValueError(f"Unsupported version family: {version!r} -> {fam!r}")
    
def normalize_platform(raw: Optional[str]) -> str:
    if not raw:
        return "linux"
    r = raw.lower().replace("-", "_")
    if "ios_xe" in r or "iosxe" in r:
        return "cisco_iosxe"
    if "ios" in r:
        return "cisco_ios"
    if "nxos" in r or "nx_os" in r:
        return "cisco_nxos"
    if "junos" in r:
        return "juniper_junos"
    if "huawei" in r or "vrp" in r:
        return "huawei_vrp"
    return r
    
def _build_hosts_data(payload: ConfigureRequest) -> list:
    

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
            "change": payload.change,
        })
    return hosts
    
def db():
    return mysql.connector.connect(
        host="localhost", user="root", password="", database="sharnam_db"
    )

def set_job_status(job_id, status, result=None):
    if not job_id:
        return
    conn = db()
    try:
        cur = conn.cursor()
        if result is None:
            cur.execute("UPDATE jobs SET status=%s WHERE job_id=%s", (status, job_id))
        else:
            cur.execute(
                "UPDATE jobs SET status=%s, result=%s WHERE job_id=%s",
                (status, result, job_id),
            )
        conn.commit()
    finally:
        conn.close()

    
def iosxe_aaa_features_task(task):
    change: ConfigureFeature = task.host["change"]

    conn = task.host.get_connection("scrapli_netconf")
    candidate = _has_candidate(conn)
    if not candidate:
        log.warning("[%s] device has no candidate datastore; skipping", task.host.name)
        return

    # pick train from the device's actual version, not from the request
    train = _feature_train_for(task.host.get("version"))
    # (optionally: assert train == change.train.value, or override change.train)

    rendered = render(change, train)          # from aaa_schemas
    # rendered is a string (or list — see the multi-<config> note below)
    if candidate:
      try:
        result = task.run(
          task=netconf_edit_config,
          config=rendered,
          target="candidate",            # or "running" — see below
        )
        log.info("[%s] edit-config rc=%s", task.host.name, getattr(result, "result", None))
        
      except Exception as e:
        raise RuntimeError(f"{task.host.name}: edit-config failed: {e}") from e
        
      
    else:
      try:
         result = task.run(
          task=netconf_edit_config,
          config=rendered,
          target="running",            # or "running" — see below
         )
         log.info("[%s] edit-config rc=%s", task.host.name, getattr(result, "result", None))
      except Exception as e:
         raise RuntimeError(f"{task.host.name}: edit-config failed: {e}") from e     
              
 

def run_feature_job(payload: ConfigureRequest):
    set_job_status(payload.job_id, "running")
    log.info("job %s: feature start, %d devices", payload.job_id,
             len(payload.devices))

    try:
        hosts_data = _build_hosts_data(payload)

        nr = InitNornir(
            runner={"plugin": "threaded", "options": {"num_workers": len(hosts_data) or 10}},
            inventory={
                "plugin": "FlatDataInventory",
                "options": {"data": hosts_data},
            },
        )

        filtered = nr.filter(F(platform="cisco_iosxe"))
        result = filtered.run(task=iosxe_aaa_features_task)

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
 

class FeatureResponse(BaseModel):
    job_id: Optional[str] = None
    status: str
    message: Optional[str] = None
    
    
app = FastAPI()

@app.post("/aaa", response_model=FeatureResponse)
def configure(payload: ConfigureRequest):
    if payload.async_:
        try:
            Thread(target=run_feature_job, args=(payload,), daemon=True).start()
            return FeatureResponse(job_id=payload.job_id, status="accepted",
                                   message="job queued (async)")
        except Exception as e:
            set_job_status(payload.job_id, "failed", str(e))
            return FeatureResponse(job_id=payload.job_id, status="failed",
                                   message=str(e))
    else:
        run_feature_job(payload)
        return FeatureResponse(job_id=payload.job_id, status="done")