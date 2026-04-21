## Context

The current `runbook-manager` app is a single route that mixes summary metrics, creation forms, version management, and publishing controls into one page. It uses a warm glassmorphism aesthetic that conflicts with the repository design system, and it does not provide a dedicated navigation model for future app areas. On the behavior side, the current domain services are richer than the product now requires: they model versions and publication history, while the desired scope is a simpler library of single-file runbooks with create, list, view, and delete flows only.

This change touches both the Next.js application layer and the runbook domain services. The design must preserve the existing local-storage architecture, keep the design system as the visual source of truth, and create room for an agent chat section without implementing the chat workflow yet.

## Goals / Non-Goals

**Goals:**
- Introduce a design-system-compliant application shell for `runbook-manager`.
- Split the experience into clear views for runbook management and agent chat.
- Support the core runbook management flows the user requested: create, list, dedicated view, and delete.
- Reduce the data entry model to title, markdown file, and optional tags.
- Move the creation form into its own dedicated route rather than embedding it on the list screen.
- Keep the implementation compatible with the current local adapters and storage layout.

**Non-Goals:**
- Building the actual chat experience, retrieval loop, or message persistence.
- Replacing the local metadata/content/index adapters with cloud infrastructure.
- Introducing a general runbook editing workflow.
- Reintroducing revisions, republishing, or version history in the UI.
- Expanding the creation form beyond title, file upload, and optional tags.
- Introducing a large client-side state library or a separate component framework.

## Decisions

### Decision: Build a two-area application shell within the Next.js `app/` router
The app will move from a single landing page to a workspace shell with persistent navigation and two primary areas: `Runbooks` and `Agent Chat`. The runbooks area remains functional, while the chat area renders a static `"coming soon"` state.

Rationale:
- This matches the user request for both runbook management and a separate chat view.
- It creates a stable IA now, so later chat implementation can slot into an existing route.
- It lets the redesign express the design system through navigation, section rhythm, cards, and empty states instead of only form restyling.

Alternatives considered:
- Keep a single page with anchor sections. Rejected because it does not establish a real app shell or a distinct chat view.
- Add tabs with client-side conditional rendering only. Rejected because route-based navigation is more durable and linkable.

### Decision: Translate the design system into shared CSS tokens and reusable layout classes
The redesign will use `app/globals.css` as the initial home for shared tokens and primitives derived from `docs/design-system.md`, including warm neutrals, Notion-style typography hierarchy, whisper borders, pill badges, and soft card shadows.

Rationale:
- The app is currently small, so introducing a design-token layer in the existing global stylesheet keeps complexity low.
- The design system document is specific enough to map into CSS custom properties and a small set of semantic utility classes.
- This creates consistency across the shell, forms, lists, detail panes, and placeholder states.

Alternatives considered:
- Inline styles per route component. Rejected because it would make the design system hard to enforce.
- Introduce a new CSS framework. Rejected because the repository already has a clear visual spec and does not need another abstraction layer.

### Decision: Simplify the domain model to single-file runbooks
The web UI and service layer will treat a runbook as a single stored markdown document with a title, optional tags, and one content path. Runbook viewing will use a dedicated route rather than an inline split view. Deletion will remove the metadata entry, stored content file, and indexed knowledge entry only after the user confirms the action by typing the runbook slug.

Rationale:
- The requested management experience cannot be implemented cleanly with list-only access.
- A dedicated route makes the runbook page linkable, clearer, and more aligned with the requested behavior than an embedded detail pane.
- The user explicitly removed revisions from scope, so keeping version-oriented forms or data paths would add complexity without product value.
- Deletion semantics belong in the domain service layer so server actions and API routes remain thin.
- Keeping removal logic centralized reduces the risk of orphaned metadata, content files, or index records.

Alternatives considered:
- Implement deletion only at the UI file-system layer. Rejected because it bypasses the service contract and spreads persistence rules into route code.
- Soft-delete runbooks. Rejected for now because the current local-storage product shape does not require recovery semantics.

### Decision: Put creation on its own page and require a file upload
The list view will focus on browsing and navigation. Creation moves to a dedicated `/runbooks/new` route reached from a `Publish` button on the list page. The form will require a markdown file and a title, with tags optional, and it will not allow pasted markdown content.

Rationale:
- The list screen becomes calmer and more useful when it is not competing with a large form.
- Requiring a file upload enforces a clearer content source and removes ambiguity between pasted text and uploaded markdown.
- The narrower form matches the requested model exactly and removes unnecessary summary and revision fields.
- The design system favors calm, content-first layouts over dense administrative stacking.

Alternatives considered:
- Keep the form in the list view. Rejected because it crowds the page and makes the list feel secondary.
- Support both upload and pasted markdown. Rejected because the user explicitly wants file-only creation.

## Risks / Trade-offs

- [Deleting runbooks removes local data permanently] -> Mitigation: add a clear destructive action treatment and require the user to type the runbook slug before the delete action is enabled.
- [Reading full runbook content may require additional content-store access on page load] -> Mitigation: scope detail fetching to the selected runbook route or view instead of loading all content for the list.
- [A global CSS token pass can accidentally regress existing controls] -> Mitigation: keep token names semantic, test form states manually, and validate both desktop and mobile layouts.
- [Adding route structure now may require minor refactors later when chat becomes real] -> Mitigation: keep the chat route intentionally thin and avoid premature abstractions beyond the shared shell.
- [Simplifying the model may require adapting existing stored metadata] -> Mitigation: keep read/write behavior local to the runbook package and validate with the current local storage data during implementation.

## Migration Plan

1. Introduce the shared shell, design tokens, and route structure with dedicated list, create, and runbook detail routes.
2. Simplify the domain and server-action layer to single-file runbooks with detail retrieval and deletion by typed slug confirmation.
3. Move the creation form into its own route, remove revision-related UI and APIs, and add the chat placeholder route.
4. Manually validate the runbook flows, deletion behavior, and responsive layout before shipping.

Rollback would consist of reverting the route and service changes together, since the UI and domain updates are coupled in this redesign.

## Open Questions

- None. This design assumes dedicated runbook routes, typed-slug delete confirmation, and a single-file create/list/view/delete scope.
