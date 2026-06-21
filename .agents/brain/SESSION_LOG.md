# SESSION LOG — append-only
> Newest entries at the top. Repo: https://github.com/sadeqnotion1/lingua

## 2026-06-21
- Completed **M1 — Data layer** by applying fixes from `fixes/14356212026/APPLY.md`.
- Updated `backend/app/models/term.py` to enforce a case-insensitive `UniqueConstraint` on language and terms.
- Overwrote `backend/tools/seed.py` to seed sample data (1 language, 1 book, 2 texts, 5 terms).
- Added `backend/tests/conftest.py` and `backend/tests/test_models.py` to verify DB schema and constraints.
- Verified test suite passes successfully (3 passed tests total).
- Staged, committed, and pushed code changes. Next task is **M2 — Library API**.

## 2026-06-21
- Reworked the brain prompts so context can come from the **GitHub repo**
  (https://github.com/sadeqnotion1/lingua) in addition to attached/pasted files.
- Standardized path spelling `.agent/` → `.agents/` across brain files.
- Flagged DECISIONS D5: `.agents/` is committed to the public repo despite the
  old "local-only" note — needs a decision (track vs. gitignore).
- No code changes. Next task remains **M1 — Data layer**.
