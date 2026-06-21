"""Text model: a single readable page within a book."""
from sqlalchemy import Column, Integer, String, Text as SAText, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Text(Base):
    __tablename__ = "texts"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    content = Column(SAText, nullable=False)
    page_number = Column(Integer, default=1)
    book_id = Column(Integer, ForeignKey("books.id"))

    book = relationship("Book", back_populates="texts")
