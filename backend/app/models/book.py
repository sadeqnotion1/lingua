"""Book model: a library item containing one or more texts (pages)."""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    source = Column(String)  # e.g. import source / URL
    cover_url = Column(String)
    language_id = Column(Integer, ForeignKey("languages.id"))

    language = relationship("Language", back_populates="books")
    texts = relationship("Text", back_populates="book", order_by="Text.page_number")
