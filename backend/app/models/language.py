"""Language model (mirrors Lute's language concept)."""
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class Language(Base):
    __tablename__ = "languages"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    # Regex/char config for word splitting (Lute-style parsing).
    word_chars = Column(String, default="a-zA-Z\u00c0-\u017f")
    right_to_left = Column(Boolean, default=False)
    show_romanization = Column(Boolean, default=False)

    books = relationship("Book", back_populates="language")
    terms = relationship("Term", back_populates="language")
