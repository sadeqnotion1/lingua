"""Pydantic response schemas for the Search API (M8).

The search spans the three things a learner actually has: books, texts (pages)
and terms. Each hit carries just enough to render + navigate (e.g. a text hit
knows its ``text_id`` so the UI can deep-link to /read/:textId).
"""
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class BookHit(BaseModel):
    id: int
    title: str
    language_id: Optional[int] = None
    language_name: Optional[str] = None
    page_count: int = 0


class TextHit(BaseModel):
    text_id: int
    title: Optional[str] = None
    book_id: Optional[int] = None
    book_title: Optional[str] = None
    page_number: int = 1
    language_name: Optional[str] = None
    snippet: str = ""


class TermHit(BaseModel):
    id: int
    text: str
    translation: Optional[str] = None
    status: int = 0
    language_id: Optional[int] = None
    language_name: Optional[str] = None


class SearchResults(BaseModel):
    query: str = ""
    books: List[BookHit] = Field(default_factory=list)
    texts: List[TextHit] = Field(default_factory=list)
    terms: List[TermHit] = Field(default_factory=list)
    total: int = 0
