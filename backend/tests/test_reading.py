"""M5 Reader tests.

Two layers:

* Pure-logic tests for ``enrich_tokens`` / ``build_term_index`` - no DB, run
  anywhere the tokenizer is importable.
* An integration test that builds an in-memory SQLite DB, seeds a tiny book,
  and exercises the real ``get_reader_text`` end-to-end.
"""
from types import SimpleNamespace

import pytest

from app.services.parser import tokenize
from app.services.reading import (
    TextNotFoundError,
    build_term_index,
    enrich_tokens,
    get_reader_text,
)


# --------------------------- pure-logic tests ---------------------------

def _term(id, text, status, text_lower=None):
    return SimpleNamespace(
        id=id, text=text, text_lower=text_lower or text.lower(), status=status
    )


def test_enrich_is_lossless():
    content = "The cat sat.\nThe dog ran!"
    tokens = enrich_tokens(content, "a-zA-Z", {})
    assert "".join(t["text"] for t in tokens) == content


def test_enrich_marks_words_and_nonwords():
    tokens = enrich_tokens("Hi, you", "a-zA-Z", {})
    kinds = [(t["text"], t["is_word"]) for t in tokens]
    assert kinds == [("Hi", True), (", ", False), ("you", True)]


def test_enrich_attaches_status_case_insensitively():
    index = build_term_index([_term(7, "The", 3)])
    tokens = enrich_tokens("the THE The", "a-zA-Z", index)
    words = [t for t in tokens if t["is_word"]]
    assert all(w["status"] == 3 and w["term_id"] == 7 for w in words)


def test_enrich_new_word_has_null_status():
    index = build_term_index([_term(1, "cat", 5)])
    tokens = enrich_tokens("cat dog", "a-zA-Z", index)
    by_text = {t["text"]: t for t in tokens if t["is_word"]}
    assert by_text["cat"]["status"] == 5
    assert by_text["dog"]["status"] is None
    assert by_text["dog"]["term_id"] is None


def test_empty_content_yields_no_tokens():
    assert enrich_tokens("", "a-zA-Z", {}) == []
    assert enrich_tokens(None, "a-zA-Z", {}) == []


def test_enrich_uses_same_tokenization_as_parser():
    content = "Hello,  world\u2014friend"
    assert [t["text"] for t in enrich_tokens(content, "a-zA-Z", {})] == tokenize(
        content, "a-zA-Z"
    )


# --------------------------- integration test ---------------------------

@pytest.fixture()
def db_session():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    from app.database import Base
    from app import models  # noqa: F401  (register tables on the metadata)

    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    db = Session()
    try:
        yield db
    finally:
        db.close()


def test_get_reader_text_end_to_end(db_session):
    from app.models.book import Book
    from app.models.language import Language
    from app.models.term import Term
    from app.models.text import Text

    db = db_session
    lang = Language(name="English", word_chars="a-zA-Z")
    db.add(lang)
    db.flush()

    book = Book(title="Primer", language_id=lang.id)
    db.add(book)
    db.flush()

    p1 = Text(title="Page 1", content="The cat sat.", page_number=1, book_id=book.id)
    p2 = Text(title="Page 2", content="The dog ran.", page_number=2, book_id=book.id)
    db.add_all([p1, p2])
    db.add(Term(text="the", text_lower="the", status=5, language_id=lang.id))
    db.add(Term(text="cat", text_lower="cat", status=2, language_id=lang.id))
    db.commit()

    payload = get_reader_text(db, p1.id)

    assert payload["book_title"] == "Primer"
    assert payload["language"]["name"] == "English"
    assert payload["pagination"] == {
        "page_number": 1,
        "page_count": 2,
        "prev_text_id": None,
        "next_text_id": p2.id,
    }
    # lossless round-trip
    assert "".join(t["text"] for t in payload["tokens"]) == "The cat sat."
    words = {t["text"].lower(): t for t in payload["tokens"] if t["is_word"]}
    assert words["the"]["status"] == 5
    assert words["cat"]["status"] == 2
    assert words["sat"]["status"] is None  # brand-new word


def test_get_reader_text_missing_raises(db_session):
    with pytest.raises(TextNotFoundError):
        get_reader_text(db_session, 999999)
