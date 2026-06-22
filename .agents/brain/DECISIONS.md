# DECISIONS — the "why"

> Repo: https://github.com/sadeqnotion1/lingua

- **D1 — FastAPI over Flask.** Lute v3 is Flask + server-rendered templates. We want a
  separate SPA, so an API-first framework fits better. Domain logic still ports over.
- **D2 — React + Vite + TypeScript SPA.** Fast dev server, typed client, clean split
  from the backend. Dev proxy `:5173 → :8000`; prod served from `frontend/dist`.
- **D3 — SQLite, local-first.** Matches Lute's model; zero-config; file at
  `backend/data/lingua.db`.
- **D4 — Domain modeled on Lute v3.** Language → Book → Text → Term, parent terms via
  `Term.parent_id`, numeric `status` (0-99 familiarity).
- **D5 — `.agents/` location.** Holds `agent.md`, the knowledge graph (`.agents/graph/`),
  and this brain (`.agents/brain/`).
  ⚠️ **NEEDS A DECISION:** originally declared "gitignored, local-only, not committed" —
  but the folder is currently committed to the public repo (that's how a fresh chat can
  pull it from GitHub). Pick ONE and update this line:
    - **(a) Keep it tracked** — chats pull context straight from the repo. Make sure no
      secrets ever land in `.agents/`.
    - **(b) Re-ignore it** — add `.agents/` back to `.gitignore` and `git rm -r --cached .agents`;
      then context must be attached/pasted each chat.
- **D6 — Terms are case-insensitive.** A term's identity is `(language_id, text_lower)`;
  "The" and "the" are the same term. Enforced at the DB level by `UniqueConstraint
  uq_term_lang_lower`; `seed.py` (and future ingest) must set `text_lower = text.lower()`.
  (Session 2026-06-21, M1.)
- **D7 — Start language = English; no extra Book/Text fields yet.** Seed ships English only.
  Cover image / source URL / author stay deferred until a feature needs them — don't add
  speculative columns. (Session 2026-06-21, M1.)

- **D8 — Duplicate book imports raise 409 Conflict.** When importing a book, if a book with the same title already exists in the target language, we return a `409 Conflict` containing the existing book metadata. This avoids accidental duplicate shelf-cards. (Session 2026-06-21, M2.)
- **D9 — Single local User model + seeded user.** A single local user row in the SQLite database backs the Account page details. Profile settings remain read-only until authentication/editing is added. (Session 2026-06-22, M7.)
- **D10 (M8) — Dashboard is the landing route.** `/` redirects to `/dashboard`; unknown routes also redirect there. Library remains at `/library`.
- **D11 (M8) — Settings preferences stored in a new `app_settings` key/value table.** The Setting model is used rather than widening the single-row User. Theme + accent are persisted server-side AND in localStorage (instant apply, no theme flash). Settings that are not supported (e.g. password, billing, billing plans) are clearly labeled as "Not available in this build" rather than being faked.

---
