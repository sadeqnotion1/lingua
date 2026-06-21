# NEXT — the handoff card
_This is the FIRST thing to act on in a new chat (after the START prompt).
The AI rewrites this at the end of every session._

> Repo: https://github.com/sadeqnotion1/lingua

## ➡️ The one next task
**M3 — Library UI.** Build the Library screen in the React frontend, rendering lesson/book cards grouped by language shelves, and implementing the import bar at the top to call `POST /api/library/import`.

## Start the next chat with this
> "Let's do M3 (Library UI). Pull the frontend source files, routers, and client code from the repo (https://github.com/sadeqnotion1/lingua), or I'll paste them below: …"

## What to paste / give me at the start
Pull these from the repo:
1. `frontend/src/pages/Library.tsx` (or the library page file)
2. `frontend/src/components/` files relating to shelves or cards (e.g. `ShelfRow.tsx`, `LessonCard.tsx`)
3. `frontend/src/api/client.ts`

## Decisions I need from you for M3
- Any design or styling preferences for the shelves/cards layout? (Recommended: minimalist layout mirroring the provided layout screenshots).

## Definition of done for this task
- Library page displays shelves grouped by language, with each book rendered as a lesson card showing title, progress, and metadata.
- Import bar allows inputting title, selecting language, and pasting text to import a book, updating the UI shelves live.
- Frontend builds successfully without TypeScript or bundler errors.
- I update `STATE.md` (M3 → ✅), append to `SESSION_LOG.md`, and set `NEXT.md` to M4.
