"""M2 - Library API tests.

These call the router functions directly with the in-memory ``db_session``
fixture (backend/tests/conftest.py). Driving the functions directly keeps the
suite dependency-free (no httpx / TestClient needed) while still exercising the
endpoint logic, including HTTPException mapping for the error cases.
"""
import pytest
from fastapi import HTTPException

from app.routers import library as library_router
from app.schemas.library import ImportRequest


def test_list_books_empty(db_session):
    assert library_router.list_books(db=db_session) == []


def test_import_creates_book_default_english(db_session):
    payload = ImportRequest(title="My First Book", text="Hello world. Another line.")
    resp = library_router.import_text(payload, db=db_session)

    assert resp["created"] is True
    assert resp["book"]["title"] == "My First Book"
    assert resp["book"]["page_count"] == 1
    assert resp["book"]["language_id"] is not None
    assert isinstance(resp["text_id"], int)

    groups = library_router.list_books(db=db_session)
    assert len(groups) == 1
    assert groups[0]["language_name"] == "English"
    assert groups[0]["books"][0]["title"] == "My First Book"


def test_import_by_language_name_creates_shelf(db_session):
    library_router.import_text(
        ImportRequest(
            title="Le Petit Livre", text="Bonjour le monde.", language="French"
        ),
        db=db_session,
    )
    groups = library_router.list_books(db=db_session)
    names = {g["language_name"] for g in groups}
    assert "French" in names


def test_import_by_language_id(db_session):
    first = library_router.import_text(
        ImportRequest(title="Book A", text="x"), db=db_session
    )
    lang_id = first["book"]["language_id"]

    second = library_router.import_text(
        ImportRequest(title="Book B", text="y", language=lang_id), db=db_session
    )
    assert second["book"]["language_id"] == lang_id

    groups = library_router.list_books(db=db_session)
    assert len(groups) == 1  # both under the same language
    assert len(groups[0]["books"]) == 2


def test_import_unknown_language_id_returns_404(db_session):
    with pytest.raises(HTTPException) as exc:
        library_router.import_text(
            ImportRequest(title="X", text="y", language=999999), db=db_session
        )
    assert exc.value.status_code == 404


def test_import_duplicate_title_returns_409_with_existing(db_session):
    library_router.import_text(ImportRequest(title="Dup", text="one"), db=db_session)
    with pytest.raises(HTTPException) as exc:
        library_router.import_text(ImportRequest(title="Dup", text="two"), db=db_session)

    assert exc.value.status_code == 409
    assert exc.value.detail["book"]["title"] == "Dup"

    # the rejected duplicate did not create a second book
    groups = library_router.list_books(db=db_session)
    assert len(groups[0]["books"]) == 1
