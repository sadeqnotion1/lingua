# ROADMAP — ordered build plan
Build in order. Each milestone is small enough to finish in roughly one chat.
Don't start the next one until the current one's acceptance criteria pass.

> Repo: https://github.com/sadeqnotion1/lingua

---

- **M0 — Scaffold & wiring** ✅ — FastAPI + SQLAlchemy + SQLite backend, React+Vite+TS SPA; boots, `/api/health` OK.
- **M1 — Data layer** ✅ — models, `init_db()`, `seed.py`; seed + query back; case-insensitive terms; `pytest` passes.
- **M2 — Library API** ✅ — real endpoints for books/texts (replace router stubs).
- **M3 — Library UI** ✅ — shelves + search/import bar (matches screenshot 1). Polished with hover zoom and clean focus rings.
- **M4 — Tokenizer** ✅ — implement config-driven parser/tokenizer in `services/parser.py` (Lute-style tokenization).
- **M5 — Reader** ✅ — word-by-word render + status colors and page navigation.
- **M6 — Terms** ✅ — status, parent term, translation.
- **M7 — Account page** ✅ — matches screenshot 2. Read-only profile backed by local DB-backed User.
- **M8 — Polish** ✅ **verified** — stats, search, settings. Live smoke-test passed 2026-06-22 (uvicorn+vite).
- **M9 — SQLite FTS5 Search-at-scale** ✅ — Migrated global search from in-memory scans to SQLite FTS5 index (trigram tokenizer + sync triggers) with automated backfill.
- **M10 — TBD** ⏳ — **pick from Backlog**. Scope via PLAYBOOK feature-intake before building. See NEXT.md.

## Backlog / maybe-later
- [ ] Audio + sentence playback
- [ ] Dictionary / translation API integration
- [ ] SRS review queue
- [ ] Export of known terms
- [ ] Multi-user / auth
- [ ] Deployment packaging
