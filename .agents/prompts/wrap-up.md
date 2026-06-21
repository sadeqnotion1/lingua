# Wrap-Up Prompt — #WRAP_UP

Paste at the end of a session, before opening a fresh chat.

---

② #WRAP_UP

Wrap up this session before I open a fresh chat. **Update the brain so the next chat
continues with zero context loss.** Keep edits tight, additive, and anchored.

Update each file:
- **brain/STATE.md**     → refresh the per-part status table + the one-line status.
- **brain/NEXT.md**      → set the next single task, the **start line**, and the exact
  files / logs / decisions I should hand you next time.
- **brain/SESSION_LOG.md** → append a short entry: date, what we did, decisions made,
  and the exact stop point.
- **brain/DECISIONS.md** → add any new decisions as `Dn` entries (append-only).
- **brain/ROADMAP.md**   → tick off / adjust milestones if scope changed.
- **graph/**             → if code structure changed, update `graph.json`, then
  regenerate `graph.html` (`python .agents/graph/render_graph.py`).

**Quality gate before you finish:**
- [ ] STATE.md + NEXT.md are accurate enough to boot a fresh chat cold.
- [ ] SESSION_LOG.md has today's entry with a clear stop point.
- [ ] Any structural change is reflected in graph.json (+ regenerated graph.html).
- [ ] No stray files at repo root (Scaffolding Standard respected).

**Then give me:**
1. The **updated files** to save into `.agents/` (show full file contents).
2. A **one-paragraph recap** of exactly what to do next session.
