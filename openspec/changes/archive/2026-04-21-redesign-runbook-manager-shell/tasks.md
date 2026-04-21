## 1. App shell and routing

- [x] 1.1 Introduce a shared `runbook-manager` workspace shell with primary navigation for `Runbooks` and `Agent Chat`
- [x] 1.2 Add a dedicated agent chat view that renders a `coming soon` placeholder inside the shared shell
- [x] 1.3 Refactor the current single-page entrypoint into route-aligned runbook management views with dedicated list, create, and runbook detail routes

## 2. Design system adoption

- [x] 2.1 Replace the existing global visual treatment with design tokens and shared styles derived from `packages/runbook-manager/docs/design-system.md`
- [x] 2.2 Restyle the runbook management surfaces to use the design system typography, spacing, cards, badges, inputs, button patterns, and modal confirmation treatment
- [x] 2.3 Validate the redesigned layout on desktop and mobile breakpoints defined by the design system

## 3. Runbook management capabilities

- [x] 3.1 Add service and server-action support for loading a single runbook with the data needed for a detail view
- [x] 3.2 Add service and server-action support for deleting a runbook, including typed-slug confirmation, metadata cleanup, stored content cleanup, and knowledge-index cleanup
- [x] 3.3 Replace the current runbook form model with a create-only flow that requires a title and markdown file, with optional tags and no summary field
- [x] 3.4 Build the runbook library UI for list browsing, dedicated runbook detail viewing, separate create navigation, and typed-slug deletion confirmation
- [x] 3.5 Remove revision, publish-new-version, inline-creation, and visible internal-ID interactions from the redesigned runbook experience

## 4. Verification

- [x] 4.1 Manually verify create, list, dedicated detail view, and typed-slug deletion flows in the web app
- [x] 4.2 Run `pnpm nx run runbook-manager:typecheck` and `pnpm nx run runbook-manager:build`
