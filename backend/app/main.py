"""FastAPI application: wires routers and serves the built SPA."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.config import settings
from app.database import init_db
from app.routers import account, library, reading, terms

app = FastAPI(title=f"{settings.app_name} API", version="0.1.0")

# Allow the Vite dev server to call the API during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def _startup() -> None:
    init_db()


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "app": settings.app_name, "version": "0.1.0"}


# Feature routers (stubs for now).
app.include_router(library.router, prefix="/api")
app.include_router(reading.router, prefix="/api")
app.include_router(terms.router, prefix="/api")
app.include_router(account.router, prefix="/api")

# Serve the built frontend if present (production / local run).
if settings.frontend_dist.exists():
    app.mount(
        "/",
        StaticFiles(directory=str(settings.frontend_dist), html=True),
        name="spa",
    )
