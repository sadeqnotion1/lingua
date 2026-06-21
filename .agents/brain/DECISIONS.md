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

---
