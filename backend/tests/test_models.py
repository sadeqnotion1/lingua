import pytest
from sqlalchemy.exc import IntegrityError

from app.models import Book, Language, Term, Text


def _seed(session):
    lang = Language(name="English")
    session.add(lang)
    session.flush()

    book = Book(title="Welcome to LinguaRead", language_id=lang.id)
    session.add(book)
    session.flush()

    text = Text(title="Page 1", content="This is a sample text.",
                page_number=1, book_id=book.id)
    session.add(text)

    look = Term(text="look", text_lower="look", status=2, language_id=lang.id)
    session.add(look)
    session.flush()
    session.add(Term(text="looking", text_lower="looking", status=1,
                     parent_id=look.id, language_id=lang.id))
    session.commit()
    return lang, book, text


def test_seed_and_query_back(db_session):
    lang, book, text = _seed(db_session)

    assert db_session.query(Language).count() == 1
    assert db_session.query(Book).count() == 1
    assert db_session.query(Text).count() == 1
    assert db_session.query(Term).count() == 2

    assert book.language.name == "English"          # relationships wire up
    assert text.book.title == "Welcome to LinguaRead"

    child = db_session.query(Term).filter_by(text_lower="looking").one()
    assert child.parent.text == "look"              # self-referential parent


def test_terms_are_case_insensitive(db_session):
    lang = Language(name="English")
    db_session.add(lang)
    db_session.flush()

    db_session.add(Term(text="The", text_lower="the", language_id=lang.id))
    db_session.commit()

    db_session.add(Term(text="the", text_lower="the", language_id=lang.id))
    with pytest.raises(IntegrityError):             # "the" == "The" -> rejected
        db_session.commit()
    db_session.rollback()
