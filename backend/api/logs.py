from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

router = APIRouter(prefix="/api/logs", tags=["logs"])

@router.get("/")
def list_logs():
    return {"message": "List of available log files"}

@router.get("/{scenario_id}/{log_type}/download")
def download_log(scenario_id: str, log_type: str):
    ext = "json" if log_type in ["windows_event", "sysmon"] else "log"
    path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "logs_output", f"{scenario_id}_{log_type}.{ext}"))
    if os.path.exists(path):
        return FileResponse(path, media_type="application/octet-stream", filename=f"{log_type}.{ext}")
    return {"error": "Log file not found"}
