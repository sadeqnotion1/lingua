"""Library endpoints: books/shelves shown on the Library screen."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.library import ImportRequest, ImportResponse, LanguageGroup
from app.services import library as service

router = APIRouter(prefix="/library", tags=["library"])


@router.get("/books", response_model=list[LanguageGroup])
def list_books(db: Session = Depends(get_db)) -> list:
    """List library books grouped by language."""
    return service.list_books_grouped(db)


@router.post("/import", response_model=ImportResponse, status_code=201)
def import_text(payload: ImportRequest, db: Session = Depends(get_db)) -> dict:
    """Import a new text/book, creating Book + Text rows."""
    try:
        book, page = service.import_text(
            db,
            title=payload.title,
            text=payload.text,
            language=payload.language,
        )
    except service.LanguageNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except service.DuplicateBookError as exc:
        raise HTTPException(
            status_code=409,
            detail={
                "message": str(exc),
                "book": service.serialize_book(exc.existing),
            },
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    return {
        "book": service.serialize_book(book),
        "text_id": page.id,
        "created": True,
    }
