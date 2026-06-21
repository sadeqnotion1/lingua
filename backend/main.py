"""LinguaRead backend entry point (thin launcher).

Resolves the repo root robustly, puts ``backend/`` on the path, then starts
uvicorn. Keeps the repo root free of source files per the scaffolding standard.
"""
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
BACKEND = REPO_ROOT / "backend"
FRONTEND = REPO_ROOT / "frontend"

# Make the ``app`` package importable regardless of the current working dir.
sys.path.insert(0, str(BACKEND))


def main() -> None:
    import uvicorn
    from app.main import app
    from app.config import settings

    uvicorn.run(app, host=settings.host, port=settings.port)


if __name__ == "__main__":
    main()
