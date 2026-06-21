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
│   └── DECISIONS.md     # Append-only decision log (the "why")
├── graph/
│   ├── graph.json       # Repo knowledge graph (query it, never dump it whole)
│   └── README.md        # Graph schema + how to query without dumping
├── skills/
│   ├── index.md         # Skill registry: name + one-line description + when to use
│   └── _template/
│       └── SKILL.md     # Copy this to author a new skill
└── prompts/
    └── session-lead.md  # The kickoff prompt that boots a session lead
```

## How a session works (short version)

1. AI reads `agents.md` → `brain/STATE.md` → `brain/NEXT.md` → `brain/ROADMAP.md`
   (current milestone only) → `brain/PLAYBOOK.md`.
2. AI queries `graph/graph.json` only for the nodes/edges it needs.
3. AI discovers `skills/` and loads a matching skill, or declares "none found".
4. AI reports the four-part status (a/b/c/d) and waits, unless PLAYBOOK says proceed.
5. After the task, AI updates `STATE.md`, `NEXT.md`, `DECISIONS.md`, and the graph.

## Maintenance contract

- Keep files **small and current**. STATE/NEXT are living docs; prune aggressively.
- `DECISIONS.md` is append-only. Never rewrite history; add a new entry.
- Edits to the brain are **minimal, additive, anchored**. Back up before destructive change.

_Version: brain v2 · template — replace placeholders in ... with real values._
