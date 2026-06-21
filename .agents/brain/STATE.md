# STATE — where we are right now

_Last updated: 2026-06-21 (Session 1). Update this at the end of every session._

## One-line status

Scaffold + knowledge graph + brain are in place. **Nothing is implemented yet** —
all handlers and the tokenizer are stubs. Next up: **M1 — Data layer**.

## Current milestone

**M1 — Data layer** (see `ROADMAP.md`). Not started.

## Per-part status

Legend: ⬜ not started · 🟨 in progress · ✅ done · ⛔ blocked

| Part | Status | Notes |
|---|---|---|
| Scaffold & wiring | ✅ | FastAPI + SQLAlchemy + SQLite backend, React+Vite+TS SPA. Boots, `/api/health` works. |
| Knowledge graph (`.agent/graph/`) | ✅ | 53 nodes / 70 edges. Regenerate via `build_graph_html.py`. |
| Brain (`.agent/brain/`) | ✅ | This system. |
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

- The Vite dev-proxy ↔ backend-serves-dist circular coupling (see graph). Keep both
  ends in sync when changing how the app is served.
- `api/client.ts` paths must stay aligned with router paths (no compile-time check).
