"""Pydantic response schemas for the Reader API (M5).

Server-enriched contract: the backend returns the full, ordered token list with
each word already carrying its matched term status, so the frontend only has to
render (no client-side term matching).
"""
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class TokenOut(BaseModel):
    """One lossless piece of the text, in reading order.

    ``is_word``  - True for a word run, False for spaces/punctuation/newlines.
    ``status``   - the matched Term.status for word tokens, or None when the
                   word is brand-new (no Term row yet). Always None for
                   non-word tokens.
    ``term_id``  - the matched Term.id, or None.
    """

    text: str
    is_word: bool
    status: Optional[int] = None
    term_id: Optional[int] = None


class ReaderLanguage(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    right_to_left: bool = False


class ReaderPagination(BaseModel):
    """Where this page sits within its book (for prev/next navigation)."""

    page_number: int = 1
    page_count: int = 1
    prev_text_id: Optional[int] = None
    next_text_id: Optional[int] = None


class ReaderText(BaseModel):
    """Everything the reader needs to render one text/page."""

    text_id: int
    title: Optional[str] = None
    book_id: Optional[int] = None
    book_title: Optional[str] = None
    language: ReaderLanguage
    pagination: ReaderPagination
    tokens: List[TokenOut]

    model_config = ConfigDict(from_attributes=True)
