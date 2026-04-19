# Roadmap

## Current Direction

- Keep the Python agent working against the existing local RAG pipeline during migration.
- Make retrieval available through a synchronous API so the agent can consume published knowledge.
- Preserve local fallback behavior until the web-managed path is stable.

## Phase 0 - Foundation

- Confirm the exact system signals the agent must recover from Kubernetes and Prometheus.
- Define the minimum end-to-end flow: runbook upload, publication, retrieval, diagnosis.
- Inventory every piece of state that still lives on local disk or in process memory.

## Phase 1 - Monorepo Platform

- Create the `Next.js` fullstack app in `apps/web`.
- Move runbook management out of `data/*.md` and into application-owned entities.
- Implement pragmatic hexagonal boundaries for runbook management, knowledge processing, and retrieval.
- Add local adapters for file storage, metadata persistence, indexing, and inline job dispatch.
- Expose REST endpoints for runbook CRUD, publication, and knowledge retrieval.

## Phase 2 - Agent Integration

- Make the Python agent consume a remote retrieval API when configured.
- Keep the existing local vector store path as a fallback during migration.
- Ensure the agent only retrieves published knowledge.

## Phase 3 - Cloud-Ready Infrastructure

- Define infrastructure ports for `BlobStore`, `MetadataRepository`, `VectorIndex`, `JobQueue`, and `SecretsProvider`.
- Implement Azure adapters first.
- Keep provider selection configuration-driven so AWS can be added without changing domain code.
- Externalize durable state and remove local-machine assumptions from runtime code.

## Phase 4 - Async Knowledge Processing

- Replace inline indexing with a real worker and queue-backed job flow.
- Track ingestion status transitions: `pending`, `indexed`, `failed`.
- Add retries and operational visibility for failed indexing jobs.

## Phase 5 - Kubernetes Runtime

- Containerize the agent and the supporting services.
- Add health checks, config docs, and runtime permissions.
- Run the agent in a local cluster before promoting to managed Kubernetes.
- Add the minimum RBAC required for cluster-read access.

## Phase 6 - Multi-Cloud & Operations

- Add AWS adapters that implement the same infrastructure contracts as Azure.
- Add structured incident reports and store them in a queryable backend.
- Add smoke and integration tests for upload, index, retrieval, and diagnosis.
- Harden observability, deployment pipelines, and rollback paths.
