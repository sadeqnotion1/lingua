# NEXT — the handoff card
_This is the FIRST thing to act on in a new chat (after the START prompt).
The AI rewrites this at the end of every session._

> Repo: https://github.com/sadeqnotion1/lingua

## ➡️ The one next task
**M6 — Terms.** Implement term interaction inside the reader screen. This includes clicking any word token to open a term drawer/modal, editing the translation, updating the familiarity status (0-5 or 98/99), linking a parent term, and persisting updates via a new backend API endpoint.

## Start the next chat with this
> "Let's build M6 (Terms). Pull the backend term routers and database models, and the frontend reader page so we can wire up the click-to-define lookup pane, status editing, and translation persistence."

## What to paste / give me at the start
Pull these from the repo:
1. `backend/app/routers/` (specifically if there's a term or dictionary router)
2. `backend/app/models/term.py` (the database models for terms)
3. `frontend/src/pages/Reader.tsx` (the reader screen where we need to capture click events and show the term drawer)

## Decisions I need from you for M6
- UI Design: Should the lookup form be a sliding side pane (drawer) next to the text or a floating modal?
- API endpoints: Should we introduce a unified endpoint like `POST /api/terms` that handles both creation and updates (upsert) for terms?

## Definition of done for this task
- Clicking a word token in `Reader.tsx` opens a term lookup/edit interface showing the word, its current status, translation, and parent term link.
- User can save status changes (1–5, 98, or null/0) and translations. Saving persists the changes to the database and updates the token color in the reader view dynamically without full page reload.
- Full type-safety across backend schemas and frontend API client.
- Fully verified locally with pytest and TypeScript checks passing.
