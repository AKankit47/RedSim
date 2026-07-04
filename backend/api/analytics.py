from fastapi import APIRouter

router = APIRouter(prefix="/api/analytics", tags=["analytics"])

@router.get("/dashboard")
async def get_dashboard_stats():
    # Return empty/zero stats as real data isn't generated yet
    return {
        "active_alerts": 0,
        "total_events": 0,
        "monitored_hosts": 0,
        "global_risk": 0,
        "risk_graph": [],
        "recent_detections": []
    }

@router.get("/")
def get_analytics():
    return {"message": "List of analytics"}
