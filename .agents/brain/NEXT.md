# NEXT — the handoff card
_This is the FIRST thing to act on in a new chat (after the START prompt).
The AI rewrites this at the end of every session._

> Repo: https://github.com/sadeqnotion1/lingua

## ➡️ The one next task
**M5 — Reader.** Implement the reading interface that renders text word-by-word, displaying words colored by their learning status (new vs. known/learning) and integrating the tokenizer service `backend/app/services/parser.py`.

## Start the next chat with this
> "Let's build M5 (Reader). Pull the reader page component (frontend/src/pages/Reader.tsx), the backend router/endpoints layout, and any relevant backend services so we can wire up the page rendering and status coloring."

## What to paste / give me at the start
Pull these from the repo:
1. `backend/app/routers/` (specifically if there's a text/reader router)
2. `frontend/src/pages/Reader.tsx` (or the router/App.tsx wiring)
3. Any existing API schemas for reading a text or page

## Decisions I need from you for M5
- Define the API structure: Should `GET /api/texts/{text_id}/reader` return the entire token list enriched with term status, or does the frontend match terms client-side?
- Agree on the color palette for term statuses (0-5 or 0-99).

## Definition of done for this task
- Backend endpoint created to serve a text/book page as a sequence of token items (each carrying its text, `is_word` flag, and matched term status if it exists in the database).
- Frontend `Reader.tsx` displays the book/text word-by-word, displaying non-words as normal text and word runs styled according to their familiarity level (e.g., new words highlighted in light blue/yellow).
- Navigation controls (next/prev page, back to library shelf) functional.
- Fully verified locally with no TypeScript/bundler or backend errors.
