# Architecture

## Overview

`sre-agent` is a Python SRE incident-diagnosis agent backed by a local retrieval pipeline. It loads Markdown runbooks from `data/`, embeds them into a ChromaDB store under `vectorstore/`, and uses a ReAct loop to answer incident questions.

The longer-term direction is to move runbook ownership into the web application and expose retrieval through an HTTP API, keeping the Python agent as a consumer of published knowledge.

## Runtime Modules

- `src/ingest.py` loads runbooks, splits them into semantically coherent chunks, embeds them, and persists the vector store.
- `src/query.py` loads the local vector store or queries the remote knowledge API when `RUNBOOKS_API_BASE_URL` is configured.
- `src/agent.py` runs the ReAct diagnosis loop and formats the response as a Markdown report.
- `src/config.py` centralizes shared paths, model names, chunking parameters, and environment loading.

## Operational Constants

- Chunking is tuned for SRE runbooks with `chunk_size=800` and `chunk_overlap=100`.
- Embeddings use `text-embedding-3-small`.
- The agent LLM uses `gpt-4o-mini`.
- Local retrieval falls back to ChromaDB when the remote API is unavailable.

## Data Model

- `data/` contains one Markdown runbook per incident type.
- `vectorstore/` is derived state and should be treated as disposable local output.
- Runbooks should keep clear headings so the text splitter preserves procedural sections.

## Project Layout

- `src/` contains the Python package.
- `data/` contains source runbooks.
- `docs/` contains project documentation.
- `agent-plans/` contains the persisted delivery plan.

## Environment

- Use `mamba env create -f environment.yml` to create the Python 3.11 environment.
- Store secrets in `.env`.
- Load `OPENAI_API_KEY` locally before ingesting or querying.
