"""SQLAlchemy models. Import all so they register on Base.metadata."""

from app.models.language import Language
from app.models.book import Book
from app.models.text import Text
from app.models.term import Term
from app.models.user import User
from app.models.setting import Setting

__all__ = ["Language", "Book", "Text", "Term", "User", "Setting"]
