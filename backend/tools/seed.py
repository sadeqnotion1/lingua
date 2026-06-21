"""Seed the local database with a sample language + book for development.

Usage (from repo root, after installing backend deps):
    python backend/tools/seed.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database import SessionLocal, init_db  # noqa: E402
from app.models import Book, Language, Term, Text  # noqa: E402


def _norm(surface: str) -> str:
    """Normalize a surface form for case-insensitive lookup."""
    return surface.lower()


def run() -> None:
    init_db()
    db = SessionLocal()
    try:
        if db.query(Language).first():
            print("Already seeded.")
            return

        # 1) Language
        english = Language(name="English")
        db.add(english)
        db.flush()

        # 2) Book + a couple of pages (texts)
        book = Book(
            title="Welcome to LinguaRead",
            source="bundled-sample",
            language_id=english.id,
        )
        db.add(book)
        db.flush()

        db.add_all([
            Text(
                title="Page 1",
                content="This is a sample text. Click a word to look it up.",
                page_number=1,
                book_id=book.id,
            ),
            Text(
                title="Page 2",
                content="Words you know turn green. Keep reading every day.",
                page_number=2,
                book_id=book.id,
            ),
        ])

        # 3) A few terms (status: 0 unknown ... 5 known); one parent-term link
        look = Term(
            text="look", text_lower=_norm("look"), status=2,
            translation="to direct your eyes", language_id=english.id,
        )
        db.add(look)
        db.flush()

        db.add_all([
            Term(text="this", text_lower=_norm("this"), status=5,
                 language_id=english.id),
            Term(text="sample", text_lower=_norm("sample"), status=3,
                 translation="an example", language_id=english.id),
            Term(text="word", text_lower=_norm("word"), status=1,
                 language_id=english.id),
            # parent-term link: "looking" -> "look"
            Term(text="looking", text_lower=_norm("looking"), status=1,
                 parent_id=look.id, language_id=english.id),
        ])

        db.commit()

        # 4) Verify: read everything back and report counts
        print("Seeded sample data.")
        print(f"  languages: {db.query(Language).count()}")
        print(f"  books:     {db.query(Book).count()}")
        print(f"  texts:     {db.query(Text).count()}")
        print(f"  terms:     {db.query(Term).count()}")
    finally:
        db.close()


if __name__ == "__main__":
    run()
