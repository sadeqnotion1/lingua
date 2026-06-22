"""Stats endpoint (M8): dashboard aggregates over real library data.

Thin router (see backend/docs/ARCHITECTURE.md): all logic lives in
services/stats.py.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.stats import StatsOut
from app.services import stats as service

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("", response_model=StatsOut)
def get_stats(db: Session = Depends(get_db)) -> dict:
    """Return library-wide totals + per-language term/word breakdowns."""
    return service.get_stats(db)
