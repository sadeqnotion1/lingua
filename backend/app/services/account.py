"""Account/profile logic (M7).

Framework-free, mirroring services/terms.py and services/reading.py so the
logic stays reusable and unit-testable without FastAPI.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.models.user import User

if TYPE_CHECKING:  # pragma: no cover - typing only, avoids a hard runtime dep
    from sqlalchemy.orm import Session


class AccountNotFoundError(Exception):
    """Raised when no local user has been seeded yet."""

    def __init__(self) -> None:
        super().__init__(
            "No account found. Seed the local user first: "
            "python backend/tools/seed.py"
        )


def get_account(db: "Session") -> User:
    """Return the single local user, or raise AccountNotFoundError.

    LinguaRead is single-user, so the lowest id is the account.
    """
    user = db.query(User).order_by(User.id).first()
    if user is None:
        raise AccountNotFoundError()
    return user


def serialize_account(user: User) -> dict:
    """Serialize a User ORM row into the AccountOut shape."""
    member_since = (
        user.created_at.date().isoformat() if user.created_at is not None else None
    )
    return {
        "username": user.username or "",
        "email": user.email or "",
        "tier": user.tier or "free",
        "member_since": member_since,
    }
