"""Seed the local database with a sample language + book for development.

Usage (from repo root, after installing backend deps):
    python backend/tools/seed.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database import SessionLocal, init_db  # noqa: E402
from app.models import Book, Language, Text  # noqa: E402


def run() -> None:
    init_db()
    db = SessionLocal()
    try:
        if db.query(Language).first():
            print("Already seeded.")
            return
        lang = Language(name="English")
        db.add(lang)
        db.flush()
        book = Book(title="Welcome to LinguaRead", language_id=lang.id)
        db.add(book)
        db.flush()
        db.add(
            Text(
                title="Page 1",
                content="This is a sample text. Click a word to look it up.",
                page_number=1,
                book_id=book.id,
            )
        )
        db.commit()
        print("Seeded sample data.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
