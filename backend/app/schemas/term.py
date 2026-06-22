"""Pydantic request/response schemas for the Terms API (M6).

Mirrors the conventions in schemas/library.py: `from_attributes` for ORM
serialization, explicit Field constraints, and small focused models. Create and
update are *separate* shapes (separate endpoints), not an upsert.

Status follows the Term model docstring / Lute semantics:
    0  = new / unknown
    1-4 = learning
    5  = known
    98 = ignored
    99 = well-known
"""
from __future__ import annotations
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

# The only status values the API accepts. Kept here so the schema layer can
# document them; the service layer enforces the same set defensively.
ALLOWED_STATUSES = frozenset({0, 1, 2, 3, 4, 5, 98, 99})


class TermOut(BaseModel):
    """A tracked term as returned to the client."""

    id: int
    text: str
    text_lower: str
    translation: Optional[str] = None
    status: int = 0
    parent_id: Optional[int] = None
    language_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class TermCreate(BaseModel):
    """Payload for POST /api/terms (create a brand-new term)."""

    text: str = Field(min_length=1, description="Surface form of the word/phrase.")
    language_id: int = Field(description="Language the term belongs to.")
    translation: Optional[str] = Field(default=None, description="User translation/definition.")
    status: int = Field(default=0, description="Familiarity: 0,1-5,98,99.")
    parent_id: Optional[int] = Field(default=None, description="Parent (root) term id.")


class TermUpdate(BaseModel):
    """Payload for PUT /api/terms/{id} (update an existing term).

    All fields optional: only the fields actually present in the request body
    are applied (partial update). `translation` and `parent_id` may be set to
    null to clear them; omit a field to leave it unchanged.
    """

    translation: Optional[str] = None
    status: Optional[int] = None
    parent_id: Optional[int] = None
