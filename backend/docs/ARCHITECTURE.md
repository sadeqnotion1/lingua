# Architecture

## Overview

LinguaRead is a self-hosted reading-based language learner. It separates a
JSON API backend from a single-page frontend.

```
React SPA (frontend/)  --fetch /api/*-->  FastAPI (backend/app/)  -->  SQLite (backend/data/)
```

In local/production runs the backend also serves the built SPA (`frontend/dist`),
so the whole app launches from one command (`run.sh` / `run.bat`).

## Backend layers

- **models/** — SQLAlchemy ORM (Language, Book, Text, Term). Mirrors Lute's domain.
- **schemas/** — Pydantic request/response models.
- **services/** — framework-free business logic ported from Lute (parsing, term
  status, parent terms, SRS). The valuable, reusable part.
- **routers/** — thin HTTP layer mapping endpoints to services.

## Domain (from Lute)

- A **Language** defines how text is tokenized and displayed.
- A **Book** is a library item; it has ordered **Text** pages.
- A **Term** is a tracked word/phrase with a learning **status** and optional
  **parent term** (root form), so a definition applies to all inflections.

## Reading flow (target)

1. Import text → stored as Book + Text.
2. Open a Text → backend tokenizes and tags each word with its term status.
3. Click a word → create/update a Term, set status, add translation.
4. Review → SRS schedules due terms.

## Why FastAPI (not Flask)

Lute uses Flask with server-rendered templates. Since the chosen UI is a
separate SPA, an API-first framework (FastAPI) is a cleaner fit while the
domain logic ports over largely unchanged.
