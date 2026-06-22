# SESSION LOG — append-only
> Newest entries at the top. Repo: https://github.com/sadeqnotion1/lingua

## 2026-06-22 — M8 Polish minor-findings fixes ✅
- Perf: memoized dashboard word counts (content fingerprint, never stale); removed search N+1 (grouped page-count + IN-batched parent books).
- Search race guard: AbortController + request-id in Search.tsx.
- Book search hits deep-link to /library?q=<title>; Library seeds filter from URL.
- Theme "System" now live via matchMedia; accent auto-saves (debounced).
- Email validated (stdlib regex, no new dep); startup moved to FastAPI lifespan.
- Verified offline (py_compile + pure-logic unit tests + prettier); live uvicorn+vite smoke-test done on local machine.
- Deferred: SQLite FTS5 search (schema-level migration) — logged as a future item.

## 2026-06-22 — M8 Polish ✅ (wrap-up)
- Completed **M8 — Polish** by applying the package from `.agents/fixes/1441`.
  - Backend new: models/setting.py; schemas/{stats,search,settings}.py; services/{stats,search,settings}.py; routers/{stats,search,settings}.py.
  - Backend changed: main.py (include 3 routers), models/__init__.py (+Setting).
  - Frontend new: api/m8.ts; pages/{Dashboard,Search,Settings}.tsx; styles/{theme,dashboard,search,settings}.css.
  - Frontend changed: App.tsx (routes + landing + theme boot), components/Sidebar.tsx (nav + icons).
  - Verified: Running verify_m8.py in the root passes all compiler, schema validation, and helper function tests; python pytest passes 105 tests; npm run build builds the React app cleanly with TypeScript.

## 2026-06-22 — M7 Account page ✅ (wrap-up)
- Completed **M7 — Account page** by applying the package from `.agents/fixes/8566222026`.
  - Copied new backend files: `backend/app/models/user.py` (User model with table `users`), `backend/app/schemas/account.py` (AccountOut schema), and `backend/app/services/account.py` (Account service layer with `get_account` and `serialize_account`).
  - Added new unit test suite: `backend/tests/test_account.py` (in-memory SQLite session with 3 new test cases verified).
  - Replaced router/page stubs: `backend/app/models/__init__.py` (added User to the model registry), `backend/app/routers/account.py` (DB-backed account endpoints querying the seeded User), and `frontend/src/pages/Account.tsx` (read-only profile UI showing username, email, plan tier, and member-since date).
  - Created frontend styles: `frontend/src/styles/account.css` matching the dark/glassmorphic aesthetics.
  - Edited `backend/tools/seed.py` to import `User` and idempotently seed the single local user (`SadeQ`).
  - Verified: All 105 python backend tests passed successfully with no regressions, and the frontend compiles cleanly.
- **Stop point:** M7 Account complete. Next chat targets **M8 — Polish (stats, search, settings)**.

## 2026-06-22 — M6 Terms ✅ (wrap-up)
- Completed **M6 — Terms** by implementing interactive click-to-define drawer panels.
  - Copied new backend files: `backend/app/schemas/term.py` (TermOut, TermCreate, TermUpdate schemas) and `backend/app/services/terms.py` (Term business logic: create/update terms, case-insensitive normalization).
  - Replaced router/page stubs: `backend/app/routers/terms.py` (endpoints for loading details, creating, and updating terms) and `frontend/src/pages/Reader.tsx` (fully wired word token selection, dynamic token status coloring, and TermDrawer mounting).
  - Created new frontend files: `frontend/src/components/TermDrawer.tsx` (sliding drawer component for inspecting/editing terms, picking familiarity status, defining translations, and linking parent terms) and `frontend/src/styles/term-drawer.css` (dark, glassmorphic styling matching spec).
  - Merged additions to `frontend/src/api/client.ts` containing new interfaces (`Term`, `TermCreate`, `TermUpdate`) and API endpoints (`getTerm`, `createTerm`, `updateTerm`).
  - Added new backend service test suite in `backend/tests/test_terms.py` (13 test cases verified).
  - Verified: All 102 python backend tests passed successfully with no regressions, and frontend compiled with TypeScript checking passing cleanly.
  - Updated the knowledge graph `backend/docs/graph.json` to index the new endpoints, service logic, and frontend components, and regenerated `backend/docs/graph.html`.
- **Stop point:** M6 Terms complete. Next chat targets **M7 — Account page**.

## 2026-06-22 — M5 Reader ✅ (wrap-up)
- Completed **M5 — Reader** by applying the server-enriched reading screen and client view.
  - Copied new backend files: `backend/app/schemas/reading.py`, `backend/app/services/reading.py`, and `backend/tests/test_reading.py`.
  - Copied new frontend stylesheet: `frontend/src/styles/reader.css`.
  - Replaced router/page stubs: `backend/app/routers/reading.py` (serves tokenized text + term status) and `frontend/src/pages/Reader.tsx` (word-by-word reader view with Claude-style status colors, legend, skeleton loader, pagination, and RTL language support).
  - Merged additions to `frontend/src/api/client.ts` with new interfaces (`ReaderToken`, `ReaderLanguage`, `ReaderPagination`, `ReaderText`) and the `getReaderText` API client method.
- Fixed path resolution in `.agents/graph/build_graph_html.py` to point to `backend/docs` relative to the repository root.
- Verified: Both frontend production builds compiled without TypeScript/bundler errors, and Python backend tests pass (89 passed, including the new integration tests in `test_reading.py`).
- Regenerated graph representation `backend/docs/graph.html` using the fixed builder.
- **Stop point:** M5 Reader complete. Next chat targets **M6 — Terms**.

## 2026-06-21 — M4 Tokenizer & M3 Design Polish ✅ (wrap-up)
- Completed **M4 — Tokenizer** by applying the config-driven parser/tokenizer.
  - `backend/app/services/parser.py`: Implemented Lute-style parser/tokenizer splitting text into lossless alternating runs of word/non-word strings, matching language config rules.
  - `backend/tests/test_parser.py`: Created an expanded test suite covering 22 test cases and 81 parametrization scenarios.
- Applied final design polish to **M3 — Library UI**:
  - `frontend/src/styles/library.css`: Added font-smoothing, standard focus rings (`--ring`/`--ring-soft`), and hover zoom configurations.
  - `frontend/src/components/LessonCard.tsx`: Refactored cover layout to isolate hover-zoom animation effects without dragging badges or chips.
- Verified: Both frontend production builds and the backend test suite run cleanly (all 81 tests passed).
- Committed + pushed to `main`.

## 2026-06-21 — M3 Library UI ✅ (build + wrap-up)
- Completed **M3 — Library UI** by applying the M3 delivery package.
- `frontend/src/api/client.ts`: replaced with full implementation for listing books and importing text. Added typed `BookOut`, `LanguageGroup`, `ImportRequest`, `ImportResponse`, and custom `ApiError` mapping for HTTP 409 duplicate book conflict warnings.
- `frontend/src/pages/Library.tsx`: replaced stub. Implemented live search, language-grouped shelves, collapsible import form with validation/error handling, flash status notifications, and skeleton loaders.
- `frontend/src/components/ShelfRow.tsx`: replaced stub. Horizontal scrollable shelf rows with bold title chevron headers, counts, and interactive smooth-scroll arrows.
- `frontend/src/components/LessonCard.tsx`: replaced stub. Landscape card format matching the spec with cover placeholders and overlaid page count badges.
- `frontend/src/styles/library.css`: created scoping stylesheet for all library components.
- Verified: `npm run build` compiled without any TypeScript or bundler errors, and python backend tests continue to pass (9 passed).
- Regenerated graph representation `.agents/graph/graph.html`.

## 2026-06-21 — M2 Library API ✅ (build + wrap-up)
- Completed **M2 — Library API** by applying the M2 delivery package.
- `backend/app/schemas/library.py`: added schemas (`BookOut`, `LanguageGroup`, `ImportRequest`, `ImportResponse`). Updated to use standard `typing` types for compatibility with Python 3.9.
- `backend/app/services/library.py`: implemented service logic (`list_books_grouped`, `import_text`, `resolve_or_create_language`) with custom duplicate checking. Updated to use standard `typing` types for compatibility with Python 3.9.
- `backend/app/routers/library.py`: implemented endpoints `GET /api/library/books` and `POST /api/library/import`.
- `backend/tests/test_library_api.py`: added 6 tests covering grouped listing and book importing with duplicates/defaults.
- Verified test suite: all 9 tests passed.
- Decisions recorded: **D8** (duplicate book imports raise `409 Conflict`).
- Committed + pushed to `main`.
- **Stop point:** M2 complete & pushed. Next chat targets **M3 — Library UI**.

## 2026-06-21 — M1 Data layer ✅ (build + wrap-up)
- Completed **M1 — Data layer** by applying the M1 delivery (`APPLY.md`).
- `backend/app/models/term.py`: added case-insensitive `UniqueConstraint("language_id","text_lower")` (`uq_term_lang_lower`).
- `backend/tools/seed.py`: seeds 1 language (English), 1 book, 2 texts, 5 terms (incl. a `looking → look` parent link) + prints verification counts.
- Added `backend/tests/conftest.py` (in-memory SQLite fixture) and `backend/tests/test_models.py` (seed/query-back + case-insensitive uniqueness).
- Verified locally: `python backend/tools/seed.py` printed expected counts; `pytest` → **3 passed**.
- Reset the dev SQLite DB so the new constraint applied.
- Decisions recorded: **D6** (terms case-insensitive, enforced), **D7** (start language English; no extra Book/Text fields yet).
- Committed + pushed to `main`.
- **Stop point:** M1 complete & pushed; brain updated. Next chat boots cold on **M2 — Library API** (see NEXT.md). Open: M2 duplicate-import behavior; D5 `.agents/` tracking.

## 2026-06-21
- Reworked the brain prompts so context can come from the **GitHub repo**
  (https://github.com/sadeqnotion1/lingua) in addition to attached/pasted files.
- Standardized path spelling `.agent/` → `.agents/` across brain files.
- Flagged DECISIONS D5: `.agents/` is committed to the public repo despite the
  old "local-only" note — needs a decision (track vs. gitignore).
- No code changes. Next task remains **M1 — Data layer**.
