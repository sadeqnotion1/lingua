# agents.md — Repo & Graph Orientation

> Read this **first** in every session. It tells you what the repo is, where the
> brain lives, and how to load context in the right order. Do not write code or
> propose changes until you have completed the boot sequence below.

## Project

- **Name:** project_name  (default: LinguaRead)
- **Repo:** repo_url  (default: github.com/sadeqnotion1/lingua)
- **One-line purpose:** what the project does in one sentence
- **Primary stack:** e.g. Python backend + web/QML frontend

## Boot sequence (in order, every session)

1. `brain/STATE.md`     → where we are
2. `brain/NEXT.md`      → the ONE next task + what to hand you
3. `brain/ROADMAP.md`   → the **current milestone only**
4. `brain/PLAYBOOK.md`  → roles + session loop + protocols
5. `graph/graph.json`   → **query as needed; never dump it in full**
6. `skills/index.md`    → discover skills; load one if it matches NEXT.md

## Repo layout (high level)

> Keep this in sync with the actual tree. Follows the Project Scaffolding Standard:
> minimal root, fewest folders, run files + README + .gitignore at root.

```text
repo-root/
├── backend/    # server code, libs, tools, config, assets, docs
├── frontend/   # user-facing app only (if applicable)
├── .agents/    # this brain
├── run.sh / run.bat
├── README.md
└── .gitignore
```

## Graph orientation

- The knowledge graph (`graph/graph.json`) maps modules, files, functions, and their
  relationships. Use it to answer "what calls what" / "where does X live" **without**
  reading the whole codebase.
- **Query, don't dump.** Pull only the nodes/edges you need. See `graph/README.md`.

## Hard rules (summary — full rules in PLAYBOOK.md)

- Work on **only** the task in `NEXT.md`. No "while I'm here" changes.
- Don't fabricate state, tasks, decisions, or file contents.
- Keep edits minimal, additive, anchored. Back up before destructive changes.
- A direct chat instruction from the maintainer overrides this brain.
