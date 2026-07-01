"""Search endpoint (M8): one query across books, texts and terms.

Thin router (see backend/docs/ARCHITECTURE.md): all logic lives in
services/search.py.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.search import SearchResults
# M9: FTS5-backed search. search_fts mirrors services/search's contract and
# internally falls back to the original LIKE search for empty/short queries or
# if FTS5 is unavailable, so behaviour never regresses.
from app.services import search_fts as service

router = APIRouter(prefix="/search", tags=["search"])


@router.get("", response_model=SearchResults)
def search(
    q: str = Query("", description="Search query (case-insensitive contains)."),
    db: Session = Depends(get_db),
) -> dict:
    """Return grouped hits for ``q``. An empty query returns empty groups."""
    return service.search(db, q)
