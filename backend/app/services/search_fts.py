"""SQLite FTS5 search index for LinguaRead (M9 — search-at-scale).

ADDITIVE drop-in module. The original LIKE-based search in
``app/services/search.py`` is intentionally left UNTOUCHED and is reused here as
a safe fallback (empty/short queries, or if FTS5/trigram is unavailable), so this
change cannot regress existing behaviour.

What this provides
------------------
* ``ensure_index(engine)`` — idempotently creates the FTS5 virtual tables
  (``books_fts``, ``texts_fts``, ``terms_fts``), keep-in-sync triggers, and runs a
  one-time backfill (``'rebuild'``) over any rows that existed before the index.
  Safe + cheap to call on every boot; wired into ``init_db()``.
* ``search(db, query, limit)`` — SAME input/output contract as
  ``app.services.search.search`` (identical dict shape), but matches + ranks via
  FTS5 ``bm25`` instead of scanning every row with ``LIKE '%q%'``.

Why this scales
---------------
``LIKE '%q%'`` cannot use an index and scans the whole table on every keystroke.
FTS5 maintains an inverted index that the DB queries directly, and ``bm25`` ranks
the hits. We use the **trigram** tokenizer so matching stays case-insensitive and
*substring*-based — the closest parity with the previous ``LIKE`` behaviour.
Trigram needs SQLite >= 3.34 and queries of >= 3 characters; shorter queries fall
back to the original LIKE search so nothing breaks.
"""
from __future__ import annotations

import re
from typing import TYPE_CHECKING, Dict, List

if TYPE_CHECKING:  # pragma: no cover - typing only
    from sqlalchemy.engine import Engine
    from sqlalchemy.orm import Session

# Keep parity with services/search.DEFAULT_LIMIT (kept local to avoid an
# import-time dependency on that module).
DEFAULT_LIMIT = 50

# Trigram tokenizer can only match queries of at least this many characters.
_MIN_TRIGRAM = 3

# Active tokenizer, decided once by ensure_index() and read by search().
_TOKENIZER = "trigram"


def _ddl(tokenizer: str) -> List[str]:
    """Idempotent DDL (virtual tables + sync triggers) for the chosen tokenizer."""
    tok = f", tokenize='{tokenizer}'" if tokenizer else ""
    return [
        # ---------------- books (title, source) ----------------
        f"CREATE VIRTUAL TABLE IF NOT EXISTS books_fts USING fts5("
        f"title, source, content='books', content_rowid='id'{tok})",
        "CREATE TRIGGER IF NOT EXISTS books_ai AFTER INSERT ON books BEGIN"
        "  INSERT INTO books_fts(rowid, title, source)"
        "  VALUES (new.id, new.title, new.source); END",
        "CREATE TRIGGER IF NOT EXISTS books_ad AFTER DELETE ON books BEGIN"
        "  INSERT INTO books_fts(books_fts, rowid, title, source)"
        "  VALUES('delete', old.id, old.title, old.source); END",
        "CREATE TRIGGER IF NOT EXISTS books_au AFTER UPDATE ON books BEGIN"
        "  INSERT INTO books_fts(books_fts, rowid, title, source)"
        "  VALUES('delete', old.id, old.title, old.source);"
        "  INSERT INTO books_fts(rowid, title, source)"
        "  VALUES (new.id, new.title, new.source); END",
        # ---------------- texts (title, content) ----------------
        f"CREATE VIRTUAL TABLE IF NOT EXISTS texts_fts USING fts5("
        f"title, content, content='texts', content_rowid='id'{tok})",
        "CREATE TRIGGER IF NOT EXISTS texts_ai AFTER INSERT ON texts BEGIN"
        "  INSERT INTO texts_fts(rowid, title, content)"
        "  VALUES (new.id, new.title, new.content); END",
        "CREATE TRIGGER IF NOT EXISTS texts_ad AFTER DELETE ON texts BEGIN"
        "  INSERT INTO texts_fts(texts_fts, rowid, title, content)"
        "  VALUES('delete', old.id, old.title, old.content); END",
        "CREATE TRIGGER IF NOT EXISTS texts_au AFTER UPDATE ON texts BEGIN"
        "  INSERT INTO texts_fts(texts_fts, rowid, title, content)"
        "  VALUES('delete', old.id, old.title, old.content);"
        "  INSERT INTO texts_fts(rowid, title, content)"
        "  VALUES (new.id, new.title, new.content); END",
        # ---------------- terms (text, translation) ----------------
        f"CREATE VIRTUAL TABLE IF NOT EXISTS terms_fts USING fts5("
        f"text, translation, content='terms', content_rowid='id'{tok})",
        "CREATE TRIGGER IF NOT EXISTS terms_ai AFTER INSERT ON terms BEGIN"
        "  INSERT INTO terms_fts(rowid, text, translation)"
        "  VALUES (new.id, new.text, new.translation); END",
        "CREATE TRIGGER IF NOT EXISTS terms_ad AFTER DELETE ON terms BEGIN"
        "  INSERT INTO terms_fts(terms_fts, rowid, text, translation)"
        "  VALUES('delete', old.id, old.text, old.translation); END",
        "CREATE TRIGGER IF NOT EXISTS terms_au AFTER UPDATE ON terms BEGIN"
        "  INSERT INTO terms_fts(terms_fts, rowid, text, translation)"
        "  VALUES('delete', old.id, old.text, old.translation);"
        "  INSERT INTO terms_fts(rowid, text, translation)"
        "  VALUES (new.id, new.text, new.translation); END",
    ]


_FTS_TABLES = (("books", "books_fts"), ("texts", "texts_fts"), ("terms", "terms_fts"))


def ensure_index(engine: "Engine") -> None:
    """Create FTS5 tables + triggers and backfill existing rows. Idempotent."""
    global _TOKENIZER

    tokenizer = "trigram"
    with engine.begin() as conn:
        # Probe trigram support once; fall back to the built-in unicode61
        # tokenizer on older SQLite builds.
        try:
            conn.exec_driver_sql(
                "CREATE VIRTUAL TABLE IF NOT EXISTS _fts_probe "
                "USING fts5(x, tokenize='trigram')"
            )
            conn.exec_driver_sql("DROP TABLE IF EXISTS _fts_probe")
        except Exception:
            tokenizer = "unicode61"
        _TOKENIZER = tokenizer

        for stmt in _ddl(tokenizer):
            conn.exec_driver_sql(stmt)

        # One-time backfill: if the base table has rows but its index is empty
        # (i.e. rows pre-date this kit), rebuild from the content table. After
        # the first run the triggers keep everything in sync, so this is a no-op.
        for base, fts in _FTS_TABLES:
            base_n = conn.exec_driver_sql(f'SELECT COUNT(*) FROM "{base}"').scalar() or 0
            idx_n = conn.exec_driver_sql(f'SELECT COUNT(*) FROM "{fts}_docsize"').scalar() or 0
            if base_n and not idx_n:
                conn.exec_driver_sql(f"INSERT INTO {fts}({fts}) VALUES('rebuild')")


def _match_expr(q: str) -> str:
    """Build a safe FTS5 MATCH expression for ``q``."""
    if _TOKENIZER == "trigram":
        # A quoted string is matched as a case-insensitive substring by trigram.
        return '"' + q.replace('"', '""') + '"'
    # unicode61 fallback: AND-combine prefix-matched tokens.
    tokens = [t for t in re.split(r"\s+", q) if t]
    return " ".join(f'"{t.replace(chr(34), chr(34) * 2)}"*' for t in tokens) or '""'


def _matched_ids(db: "Session", table: str, match: str, limit: int) -> List[int]:
    """Return rowids for ``table`` matching ``match``, best-ranked first."""
    from sqlalchemy import text as sa_text

    rows = db.execute(
        sa_text(
            f"SELECT rowid FROM {table} WHERE {table} MATCH :m ORDER BY rank LIMIT :lim"
        ),
        {"m": match, "lim": limit},
    )
    return [int(r[0]) for r in rows]


def search(db: "Session", query: str, limit: int = DEFAULT_LIMIT) -> dict:
    """FTS5-backed search across books, texts and terms (ranked by bm25).

    Returns the exact same dict shape as ``app.services.search.search`` so the
    router and schemas need no changes.
    """
    q = (query or "").strip()
    if not q:
        return {"query": "", "books": [], "texts": [], "terms": [], "total": 0}

    # Trigram needs >= 3 chars; for shorter queries reuse the original LIKE
    # search so small-query behaviour is identical and never errors.
    if _TOKENIZER == "trigram" and len(q) < _MIN_TRIGRAM:
        from app.services.search import search as like_search

        return like_search(db, q, limit)

    try:
        return _fts_search(db, q, limit)
    except Exception:
        # Defensive (Delivery Standard §5): never break search.
        from app.services.search import search as like_search

        return like_search(db, q, limit)


def _fts_search(db: "Session", q: str, limit: int) -> dict:
    from sqlalchemy import func

    from app.models.book import Book
    from app.models.language import Language
    from app.models.term import Term
    from app.models.text import Text
    from app.services.search import make_snippet

    match = _match_expr(q)
    lang_names = {l.id: l.name for l in db.query(Language).all()}

    # ---------------- books ----------------
    book_ids = _matched_ids(db, "books_fts", match, limit)
    book_by_id = {b.id: b for b in db.query(Book).filter(Book.id.in_(book_ids)).all()} if book_ids else {}
    page_counts: Dict[int, int] = {}
    if book_ids:
        for bid, n in (
            db.query(Text.book_id, func.count(Text.id))
            .filter(Text.book_id.in_(book_ids))
            .group_by(Text.book_id)
            .all()
        ):
            page_counts[bid] = n
    books: List[dict] = []
    for bid in book_ids:
        b = book_by_id.get(bid)
        if b is None:
            continue
        books.append(
            {
                "id": b.id,
                "title": b.title,
                "language_id": b.language_id,
                "language_name": lang_names.get(b.language_id),
                "page_count": page_counts.get(b.id, 0),
            }
        )

    # ---------------- texts ----------------
    text_ids = _matched_ids(db, "texts_fts", match, limit)
    text_by_id = {t.id: t for t in db.query(Text).filter(Text.id.in_(text_ids)).all()} if text_ids else {}
    text_book_ids = {t.book_id for t in text_by_id.values() if t.book_id is not None}
    books_by_id: Dict[int, object] = {}
    if text_book_ids:
        for b in db.query(Book).filter(Book.id.in_(text_book_ids)).all():
            books_by_id[b.id] = b
    texts: List[dict] = []
    for tid in text_ids:
        t = text_by_id.get(tid)
        if t is None:
            continue
        book = books_by_id.get(t.book_id)
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

    # ---------------- terms ----------------
    term_ids = _matched_ids(db, "terms_fts", match, limit)
    term_by_id = {t.id: t for t in db.query(Term).filter(Term.id.in_(term_ids)).all()} if term_ids else {}
    terms: List[dict] = []
    for tid in term_ids:
        t = term_by_id.get(tid)
        if t is None:
            continue
        terms.append(
            {
                "id": t.id,
                "text": t.text,
                "translation": t.translation,
                "status": t.status if t.status is not None else 0,
                "language_id": t.language_id,
                "language_name": lang_names.get(t.language_id),
            }
        )

    return {
        "query": q,
        "books": books,
        "texts": texts,
        "terms": terms,
        "total": len(books) + len(texts) + len(terms),
    }
