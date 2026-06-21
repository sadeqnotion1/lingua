# DECISIONS (lightweight ADR log)

Why we chose things, so we don't re-argue them. Add an entry when a real choice is made.

---

- **D1 — FastAPI over Flask.** Lute v3 is Flask + server-rendered templates. We want a
  separate SPA, so an API-first framework fits better. Domain logic still ports over.
- **D2 — React + Vite + TypeScript SPA.** Fast dev server, typed client, clean split
  from the backend. Dev proxy `:5173 → :8000`; prod served from `frontend/dist`.
- **D3 — SQLite, local-first.** Matches Lute's model; zero-config; file at
  `backend/data/lingua.db`.
- **D4 — Domain modeled on Lute v3.** Language → Book → Text → Term, parent terms via
  `Term.parent_id`, numeric `status` (0-99 familiarity).
- **D5 — `.agent/` is local-only (gitignored).** Holds `agent.md`, the knowledge graph
  (`.agent/graph/`), and this brain (`.agent/brain/`). Not committed to the repo.

---

_(template)_
- **Dn — <decision>.** <why>.
