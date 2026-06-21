# SESSION LOG — append-only
> Newest entries at the top. Repo: https://github.com/sadeqnotion1/lingua

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
