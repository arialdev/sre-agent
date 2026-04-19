# Plan: monorepo fullstack + agente SRE multi-cloud con retrieval REST

> Snapshot del plan del agente. El roadmap activo y consolidado vive en `docs/roadmap.md`.

## Summary
La arquitectura objetivo es un **monorepo con servicios separados**: una app web fullstack en `Next.js`, un runtime del agente SRE en Python y, cuando el pipeline lo requiera, un worker de ingestión desacoplado. El backend de la web será dueño de la gestión de runbooks, versionado, publicación y estados de ingestión; el agente consultará el conocimiento publicado a través de una **API síncrona de retrieval**.

La infraestructura se diseña desde el inicio con **puertos de infraestructura desacoplados** para arrancar en Azure y soportar AWS sin reescribir el dominio. La arquitectura aplicará hexagonal y principios `SOLID` de forma pragmática: puertos y adaptadores donde haya una razón real de sustitución o testabilidad, sin crear capas vacías.

## Architecture Decisions
- `Next.js` como framework fullstack TS/JS para la app web.
- Monorepo con ciclos de vida separados para `apps/web`, el agente Python y los workers que aparezcan.
- El agente no dependerá del filesystem del repo como fuente principal de runbooks.
- El flujo de runbooks se divide en tres bounded contexts:
  - **Runbook Management**: CRUD, versionado, publicación y auditoría.
  - **Knowledge Processing**: validación, chunking, embeddings e indexado.
  - **Agent Retrieval**: consulta del conocimiento publicado.
- Los puntos de variación de infraestructura se modelan como puertos:
  - `BlobStore`
  - `MetadataRepository`
  - `VectorIndex`
  - `JobQueue`
  - `SecretsProvider`
  - `KnowledgeRetriever`
- Azure será el primer conjunto de adaptadores; AWS se añadirá más tarde contra los mismos puertos.

## Integration Model
- La lectura del conocimiento por parte del agente será **síncrona** mediante una API interna/REST.
- La subida, reindexado y trabajos pesados del pipeline serán **asíncronos** detrás de un puerto de cola.
- No se usará mensajería como mecanismo primario para que el agente consulte runbooks.
- La web gestionará estados de cada versión:
  - `draft`
  - `published`
  - `archived`
- El pipeline de indexado gestionará estados operativos:
  - `pending`
  - `indexed`
  - `failed`

## Delivery Plan
### Phase 1
- Crear `apps/web` con `Next.js`.
- Implementar la base del dominio de runbooks con puertos y adaptadores locales.
- Exponer APIs para alta, versionado, publicación y consulta.

### Phase 2
- Sustituir persistencia local por adaptadores cloud-ready.
- Separar el indexado a un worker dedicado detrás del puerto `JobQueue`.
- Adaptar el agente Python para consultar la API de knowledge retrieval.

### Phase 3
- Añadir adaptadores Azure reales para storage, metadata, cola y secretos.
- Mantener el dominio intacto y activar proveedor por configuración.

### Phase 4
- Añadir adaptadores AWS equivalentes sin cambiar los casos de uso.
- Endurecer observabilidad, retries, DLQ y despliegue multi-servicio.

## Public Interfaces
- `POST /api/runbooks`
- `POST /api/runbooks/:id/versions`
- `POST /api/runbooks/:id/publish`
- `GET /api/runbooks`
- `POST /api/knowledge/query`

## Acceptance Criteria
- La web permite crear y publicar runbooks sin depender de `data/*.md`.
- El agente puede consultar runbooks publicados mediante HTTP si la URL está configurada.
- El dominio no conoce SDKs concretos de Azure o AWS.
- El repositorio refleja el roadmap en `docs/roadmap.md`.
