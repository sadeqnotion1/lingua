"""Pydantic schemas for the Settings API (M8).

Settings are bound to real rows only (Delivery Standard 4):
- profile      -> the single local User (username/email editable; tier + member
                  since read-only, no auth yet).
- languages    -> the real parser/reader knobs on each Language row
                  (word_chars, right_to_left, show_romanization).
- preferences  -> a small key/value store (app_settings table) for appearance.
- totals       -> live counts, mirroring LingQ's 'Total LingQs / Imports'.
"""
from __future__ import annotations

import re
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

# Lightweight, dependency-free email check (avoids pulling in email-validator).
# Intentionally permissive: one '@', a dot in the domain, no whitespace.
_EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class ProfileOut(BaseModel):
    username: str
    email: str
    tier: str = "free"
    member_since: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class ProfileUpdate(BaseModel):
    username: Optional[str] = Field(default=None, min_length=1)
    email: Optional[str] = None

    @field_validator("email")
    @classmethod
    def _validate_email(cls, v: Optional[str]) -> Optional[str]:
        """Reject malformed emails so a bad value never reaches the DB.

        ``None`` means 'leave unchanged' and is allowed through untouched.
        A provided value must be a non-empty, syntactically valid address;
        the cleaned (stripped) value is returned.
        """
        if v is None:
            return v
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("Email must not be empty.")
        if not _EMAIL_RE.match(cleaned):
            raise ValueError("Enter a valid email address.")
        return cleaned


class LanguageSettingOut(BaseModel):
    id: int
    name: str
    word_chars: Optional[str] = None
    right_to_left: bool = False
    show_romanization: bool = False
    book_count: int = 0
    term_count: int = 0

    model_config = ConfigDict(from_attributes=True)


class LanguageSettingUpdate(BaseModel):
    word_chars: Optional[str] = None
    right_to_left: Optional[bool] = None
    show_romanization: Optional[bool] = None


class LibraryTotals(BaseModel):
    languages: int = 0
    books: int = 0
    texts: int = 0
    terms: int = 0


class SettingsOut(BaseModel):
    profile: ProfileOut
    preferences: Dict[str, str] = Field(default_factory=dict)
    languages: List[LanguageSettingOut] = Field(default_factory=list)
    totals: LibraryTotals = Field(default_factory=LibraryTotals)


class SettingsUpdate(BaseModel):
    profile: Optional[ProfileUpdate] = None
    preferences: Optional[Dict[str, str]] = None
