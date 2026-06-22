"""Account/profile schema (M7). Mirrors the shape the frontend already expects
(frontend/src/api/client.ts -> Account).
"""

from typing import Optional

from pydantic import BaseModel, ConfigDict


class AccountOut(BaseModel):
    """The current user's profile as returned to the client."""

    username: str
    email: str
    tier: str = "free"
    member_since: Optional[str] = None  # ISO date string, or null if unknown

    model_config = ConfigDict(from_attributes=True)
