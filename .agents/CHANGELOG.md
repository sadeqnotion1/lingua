# Brain Changelog

## v2.1 — YYYY-MM-DD (prompts + session memory)
- Added `prompts/start.md` (#START) and `prompts/wrap-up.md` (#WRAP_UP); removed `session-lead.md`.
- Added `brain/SESSION_LOG.md` (append-only session history with stop points).
- Added `graph/render_graph.py` + generated `graph/graph.html` (offline viewer).
- PLAYBOOK now has an explicit Wrap-up checklist (STATE/NEXT/SESSION_LOG/DECISIONS/ROADMAP/graph).
- agents.md boot sequence now includes DECISIONS.md and points to the prompts.

## v2 — YYYY-MM-DD (upgraded scaffold)
- Added `agents.md` boot sequence with explicit read order.
- Split brain into STATE / NEXT / ROADMAP / PLAYBOOK / DECISIONS.
- Added append-only `DECISIONS.md` (the "why" memory).
- Added `graph/README.md` with schema + jq query recipes ("query, don't dump").
- Added `skills/index.md` registry + `_template/SKILL.md` authoring template.
- Formalized New-Chat Protocol, Output Contract, Auto-proceed policy, Quality gate.

## v1 — prior
- Initial brain (pre-upgrade).
