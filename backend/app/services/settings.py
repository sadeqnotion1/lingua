"""Settings logic (framework-free) for M8.

- Profile is the single local User (reuses services/account).
- Preferences are a small key/value store (app_settings table).
- Language settings expose the real parser/reader knobs (word_chars, RTL,
  romanization).
- Totals are live counts.

Everything is bound to real rows - no fabricated fields (Delivery Standard 4).
ORM imports are deferred inside functions, mirroring services/reading.py.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional

if TYPE_CHECKING:  # pragma: no cover - typing only, avoids a hard runtime dep
    from sqlalchemy.orm import Session

# Known preference keys + safe defaults. Unknown keys are still stored, but
# these guarantee the UI always has something sensible to render.
DEFAULT_PREFERENCES: Dict[str, str] = {
    "theme": "system",   # "light" | "dark" | "system"
    "accent": "#2f80ed",  # global accent colour (CSS --accent)
}

ALLOWED_THEMES = {"light", "dark", "system"}

# Sentinel for partial language updates: distinguishes 'leave unchanged' from
# an explicit value (mirrors services/terms.py).
_UNSET = object()


class LanguageNotFoundError(Exception):
    """Raised when a settings update references a missing language id."""

    def __init__(self, language_id: int) -> None:
        self.language_id = language_id
        super().__init__(f"Language id {language_id} not found.")


def get_preferences(db: "Session") -> Dict[str, str]:
    """Return stored preferences merged over the built-in defaults."""
    from app.models.setting import Setting

    stored = {s.key: s.value for s in db.query(Setting).all()}
    merged = dict(DEFAULT_PREFERENCES)
    merged.update({k: v for k, v in stored.items() if v is not None})
    return merged


def set_preferences(db: "Session", prefs: Optional[Dict[str, str]]) -> Dict[str, str]:
    """Upsert the given preference key/values, then return the merged set."""
    from app.models.setting import Setting

    for key, value in (prefs or {}).items():
        if value is None:
            continue
        sval = str(value)
        if key == "theme" and sval not in ALLOWED_THEMES:
            continue  # ignore invalid theme, keep current
        row = db.get(Setting, key)
        if row is None:
            db.add(Setting(key=key, value=sval))
        else:
            row.value = sval
    db.commit()
    return get_preferences(db)


def update_profile(
    db: "Session",
    *,
    username: Optional[str] = None,
    email: Optional[str] = None,
):
    """Update the local user's editable profile fields. Raises
    AccountNotFoundError (from services.account) when no user is seeded."""
    from app.services.account import get_account

    user = get_account(db)
    if username is not None:
        cleaned = username.strip()
        if cleaned:
            user.username = cleaned
    if email is not None:
        user.email = email.strip()
    db.commit()
    db.refresh(user)
    return user


def _language_payload(db: "Session", lang) -> dict:
    from app.models.book import Book
    from app.models.term import Term

    return {
        "id": lang.id,
        "name": lang.name,
        "word_chars": lang.word_chars,
        "right_to_left": bool(lang.right_to_left),
        "show_romanization": bool(lang.show_romanization),
        "book_count": db.query(Book).filter(Book.language_id == lang.id).count(),
        "term_count": db.query(Term).filter(Term.language_id == lang.id).count(),
    }


def list_language_settings(db: "Session") -> List[dict]:
    from app.models.language import Language

    return [
        _language_payload(db, l)
        for l in db.query(Language).order_by(Language.name).all()
    ]


def update_language(
    db: "Session",
    language_id: int,
    *,
    word_chars=_UNSET,
    right_to_left=_UNSET,
    show_romanization=_UNSET,
) -> dict:
    """Partially update a Language's parser/reader config. Only args that are
    not _UNSET are applied. Raises LanguageNotFoundError if absent."""
    from app.models.language import Language

    lang = db.get(Language, language_id)
    if lang is None:
        raise LanguageNotFoundError(language_id)

    if word_chars is not _UNSET and word_chars is not None:
        lang.word_chars = word_chars
    if right_to_left is not _UNSET and right_to_left is not None:
        lang.right_to_left = bool(right_to_left)
    if show_romanization is not _UNSET and show_romanization is not None:
        lang.show_romanization = bool(show_romanization)

    db.commit()
    db.refresh(lang)
    return _language_payload(db, lang)


def library_totals(db: "Session") -> dict:
    from app.models.book import Book
    from app.models.language import Language
    from app.models.term import Term
    from app.models.text import Text

    return {
        "languages": db.query(Language).count(),
        "books": db.query(Book).count(),
        "texts": db.query(Text).count(),
        "terms": db.query(Term).count(),
    }


def get_settings(db: "Session") -> dict:
    """Aggregate everything the Settings screen needs in one call."""
    from app.services.account import get_account, serialize_account

    user = get_account(db)  # raises AccountNotFoundError when unseeded
    return {
        "profile": serialize_account(user),
        "preferences": get_preferences(db),
        "languages": list_language_settings(db),
        "totals": library_totals(db),
    }
