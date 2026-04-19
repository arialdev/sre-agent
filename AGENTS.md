# Repository Guidelines

## Project Structure & Module Organization
- `packages/runbook-manager/` contains the Next.js fullstack package:
  - `app/` holds the UI, server actions, and route handlers.
  - `src/lib/runbooks/` holds the runbook domain, ports, and local adapters.
  - `storage/` is generated local state and should not be committed.
- `packages/sre-agent/` contains the Python package:
  - `src/sre_agent/config.py` centralizes shared paths, models, and environment loading.
  - `src/sre_agent/ingest.py` loads Markdown runbooks from `data/`, chunks them, embeds them, and persists a local ChromaDB store in `vectorstore/`.
  - `src/sre_agent/query.py` provides retrieval helpers and the `search_runbooks` tool.
  - `src/sre_agent/agent.py` runs the ReAct incident-diagnosis agent.
- Project docs live in `README.md`, `docs/architecture.md`, and `docs/roadmap.md`. Package-specific docs live next to the package that owns them.

## Build, Test, and Development Commands
- `pnpm install` installs root tooling and JS package dependencies.
- `pnpm nx run runbook-manager:dev` starts the Next.js package.
- `pnpm nx run runbook-manager:build` builds the web package.
- `cd packages/sre-agent && uv sync` creates the Python environment.
- `pnpm nx run sre-agent:ingest` ingests runbooks and builds the local vector store.
- `pnpm nx run sre-agent:query -- "error text"` runs retrieval only and prints matching runbook excerpts.
- `pnpm nx run sre-agent:agent -- "error text"` runs the full ReAct diagnosis flow.

## Coding Style & Naming Conventions
- Use Python 3.11, 4-space indentation, and type hints where they improve clarity.
- Prefer small, explicit functions with descriptive names such as `load_documents` or `create_vectorstore`.
- Keep module-level constants in `UPPER_SNAKE_CASE` and file names in `snake_case.py`.
- Match the existing style: straightforward procedural code, docstrings for public helpers, and minimal abstraction.

## UI / Design Rules
- For any UI, frontend, or visual design work, follow `packages/runbook-manager/docs/design-system.md` as the source of truth.
- Preserve the visual system, spacing, typography, color, and component rules defined there unless the user explicitly asks to change them.

## Testing Guidelines
- There is no automated test suite in the repository yet.
- Validate changes manually by running `pnpm nx run runbook-manager:typecheck`, `pnpm nx run runbook-manager:build`, then `pnpm nx run sre-agent:ingest`, `pnpm nx run sre-agent:query ...`, and finally `pnpm nx run sre-agent:agent ...`.
- If you add tests, place them under a new `tests/` directory and use `test_*.py` naming.

## Commit & Pull Request Guidelines
- Follow the existing Conventional Commit style with a scope, for example: `feat(sre-agent): ...`, `docs(sre-agent): ...`, `chore(sre-agent): ...`.
- Keep commits focused on one change.
- PRs should describe the behavior change, list verification steps, and note any updates to `data/`, regenerated `vectorstore/` content, or moved docs.

## Security & Configuration Tips
- Create a local root `.env` or `packages/sre-agent/.env` with `OPENAI_API_KEY`; do not commit secrets.
- Treat `packages/sre-agent/vectorstore/` as disposable local state. Re-run ingestion after changing runbooks or embedding settings.
