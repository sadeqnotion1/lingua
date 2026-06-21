# graph/ — Repo Knowledge Graph

`graph.json` is a queryable map of the codebase: modules, files, functions/classes,
routes, assets, and how they relate. It lets the AI answer structural questions
("what calls X?", "where does Y live?") **without** reading the whole repo.

## Query, don't dump

Never paste the whole file into a response. Instead, pull only what you need.

### Schema

- **nodes[]**: `{ id, type, path, summary, symbols? }`
  - `type` ∈ `module | file | function | class | route | asset | doc | external`
- **edges[]**: `{ from, to, type, note? }`
  - `type` ∈ `contains | imports | calls | references | renders | depends_on`

### Example queries (jq)

```bash
# All files inside the backend module
jq '.edges[] | select(.from=="backend" and .type=="contains") | .to' .agents/graph/graph.json

# Everything that depends on a given node
jq --arg n "backend/entry" '.edges[] | select(.to==$n)' .agents/graph/graph.json

# Look up one node by id
jq --arg id "frontend" '.nodes[] | select(.id==$id)' .agents/graph/graph.json
```

## Keeping it fresh

- Regenerate / hand-edit whenever files move, are added, or relationships change.
- Bump `version` and update `generated` when you do.
- Keep `summary` fields short — they are the AI's fast index into the code.
