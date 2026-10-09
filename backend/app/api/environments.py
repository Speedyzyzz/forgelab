from typing import List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.provisioner.watchdog import EnvironmentWatchdog

router = APIRouter(prefix="/environments", tags=["Environments"])
watchdog = EnvironmentWatchdog()

class LaunchEnvRequest(BaseModel):
    env_id: str
    agent_id: str
    resources: List[str]
    ttl_seconds: Optional[int] = 120

@router.post("")
async def launch_environment(req: LaunchEnvRequest):
    env = watchdog.register_environment(req.env_id, req.agent_id, req.resources, req.ttl_seconds)
    return env.model_dump()

@router.post("/{env_id}/heartbeat")
async def heartbeat_environment(env_id: str):
    ok = watchdog.heartbeat(env_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Environment not found or torn down.")
    return {"status": "heartbeated"}

@router.delete("/{env_id}")
async def teardown_environment(env_id: str):
    ok = watchdog.teardown_environment(env_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Environment not found.")
    return {"status": "torn_down", "env_id": env_id}
