"""Search endpoint (M8): one query across books, texts and terms.

Thin router (see backend/docs/ARCHITECTURE.md): all logic lives in
services/search.py.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.search import SearchResults
from app.services import search as service

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=SearchResults)
def search(
    q: str = Query("", description="Search query (case-insensitive contains)."),
    db: Session = Depends(get_db),
) -> dict:
    """Return grouped hits for ``q``. An empty query returns empty groups."""
    return service.search(db, q)
