"""Unit tests for the M6 term service (framework-free, in-memory SQLite).

Self-contained: builds its own engine/session so it runs regardless of any
project conftest. Mirrors the style of the existing service-level tests.

Run from the backend/ directory:
    pytest tests/test_terms.py -q
"""
from __future__ import annotations

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
import app.models  # noqa: F401  (register all models on the metadata)
from app.models.language import Language
from app.services import terms as service


@pytest.fixture()
def db():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = Session()
    # Seed one language to attach terms to.
    lang = Language(name="English")
    session.add(lang)
    session.commit()
    session.refresh(lang)
    session.lang_id = lang.id  # type: ignore[attr-defined]
    try:
        yield session
    finally:
        session.close()


def test_create_sets_normalized_lower_and_status(db):
    term = service.create_term(
        db, text="Bonjour", language_id=db.lang_id, translation="Hello", status=3
    )
    assert term.id is not None
    assert term.text == "Bonjour"
    assert term.text_lower == "bonjour"
    assert term.status == 3
    assert term.translation == "Hello"


def test_create_trims_whitespace(db):
    term = service.create_term(db, text="  hola  ", language_id=db.lang_id)
    assert term.text == "hola"
    assert term.text_lower == "hola"
    assert term.status == 0


def test_create_duplicate_raises_with_existing(db):
    first = service.create_term(db, text="the", language_id=db.lang_id)
    with pytest.raises(service.DuplicateTermError) as ei:
        # Case-insensitive identity: "The" collides with "the".
        service.create_term(db, text="The", language_id=db.lang_id)
    assert ei.value.existing.id == first.id


def test_create_invalid_status_raises(db):
    with pytest.raises(service.InvalidStatusError):
        service.create_term(db, text="word", language_id=db.lang_id, status=7)


def test_update_status_and_translation(db):
    term = service.create_term(db, text="casa", language_id=db.lang_id)
    updated = service.update_term(
        db, term.id, status=5, translation="house"
    )
    assert updated.status == 5
    assert updated.translation == "house"


def test_update_is_partial(db):
    term = service.create_term(
        db, text="perro", language_id=db.lang_id, translation="dog", status=2
    )
    # Only change status; translation must be preserved.
    updated = service.update_term(db, term.id, status=4)
    assert updated.status == 4
    assert updated.translation == "dog"


def test_update_can_clear_translation(db):
    term = service.create_term(
        db, text="gato", language_id=db.lang_id, translation="cat"
    )
    updated = service.update_term(db, term.id, translation=None)
    assert updated.translation is None


def test_update_status_none_resets_to_new(db):
    term = service.create_term(db, text="libro", language_id=db.lang_id, status=5)
    updated = service.update_term(db, term.id, status=None)
    assert updated.status == 0


def test_update_missing_raises(db):
    with pytest.raises(service.TermNotFoundError):
        service.update_term(db, 9999, status=1)


def test_parent_link_persists(db):
    parent = service.create_term(db, text="run", language_id=db.lang_id)
    child = service.create_term(db, text="running", language_id=db.lang_id)
    updated = service.update_term(db, child.id, parent_id=parent.id)
    assert updated.parent_id == parent.id


def test_parent_self_reference_rejected(db):
    term = service.create_term(db, text="swim", language_id=db.lang_id)
    with pytest.raises(ValueError):
        service.update_term(db, term.id, parent_id=term.id)


def test_parent_must_exist(db):
    term = service.create_term(db, text="walk", language_id=db.lang_id)
    with pytest.raises(service.TermNotFoundError):
        service.update_term(db, term.id, parent_id=4242)


def test_get_term_missing_raises(db):
    with pytest.raises(service.TermNotFoundError):
        service.get_term(db, 12345)
