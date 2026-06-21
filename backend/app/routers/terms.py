"""Term endpoints: create/update terms and their learning status."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(prefix="/terms", tags=["terms"])


@router.get("")
def list_terms(db: Session = Depends(get_db)) -> list:
    """List saved terms. TODO: implement."""
    return []


@router.post("")
def upsert_term() -> dict:
    """Create or update a term (text, translation, status). TODO: implement."""
    return {"status": "not_implemented"}
