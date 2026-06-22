"""Reading endpoints: serve a text rendered with per-word term status."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.reading import ReaderText
from app.services import reading as service

router = APIRouter(prefix="/reading", tags=["reading"])


@router.get("/text/{text_id}", response_model=ReaderText)
def get_text(text_id: int, db: Session = Depends(get_db)) -> dict:
    """Return the tokenized text enriched with per-word term status.

    Server-enriched: every word token already carries its matched term status
    (or None when the word is brand-new), so the reader only renders.
    """
    try:
        return service.get_reader_text(db, text_id)
    except service.TextNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
