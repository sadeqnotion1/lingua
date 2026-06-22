"""User model (M7).

LinguaRead is self-hosted and single-user, so this is intentionally one row:
the local account/profile shown on the Account screen. No auth yet (that's a
later milestone) — this just makes the profile real instead of hardcoded.
"""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String

from app.database import Base


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True)
    tier = Column(String, default="free")          # plan label shown on Account
    created_at = Column(DateTime, default=_utcnow)  # surfaced as "member since"
