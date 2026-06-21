# STATE — where we are right now

> Single source of truth. If this disagrees with the real code, the **code wins** —
> tell me and I fix the brain. Repo: https://github.com/sadeqnotion1/lingua

| Part | Status | Notes |
|---|---|---|
| Scaffold & wiring | ✅ | FastAPI + SQLAlchemy + SQLite backend, React+Vite+TS SPA. Boots, `/api/health` works. |
| Knowledge graph (`.agents/graph/`) | ✅ | ~52–53 nodes / ~58–70 edges. Regenerate via `build_graph_html.py`. |
| Brain (`.agents/brain/`) | ✅ | This system. |
| M1 Data layer (models/init_db/seed) | ⬜ | Models exist as classes; need verified `init_db`, real seed data, a smoke test. |
| M2 Library API | ⬜ | Routers are stubs. |
| M3 Library UI (shelves + import bar) | ⬜ | Matches screenshot 1. |
| M4 Tokenizer (`services/parser.py`) | ⬜ | `tokenize()` raises NotImplementedError. CORE. |
| M5 Reader | ⬜ | Word-by-word render + status colors. |
| M6 Terms (status, parent, translation) | ⬜ | |
| M7 Account page | ⬜ | Matches screenshot 2. |
| M8 Polish (stats, search, settings) | ⬜ | |

## Open decisions / questions waiting on you
- None right now. (When I need a product decision I'll list it here and in `NEXT.md`.)

## Known risks / watch-items
- `.agents/` is currently committed to the public repo (see DECISIONS D5) — confirm that's intended.
- Path spelling standardized to `.agents/` (older notes said `.agent/`).
