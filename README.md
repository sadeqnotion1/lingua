# LinguaRead

A self-hosted, LingQ-style **read-to-learn** app: import texts, read them with click-to-define lookups, save terms with known/learning status, and review. Backend logic is modeled on **[Lute v3](https://github.com/LuteOrg/lute-v3)** (Python/Flask → ported to FastAPI here); the UI follows the LingQ **Library** and **Account** screens.

> **START HERE** — this README is the front door (the repo root is kept intentionally minimal, so quickstart lives here instead of a separate file).

## Quickstart

### Windows
```bat
run.bat
```

### macOS / Linux
```bash
chmod +x run.sh   # first time only
./run.sh
```

Then open http://127.0.0.1:8000

The run wrappers are thin launchers — they call the real entry point at `backend/main.py`, which starts the API and serves the built frontend.

## First-time setup

```bash
# Backend deps
python -m venv .venv && . .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt

# Frontend deps + build (output lands in frontend/dist, served by the backend)
cd frontend && npm install && npm run build && cd ..
```

During frontend development, run the Vite dev server (`cd frontend && npm run dev`) alongside the backend; it proxies `/api` to port 8000.

## Layout

```
repo-root/
├── backend/          # all server code, libs, tools, config, docs, data
│   ├── main.py       # entry point (uvicorn launcher + static serving)
│   ├── app/          # FastAPI app: models, schemas, services, routers
│   ├── data/         # SQLite db lives here (gitignored)
│   ├── tools/        # helper scripts (seed, etc.)
│   ├── docs/         # CHANGELOG, ARCHITECTURE
│   ├── tests/        # backend tests
│   └── requirements.txt
├── frontend/         # the user-facing SPA only (React + Vite + TS)
│   └── src/          # pages (Library, Reader, Account), components, api client
├── run.bat           # Windows launcher (thin wrapper)
├── run.sh            # macOS/Linux launcher (thin wrapper)
├── README.md
└── .gitignore
```

## Stack

| Layer | Choice | Why |
|---|---|---|
| Backend | FastAPI + SQLAlchemy | Clean JSON API for a SPA; reuses Lute's Python domain logic |
| Database | SQLite (local file) | Matches Lute; zero-config, self-hosted |
| Frontend | React + Vite + TypeScript | Fast SPA matching the LingQ library/account UI |
| Serving | Backend serves `frontend/dist` | One launch command, clean root |

This is an **empty scaffold** — folders and stubs are in place, endpoints/pages return placeholders. Build features on top.
