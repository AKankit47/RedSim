import os
routes = ["scenarios", "events", "alerts", "logs", "reports", "mitre", "analytics", "search", "users", "notifications"]
template = """from fastapi import APIRouter
router = APIRouter(prefix="/api/{0}", tags=["{0}"])
@router.get("/")
def get_{0}():
    return {{"message": "List of {0}"}}
"""
for r in routes:
    path = os.path.join("api", f"{r}.py")
    with open(path, "w") as f:
        f.write(template.format(r))
