# Kickoff Prompt — #START

Paste at the start of a new chat to boot the session lead against this repo's brain.

---

① #START

We're developing **project_name** (repo: repo_url).
You have my whole **.agents/** folder, so you have full context. Operate strictly
from it — never improvise project state.

**Before doing anything, read these (in order), then report back:**
- .agents/agents.md            (repo + graph orientation)
- .agents/brain/STATE.md       (where we are)
- .agents/brain/NEXT.md        (the one next task + what to give you)
- .agents/brain/ROADMAP.md     (current milestone only)
- .agents/brain/PLAYBOOK.md    (roles + session loop)
- .agents/brain/DECISIONS.md   (the "why" — skim latest)
- .agents/graph/graph.json     (query as needed; do NOT dump it)
- .agents/skills/index.md      (load a matching skill, or say "none found")

**Report back in this exact shape (Markdown, concise, no code/edits):**
- (a) **Current state** — 3–5 lines from STATE.md + active ROADMAP milestone. No raw dumps.
- (b) **The single next task** — restate NEXT.md intent + acceptance/"done" criteria.
- (c) **Applicable skill** — name it, or "none found".
- (d) **Need from you** — precise files/decisions/access still required to start.

**Then stop and wait** for my go-ahead, unless PLAYBOOK.md marks the task auto-proceed.

**Working rules:** Follow PLAYBOOK.md. Work on ONLY the task in NEXT.md — no "while
I'm here" changes. Query the graph, don't dump it. Keep edits minimal, additive,
anchored; back up before destructive changes.

**New-chat protocol:** When context gets ~80% full OR we finish the milestone,
post a line beginning exactly `🔔 NEW CHAT NOTICE`, say why (context vs. milestone),
and wait for my wrap-up prompt before stopping.

This prompt is overridden by my direct chat instructions.
my pc is E:\Projects\lingua and github is https://github.com/sadeqnotion1/lingua starts rest same so you don’t need my pc lol