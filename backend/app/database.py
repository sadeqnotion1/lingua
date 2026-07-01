"""SQLAlchemy engine, session, and base."""
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},  # SQLite + threaded server
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


def init_db() -> None:
    """Create tables. Import models so they register on the metadata."""
    from app import models  # noqa: F401

    Base.metadata.create_all(bind=engine)

    # === M9 (SQLite FTS5) — create the search index + triggers, backfill once ===
    from app.services.search_fts import ensure_index

    ensure_index(engine)


def get_db():
    """FastAPI dependency that yields a scoped session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
