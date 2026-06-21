# agent.md — LinguaRead

> Local orientation file for CLI AI coding agents (Codex, Claude Code, Cursor, etc.).
> **Location:** `.agents/agent.md`. Repo: https://github.com/sadeqnotion1/lingua
>
> **Context sources (in priority order):**
> 1. Files attached/pasted into the chat.
> 2. The repo on GitHub — pull the `.agents/` folder and source from
>    https://github.com/sadeqnotion1/lingua
>
> I cannot read your local disk. If a file isn't attached and isn't on GitHub,
> I'll ask for it by name.
>
> Read this first. It tells you what the project is, how it's wired, where things
> live, how to run it, and the conventions to respect. A machine-readable
> knowledge graph of the whole repo lives in **`.agents/graph/`** — query it
> before re-reading source.

## What this is
LinguaRead is a self-hosted, LingQ-style **language-learning reader**. You import
texts in a foreign language, read them, and track each word/term's familiarity as
you go. The domain model is ported from [Lute v3](https://github.com/LuteOrg/lute-v3)
(Language → Book → Text → Term, with parent-terms and numeric status levels), but
the architecture is **API-first**, not Lute's server-rendered Flask templates.

## Stack & layout
- `backend/` — FastAPI + SQLAlchemy + SQLite. Everything that isn't UI.
- `frontend/` — React + Vite + TypeScript SPA. The user-facing app only.
- Run wrappers `run.sh` / `run.bat` launch `backend/main.py`, which starts the API
  and serves the built SPA (`frontend/dist`).

```
lingua/
  .agents/                 # local agent context (see DECISIONS D5 re: tracking)
    agent.md              # <- you are here
    brain/                # shared memory between you and the AI
    graph/                # repo knowledge graph
      graph.json          # machine-readable graph
      GRAPH_REPORT.md     # human digest
      graph.html          # interactive viewer (self-contained)
      build_graph_html.py # regenerates graph.html from graph.json
    skills/               # reusable skill packs
  run.sh / run.bat        # single launch command -> backend/main.py
  README.md               # human START_HERE
  backend/
    main.py               # entry point; sets sys.path, runs uvicorn
    requirements.txt
    app/
      config.py           # Settings (host, port, db url, frontend_dist)
      database.py         # engine, SessionLocal, Base, init_db, get_db
      main.py             # FastAPI app: CORS, startup, routers, static mount
      models/             # Language, Book, Text, Term (SQLAlchemy)
      schemas/            # Pydantic models (stubs)
      services/parser.py  # tokenize() -> NotImplementedError (CORE TODO)
      routers/            # library, reading, terms, account (HTTP endpoints)
      static/             # optional server-side static
    data/                 # SQLite db lives here (gitignored)
    tools/seed.py         # dev seed data
    tests/test_health.py
    docs/
      ARCHITECTURE.md     # the "why" behind decisions
      CHANGELOG.md
  frontend/
    package.json, vite.config.ts, tsconfig.json, index.html
    src/
      main.tsx, App.tsx   # BrowserRouter + routes
      api/client.ts       # the ONLY bridge to the backend (HTTP)
      components/         # Sidebar, ShelfRow, LessonCard
      pages/              # Library, Reader, Account
      styles/global.css
```

## Run
```bash
./run.sh            # macOS/Linux (chmod +x run.sh first time)
run.bat             # Windows
# then open http://127.0.0.1:8000
```

## Quality gate (before declaring a task done)
1. `python -m py_compile $(git ls-files 'backend/**/*.py')` — backend compiles.
2. `pytest backend/tests` — tests pass (`test_health` at minimum).
3. `cd frontend && npm run build` — SPA builds (if you touched frontend).
4. App boots via `./run.sh` and `GET /api/health` returns OK.
5. If structure changed, update `.agents/graph/graph.json` and regenerate
   `graph.html`; confirm `graph.json` is valid JSON and every edge endpoint is a
   real node id.

## Pointers
- Repo knowledge graph: `.agents/graph/` (`graph.json`, `GRAPH_REPORT.md`, `graph.html`)
- Decisions & rationale: `backend/docs/ARCHITECTURE.md`
- Change log: `backend/docs/CHANGELOG.md`
- Upstream domain reference: Lute v3 — https://github.com/LuteOrg/lute-v3
