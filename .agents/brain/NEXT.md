# NEXT — the handoff card
_This is the FIRST thing to act on in a new chat (after the START prompt).
The AI rewrites this at the end of every session._

> Repo: https://github.com/sadeqnotion1/lingua

## ➡️ The one next task
**M1 — Data layer.** Verify/finish the models, `init_db()`, and `seed.py`, then
prove it works by seeding the DB and querying it back.

## Start the next chat with this
> "Let's do M1 (Data layer). Pull the current backend model files and seed.py from
> the repo (https://github.com/sadeqnotion1/lingua), or I'll paste them below: …"

## What to paste / give me at the start
Pull these from the repo if committed; otherwise paste their contents
(I can't read your local disk):
1. `backend/app/models/__init__.py`
2. `backend/app/models/language.py`, `book.py`, `text.py`, `term.py`
3. `backend/app/database.py`
4. `backend/tools/seed.py`
(If they're unchanged from the scaffold I generated, just say "unchanged" and I'll
work from the scaffold version.)

## Decisions I need from you for M1
- Which language(s) do you want to start with (e.g. Spanish, German)?
- Should terms be case-insensitive (treat "The"/"the" as one term)? (Recommended: yes.)
- Any extra fields on Book/Text you want now (cover image, source URL, author)?

## Definition of done for this task
- `python backend/tools/seed.py` creates `backend/data/lingua.db` with sample rows.
- A query returns the seeded language/book/text/terms.
- `pytest backend/tests` passes.
- I update `STATE.md` (M1 → ✅), append to `SESSION_LOG.md`, and set `NEXT.md` to M2.
