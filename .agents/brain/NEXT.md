# NEXT — the handoff card
_This is the FIRST thing to act on in a new chat (after the START prompt).
The AI rewrites this at the end of every session._

> Repo: https://github.com/sadeqnotion1/lingua

## ➡️ The one next task
**M2 — Library API.** Implement HTTP endpoints in the backend to back the Library screen, including listing books grouped by language, importing a text/book, and wiring database sessions with proper Pydantic schemas.

## Start the next chat with this
> "Let's do M2 (Library API). Pull the current backend router files and library endpoint code from the repo (https://github.com/sadeqnotion1/lingua), or I'll paste them below: …"

## What to paste / give me at the start
Pull these from the repo if committed; otherwise paste their contents:
1. `backend/app/routers/library.py` (or the library router file)
2. `backend/app/schemas/` files
3. `backend/app/main.py` (to see router mounting)

## Decisions I need from you for M2
- How do we handle duplicate book imports? (e.g., raise error, allow duplicates, or append?)

## Definition of done for this task
- `GET /api/library/books` successfully returns seeded/imported books grouped by language.
- `POST /api/library/import` accepts title, language name/ID, and raw text, creating corresponding Book + Text rows in the DB.
- API is fully tested and verified with pytest.
- I update `STATE.md` (M2 → ✅), append to `SESSION_LOG.md`, and set `NEXT.md` to M3.
