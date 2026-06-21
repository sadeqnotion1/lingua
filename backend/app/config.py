"""Central configuration and path resolution.

All paths are derived from the repo root so the app never depends on the
current working directory.
"""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = REPO_ROOT / "backend"
FRONTEND_DIST = REPO_ROOT / "frontend" / "dist"
DATA_DIR = BACKEND_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)


class Settings:
    app_name: str = "LinguaRead"
    host: str = "127.0.0.1"
    port: int = 8000
    database_url: str = f"sqlite:///{DATA_DIR / 'lingua.db'}"
    frontend_dist: Path = FRONTEND_DIST


settings = Settings()
