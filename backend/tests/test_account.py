"""Tests for the M7 account service.

Self-contained in-memory SQLite session (does not depend on conftest fixtures)
so it stays robust regardless of fixture names.
"""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models.user import User
from app.services import account as service


@pytest.fixture()
def session():
    engine = create_engine(
        "sqlite:///:memory:", connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    TestingSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


def test_get_account_raises_when_empty(session):
    with pytest.raises(service.AccountNotFoundError):
        service.get_account(session)


def test_get_account_returns_seeded_user(session):
    session.add(
        User(username="SadeQ", email="sadeqnotion1@atomicmail.io", tier="free")
    )
    session.commit()

    user = service.get_account(session)
    assert user.username == "SadeQ"
    assert user.email == "sadeqnotion1@atomicmail.io"


def test_serialize_account_shape(session):
    session.add(User(username="SadeQ", email="x@y.z", tier="free"))
    session.commit()

    data = service.serialize_account(service.get_account(session))
    assert set(data) == {"username", "email", "tier", "member_since"}
    assert data["tier"] == "free"
    # member_since is an ISO date string when created_at is set.
    assert data["member_since"] is None or len(data["member_since"]) == 10
