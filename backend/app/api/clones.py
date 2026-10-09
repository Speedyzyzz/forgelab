from typing import Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.cloner.sqlite_cow import CopyOnWriteCloner

router = APIRouter(prefix="/clones", tags=["Database Clones"])
cloner = CopyOnWriteCloner()

class ProvisionCloneRequest(BaseModel):
    template_name: str
    clone_id: str

@router.post("")
async def provision_clone(req: ProvisionCloneRequest):
    try:
        res = cloner.provision_clone(req.template_name, req.clone_id)
        return res
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.delete("/{clone_id}")
async def destroy_clone(clone_id: str):
    ok = cloner.destroy_clone(clone_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Clone not found.")
    return {"status": "destroyed", "clone_id": clone_id}
