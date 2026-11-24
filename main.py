# main.py
from fastapi import FastAPI, BackgroundTasks
from add_interfaces import ConfigureRequest, run_config_job, do_delete

from add_vlans import (
    ConfigureRequest as VlanConfigureRequest,
    run_config_job as run_vlan_job,
    do_delete as delete_vlans,
)

from add_trunks_access import (
    ConfigureRequest as TrunkConfigureRequest,
    run_config_job as run_trunk_job,
)

from add_port_channels import (
    ConfigureRequest as PcConfigureRequest,
    run_config_job as run_pc_job,
)

from stacking import (
    StackRequest,
    run_stack_job,
)


from add_interface_features import (
    ConfigureRequest as FeatureConfigureRequest,
    run_feature_job,
    FeatureResponse,
)


app = FastAPI(
    title="SHARNAM-NetTool API",
    description="Automation API for managing switches, VLANs, and interfaces via NETCONF.",
    version="1.0.0",
    contact={
        "name": "Sharnam NetOps",
        "url": "https://localhost/sharnam/",
    },
)



# adding interfaces
@app.post("/add_interfaces")
def add_interfaces(payload: ConfigureRequest, bg: BackgroundTasks):

    if payload.action == "delete":
        do_delete(payload)
        return {"status": "success"}

    if payload.async_:
        if not payload.job_id:
            return {"status": "error", "message": "job_id required for async configure"}
        bg.add_task(run_config_job, payload)
        return {"status": "accepted", "job_id": payload.job_id}

    run_config_job(payload)
    return {"status": "success"}
   
 #adding vlans  
@app.post("/add_vlans")
def add_vlans(payload: VlanConfigureRequest, bg: BackgroundTasks):
    if payload.action == "delete":
        delete_vlans(payload)
        return {"status": "success"}

    if payload.async_:
        if not payload.job_id:
            return {"status": "error", "message": "job_id required for async configure"}
        bg.add_task(run_vlan_job, payload)
        return {"status": "accepted", "job_id": payload.job_id}

    run_vlan_job(payload)
    return {"status": "success"}
    
    
   
@app.post("/add_trunks_access", tags=["Trunk/Access"])
def add_trunks_access(payload: TrunkConfigureRequest, bg: BackgroundTasks):
    if payload.async_:
        if not payload.job_id:
            return {"status": "error", "message": "job_id required for async configure"}
        bg.add_task(run_trunk_job, payload)
        return {"status": "accepted", "job_id": payload.job_id}

    run_trunk_job(payload)
    return {"status": "success"}


@app.post("/add_port_channels", tags=["Port-Channels"])
def add_port_channels(payload: PcConfigureRequest, bg: BackgroundTasks):
    if payload.async_:
        if not payload.job_id:
            return {"status": "error", "message": "job_id required for async configure"}
        bg.add_task(run_pc_job, payload)
        return {"status": "accepted", "job_id": payload.job_id}

    run_pc_job(payload)
    return {"status": "success"}
    

@app.post("/add_stacks", tags=["Stack"])
def stack(payload: StackRequest, bg: BackgroundTasks):
    if payload.async_:
        if not payload.job_id:
            return {"status": "error", "message": "job_id required for async configure"}
        bg.add_task(run_stack_job, payload)
        return {"status": "accepted", "job_id": payload.job_id}

    run_stack_job(payload)
    return {"status": "success"}
    
    
    
@app.post("/add_interface_features", tags=["Interface Features"], response_model=FeatureResponse)
def add_interface_features(payload: FeatureConfigureRequest, bg: BackgroundTasks):
    if payload.operation not in ("feature_add", "feature_remove"):
        return FeatureResponse(
            job_id=payload.job_id,
            status="error",
            message=f"unsupported operation {payload.operation!r}; "
                    f"expected feature_add or feature_remove",
        )

    if payload.async_:
        if not payload.job_id:
            return FeatureResponse(job_id=None, status="error",
                                   message="job_id required for async configure")
        bg.add_task(run_feature_job, payload)
        return FeatureResponse(job_id=payload.job_id, status="accepted",
                               message="job queued (async)")

    run_feature_job(payload)
    return FeatureResponse(job_id=payload.job_id, status="done")