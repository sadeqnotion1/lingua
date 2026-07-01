# NEXT — the handoff card
_This is the FIRST thing to act on in a new chat (after the START prompt).
The AI rewrites this at the end of every session._

> Repo: https://github.com/sadeqnotion1/lingua

## ▶️ Start line (paste after the START prompt in the fresh chat)
> "M9 is done and verified. Begin **M10** — let's scope the next Backlog item. My pick: <audio/sentence playback | dictionary/translation API | SRS review queue | export known terms | multi-user/auth | deployment packaging>."

## ➡️ The one next task
**Select & scope the next milestone (M10) from Backlog, then build it.**
M0–M9 are complete and verified; there is **no active milestone**. The first move is choosing which Backlog item to promote to M10, then running the PLAYBOOK feature-intake before any code.

Backlog candidates (pick one):
- Audio + sentence playback
- Dictionary / translation API integration
- SRS review queue
- Export of known terms
- Multi-user / auth
- Deployment packaging

Before writing code, run the PLAYBOOK feature-intake for the chosen item: goal, UI reference, data impact, API shape, edge cases, acceptance, scope cut.

## Definition of done for this task
- M10 is named, scoped via feature-intake, and given a single-chat-sized acceptance test — then implemented and verified, with the brain updated.

## What to hand me next time
- **Your pick** for M10 (one Backlog item) — or paste the start line above with the bracket filled in.
- Any **UI reference / screenshot** if the chosen item has a front end.
- The current `.agents/graph/graph.json` if the code structure has drifted since last session.
