"""Stats/dashboard logic (framework-free) for M8.

The pure helpers (``bucket_statuses`` / ``count_words``) avoid importing the ORM
so they can be imported and unit-tested with only the stdlib + the M4 tokenizer.
The DB-facing ``get_stats`` defers model imports, mirroring services/reading.py.
Nothing here is mocked: every number comes from the real rows.

Perf note (minor-finding fix): tokenizing the whole library on every dashboard
load is the expensive part. ``count_words_cached`` memoizes the word count per
text, keyed by a cheap content fingerprint, so an unchanged page is only
tokenized once. Editing a page changes its fingerprint and forces a recompute,
so the cache can never go stale.
"""
from __future__ import annotations

import hashlib
from typing import TYPE_CHECKING, Dict, Iterable, List, Optional, Tuple

# Tokenizer from M4 (stdlib-only). Reused verbatim so 'words' matches the reader.
from app.services.parser import DEFAULT_WORD_CHARS, tokenize_tagged

if TYPE_CHECKING:  # pragma: no cover - typing only, avoids a hard runtime dep
    from sqlalchemy.orm import Session


def bucket_statuses(statuses: Iterable[Optional[int]]) -> dict:
    """Bucket raw Term.status values into LingQ-style familiarity groups.

    0 -> new, 1-4 -> learning, 5 -> known, 99 -> well_known, 98 -> ignored.
    Anything unexpected is counted as 'new' (defensive, never drops a term).
    """
    b = {"new": 0, "learning": 0, "known": 0, "well_known": 0, "ignored": 0, "total": 0}
    for raw in statuses:
        s = raw or 0
        b["total"] += 1
        if s == 0:
            b["new"] += 1
        elif 1 <= s <= 4:
            b["learning"] += 1
        elif s == 5:
            b["known"] += 1
        elif s == 99:
            b["well_known"] += 1
        elif s == 98:
            b["ignored"] += 1
        else:
            b["new"] += 1
    return b


def count_words(content: Optional[str], word_chars: Optional[str] = None) -> int:
    """Count word tokens in ``content`` using the language's ``word_chars``."""
    return sum(
        1
        for tok in tokenize_tagged(content or "", word_chars or DEFAULT_WORD_CHARS)
        if tok.is_word
    )


# text_id -> (fingerprint, word_count). Bounded by the number of texts.
_WORD_COUNT_CACHE: Dict[int, Tuple[str, int]] = {}


def _fingerprint(content: Optional[str], word_chars: str) -> str:
    """Cheap content+config signature. Hashing is far cheaper than tokenizing."""
    h = hashlib.md5()
    h.update(word_chars.encode("utf-8"))
    h.update(b"\x00")
    h.update((content or "").encode("utf-8"))
    return h.hexdigest()


def count_words_cached(
    text_id: Optional[int], content: Optional[str], word_chars: Optional[str] = None
) -> int:
    """Memoized :func:`count_words`, keyed by text id + content fingerprint.

    Falls back to a plain (uncached) count when ``text_id`` is None. The cache
    is correctness-safe: any change to the content or word_chars changes the
    fingerprint, so a recompute happens automatically.
    """
    wc = word_chars or DEFAULT_WORD_CHARS
    if text_id is None:
        return count_words(content, wc)
    fp = _fingerprint(content, wc)
    cached = _WORD_COUNT_CACHE.get(text_id)
    if cached is not None and cached[0] == fp:
        return cached[1]
    n = count_words(content, wc)
    _WORD_COUNT_CACHE[text_id] = (fp, n)
    return n


def get_stats(db: "Session") -> dict:
    """Assemble dashboard aggregates over the whole library."""
    from app.models.book import Book
    from app.models.language import Language
    from app.models.term import Term
    from app.models.text import Text

    languages = db.query(Language).order_by(Language.name).all()
    lang_by_id = {l.id: l for l in languages}

    books = db.query(Book).all()
    texts = db.query(Text).all()
    terms = db.query(Term).all()

    book_lang = {b.id: b.language_id for b in books}

    # Per-language accumulators (only languages that exist as rows).
    per: dict = {
        l.id: {"books": 0, "texts": 0, "words": 0, "statuses": []}
        for l in languages
    }

    for b in books:
        if b.language_id in per:
            per[b.language_id]["books"] += 1

    for t in texts:
        lid = book_lang.get(t.book_id)
        word_chars = (
            lang_by_id[lid].word_chars if lid in lang_by_id else DEFAULT_WORD_CHARS
        )
        words = count_words_cached(t.id, t.content, word_chars)
        if lid in per:
            per[lid]["texts"] += 1
            per[lid]["words"] += words

    for term in terms:
        if term.language_id in per:
            per[term.language_id]["statuses"].append(term.status)

    language_stats: List[dict] = []
    total_words = 0
    for l in languages:
        p = per[l.id]
        total_words += p["words"]
        language_stats.append(
            {
                "language_id": l.id,
                "language_name": l.name,
                "books": p["books"],
                "texts": p["texts"],
                "words": p["words"],
                "terms": bucket_statuses(p["statuses"]),
            }
        )

    return {
        "totals": {
            "languages": len(languages),
            "books": len(books),
            "texts": len(texts),
            "words": total_words,
            "terms": len(terms),
        },
        "terms": bucket_statuses([t.status for t in terms]),
        "languages": language_stats,
    }
