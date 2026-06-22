"""Account/profile endpoints (M7).

Replaces the earlier stub that returned hardcoded empty values. Now backed by
the real seeded User row via the framework-free service layer.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.account import AccountOut
from app.services import account as service

router = APIRouter(prefix="/account", tags=["account"])


@router.get("", response_model=AccountOut)
def get_account(db: Session = Depends(get_db)) -> dict:
    """Return the current (single, local) user's account/profile."""
    try:
        user = service.get_account(db)
    except service.AccountNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
    return service.serialize_account(user)
