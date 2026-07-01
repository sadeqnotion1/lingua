# STATE — where we are right now

> Single source of truth. If this disagrees with the real code, the **code wins** —
> tell me and I fix the brain. Repo: https://github.com/sadeqnotion1/lingua

**Status (one-liner):** M9 (FTS5 Search) ✅ **verified live** — Global search migrated to SQLite FTS5 index (trigram tokenizer + sync triggers) with bm25 ranking and short-query/fallback LIKE support. M0–M9 complete; **no active milestone** — next chat selects + scopes the first Backlog item as M10 (see NEXT.md / ROADMAP.md).
  - Live smoke-test (2026-06-22): `/dashboard`, `/search`, `/settings` load; Dashboard totals correct (1 lang / 1 book / 2 pages / 21 words / 5 terms) + vocab status bar/legend; search query "sample" returns 3 hits across Books/Pages/Terms and page hits open the reader (`/read/1`); profile + theme (dark/light/system) + accent + per-language (`word_chars`/RTL/romanization) all persist; `app_settings` table auto-created on boot (`init_db`).
Next up: Pick + scope the next milestone (M10) from Backlog, then build it. See NEXT.md.

| Part | Status | Notes |
|---|---|---|
| Scaffold & wiring | ✅ | FastAPI + SQLAlchemy + SQLite backend, React+Vite+TS SPA. Boots, `/api/health` works. |
| Knowledge graph (`.agents/graph/`) | ✅ | ~52–53 nodes / ~58–70 edges. Regenerate via `render_graph.py`. Unchanged this session (no code change). |
| Brain (`.agents/brain/`) | ✅ | This system. |
| M1 Data layer (models/init_db/seed) | ✅ | Case-insensitive terms enforced (`UniqueConstraint` on `language_id`+`text_lower`); seed = 1 lang / 1 book / 2 texts / 5 terms (incl. parent-term link); `pytest` green (3 tests). |
| M2 Library API | ✅ | Endpoints for listing books grouped by language and importing books implemented; duplicate checks (raise 409 Conflict + return existing) in place; 9 unit tests green. |
| M3 Library UI (shelves + import bar) | ✅ | Matches screenshot 1. Polished with font-smoothing, focus rings, hover-zoom covers, and reduced motion paths. |
| M4 Tokenizer (`services/parser.py`) | ✅ | Lossless, Lute-style alternating runs parser implemented and verified with 22 unit tests. |
| M5 Reader | ✅ | Word-by-word render + status colors and page navigation complete and verified. |
| M6 Terms (status, parent, translation) | ✅ | Click-to-define drawer, status selection, translation/parent persistence. Complete & verified. |
| M7 Account page | ✅ | Matches screenshot 2. Read-only profile backed by local User row. |
| M8 Polish (stats, search, settings) | ✅ verified | Dashboard, global search, settings. **Live smoke-test passed 2026-06-22** (uvicorn+vite) — all acceptance criteria green. |
| M9 FTS5 Search-at-scale | ✅ verified | FTS5 external-content virtual tables + trigram substring matching + automated sync triggers. **Live smoke-test passed 2026-06-22**. |

## Open decisions / questions waiting on you
- **Next milestone (M10):** choose the next Backlog item to build. See NEXT.md for candidates.

## Resolved this session
- **D5 → resolved (D13):** keep `.agents/` **tracked** in the public repo (Option A); never commit secrets/API keys.
- **`agents.md` 404 → resolved (D14):** canonical orientation file is uppercase `.agents/AGENTS.md`; the lowercase path 404s on case-sensitive GitHub/Linux. Boot sequence references `AGENTS.md`.

## Known risks / watch-items
- Keep secrets/tokens/API keys **out** of the now-public tracked `.agents/` folder.
- Global search is currently **in-memory**; migrate to SQLite FTS5 before libraries get large (Backlog front-runner).
