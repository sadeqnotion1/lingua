"""Library business logic (framework-free) for M2.

Thin routers call into these helpers; tests can drive them with a plain
SQLAlchemy session. No FastAPI imports here on purpose (see
backend/docs/ARCHITECTURE.md: services = reusable, framework-free logic).
"""
from __future__ import annotations
from typing import Optional, Union

from sqlalchemy.orm import Session

# Import from concrete model modules so this works regardless of whether
# app/models/__init__.py re-exports the classes.
from app.models.book import Book
from app.models.language import Language
from app.models.text import Text

DEFAULT_LANGUAGE_NAME = "English"


class LanguageNotFoundError(Exception):
    """Raised when an import references a language id that does not exist."""

    def __init__(self, language_id: int) -> None:
        self.language_id = language_id
        super().__init__(f"Language id {language_id} not found.")


class DuplicateBookError(Exception):
    """Raised when a book with the same title already exists in the language."""

    def __init__(self, existing: Book) -> None:
        self.existing = existing
        super().__init__(
            f"A book titled {existing.title!r} already exists in this language."
        )


def serialize_book(book: Book) -> dict:
    """Serialize a Book ORM row into the BookOut shape."""
    return {
        "id": book.id,
        "title": book.title,
        "source": book.source,
        "cover_url": book.cover_url,
        "language_id": book.language_id,
        "page_count": len(book.texts),
    }


def list_books_grouped(db: Session) -> list[dict]:
    """Return books grouped by language (languages with >= 1 book)."""
    groups: list[dict] = []

    languages = db.query(Language).order_by(Language.name).all()
    for lang in languages:
        books = (
            db.query(Book)
            .filter(Book.language_id == lang.id)
            .order_by(Book.title)
            .all()
        )
        if not books:
            continue
        groups.append(
            {
                "language_id": lang.id,
                "language_name": lang.name,
                "books": [serialize_book(b) for b in books],
            }
        )

    # Defensive: surface any books not attached to a language.
    orphans = (
        db.query(Book)
        .filter(Book.language_id.is_(None))
        .order_by(Book.title)
        .all()
    )
    if orphans:
        groups.append(
            {
                "language_id": None,
                "language_name": "Uncategorized",
                "books": [serialize_book(b) for b in orphans],
            }
        )

    return groups


def _get_or_create_by_name(db: Session, name: str) -> Language:
    lang = db.query(Language).filter(Language.name == name).first()
    if lang is None:
        lang = Language(name=name)
        db.add(lang)
        db.flush()
    return lang


def resolve_or_create_language(db: Session, language: Optional[Union[str, int]]) -> Language:
    """Resolve a language by id or name; create by name when needed.

    - None -> the default language (English), created if missing.
    - int  -> look up by id; raise LanguageNotFoundError if absent.
    - str  -> look up by stored name; create if missing.
    """
    if language is None:
        return _get_or_create_by_name(db, DEFAULT_LANGUAGE_NAME)

    # bool is a subclass of int; never treat True/False as a language id.
    if isinstance(language, bool):
        raise LanguageNotFoundError(int(language))

    if isinstance(language, int):
        lang = db.get(Language, language)
        if lang is None:
            raise LanguageNotFoundError(language)
        return lang

    name = language.strip()
    if not name:
        return _get_or_create_by_name(db, DEFAULT_LANGUAGE_NAME)
    return _get_or_create_by_name(db, name)


def import_text(
    db: Session,
    *,
    title: str,
    text: str,
    language: Optional[Union[str, int]] = None,
) -> tuple[Book, Text]:
    """Create a Book + its first Text page.

    Raises DuplicateBookError if a book with the same title already exists in
    the resolved language (the existing book is attached to the error).
    """
    title = title.strip()
    if not title:
        raise ValueError("title must not be empty")
    if not text or not text.strip():
        raise ValueError("text must not be empty")

    lang = resolve_or_create_language(db, language)

    existing = (
        db.query(Book)
        .filter(Book.language_id == lang.id, Book.title == title)
        .first()
    )
    if existing is not None:
        raise DuplicateBookError(existing)

    book = Book(title=title, language_id=lang.id)
    db.add(book)
    db.flush()

    page = Text(title=title, content=text, page_number=1, book_id=book.id)
    db.add(page)
    db.flush()

    db.commit()
    db.refresh(book)
    return book, page
