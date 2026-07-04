from fastapi import APIRouter
router = APIRouter(prefix="/api/users", tags=["users"])
@router.get("/")
def get_users():
    return {"message": "List of users"}
