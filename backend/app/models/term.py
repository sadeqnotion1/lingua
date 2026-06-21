"""Term model: a word/phrase the learner is tracking.

Status mirrors Lute / LingQ: 0=unknown, 1-4=learning, 5=known/well-known,
98=ignored, 99=well-known. Keep as int for SRS flexibility.
"""
from sqlalchemy import Column, Integer, String, Text as SAText, ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class Term(Base):
    __tablename__ = "terms"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)        # surface form
    text_lower = Column(String, index=True)      # normalized for lookup
    translation = Column(SAText)
    status = Column(Integer, default=0)
    parent_id = Column(Integer, ForeignKey("terms.id"))  # Lute "parent term"
    language_id = Column(Integer, ForeignKey("languages.id"))

    language = relationship("Language", back_populates="terms")
    parent = relationship("Term", remote_side=[id])
