from fastapi import APIRouter
router = APIRouter(prefix="/api/events", tags=["events"])
@router.get("/")
def get_events():
    return {"message": "List of events"}
