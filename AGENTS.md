# Repository Guidelines

## Project Structure & Module Organization
- `src/` contains the Python package:
  - `src/ingest.py` loads Markdown runbooks from `data/`, chunks them, embeds them, and persists a local ChromaDB store in `vectorstore/`.
  - `src/query.py` provides retrieval helpers and the `search_runbooks` tool.
  - `src/agent.py` runs the ReAct incident-diagnosis agent.
- `data/` stores source runbooks in Markdown. Keep each file focused on one incident type and use clear section headings.
- `vectorstore/` is generated locally and should not be committed.
- Project docs live at the repo root (`README.md`, `CLAUDE.md`, `GEMINI.md`, `TODO.md`).

## Build, Test, and Development Commands
- `mamba env create -f environment.yml` creates the Python 3.11 environment.
- `mamba activate sre-agent` activates the environment.
- `python -m src.ingest` ingests runbooks and builds the local vector store.
- `python -m src.query "error text"` runs retrieval only and prints matching runbook excerpts.
- `python -m src.agent "error text"` runs the full ReAct diagnosis flow.

## Coding Style & Naming Conventions
- Use Python 3.11, 4-space indentation, and type hints where they improve clarity.
- Prefer small, explicit functions with descriptive names such as `load_documents` or `create_vectorstore`.
- Keep module-level constants in `UPPER_SNAKE_CASE` and file names in `snake_case.py`.
- Match the existing style: straightforward procedural code, docstrings for public helpers, and minimal abstraction.

## Testing Guidelines
- There is no automated test suite in the repository yet.
- Validate changes manually by running `python -m src.ingest`, then `python -m src.query ...`, and finally `python -m src.agent ...`.
- If you add tests, place them under a new `tests/` directory and use `test_*.py` naming.

## Commit & Pull Request Guidelines
- Follow the existing Conventional Commit style with a scope, for example: `feat(sre-agent): ...`, `docs(sre-agent): ...`, `chore(sre-agent): ...`.
- Keep commits focused on one change.
- PRs should describe the behavior change, list verification steps, and note any updates to `data/` or regenerated `vectorstore/` content.

## Security & Configuration Tips
- Create a local `.env` with `OPENAI_API_KEY`; do not commit secrets.
- Treat `vectorstore/` as disposable local state. Re-run ingestion after changing runbooks or embedding settings.
