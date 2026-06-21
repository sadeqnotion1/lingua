# DECISIONS.md — Decision Log (append-only)

> Append a new entry whenever a non-trivial decision is made. Never rewrite or delete
> past entries — supersede them with a new dated entry instead. This is the project's
> "why" memory.

## Format

```
### YYYY-MM-DD — short title
- **Context:** what prompted the decision
- **Decision:** what we chose
- **Alternatives considered:** what we rejected and why
- **Consequences:** follow-ups / things now constrained
- **Supersedes:** (optional) link to the entry this replaces
```

---

### YYYY-MM-DD — Adopted `.agents/` brain v2
- **Context:** Needed zero-context-loss handoffs between AI sessions.
- **Decision:** Standardized on this brain layout (agents.md + brain/ + graph/ + skills/).
- **Alternatives considered:** Single monolithic NOTES.md (too coarse); issue tracker only (no orientation).
- **Consequences:** Every session boots through agents.md; brain must be updated at session end.
