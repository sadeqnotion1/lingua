"""Term endpoints (M6): create / read / update tracked terms.

Replaces the M0 stub. Thin HTTP layer over services/terms.py. Create and update
are *separate* endpoints (no upsert), per the chosen API shape:

    GET  /api/terms/{term_id}  -> load a term's full details (for the drawer)
    POST /api/terms            -> create a new term (201)
    PUT  /api/terms/{term_id}  -> update status / translation / parent
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.term import TermCreate, TermOut, TermUpdate
from app.services import terms as service

router = APIRouter(prefix="/terms", tags=["terms"])


@router.get("/{term_id}", response_model=TermOut)
def read_term(term_id: int, db: Session = Depends(get_db)) -> dict:
    """Return a single term's full details."""
    try:
        return service.serialize_term(service.get_term(db, term_id))
    except service.TermNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.post("", response_model=TermOut, status_code=201)
def create_term(payload: TermCreate, db: Session = Depends(get_db)) -> dict:
    """Create a new term. 409 (with the existing term) if it already exists."""
    try:
        term = service.create_term(
            db,
            text=payload.text,
            language_id=payload.language_id,
            translation=payload.translation,
            status=payload.status,
            parent_id=payload.parent_id,
        )
        return service.serialize_term(term)
    except service.InvalidStatusError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except service.DuplicateTermError as exc:
        # Mirror the library 409 pattern: return the existing row so the client
        # can switch to an update instead of failing.
        raise HTTPException(
            status_code=409,
            detail={
                "message": str(exc),
                "term": service.serialize_term(exc.existing),
            },
        )
    except service.TermNotFoundError as exc:  # bad parent_id
        raise HTTPException(status_code=422, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))


@router.put("/{term_id}", response_model=TermOut)
def update_term(
    term_id: int, payload: TermUpdate, db: Session = Depends(get_db)
) -> dict:
    """Update an existing term. Only fields present in the body are applied."""
    # Forward only the fields the client actually sent (partial update).
    provided = payload.model_dump(exclude_unset=True)
    try:
        term = service.update_term(db, term_id, **provided)
        return service.serialize_term(term)
    except service.TermNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    except service.InvalidStatusError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
