"""Domain/business logic ported from Lute v3.

Keep web-framework code out of here so the logic stays reusable and testable.
Planned modules:
  - parser.py   : split text into words/sentences (Lute-style tokenization)
  - terms.py    : create/update terms, parent-term resolution, status changes
  - reading.py  : render a text with per-word known/learning status
  - srs.py      : spaced-repetition review scheduling
"""
