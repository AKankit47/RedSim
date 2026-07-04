from fastapi import APIRouter, HTTPException
from lab_manager.docker_manager import docker_manager

router = APIRouter(prefix="/api/labs", tags=["labs"])


@router.get("")
async def list_labs():
    """List all known labs with live Docker status and resource stats."""
    return docker_manager.list_labs()


@router.post("/start/{lab_id}")
async def start_lab(lab_id: str):
    res = docker_manager.start_lab(lab_id)
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res


@router.post("/stop/{lab_id}")
async def stop_lab(lab_id: str):
    res = docker_manager.stop_lab(lab_id)
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res


@router.post("/restart/{lab_id}")
async def restart_lab(lab_id: str):
    res = docker_manager.restart_lab(lab_id)
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res


@router.get("/status")
async def get_status():
    return docker_manager.status()


@router.get("/{lab_id}/stats")
async def get_lab_stats(lab_id: str):
    """Live CPU% and RAM MB for a running container."""
    res = docker_manager.get_stats(lab_id)
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res
