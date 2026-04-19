# sre-agent

Python SRE agent for incident diagnosis with a local RAG pipeline and a path toward a web-managed knowledge base.

## Quickstart

```bash
mamba env create -f environment.yml
mamba activate sre-agent
cp .env.example .env
```

Add your OpenAI key to `.env`, then ingest the runbooks and run the agent:

```bash
python -m src.ingest
python -m src.agent "ECONNREFUSED error on port 5432 in production logs"
```

## Commands

```bash
python -m src.ingest
python -m src.query "error text"
python -m src.agent "error text"
```

## Documentation

- [Architecture](docs/architecture.md)
- [Roadmap](docs/roadmap.md)
- [Agent plan](agent-plans/codex-plan.md)

## Configuration

- Required: `OPENAI_API_KEY`
- Optional: `RUNBOOKS_API_BASE_URL` to query a remote knowledge API before falling back to the local vector store

Generated state lives in `vectorstore/` and is not meant to be committed.
