"""Reader business logic (framework-free) for M5.

The router stays thin and calls into these helpers; tests can drive them with a
plain SQLAlchemy session. Following the same convention as services/library.py,
there are no FastAPI imports here.

The heavy import of SQLAlchemy models is deferred into ``get_reader_text`` so
the pure helpers below (``build_term_index`` / ``enrich_tokens``) can be
imported and unit-tested with only the stdlib + the tokenizer present.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Iterable, List, Optional

# Tokenizer from M4 (stdlib-only). Reused verbatim - we do NOT re-tokenize.
from app.services.parser import DEFAULT_WORD_CHARS, tokenize_tagged

if TYPE_CHECKING:  # pragma: no cover - typing only, avoids a hard runtime dep
    from sqlalchemy.orm import Session


class TextNotFoundError(Exception):
    """Raised when a reader request references a text id that does not exist."""

    def __init__(self, text_id: int) -> None:
        self.text_id = text_id
        super().__init__(f"Text id {text_id} not found.")


def build_term_index(terms: Iterable) -> dict:
    """Map a language's terms by their lowercase surface form.

    Identity matches the DB rule (D6): a term is keyed by ``text_lower``
    (falling back to ``text.lower()`` if a row predates normalization). Later
    rows win on collision, which cannot happen given the unique constraint.
    """
    index: dict = {}
    for t in terms:
        key = (getattr(t, "text_lower", None) or (t.text or "").lower()).strip()
        if not key:
            continue
        index[key] = {"id": t.id, "status": t.status}
    return index


def enrich_tokens(
    content: Optional[str],
    word_chars: Optional[str],
    term_index: dict,
) -> List[dict]:
    """Tokenize ``content`` and attach term status to each word run.

    Pure function (no DB): given the language's ``word_chars`` and a
    ``text_lower -> {id, status}`` index, returns an ordered, lossless list of
    token dicts. ``"".join(t['text'] for t in result) == content`` always
    holds, so the reader can render every token in order.
    """
    tokens: List[dict] = []
    for tok in tokenize_tagged(content or "", word_chars or DEFAULT_WORD_CHARS):
        if tok.is_word:
            match = term_index.get(tok.text.lower())
            tokens.append(
                {
                    "text": tok.text,
                    "is_word": True,
                    "status": match["status"] if match else None,
                    "term_id": match["id"] if match else None,
                }
            )
        else:
            tokens.append(
                {"text": tok.text, "is_word": False, "status": None, "term_id": None}
            )
    return tokens


def _paginate(book, text_id: int, fallback_page: int) -> dict:
    """Compute prev/next text ids and page position within a book."""
    if book is None or not book.texts:
        return {
            "page_number": fallback_page or 1,
            "page_count": 1,
            "prev_text_id": None,
            "next_text_id": None,
        }

    pages = sorted(book.texts, key=lambda t: (t.page_number or 0, t.id))
    ids = [p.id for p in pages]
    page_count = len(pages)
    prev_id = next_id = None
    page_number = fallback_page or 1

    if text_id in ids:
        i = ids.index(text_id)
        page_number = pages[i].page_number or (i + 1)
        if i > 0:
            prev_id = ids[i - 1]
        if i < page_count - 1:
            next_id = ids[i + 1]

    return {
        "page_number": page_number,
        "page_count": page_count,
        "prev_text_id": prev_id,
        "next_text_id": next_id,
    }


def get_reader_text(db: "Session", text_id: int) -> dict:
    """Assemble the server-enriched reader payload for one text/page.

    Raises ``TextNotFoundError`` if the text id does not exist.
    """
    # Deferred imports: keep the pure helpers above importable without the ORM.
    from app.models.book import Book
    from app.models.language import Language
    from app.models.term import Term
    from app.models.text import Text

    text = db.get(Text, text_id)
    if text is None:
        raise TextNotFoundError(text_id)

    book = db.get(Book, text.book_id) if text.book_id is not None else None
    language = (
        db.get(Language, book.language_id)
        if book is not None and book.language_id is not None
        else None
    )

    word_chars = language.word_chars if language is not None else DEFAULT_WORD_CHARS
    language_id = language.id if language is not None else None

    terms = (
        db.query(Term).filter(Term.language_id == language_id).all()
        if language_id is not None
        else []
    )
    term_index = build_term_index(terms)
    tokens = enrich_tokens(text.content, word_chars, term_index)

    return {
        "text_id": text.id,
        "title": text.title,
        "book_id": book.id if book is not None else None,
        "book_title": book.title if book is not None else None,
        "language": {
            "id": language_id,
            "name": language.name if language is not None else None,
            "right_to_left": bool(language.right_to_left) if language is not None else False,
        },
        "pagination": _paginate(book, text.id, text.page_number or 1),
        "tokens": tokens,
    }
