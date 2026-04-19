# Architecture

## Overview

The repository is organized as a package-oriented monorepo rooted in
`packages/`.

- `packages/runbook-manager` is a Next.js fullstack package that owns runbook
  management, publication and retrieval APIs.
- `packages/sre-agent` is a Python package that ingests local runbooks, queries
  published knowledge over HTTP when available and diagnoses incidents.

The longer-term direction remains the same: move runbook ownership into the web
application and keep the Python agent as a consumer of published knowledge.

## Runtime modules

- `packages/runbook-manager/app` contains the Next.js UI and route handlers.
- `packages/runbook-manager/src/lib/runbooks` contains the runbook domain,
  ports and local adapters.
- `packages/sre-agent/src/sre_agent/ingest.py` loads runbooks, splits them,
  embeds them and persists the vector store.
- `packages/sre-agent/src/sre_agent/query.py` loads the local vector store or
  queries the remote knowledge API when `RUNBOOKS_API_BASE_URL` is configured.
- `packages/sre-agent/src/sre_agent/agent.py` runs the ReAct diagnosis loop.
- `packages/sre-agent/src/sre_agent/config.py` centralizes shared paths, model
  names, chunking parameters and environment loading.

## Operational Constants

- Chunking is tuned for SRE runbooks with `chunk_size=800` and `chunk_overlap=100`.
- Embeddings use `text-embedding-3-small`.
- The agent LLM uses `gpt-4o-mini`.
- Local retrieval falls back to ChromaDB when the remote API is unavailable.

## Data Model

- `packages/sre-agent/data/` contains one Markdown runbook per incident type.
- `packages/sre-agent/vectorstore/` is derived state and should be treated as
  disposable local output.
- `packages/runbook-manager/storage/` contains local development state for the
  web package.
- Runbooks should keep clear headings so the text splitter preserves procedural sections.

## Project Layout

- `packages/` contains the executable and shared packages.
- `docs/` contains project-wide documentation.
- Package-specific docs live next to the package that owns them.

## Environment

- Use `pnpm install` at the repository root for JS dependencies.
- Use `uv sync` in `packages/sre-agent` for the Python environment.
- Store agent secrets in the repository `.env` or `packages/sre-agent/.env`.
- Load `OPENAI_API_KEY` locally before ingesting or querying.
