from fastapi import APIRouter

router = APIRouter(prefix="/api/scenarios", tags=["scenarios"])

@router.get("/graph")
async def get_scenario_graph():
    # Return empty graph state replacing mock data
    return {
        "nodes": [],
        "edges": []
    }

@router.get("/")
def get_scenarios():
    return {"message": "List of scenarios"}
