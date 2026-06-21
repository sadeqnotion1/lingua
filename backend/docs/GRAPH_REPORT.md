# LinguaRead Knowledge Graph Report

> Generated per the **Graphify Protocol**. Source of truth: `graph.json` (53 nodes, 70 edges). Interactive view: `graph.html`. Query the graph before re-reading source.

The repo is treated as **one graph** across layers: backend code ↔ SQLite schema ↔ frontend code ↔ build config ↔ docs. The interesting structure lives in the cross-layer edges.

## God nodes (most-connected hubs)

| Node | Degree | Why it matters |
|---|---|---|
| `app.main:app` (FastAPI instance) | 11 | Everything flows through it: CORS, startup `init_db`, all four routers, `/api/health`, and serving the SPA build. Largest blast radius in the repo. |
| `app.models` (registry) | 6 | Imports all four ORM models so they register on `Base.metadata`; `init_db` depends on it. Structural hub of the domain layer. |
| `api.client:api` (client.ts) | 6 | The **only** bridge from UI code to the backend; every page data call routes through it over HTTP. |
| `frontend.App` (App.tsx) | 5 | SPA routing hub — the shell and every page hang off it. |
| `db.tables:terms` | 5 | Most-connected table: FKs to languages plus the self-referential `parent_id`, and the read/write target of the terms API. |
| `app.database:Base` | 5 | Declarative base all four models inherit; schema creation depends on it. |

## Communities (subsystems)

1. **Backend bootstrap & config** — launcher, `config`, `database`, and the FastAPI app wiring.
2. **Domain models & schema** — `Language`, `Book`, `Text`, `Term` and their tables (mirrors Lute).
3. **HTTP API (routers) & services** — `/api/*` endpoints + the `parser` service stub.
4. **Frontend SPA shell & routing** — `index.html`, `main.tsx`, `App.tsx`, `Sidebar`.
5. **Frontend pages, components & API client** — Library/Reader/Account pages, ShelfRow/LessonCard, fetch client.
6. **Build, run & tooling** — run wrappers, Vite/TS/package config, requirements, seed, tests.
7. **Docs & rationale** — ARCHITECTURE, CHANGELOG, README.

## Surprising connections (cross-community edges)

1. **`frontend.vite` → `app.main:app`** — a frontend build-config file hard-codes the backend's `127.0.0.1:8000` for its dev proxy. Tooling reaching into backend runtime.
2. **`app.main:app` → `frontend.vite` (dist)** — the backend serves Vite's `frontend/dist` build output, so backend runtime depends on a frontend artifact. Together with #1 this is a **circular cross-layer coupling** — the real seam to watch when refactoring how the app is served.
3. **`api.client:api` → `app.main:health` / routers** — frontend code depends on backend endpoint contracts over HTTP. These `INFERRED` edges are the true boundary between the two top-level folders; nothing enforces them at compile time.
4. **`db.tables:terms` → `db.tables:terms`** — `Term.parent_id` self-reference (Lute's "parent term"), the only recursive relationship in the schema.

## The "why" (rationale nodes)

- `ARCHITECTURE.md` **explains** the domain models, the SPA-serves-from-backend decision, and the **FastAPI-over-Flask** choice (Lute is Flask + server templates; a separate SPA wants an API-first framework, while the domain logic ports over largely unchanged).
- `README.md` **explains** the run wrappers and the intentionally minimal root.
- Code comments mark the intended-but-unimplemented seams: `services/parser.py` (`tokenize` raises `NotImplementedError`) and the stubbed router bodies.

## Suggested questions (the graph can answer these directly)

1. Trace a request: what nodes does `GET /api/library/books` traverse from the SPA down to the database?
2. How does the frontend reach the backend in dev vs production (Vite proxy vs `StaticFiles`), and where is that wired?
3. Where is the schema defined and what is the FK dependency order among `languages`/`books`/`texts`/`terms`?
4. What is the single most central node and what breaks if its contract changes?
5. Which parts are still stubs (`parser.tokenize`, router bodies) versus actually wired, so I know where to implement first?

## Confidence summary

| Confidence | Count | Meaning |
|---|---|---|
| `EXTRACTED` | 60 | Read directly from code/structure (imports, inheritance, decorators, FKs, config). |
| `INFERRED` | 9 | Deduced from naming/usage (e.g. HTTP route ↔ endpoint mapping, router → table reads). |
| `AMBIGUOUS` | 1 | `get_text` → `parser.tokenize`: intended collaborator, not yet called in code. |

_Code-structure edges are `EXTRACTED`; the frontend↔backend HTTP seam and not-yet-implemented reads/writes are flagged `INFERRED`/`AMBIGUOUS` so the next reader knows what was found vs. expected._
