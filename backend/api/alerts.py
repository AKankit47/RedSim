from fastapi import APIRouter
router = APIRouter(prefix="/api/alerts", tags=["alerts"])
@router.get("/")
def get_alerts():
    return {"message": "List of alerts"}
