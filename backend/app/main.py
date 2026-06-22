"""FastAPI application: wires routers and serves the built SPA."""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db
from app.routers import account, library, reading, search, settings as settings_router, stats, terms


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create tables on startup (replaces the deprecated on_event hook)."""
    init_db()
    yield


app = FastAPI(title=f"{settings.app_name} API", version="0.1.0", lifespan=lifespan)

# Allow the Vite dev server to call the API during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "app": settings.app_name, "version": "0.1.0"}


# Feature routers.
app.include_router(library.router, prefix="/api")
app.include_router(reading.router, prefix="/api")
app.include_router(terms.router, prefix="/api")
app.include_router(account.router, prefix="/api")
# M8 - polish (dashboard stats, global search, settings).
app.include_router(stats.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(settings_router.router, prefix="/api")

# Serve the built frontend if present (production / local run).
if settings.frontend_dist.exists():
    app.mount(
        "/",
        StaticFiles(directory=str(settings.frontend_dist), html=True),
        name="spa",
    )
