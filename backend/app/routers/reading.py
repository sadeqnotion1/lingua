"""Reading endpoints: serve a text rendered with per-word term status."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

router = APIRouter(prefix="/reading", tags=["reading"])


@router.get("/text/{text_id}")
def get_text(text_id: int, db: Session = Depends(get_db)) -> dict:
    """Return tokenized text + term status for the reader. TODO: implement."""
    return {"text_id": text_id, "tokens": []}
