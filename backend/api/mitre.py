from fastapi import APIRouter
router = APIRouter(prefix="/api/mitre", tags=["mitre"])
@router.get("/")
def get_mitre():
    return {"message": "List of mitre"}
