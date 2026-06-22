"""Settings endpoints (M8): profile, appearance preferences and per-language
parser/reader config. Thin router; logic lives in services/settings.py.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.settings import (
    LanguageSettingOut,
    LanguageSettingUpdate,
    SettingsOut,
    SettingsUpdate,
)
from app.services import account as account_service
from app.services import settings as service

router = APIRouter(prefix="/settings", tags=["settings"])


@router.get("", response_model=SettingsOut)
def get_settings(db: Session = Depends(get_db)) -> dict:
    """Return profile + preferences + language settings + live totals."""
    try:
        return service.get_settings(db)
    except account_service.AccountNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.put("", response_model=SettingsOut)
def update_settings(payload: SettingsUpdate, db: Session = Depends(get_db)) -> dict:
    """Apply a partial update to the profile and/or appearance preferences."""
    try:
        if payload.profile is not None:
            service.update_profile(
                db,
                username=payload.profile.username,
                email=payload.profile.email,
            )
        if payload.preferences is not None:
            service.set_preferences(db, payload.preferences)
        return service.get_settings(db)
    except account_service.AccountNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))


@router.put("/languages/{language_id}", response_model=LanguageSettingOut)
def update_language(
    language_id: int,
    payload: LanguageSettingUpdate,
    db: Session = Depends(get_db),
) -> dict:
    """Update a language's word_chars / RTL / romanization config."""
    kwargs = {}
    if payload.word_chars is not None:
        kwargs["word_chars"] = payload.word_chars
    if payload.right_to_left is not None:
        kwargs["right_to_left"] = payload.right_to_left
    if payload.show_romanization is not None:
        kwargs["show_romanization"] = payload.show_romanization
    try:
        return service.update_language(db, language_id, **kwargs)
    except service.LanguageNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc))
