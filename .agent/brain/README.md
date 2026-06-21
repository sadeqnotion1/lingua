# 🧠 LinguaRead Brain

> This folder is the **shared memory** between you (SadeQ) and the AI. It exists
> so that any fresh chat can pick up exactly where the last one left off — no
> re-explaining, no lost context, no confusion about "my part vs yours".
>
> Location: `.agent/brain/` (gitignored, local-only). Repo: https://github.com/sadeqnotion1/lingua

## The 5 files and what each is for

| File | Purpose | Who updates it |
|---|---|---|
| `STATE.md` | The single source of truth: where we are right now, per part. | AI, end of every session |
| `ROADMAP.md` | The full ordered build plan (milestones M0…M8) + acceptance criteria. | AI, when scope changes |
| `NEXT.md` | The handoff card: the ONE next task + the exact prompt to start the next chat + what to paste me. | AI, end of every session |
| `SESSION_LOG.md` | Append-only history of what happened each session. | AI, end of every session |
| `DECISIONS.md` | Why we chose things (so we don't re-litigate). | AI, when a decision is made |
| `PLAYBOOK.md` | The rules of engagement: roles, when to start a new chat, what logs/screenshots to give, feature-intake questions. | Rarely changes |
| `PROMPTS.md` | The two copy-paste prompts (START + WRAP-UP) that run the whole cycle. | Rarely changes |

## How to use this (the loop)

**Every time you start a new chat:**

1. Paste the **Boot Prompt** below.
2. I read `STATE.md` + `NEXT.md` (+ the graph in `.agent/graph/`) and confirm the plan.
3. We do the one task in `NEXT.md`.
4. Before we run low on context, I update `STATE.md`, `NEXT.md`, and `SESSION_LOG.md` and tell you to start a fresh chat.

You never have to remember the state. The files do.

## 🚀 The two prompts

The whole cycle runs on two copy-paste prompts that live in **`PROMPTS.md`**:

- **① START** — paste at the top of every new chat (after you've given me `.agent/`).
  I read `STATE.md` + `NEXT.md`, restate the current task, and ask for anything I need.
- **② WRAP-UP** — paste when I post a **🔔 NEW CHAT NOTICE**. I update the whole brain
  so the next chat continues with zero context loss.

```
  ① START  ->  we build  ->  I post 🔔 NEW CHAT NOTICE  ->  you paste ② WRAP-UP
      ^                                                          |
      |____________________  open a fresh chat  ________________|
```

Open `PROMPTS.md` to copy them.

## Important

- If `STATE.md` and the actual code ever disagree, **the code wins** — tell me and
  I'll correct `STATE.md`.
- Keep these files short and current. A stale brain is worse than none.
- This brain assumes you can paste file contents into chat (this AI can't read your
  local disk). The Boot Prompt tells me which files to ask you for if I don't have them.
