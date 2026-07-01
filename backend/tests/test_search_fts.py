"""Tests for the M9 SQLite FTS5 search (backend/app/services/search_fts.py).

Self-contained: builds its own temp-file SQLite DB bound to the app's models,
so it does not depend on the names in conftest.py. Run with:

    pytest backend/tests/test_search_fts.py -v
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app import models  # noqa: F401  (registers all tables on Base.metadata)
from app.models.book import Book
from app.models.language import Language
from app.models.term import Term
from app.models.text import Text
from app.services import search as like_service
from app.services import search_fts as fts_service


@pytest.fixture()
def db(tmp_path):
    engine = create_engine(
        f"sqlite:///{tmp_path / 'test.db'}",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    fts_service.ensure_index(engine)  # create FTS tables + triggers

    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    s = Session()

    english = Language(name="English")
    s.add(english)
    s.flush()
    book = Book(title="Welcome to LinguaRead", source="bundled-sample", language_id=english.id)
    s.add(book)
    s.flush()
    s.add_all([
        Text(title="Page 1", content="This is a sample text. Click a word to look it up. ", page_number=1, book_id=book.id),
        Text(title="Page 2", content="Words you know turn green. Keep reading every day. ", page_number=2, book_id=book.id),
    ])
    s.add_all([
        Term(text="look", text_lower="look", translation="to direct your eyes", status=2, language_id=english.id),
        Term(text="this", text_lower="this", status=5, language_id=english.id),
        Term(text="sample", text_lower="sample", translation="an example", status=3, language_id=english.id),
        Term(text="green", text_lower="green", status=4, language_id=english.id),
    ])
    s.commit()
    yield s
    s.close()


def _ids(res):
    return (
        sorted(b["id"] for b in res["books"]),
        sorted(t["text_id"] for t in res["texts"]),
        sorted(t["id"] for t in res["terms"]),
    )


def test_shape_matches_like_service(db):
    fts = fts_service.search(db, "sample")
    assert set(fts) == {"query", "books", "texts", "terms", "total"}


def test_parity_with_like_on_seed(db):
    """FTS returns the same books/pages/terms as the original LIKE search."""
    like = like_service.search(db, "sample")
    fts = fts_service.search(db, "sample")
    assert like["total"] == 3
    assert fts["total"] == 3
    assert _ids(fts) == _ids(like)


def test_insert_trigger_keeps_index_in_sync(db):
    eng = db.query(Language).first()
    db.add(Term(text="serendipity", text_lower="serendipity", translation="luck", status=0, language_id=eng.id))
    db.commit()
    res = fts_service.search(db, "serendipity")
    assert any(t["text"] == "serendipity" for t in res["terms"])


def test_update_and_delete_triggers(db):
    eng = db.query(Language).first()
    term = Term(text="serendipity", text_lower="serendipity", translation="luck", status=0, language_id=eng.id)
    db.add(term)
    db.commit()

    term.translation = "a happy accident zzxq"
    db.commit()
    assert any(t["id"] == term.id for t in fts_service.search(db, "zzxq")["terms"])

    db.delete(term)
    db.commit()
    assert not any(t["text"] == "serendipity" for t in fts_service.search(db, "serendipity")["terms"])


def test_substring_match_when_trigram_available(db):
    if fts_service._TOKENIZER != "trigram":
        pytest.skip("trigram tokenizer unavailable on this SQLite build")
    res = fts_service.search(db, "amp")  # inside 'sample'
    assert any(t["text"] == "sample" for t in res["terms"])


def test_backfill_reindexes_preexisting_rows(db):
    bind = db.get_bind()
    with bind.begin() as c:
        c.exec_driver_sql("DROP TABLE IF EXISTS books_fts")
        c.exec_driver_sql("DROP TABLE IF EXISTS texts_fts")
        c.exec_driver_sql("DROP TABLE IF EXISTS terms_fts")
    fts_service.ensure_index(bind)
    assert fts_service.search(db, "sample")["total"] == 3


def test_short_query_falls_back_without_error(db):
    res = fts_service.search(db, "a")  # < 3 chars -> LIKE fallback
    assert isinstance(res, dict) and "total" in res


def test_empty_query_returns_empty(db):
    assert fts_service.search(db, "   ")["total"] == 0
