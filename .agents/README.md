# `.agents/` — Project Brain (v2, upgraded)

This folder is the **single source of truth** an AI session lead reads before doing
any work on this repo. It exists so that any new chat / new model can pick up the
project with zero context loss.

> **Golden rule:** the AI operates *strictly* from these files and never improvises
> project state. If a brain file is missing or stale, the AI fixes the brain first.

## File map

```text
.agents/
├── agents.md            # Entry point: repo + graph orientation, how to start a session
├── brain/
│   ├── STATE.md         # Where we are right now (living document)
│   ├── NEXT.md          # The ONE next task + exactly what to hand the AI
│   ├── ROADMAP.md       # Milestones (only the current one is "active")
│   ├── PLAYBOOK.md      # Roles, session loop, new-chat protocol, output contract
│   ├── DECISIONS.md     # Append-only decision log (the "why", D1, D2, ...)
│   └── SESSION_LOG.md   # Append-only session history (what happened + stop point)
├── graph/
│   ├── graph.json       # Repo knowledge graph (query it, never dump it whole)
│   ├── graph.html       # Generated viewer (run render_graph.py to regenerate)
│   ├── render_graph.py  # graph.json -> self-contained offline graph.html
│   └── README.md        # Graph schema + how to query without dumping
├── skills/
│   ├── index.md         # Skill registry: name + one-line description + when to use
│   └── _template/
│       └── SKILL.md     # Copy this to author a new skill
└── prompts/
    ├── start.md         # #START kickoff prompt (boots a session lead)
    └── wrap-up.md       # #WRAP_UP prompt (close a session with zero context loss)
```

## How a session works (short version)

1. AI reads `agents.md` → `brain/STATE.md` → `brain/NEXT.md` → `brain/ROADMAP.md`
   (current milestone only) → `brain/PLAYBOOK.md`.
2. AI queries `graph/graph.json` only for the nodes/edges it needs.
3. AI discovers `skills/` and loads a matching skill, or declares "none found".
4. AI reports the four-part status (a/b/c/d) and waits, unless PLAYBOOK says proceed.
5. On wrap-up, AI updates STATE / NEXT / SESSION_LOG / DECISIONS / ROADMAP and the graph.

## Prompts

- Start a session: paste `prompts/start.md` (the #START prompt).
- End a session: paste `prompts/wrap-up.md` (the #WRAP_UP prompt).

## Maintenance contract

- Keep files **small and current**. STATE/NEXT are living docs; prune aggressively.
- `DECISIONS.md` and `SESSION_LOG.md` are append-only. Never rewrite history.
- Regenerate `graph.html` with `python .agents/graph/render_graph.py` after editing the graph.
- Edits to the brain are **minimal, additive, anchored**. Back up before destructive change.

_Version: brain v2 · template — replace placeholders in ... with real values._
