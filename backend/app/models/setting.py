"""App settings model (M8).

A tiny key/value store for user-facing application preferences (theme, accent,
...). Kept separate from the single-row User profile so preferences can grow
without schema churn. Purely additive: a brand-new table; nothing existing
changes, and ``init_db`` (Base.metadata.create_all) creates it on next boot.
"""
from sqlalchemy import Column, String

from app.database import Base


class Setting(Base):
    __tablename__ = "app_settings"

    key = Column(String, primary_key=True)
    value = Column(String)
