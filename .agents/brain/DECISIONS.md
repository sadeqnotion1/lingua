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
  ✅ **RESOLVED (see D13):** keep it **tracked** in the public repo (Option a) so fresh
  chats can pull context straight from GitHub. Never commit secrets into `.agents/`.
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
- **D12 (M8) — Dashboard word counts are memoized.** Counts are memoized per-text using a content fingerprint (MD5 hash of word_chars + content). The cache invalidates automatically if the text's contents or the language's word characters change. Full-text search via SQLite FTS5 is deferred until the library size warrants virtual table schema migrations.
- **D13 — `.agents/` stays tracked in the public repo (resolves D5 → option a).** Fresh chats pull full context directly from GitHub commits, keeping cold-starts seamless. Hard rule: never commit secrets, tokens, or personal API keys into `.agents/`. (Session 2026-06-22.)
- **D14 — Canonical orientation filename is uppercase `.agents/AGENTS.md`.** The lowercase `.agents/agents.md` returns 404 on case-sensitive hosts (GitHub/Linux), which broke cold-start fetches. The boot sequence and START prompt must reference `AGENTS.md`. (Session 2026-06-22.)

---
