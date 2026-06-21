"""Pydantic request/response schemas for the Library API (M2)."""
from __future__ import annotations
from typing import Optional, Union, List

from pydantic import BaseModel, ConfigDict, Field


class BookOut(BaseModel):
    """A single library item as shown on a shelf."""

    id: int
    title: str
    source: Optional[str] = None
    cover_url: Optional[str] = None
    language_id: Optional[int] = None
    page_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class LanguageGroup(BaseModel):
    """Books grouped under one language (a 'shelf' on the Library screen)."""

    language_id: Optional[int] = None
    language_name: str
    books: List[BookOut] = Field(default_factory=list)


class ImportRequest(BaseModel):
    """Payload for POST /api/library/import."""

    title: str = Field(min_length=1, description="Book title.")
    text: str = Field(min_length=1, description="Raw text content for page 1.")
    # Accept a language *name* (str) or an existing *id* (int). Omit for default.
    language: Optional[Union[str, int]] = Field(
        default=None,
        description="Language name or id. Defaults to English when omitted.",
    )


class ImportResponse(BaseModel):
    """Result of a successful import."""

    book: BookOut
    text_id: int
    created: bool = True
