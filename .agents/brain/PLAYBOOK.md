# PLAYBOOK — rules of engagement

How we work together so there's no headache or confusion about "my part vs yours".

## Roles — who does what

**You (SadeQ) — the hands & the product owner:**
- Run commands locally (`./run.sh`, `npm run dev`, `pytest`, `seed.py`).
- Paste back logs, errors, and screenshots when I ask.
- Make product/feature decisions (what it should do, priorities).
- Test in the browser and tell me what you actually see.
- Commit & push to GitHub.

**Me (AI) — the planner & the code:**
- Keep the brain current (`STATE`, `NEXT`, `SESSION_LOG`, `DECISIONS`).
- Write/modify code and give it to you with exact file paths.
- Define acceptance criteria and tell you the exact commands to run.
- Tell you precisely what to paste back so I can verify.
- Tell you when to start a fresh chat.

> I cannot read your disk or run your machine. You are my eyes and hands; I am the
> map and the code.

## The session loop

1. New chat → you paste the Boot Prompt (in `brain/README.md`).
2. I read `STATE.md` + `NEXT.md` and restate the current task.
3. I ask for any files/logs/decisions I need (listed in `NEXT.md`).
4. We implement the one task. You run + report; I fix until acceptance passes.
5. I update the brain and tell you to open a fresh chat.

## When to start a NEW chat (the handshake)

I watch for this so you don't have to. I'll proactively post a **🔔 NEW CHAT NOTICE**
when ANY of these is true:
- We just finished a milestone (clean boundary).
- My context is getting ~80% full / replies feel heavy.
- We're switching to a different part of the app.

**The handshake:**
1. I post: "🔔 NEW CHAT NOTICE — paste the WRAP-UP prompt so I can update the brain."
2. You paste the **② WRAP-UP prompt** (from `PROMPTS.md`).
3. I update `STATE.md`, `NEXT.md`, `SESSION_LOG.md` (+ `DECISIONS.md`/`ROADMAP.md`/graph if needed)
   and hand you the updated files + a one-paragraph recap.
4. You open a fresh chat and paste the **① START prompt**.

Never leave a chat before step 3 — that's what makes the next chat painless.
Both prompts live in `PROMPTS.md`.

## What logs / screenshots to give me (by symptom)

| Symptom | Give me |
|---|---|
| Backend won't start / 500 error | Full terminal traceback from `./run.sh` (the Python stack). |
| API returns wrong/empty data | The exact request (curl or URL) + the JSON response + the router file. |
| Frontend blank / JS error | Browser DevTools **Console** tab text + the failing component file. |
| API call fails from UI | DevTools **Network** tab: request URL, status code, response body. |
| UI looks wrong | A **screenshot** of the page + which component renders it. |
| DB / data looks off | Output of the query, or `sqlite3 backend/data/lingua.db ".schema"`. |
| Tests fail | Full `pytest` output. |
| Build fails | Full `npm run build` output. |

Rule of thumb: paste the **full** error text, not a paraphrase. Trim only secrets.

## Feature intake — what I'll ask before building a feature

When you propose a feature, I'll pin down these before writing code:
1. **Goal** — what should the user be able to do, in one sentence?
2. **UI reference** — a screenshot or the LingQ behavior you're matching.
3. **Data impact** — new fields/tables? changes to Language/Book/Text/Term?
4. **API shape** — endpoints + request/response.
5. **Edge cases** — empty states, errors, large inputs, unsupported languages.
6. **Acceptance** — how we'll know it's done (the concrete test).
7. **Scope cut** — smallest version we can ship first.

If you just say "build X", I'll ask the minimum of these I can't infer, then go.

## Keeping the graph & brain honest

- After any structural code change, I update `.agent/graph/graph.json` and regenerate
  `graph.html` (`python .agent/graph/build_graph_html.py`).
- If `STATE.md` disagrees with the real code, the **code wins** — tell me and I fix the brain.
