# NEXT — the handoff card
_This is the FIRST thing to act on in a new chat (after the START prompt).
The AI rewrites this at the end of every session._

> Repo: https://github.com/sadeqnotion1/lingua

## ➡️ The one next task
**M2 — Library API.** Implement HTTP endpoints in the backend to back the Library screen:
list books grouped by language, import a text/book, and wire DB sessions with proper
Pydantic schemas. Replace the router stubs with real, tested endpoints.

## Start the next chat with this
> "Let's do M2 (Library API). Pull the current backend router/schema/main files from the
> repo (https://github.com/sadeqnotion1/lingua), or I'll paste them below: …"

## What to paste / give me at the start
Pull these from the repo if committed; otherwise paste their contents:
1. `backend/app/routers/library.py` (or the library router file) — or say "still a stub".
2. `backend/app/schemas/` files (if any exist yet).
3. `backend/app/main.py` (to see how routers are mounted).

## Decisions I need from you for M2
- Duplicate book imports → **raise error**, **allow duplicates**, or **append** to existing? (Recommended: raise + return existing.)

## Definition of done for this task
- `GET /api/library/books` returns seeded/imported books grouped by language.
- `POST /api/library/import` accepts title, language (name or id), and raw text, creating Book + Text rows.
- Endpoints covered by `pytest` (use the existing in-memory fixture in `backend/tests/conftest.py`).
- I update `STATE.md` (M2 → ✅), append to `SESSION_LOG.md`, and set `NEXT.md` to M3.
