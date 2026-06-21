# NEXT — the handoff card
_This is the FIRST thing to act on in a new chat (after the START prompt).
The AI rewrites this at the end of every session._

> Repo: https://github.com/sadeqnotion1/lingua

## ➡️ The one next task
**M4 — Tokenizer.** Implement the Lute-style parser/tokenizer in `backend/app/services/parser.py` using language configuration settings (e.g., `word_chars`), ensuring proper handling of words, non-words, spaces, and punctuation to render them correctly in the reading interface.

## Start the next chat with this
> "Let's do M4 (Tokenizer). Pull the parser module (backend/app/services/parser.py) and any language schema/models, and let's start implementing the tokenization logic."

## What to paste / give me at the start
Pull these from the repo:
1. `backend/app/services/parser.py`
2. `backend/app/models/language.py` (or language schema definition)
3. Any tokenizer test files if they exist (e.g. under `backend/tests/`)

## Decisions I need from you for M4
- Confirm the schema details for `Language`'s parser configs (e.g. `word_chars`, whether character-based parsing is needed, etc.).

## Definition of done for this task
- The parser tokenizes text into an ordered list of strings containing alternating words and non-words.
- Unit tests written to verify correct parsing behavior with standard characters, spaces, punctuation, and custom `word_chars`.
- The test suite (`pytest`) runs and passes successfully.
- I update `STATE.md` (M4 → ✅), append to `SESSION_LOG.md`, and set `NEXT.md` to M5.
