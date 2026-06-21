# STATE — where we are right now

> Single source of truth. If this disagrees with the real code, the **code wins** —
> tell me and I fix the brain. Repo: https://github.com/sadeqnotion1/lingua

**Status (one-liner):** M0–M4 done — Library shelves, imports, dynamic styles, and tokenizer are complete and verified. Next up: **M5 — Reader**.

| Part | Status | Notes |
|---|---|---|
| Scaffold & wiring | ✅ | FastAPI + SQLAlchemy + SQLite backend, React+Vite+TS SPA. Boots, `/api/health` works. |
| Knowledge graph (`.agents/graph/`) | ✅ | ~52–53 nodes / ~58–70 edges. Regenerate via `render_graph.py`. |
| Brain (`.agents/brain/`) | ✅ | This system. |
| M1 Data layer (models/init_db/seed) | ✅ | Case-insensitive terms enforced (`UniqueConstraint` on `language_id`+`text_lower`); seed = 1 lang / 1 book / 2 texts / 5 terms (incl. parent-term link); `pytest` green (3 tests). |
| M2 Library API | ✅ | Endpoints for listing books grouped by language and importing books implemented; duplicate checks (raise 409 Conflict + return existing) in place; 9 unit tests green. |
| M3 Library UI (shelves + import bar) | ✅ | Matches screenshot 1. Polished with font-smoothing, focus rings, hover-zoom covers, and reduced motion paths. |
| M4 Tokenizer (`services/parser.py`) | ✅ | Lossless, Lute-style alternating runs parser implemented and verified with 22 unit tests. |
| M5 Reader | ⬜ | Word-by-word render + status colors. **← NEXT** |
| M6 Terms (status, parent, translation) | ⬜ | |
| M7 Account page | ⬜ | Matches screenshot 2. |
| M8 Polish (stats, search, settings) | ⬜ | |

## Open decisions / questions waiting on you
- **D5 (still open):** keep `.agents/` tracked in the public repo, or re-ignore it?

## Known risks / watch-items
- `.agents/` is currently committed to the public repo (see DECISIONS D5) — confirm that's intended.
- `.agents/agents.md` (orientation file) returned 404 when pulled from GitHub — confirm it exists / correct filename so cold-starts can read it.
- Path spelling standardized to `.agents/` (older notes said `.agent/`).
