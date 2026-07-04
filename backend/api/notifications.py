from fastapi import APIRouter
router = APIRouter(prefix="/api/notifications", tags=["notifications"])
@router.get("/")
def get_notifications():
    return {"message": "List of notifications"}
