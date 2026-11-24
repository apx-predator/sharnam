# main.py
from fastapi import FastAPI, BackgroundTasks
from add_interfaces import ConfigureRequest, run_config_job, do_delete

app = FastAPI()


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