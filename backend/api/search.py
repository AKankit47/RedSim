from fastapi import APIRouter
router = APIRouter(prefix="/api/search", tags=["search"])
@router.get("/")
def get_search():
    return {"message": "List of search"}
