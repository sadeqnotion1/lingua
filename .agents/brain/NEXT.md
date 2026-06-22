# NEXT — the handoff card
_This is the FIRST thing to act on in a new chat (after the START prompt).
The AI rewrites this at the end of every session._

> Repo: https://github.com/sadeqnotion1/lingua

## ➡️ The one next task
**Smoke-test M8 locally, then start next milestone.**
Verify that:
- uvicorn + vite run; `/dashboard`, `/search`, `/settings` all load.
- Dashboard shows real totals + vocab status bar.
- Search returns books/pages/terms; page hits open the reader.
- Settings: edit username/email; theme switch persists; accent persists; language `word_chars`/RTL/romanization save.
- `app_settings` table auto-created on boot (`init_db`).

## Definition of done for this task
- Verification steps pass, and the application functions correctly with the M8 additions.
