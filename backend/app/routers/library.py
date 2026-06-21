"""Library endpoints: books/shelves shown on the Library screen."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(prefix="/library", tags=["library"])


@router.get("/books")
def list_books(db: Session = Depends(get_db)) -> list:
    """List library books. TODO: query and serialize."""
    return []


@router.post("/import")
def import_text() -> dict:
    """Import a new text/book. TODO: implement."""
    return {"status": "not_implemented"}
