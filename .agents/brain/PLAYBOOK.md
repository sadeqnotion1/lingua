# PLAYBOOK — rules of engagement

> Repo: https://github.com/sadeqnotion1/lingua

## Session loop
1. New chat → you give me the `.agents/` folder (attach/paste, or point me at the repo)
   and paste the START prompt (in `PROMPTS.md`).
2. I read `STATE.md` + `NEXT.md` and restate the current task.
3. I ask for any files/logs/decisions I need (listed in `NEXT.md`).
4. We implement the one task. You run + report; I fix until acceptance passes.
5. I update the brain and tell you to open a fresh chat.

## Roles
- **You (SadeQ):** product decisions, running code locally, pasting logs/screenshots, final say.
- **AI:** senior engineer for the ONE task in `NEXT.md`. Minimal, additive, anchored
  edits. Backs up before destructive changes. No "while I'm here" scope creep.

## When to start a NEW chat (the handshake)
I watch for this so you don't have to. I'll proactively post a **🔔 NEW CHAT NOTICE**
when ANY of these is true:
- We just finished a milestone (clean boundary).
- My context is getting ~80% full / replies feel heavy.
- We're switching to a different part of the app.

**The handshake:**
1. I post: "🔔 NEW CHAT NOTICE — paste the WRAP-UP prompt so I can update the brain."
2. You paste the **② WRAP-UP prompt** (from `PROMPTS.md`).
3. I update `STATE.md`, `NEXT.md`, `SESSION_LOG.md` (+ `DECISIONS.md`/`ROADMAP.md`/graph
   if needed) and hand you the updated files + a one-paragraph recap.
4. You open a fresh chat and paste the **① START prompt**.

Never leave a chat before step 3 — that's what makes the next chat painless.

## Feature-intake questions (when you say "build X")
1. **Goal** — what should the user be able to do, in one sentence?
2. **UI reference** — a screenshot or the LingQ behavior you're matching.
3. **Data impact** — new fields/tables? changes to Language/Book/Text/Term?
4. **API shape** — endpoints + request/response.
5. **Edge cases** — empty states, errors, large inputs, unsupported languages.
6. **Acceptance** — how we'll know it's done (the concrete test).
7. **Scope cut** — smallest version we can ship first.
If you just say "build X", I'll ask the minimum of these I can't infer, then go.

## Keeping the graph & brain honest
- After any structural code change, I update `.agents/graph/graph.json` and regenerate
  `graph.html` (`python .agents/graph/build_graph_html.py`).
- If `STATE.md` disagrees with the real code, the **code wins** — tell me and I fix the brain.
