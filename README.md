# sre-agent

Monorepo for an SRE knowledge platform composed of a Next.js runbook manager
and a Python incident-diagnosis agent.

## Quickstart

```bash
pnpm install
cd packages/sre-agent
uv sync
cp .env.example .env
```

Add your OpenAI key to the root `.env` or `packages/sre-agent/.env`, then run the
app or the agent:

```bash
pnpm nx run runbook-manager:dev
pnpm nx run sre-agent:ingest
pnpm nx run sre-agent:agent -- "ECONNREFUSED error on port 5432 in production logs"
```

## Packages

- `packages/runbook-manager`: Next.js fullstack package for runbook management.
- `packages/sre-agent`: Python package for ingestion, retrieval and diagnosis.

## Core commands

- `pnpm nx run runbook-manager:dev`
- `pnpm nx run runbook-manager:build`
- `pnpm nx run runbook-manager:typecheck`
- `pnpm nx run sre-agent:ingest`
- `pnpm nx run sre-agent:query -- "error text"`
- `pnpm nx run sre-agent:agent -- "error text"`

## Documentation

- [Architecture](docs/architecture.md)
- [Roadmap](docs/roadmap.md)
- [Runbook manager package](packages/runbook-manager/README.md)
- [SRE agent package](packages/sre-agent/README.md)

## Configuration

- Required: `OPENAI_API_KEY`
- Optional: `RUNBOOKS_API_BASE_URL` in the root `.env` or `packages/sre-agent/.env`
  to query the runbook manager retrieval API before falling back to the local
  vector store

Generated state lives inside each package, for example
`packages/runbook-manager/storage/` and `packages/sre-agent/vectorstore/`.
