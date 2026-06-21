# agent.md — LinguaRead

> Local orientation file for CLI AI coding agents (Codex, Claude Code, Cursor, etc.).
> **Location:** `.agent/agent.md`. The `.agent/` folder is **gitignored** — it is
> local working context, not committed to the repo.
> Repo: https://github.com/sadeqnotion1/lingua
>
> Read this first. It tells you what the project is, how it's wired, where things
> live, how to run it, and the conventions to respect. A machine-readable
> knowledge graph of the whole repo lives in **`.agent/graph/`** — query it
> before re-reading source.

## What this is

LinguaRead is a self-hosted, LingQ-style **language-learning reader**. You import
texts in a foreign language, read them, and track each word/term's familiarity as
you go. The domain model is ported from [Lute v3](https://github.com/LuteOrg/lute-v3)
(Language → Book → Text → Term, with parent-terms and numeric status levels), but
the architecture is **API-first**, not Lute's server-rendered Flask templates.

This repository is currently a **scaffold**: the structure, wiring, and contracts
are in place; most handler bodies and the tokenizer are intentional stubs. Your
job as an agent is usually to implement those stubs without breaking the wiring.

## Stack

| Layer | Choice | Notes |
|---|---|---|
| Backend | **FastAPI** + **Uvicorn** | API-first; chosen over Lute's Flask because a separate SPA wants a clean JSON API. |
| ORM | **SQLAlchemy 2.0** | Declarative models under `backend/app/models/`. |
| Database | **SQLite** | Local file at `backend/data/lingua.db`. Matches Lute's local-first model. |
| Frontend | **React + Vite + TypeScript** | SPA under `frontend/`. |
| Validation | **Pydantic 2** | Request/response schemas (largely stubbed in `backend/app/schemas/`). |

## Directory map

```
lingua/
  .agent/                 # gitignored local agent context (NOT committed)
    agent.md              # <- you are here
    graph/                # repo knowledge graph (see "The knowledge graph")
      graph.json          # machine-readable graph
      GRAPH_REPORT.md      # human digest
      graph.html          # interactive viewer (self-contained)
      build_graph_html.py  # regenerates graph.html from graph.json
  run.sh / run.bat        # single launch command -> backend/main.py
  README.md               # human START_HERE
  backend/
    main.py               # entry point; sets sys.path, runs uvicorn
    requirements.txt
    app/
      config.py           # Settings (host, port, db url, frontend_dist)
      database.py          # engine, SessionLocal, Base, init_db, get_db
      main.py              # FastAPI app: CORS, startup, routers, static mount
      models/              # Language, Book, Text, Term (SQLAlchemy)
      schemas/             # Pydantic models (stubs)
      services/parser.py   # tokenize() -> NotImplementedError (CORE TODO)
      routers/             # library, reading, terms, account (HTTP endpoints)
      static/              # optional server-side static
    data/                  # SQLite db lives here (gitignored)
    tools/seed.py          # dev seed data
    tests/test_health.py
    docs/
      ARCHITECTURE.md      # the "why" behind decisions
      CHANGELOG.md
  frontend/
    package.json, vite.config.ts, tsconfig.json, index.html
    src/
      main.tsx, App.tsx    # BrowserRouter + routes
      api/client.ts        # the ONLY bridge to the backend (HTTP)
      components/          # Sidebar, ShelfRow, LessonCard
      pages/               # Library, Reader, Account
      styles/global.css
```

> Note: the graph and this file live under `.agent/` (local only). The committed
> repo is everything else. Don't move graph artifacts into the tracked tree unless
> you intend to commit them.

## How to run

- **One command from repo root:** `./run.sh` (macOS/Linux) or `run.bat` (Windows).
  It launches the FastAPI backend on `http://127.0.0.1:8000`.
- **Frontend dev (hot reload):** `cd frontend && npm install && npm run dev` →
  serves on `:5173` and proxies `/api` to `:8000` (see `vite.config.ts`).
- **Production-style:** `cd frontend && npm run build` produces `frontend/dist`,
  which the backend serves as static files (see `app/main.py` static mount).
- **Health check:** `GET /api/health`.
- **Seed dev data:** `python backend/tools/seed.py`.
- **Tests:** `pytest backend/tests`.

## How requests flow (mental model)

```
React page -> api/client.ts (fetch) --HTTP /api/*--> FastAPI app.main:app
   -> router (library|reading|terms|account) -> get_db session -> SQLAlchemy models -> SQLite
```

In dev the hop is Vite's proxy (`:5173` -> `:8000`); in prod the SPA is served by
the backend itself, so it's same-origin.

## The knowledge graph (use it)

A Graphify knowledge graph of the whole repo lives in **`.agent/graph/`** so you
don't have to re-derive structure by grepping every file:

- **`.agent/graph/graph.json`** — the graph (53 nodes, 70 edges). Each node:
  `id, label, type, location, summary, community, degree`. Each edge:
  `source, target, type, confidence, evidence`. `confidence` is `EXTRACTED`
  (read from code), `INFERRED` (deduced from naming/usage), or `AMBIGUOUS`
  (intended, not yet wired).
- **`.agent/graph/GRAPH_REPORT.md`** — human digest: god nodes, communities,
  surprising couplings, suggested questions, confidence summary.
- **`.agent/graph/graph.html`** — open in a browser for an interactive view.
- **Regenerate** the HTML after editing the JSON:
  `python .agent/graph/build_graph_html.py`.
  If you change the codebase structure, update `.agent/graph/graph.json` to match.

### How to use the graph in a task

1. **Before editing**, query the graph for the node(s) you're touching and their
   edges to learn the blast radius and contracts.
2. **Prefer the graph over full-repo grep** for "what depends on X?" questions.
3. **After structural changes**, update `graph.json` (add/remove nodes & edges,
   keep `meta.node_count` / `meta.edge_count` accurate, give every edge a
   `confidence` + `evidence`) and regenerate `graph.html`.

### Quick way to query the graph

```bash
# what connects to the FastAPI app?
jq '.edges[] | select(.source=="app.main:app" or .target=="app.main:app")' .agent/graph/graph.json
# everything in one community
jq '.nodes[] | select(.community=="domain")' .agent/graph/graph.json
# all the inferred / not-yet-solid edges
jq '.edges[] | select(.confidence!="EXTRACTED")' .agent/graph/graph.json
# list communities
jq '.communities[] | {id, name}' .agent/graph/graph.json
```

### Central nodes (high blast radius — change carefully)

| Node | Degree | Why it matters |
|---|---|---|
| `app.main:app` | 11 | FastAPI instance: CORS, startup `init_db`, all routers, `/api/health`, serves SPA build. |
| `app.models` | 6 | Imports all ORM models so they register on `Base.metadata`. |
| `api.client:api` | 6 | The only UI->backend bridge; every page call goes through it. |
| `frontend.App` | 5 | SPA routing hub. |
| `db.tables:terms` | 5 | Most-connected table; FKs + self-referential `parent_id`. |
| `app.database:Base` | 5 | Declarative base all four models inherit. |

### Cross-layer couplings to watch

1. `vite.config.ts` hard-codes the backend `127.0.0.1:8000` for its dev proxy.
2. The backend serves `frontend/dist`. (1)+(2) form a **circular cross-layer
   dependency** — if you change how the app is served, fix both ends.
3. `api/client.ts` depends on backend route contracts over HTTP; nothing enforces
   this at compile time, so keep client paths and router paths in sync.
4. `Term.parent_id` is a self-reference (parent terms) — the only recursive
   relationship in the schema.

## Conventions & rules for agents

- **API prefix:** every backend route is mounted under `/api` (see `app/main.py`).
  Frontend calls must include it; keep `api/client.ts` paths aligned with routers.
- **DB sessions:** use the `get_db` dependency in routers; don't open ad-hoc
  sessions. Models inherit from `app.database:Base`.
- **New models:** define under `backend/app/models/`, then make sure they're
  imported by `app/models/__init__.py` so they register on `Base.metadata` before
  `init_db` runs.
- **Term status:** integer familiarity level (Lute convention, 0-99); don't turn
  it into an enum/string without updating the schema and graph.
- **Keep the tracked root clean:** committed root holds only `run.*`, `README.md`,
  `.gitignore`, `backend/`, `frontend/`. Local agent context stays in `.agent/`.
  Put docs in `backend/docs/`, tooling in `backend/tools/`.
- **Stubs first:** the highest-value TODOs are `services/parser.py:tokenize()`
  and the router handler bodies. Implement these before adding new surface area.
- **Don't commit the DB or `.agent/`:** `backend/data/*.db` and `.agent/` are
  gitignored.

## Definition of done (quality gate)

Before declaring a change complete:

1. `python -m py_compile $(git ls-files 'backend/**/*.py')` — backend compiles.
2. `pytest backend/tests` — tests pass (`test_health` at minimum).
3. `cd frontend && npm run build` — SPA builds (if you touched frontend).
4. App boots via `./run.sh` and `GET /api/health` returns OK.
5. If structure changed, update `.agent/graph/graph.json` and regenerate
   `graph.html`; confirm `graph.json` is valid JSON and every edge endpoint is a
   real node id.

## Pointers

- Repo knowledge graph: `.agent/graph/` (`graph.json`, `GRAPH_REPORT.md`, `graph.html`)
- Decisions & rationale: `backend/docs/ARCHITECTURE.md`
- Change log: `backend/docs/CHANGELOG.md`
- Upstream domain reference: Lute v3 — https://github.com/LuteOrg/lute-v3
