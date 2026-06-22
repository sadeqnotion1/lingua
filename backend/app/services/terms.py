"""Term business logic (framework-free) for M6.

Thin routers call into these helpers; tests drive them with a plain SQLAlchemy
session. No FastAPI imports here on purpose (see backend/docs/ARCHITECTURE.md:
services = reusable, framework-free logic). Mirrors services/library.py.

Design notes:
- Terms are case-insensitive within a language (DECISIONS D6). Identity is
  (language_id, text_lower); we always set text_lower = text.lower().
- Create and update are separate operations (no upsert), matching the chosen
  API shape.
- Partial updates use a module-level _UNSET sentinel so callers can distinguish
  "leave unchanged" from "set to null".
"""
from __future__ import annotations
from typing import Optional

from sqlalchemy.orm import Session

from app.models.term import Term

# Allowed familiarity values (see Term model docstring / Lute semantics).
ALLOWED_STATUSES = frozenset({0, 1, 2, 3, 4, 5, 98, 99})


class _Unset:
    """Sentinel marking 'argument not provided' for partial updates."""

    def __repr__(self) -> str:  # pragma: no cover - debug aid
        return "<UNSET>"


_UNSET = _Unset()


class TermNotFoundError(Exception):
    """Raised when a term id does not exist."""

    def __init__(self, term_id: int) -> None:
        self.term_id = term_id
        super().__init__(f"Term id {term_id} not found.")


class DuplicateTermError(Exception):
    """Raised when creating a term that already exists in the language.

    The existing term is attached so the router can return it (409), mirroring
    the library duplicate-book flow.
    """

    def __init__(self, existing: Term) -> None:
        self.existing = existing
        super().__init__(
            f"A term {existing.text!r} already exists in this language."
        )


class InvalidStatusError(Exception):
    """Raised when a status value is outside the allowed set."""

    def __init__(self, status: int) -> None:
        self.status = status
        super().__init__(
            f"Invalid status {status!r}; allowed: {sorted(ALLOWED_STATUSES)}."
        )


def _validate_status(status: int) -> int:
    # bool is a subclass of int; never accept True/False as a status.
    if isinstance(status, bool) or status not in ALLOWED_STATUSES:
        raise InvalidStatusError(status)
    return status


def _validate_parent(db: Session, term_id: Optional[int], parent_id: Optional[int]) -> None:
    if parent_id is None:
        return
    if term_id is not None and parent_id == term_id:
        raise ValueError("A term cannot be its own parent.")
    if db.get(Term, parent_id) is None:
        raise TermNotFoundError(parent_id)


def serialize_term(term: Term) -> dict:
    """Serialize a Term ORM row into the TermOut shape."""
    return {
        "id": term.id,
        "text": term.text,
        "text_lower": term.text_lower,
        "translation": term.translation,
        "status": term.status if term.status is not None else 0,
        "parent_id": term.parent_id,
        "language_id": term.language_id,
    }


def get_term(db: Session, term_id: int) -> Term:
    """Fetch a term by id or raise TermNotFoundError."""
    term = db.get(Term, term_id)
    if term is None:
        raise TermNotFoundError(term_id)
    return term


def find_term(db: Session, *, language_id: int, text: str) -> Optional[Term]:
    """Look up a term by (language_id, normalized text). None if absent."""
    text_lower = text.strip().lower()
    return (
        db.query(Term)
        .filter(Term.language_id == language_id, Term.text_lower == text_lower)
        .first()
    )


def create_term(
    db: Session,
    *,
    text: str,
    language_id: int,
    translation: Optional[str] = None,
    status: int = 0,
    parent_id: Optional[int] = None,
) -> Term:
    """Create a new term.

    Raises:
        ValueError        - empty text.
        InvalidStatusError - status outside the allowed set.
        DuplicateTermError - a term with the same (language_id, text_lower)
                             already exists (existing term attached).
        TermNotFoundError  - parent_id given but no such term.
    """
    surface = text.strip()
    if not surface:
        raise ValueError("text must not be empty")

    _validate_status(status)
    _validate_parent(db, None, parent_id)

    existing = find_term(db, language_id=language_id, text=surface)
    if existing is not None:
        raise DuplicateTermError(existing)

    term = Term(
        text=surface,
        text_lower=surface.lower(),
        translation=translation,
        status=status,
        parent_id=parent_id,
        language_id=language_id,
    )
    db.add(term)
    db.commit()
    db.refresh(term)
    return term


def update_term(
    db: Session,
    term_id: int,
    *,
    translation=_UNSET,
    status=_UNSET,
    parent_id=_UNSET,
) -> Term:
    """Partially update an existing term.

    Only fields that are not _UNSET are applied, so callers can clear a value
    (pass None) without disturbing the others.

    Raises:
        TermNotFoundError  - term (or new parent) does not exist.
        InvalidStatusError - status outside the allowed set.
    """
    term = get_term(db, term_id)

    if status is not _UNSET and status is not None:
        _validate_status(status)
        term.status = status
    elif status is None:
        # Explicit reset to "new".
        term.status = 0

    if translation is not _UNSET:
        term.translation = translation

    if parent_id is not _UNSET:
        _validate_parent(db, term_id, parent_id)
        term.parent_id = parent_id

    db.commit()
    db.refresh(term)
    return term
