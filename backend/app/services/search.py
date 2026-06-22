"""Search logic (framework-free) for M8.

``make_snippet`` is pure (stdlib only) and unit-tested. ``search`` defers ORM
imports like services/reading.py and runs a case-insensitive 'contains' match
over books, texts and terms. Terms reuse the precomputed ``text_lower`` column
(DECISIONS D6); books/texts are lower-cased in SQL. Results are capped so a huge
library can't return an unbounded payload.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, List

if TYPE_CHECKING:  # pragma: no cover - typing only, avoids a hard runtime dep
    from sqlalchemy.orm import Session

DEFAULT_LIMIT = 50
SNIPPET_RADIUS = 48
_ELLIPSIS = "\u2026"


def make_snippet(content: str, query: str, radius: int = SNIPPET_RADIUS) -> str:
    """Return a trimmed snippet of ``content`` centred on the first match.

    Pure function (no DB). Falls back to the head of the text when the query is
    empty or not found. Adds leading/trailing ellipses when text is clipped.
    """
    text = content or ""
    if not query:
        return text[: radius * 2].strip()
    idx = text.lower().find(query.lower())
    if idx < 0:
        return text[: radius * 2].strip()
    start = max(0, idx - radius)
    end = min(len(text), idx + len(query) + radius)
    snippet = text[start:end].strip()
    if start > 0:
        snippet = _ELLIPSIS + snippet
    if end < len(text):
        snippet = snippet + _ELLIPSIS
    return snippet


def search(db: "Session", query: str, limit: int = DEFAULT_LIMIT) -> dict:
    """Search books, texts and terms for ``query`` (case-insensitive contains)."""
    q = (query or "").strip()
    if not q:
        return {"query": "", "books": [], "texts": [], "terms": [], "total": 0}

    from sqlalchemy import func, or_

    from app.models.book import Book
    from app.models.language import Language
    from app.models.term import Term
    from app.models.text import Text

    like = f"%{q.lower()}%"
    lang_names = {l.id: l.name for l in db.query(Language).all()}

    book_rows = (
        db.query(Book)
        .filter(
            or_(
                func.lower(Book.title).like(like),
                func.lower(func.coalesce(Book.source, "")).like(like),
            )
        )
        .order_by(Book.title)
        .limit(limit)
        .all()
    )
    books: List[dict] = [
        {
            "id": b.id,
            "title": b.title,
            "language_id": b.language_id,
            "language_name": lang_names.get(b.language_id),
            "page_count": len(b.texts),
        }
        for b in book_rows
    ]

    text_rows = (
        db.query(Text)
        .filter(
            or_(
                func.lower(func.coalesce(Text.title, "")).like(like),
                func.lower(Text.content).like(like),
            )
        )
        .limit(limit)
        .all()
    )
    texts: List[dict] = []
    for t in text_rows:
        book = t.book
        lid = book.language_id if book is not None else None
        body = (
            t.content
            if (t.content and q.lower() in t.content.lower())
            else (t.title or t.content or "")
        )
        texts.append(
            {
                "text_id": t.id,
                "title": t.title,
                "book_id": t.book_id,
                "book_title": book.title if book is not None else None,
                "page_number": t.page_number or 1,
                "language_name": lang_names.get(lid),
                "snippet": make_snippet(body, q),
            }
        )

    term_rows = (
        db.query(Term)
        .filter(
            or_(
                Term.text_lower.like(like),
                func.lower(func.coalesce(Term.translation, "")).like(like),
            )
        )
        .order_by(Term.text)
        .limit(limit)
        .all()
    )
    terms: List[dict] = [
        {
            "id": t.id,
            "text": t.text,
            "translation": t.translation,
            "status": t.status if t.status is not None else 0,
            "language_id": t.language_id,
            "language_name": lang_names.get(t.language_id),
        }
        for t in term_rows
    ]

    return {
        "query": q,
        "books": books,
        "texts": texts,
        "terms": terms,
        "total": len(books) + len(texts) + len(terms),
    }
