# Skills Registry

Skills are specialized, reusable playbooks the session lead can load for specific
task types. During boot, the AI reads this index; if a skill matches the task in
`NEXT.md`, it loads that skill's `SKILL.md` and follows it exactly. If none match,
it says "none found" and proceeds with PLAYBOOK defaults.

## How to use

1. Match the NEXT.md task against the **When to use** column below.
2. Open `skills/<name>/SKILL.md` and follow it step by step.
3. If a skill has scripts/refs, run/read them as instructed inside SKILL.md.

## Registered skills

| Skill | When to use | Path |
|-------|-------------|------|
| _template | Reference for authoring new skills (not a real skill) | `skills/_template/SKILL.md` |
| skill-name | one-line trigger condition | `skills/skill-name/SKILL.md` |

> Add a row for every skill. Keep "When to use" specific enough that matching is
> unambiguous. Remove the `_template` row reference once you have real skills.
