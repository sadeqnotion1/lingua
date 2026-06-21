# 🧠 LinguaRead Brain

> This folder is the **shared memory** between you (SadeQ) and the AI. It exists
> so that any fresh chat can pick up exactly where the last one left off — no
> re-explaining, no lost context.
>
> Location: `.agents/brain/`. Repo: https://github.com/sadeqnotion1/lingua
> **Context sources:** attached/pasted files **or** the repo above. The AI can't
> read your local disk — if a file isn't attached and isn't on GitHub, it asks.

## The files and what each is for

| File | Purpose | Who updates it |
|---|---|---|
| `STATE.md` | The single source of truth: where we are right now, per part. | AI, end of every session |
| `ROADMAP.md` | The full ordered build plan (milestones M0…M8) + acceptance criteria. | AI, when scope changes |
| `NEXT.md` | The handoff card: the ONE next task + the exact prompt to start the next chat + what to paste. | AI, end of every session |
| `SESSION_LOG.md` | Append-only history of what happened each session. | AI, end of every session |
| `DECISIONS.md` | Why we chose things (so we don't re-litigate). | AI, when a decision is made |
| `PLAYBOOK.md` | The rules of engagement: roles, when to start a new chat, what logs/screenshots to give, feature-intake questions. | Rarely changes |
| `PROMPTS.md` | The two copy-paste prompts (START + WRAP-UP) that run the whole cycle. | Rarely changes |

## How to use this (the loop)
**Every time you start a new chat:**
1. Give the AI the `.agents/` folder — attach/paste it, or point it at the repo:
   https://github.com/sadeqnotion1/lingua
2. Paste the **① START** prompt (from `PROMPTS.md`).
3. The AI reads `STATE.md` + `NEXT.md` (+ the graph in `.agents/graph/`) and confirms the plan.
4. We do the one task in `NEXT.md`.
5. Before running low on context, the AI updates `STATE.md`, `NEXT.md`, and
   `SESSION_LOG.md` and tells you to start a fresh chat.

You never have to remember the state. The files do.

## 🚀 The two prompts
- **① START** — paste at the top of every new chat (after you've given me `.agents/`).
  I read `STATE.md` + `NEXT.md`, restate the current task, and ask for anything I need.
- **② WRAP-UP** — paste when I post a **🔔 NEW CHAT NOTICE**. I update the whole brain
  so the next chat continues with zero context loss.

Open `PROMPTS.md` to copy them.
