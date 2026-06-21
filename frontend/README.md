# Frontend (React + Vite + TypeScript)

The user-facing SPA only. Talks to the backend over `/api`.

```bash
npm install
npm run dev      # http://localhost:5173 (proxies /api -> :8000)
npm run build    # outputs ./dist, served by the backend in local runs
```

## Structure
- `src/pages/` — Library, Reader, Account (mirror the LingQ screens)
- `src/components/` — Sidebar, ShelfRow, LessonCard
- `src/api/client.ts` — typed fetch wrapper
- `src/styles/global.css` — base styles
