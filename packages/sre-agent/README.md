# `sre-agent`

Python package that ingests runbooks, retrieves troubleshooting context and
runs the ReAct diagnosis loop.

## Commands

```bash
uv sync
pnpm nx run sre-agent:ingest
pnpm nx run sre-agent:query -- "error text"
pnpm nx run sre-agent:agent -- "high cpu usage"
```

## Package layout

- `src/sre_agent/` contains the Python package.
- `data/` contains runbook fixtures for local ingestion.
- `vectorstore/` contains generated ChromaDB output and is ignored by Git.
- `docs/` contains package-specific plans and notes.
