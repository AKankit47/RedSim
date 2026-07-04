from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from api.auth import router as auth_router
from api.labs import router as labs_router
from api.websockets import router as ws_router
from api.scenarios import router as scenarios_router
from api.events import router as events_router
from api.alerts import router as alerts_router
from api.logs import router as logs_router
from api.reports import router as reports_router
from api.mitre import router as mitre_router
from api.analytics import router as analytics_router
from api.search import router as search_router
from api.users import router as users_router
from api.notifications import router as notifications_router
from database.database import Base, engine

# Create tables based on our ORM schema
Base.metadata.create_all(bind=engine)

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="RedSim Simulation Platform", docs_url="/docs")

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(labs_router)
app.include_router(ws_router)
app.include_router(scenarios_router)
app.include_router(events_router)
app.include_router(alerts_router)
app.include_router(logs_router)
app.include_router(reports_router)
app.include_router(mitre_router)
app.include_router(analytics_router)
app.include_router(search_router)
app.include_router(users_router)
app.include_router(notifications_router)

@app.get("/")
@limiter.limit("5/minute")
async def root(request: Request):
    return {"message": "RedSim API is running"}
