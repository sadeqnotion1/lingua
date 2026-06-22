"""Pydantic response schemas for the Stats API (M8 dashboard).

Every field is derived from real rows by services/stats.py - there are no
fabricated metrics (Delivery Standard 4).
"""
from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class StatusBreakdown(BaseModel):
    """Term familiarity counts, bucketed by Lute/LingQ status semantics."""

    new: int = 0          # status 0
    learning: int = 0     # status 1-4
    known: int = 0        # status 5
    well_known: int = 0   # status 99
    ignored: int = 0      # status 98
    total: int = 0


class Totals(BaseModel):
    languages: int = 0
    books: int = 0
    texts: int = 0
    words: int = 0
    terms: int = 0


class LanguageStat(BaseModel):
    language_id: Optional[int] = None
    language_name: str
    books: int = 0
    texts: int = 0
    words: int = 0
    terms: StatusBreakdown = Field(default_factory=StatusBreakdown)


class StatsOut(BaseModel):
    totals: Totals = Field(default_factory=Totals)
    terms: StatusBreakdown = Field(default_factory=StatusBreakdown)
    languages: List[LanguageStat] = Field(default_factory=list)
