import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse

from api.routes import alerts, auth, dashboard, datasources, executions, rules
from core.database import init_db

FRONTEND_DIST = os.environ.get("FRONTEND_DIST", "/app/frontend_dist")


async def seed_if_needed():
    """Run seed script if database is empty. Safe to call on every startup."""
    try:
        from seed_data import seed_database
        await seed_database()
    except Exception as e:
        print(f"[DataQGuard] Seed skipped/error: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    await seed_if_needed()
    yield
    # Shutdown


app = FastAPI(
    title="DataQGuard API",
    description="Data Quality Monitoring Platform",
    version="0.1.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(datasources.router, prefix="/api/v1/datasources", tags=["datasources"])
app.include_router(rules.router, prefix="/api/v1/rules", tags=["rules"])
app.include_router(executions.router, prefix="/api/v1/executions", tags=["executions"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["alerts"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["dashboard"])


@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}


# Serve frontend SPA (all non-API routes → index.html)
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    index_path = os.path.join(FRONTEND_DIST, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    return RedirectResponse(url="/")


@app.get("/")
async def root():
    # If frontend dist exists, redirect to it; else return API info
    index_path = os.path.join(FRONTEND_DIST, "index.html")
    if os.path.isfile(index_path):
        return FileResponse(index_path)
    return {
        "message": "DataQGuard API",
        "docs": "/docs",
        "version": "0.1.0"
    }
