# NEXT — the handoff card
_This is the FIRST thing to act on in a new chat (after the START prompt).
The AI rewrites this at the end of every session._

> Repo: https://github.com/sadeqnotion1/lingua

## ▶️ Start line (paste after the START prompt in the fresh chat)
> "M8 is done and verified. Begin **M9** — let's scope the next Backlog item. My pick: <FTS5 search-at-scale | audio/sentence playback | dictionary/translation API | SRS review queue | export known terms | multi-user/auth | deployment packaging>."

## ➡️ The one next task
**Select & scope the next milestone (M9) from Backlog, then build it.**
M0–M8 are complete and verified; there is **no active milestone**. The first move is choosing which Backlog item to promote to M9, then running the PLAYBOOK feature-intake before any code.

**Front-runner:** migrate global search to **SQLite FTS5** (virtual table + sync triggers) — the only Backlog item already broken out as a near-term, self-contained milestone.

Backlog candidates (pick one):
- Search at scale → SQLite FTS5 (front-runner)
- Audio + sentence playback
- Dictionary / translation API integration
- SRS review queue
- Export of known terms
- Multi-user / auth
- Deployment packaging

Before writing code, run the PLAYBOOK feature-intake for the chosen item: goal, UI reference, data impact, API shape, edge cases, acceptance, scope cut.

## Definition of done for this task
- M9 is named, scoped via feature-intake, and given a single-chat-sized acceptance test — then implemented and verified, with the brain updated.

## What to hand me next time
- **Your pick** for M9 (one Backlog item) — or paste the start line above with the bracket filled in.
- **If FTS5:** confirm acceptance (search still returns books/pages/terms, now ranked, matching current behavior on the seed data) and whether a one-time index backfill over existing rows is in scope.
- Any **UI reference / screenshot** if the chosen item has a front end.
- The current `.agents/graph/graph.json` if the code structure has drifted since last session (so I can query it instead of re-reading the codebase).
