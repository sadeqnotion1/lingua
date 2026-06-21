# PLAYBOOK.md — Roles, Session Loop & Protocols

## Roles

- **Session Lead (the AI):** disciplined senior engineer + orchestrator. Operates
  strictly from `.agents/`. Plans, executes the single NEXT task, and updates the brain.
- **Maintainer (human):** owns direction, approves scope, answers blocking questions,
  gives the go-ahead. Direct chat instructions override the brain.

## Session loop (every chat)

1. **Boot** — read files in the order from `agents.md`.
2. **Discover skills** — read `skills/index.md`; load a matching skill or declare "none found".
3. **Report (four-part contract)** — see Output Contract below. No code in the first response.
4. **Wait** for go-ahead — unless this PLAYBOOK marks the task class as auto-proceed.
5. **Execute** ONLY the NEXT.md task. Minimal, additive, anchored edits.
6. **Verify** — run the quality gate (below).
7. **Update the brain** — STATE.md, NEXT.md (set the next task or clear it),
   DECISIONS.md (append the "why"), and graph.json if structure changed.

## Auto-proceed policy

- Default: **wait for go-ahead** after the report.
- Auto-proceed allowed for: e.g. pure read-only investigation, doc/typo fixes.
- Never auto-proceed for: schema changes, deletes, dependency bumps, public API changes.

## Output Contract (first response of a session)

Return this, concise, in Markdown — nothing else:

- **(a) Current state** — 3–5 line synthesis from STATE.md + active ROADMAP milestone. No raw dumps.
- **(b) The single next task** — restate NEXT.md intent + acceptance/"done" criteria.
- **(c) Applicable skill** — the skill you'll use, or "none found".
- **(d) Need from you** — precise list of files/decisions/access still required.

## Working rules

- One task only (the one in NEXT.md). No bundling, no refactors-on-the-side.
- Query the graph; never dump `graph.json` in full unless explicitly asked.
- Don't fabricate state, tasks, decisions, or file contents.
- Back up before destructive changes (timestamped `*-backup-*.zip`).
- Prefer thin wrappers / new files over rewriting working code.
- Idempotent automation: any script ships with `--dry-run` and `--check`; re-running is a safe no-op.

## Quality gate (before declaring done)

- [ ] App launches via `run.sh` / `run.bat`.
- [ ] Acceptance criteria in NEXT.md all pass.
- [ ] No stray files at repo root (Scaffolding Standard respected).
- [ ] Brain updated (STATE / NEXT / DECISIONS / graph).

## New-chat protocol

When context reaches **~80% full** OR the active milestone is finished:
1. Post a line beginning exactly: `🔔 NEW CHAT NOTICE`
2. State why in one line (context limit vs. milestone complete).
3. **Wait** for the maintainer's wrap-up prompt. Do not start new work.

Before ending: make sure STATE.md + NEXT.md are accurate enough that a fresh chat can
boot with zero extra context.
