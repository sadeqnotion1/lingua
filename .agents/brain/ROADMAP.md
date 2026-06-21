# ROADMAP — ordered build plan

Build in order. Each milestone is small enough to finish in roughly one chat.
Don't start the next one until the current one's acceptance criteria pass.

---

## M0 — Scaffold ✅ DONE

Structure, wiring, graph, brain. App boots; `/api/health` returns OK.

---

## M1 — Data layer

**Goal:** the four models are solid and the DB can be created and seeded.

- Confirm `Language`, `Book`, `Text`, `Term` fields & relationships (FKs, `Term.parent_id` self-ref, `status` int 0-99).
- Verify `init_db()` creates all tables (all models imported in `app/models/__init__.py`).
- Flesh out `backend/tools/seed.py`: 1 language, 1 book, 1 text, a few terms.
- Smoke test: run seed, query rows back.

**Acceptance:** `python backend/tools/seed.py` populates `backend/data/lingua.db`; a
quick query returns the seeded rows; `pytest backend/tests` still green.

**What I'll ask you for:** target languages you care about first; whether terms are
case-sensitive; any extra fields you want on Book/Text (cover image? source URL?).

---

## M2 — Library API

**Goal:** back the Library screen.

- `GET /api/library/books` — list books grouped by language (shelves).
- `POST /api/library/import` — accept title + language + raw text, create Book+Text.
- Wire `get_db` sessions; return Pydantic schemas.

**Acceptance:** import a text via curl, then see it in the books list.

---

## M3 — Library UI (matches screenshot 1)

**Goal:** shelves of lesson cards + the import bar at top.

- `pages/Library.tsx` fetches `/api/library/books` via `api/client.ts`.
- `ShelfRow` per language, `LessonCard` per book/text (title, progress, word count).
- Import bar: title + language + paste text → `POST /api/library/import`.

**Acceptance:** paste a text in the UI, it appears as a card on the right shelf.

---

## M4 — Tokenizer (`services/parser.py`) — CORE

**Goal:** turn raw text into an ordered list of tokens (words + punctuation/space).

- Implement `tokenize(text, language)` → list of `{text, is_word, order}`.
- Unicode-aware word splitting; preserve original spacing for rendering.
- Map each word to its `Term` (lowercased key per language) + status if known.

**Acceptance:** unit test: a sample paragraph tokenizes to the expected words and
round-trips back to the original string.

---

## M5 — Reader

**Goal:** read a text with each word colored by familiarity.

- `GET /api/reading/text/{id}` → tokens + per-word status.
- `pages/Reader.tsx` renders tokens; unknown/new words highlighted; click a word
  opens a panel.

**Acceptance:** open a seeded text, see colored words, click one to open the panel.

---

## M6 — Terms (status, parent, translation)

**Goal:** learning actions persist.

- `GET /api/terms?language=` , `POST /api/terms` (upsert: status, translation, parent).
- Clicking a word in the Reader sets status 1-5 / known / ignored; updates color live.
- Parent terms (lemmas) via `Term.parent_id`.

**Acceptance:** set a word to "learning 3", reload, color persists.

---

## M7 — Account page (matches screenshot 2)

**Goal:** the settings/account screen.

- `GET /api/account` → username, email, tier, member-since.
- `pages/Account.tsx` renders the fields (read-only first, then editable).

**Acceptance:** account page shows the seeded user's details.

---

## M8 — Polish

Stats (known/learning counts), search/filter in Library, settings (theme, font),
empty states, basic error toasts. Pick from this as desired.

---

## Backlog / maybe-later

- Audio + sentence playback, dictionary/translation API integration, SRS review
  queue, export of known terms, multi-user/auth, deployment packaging.
