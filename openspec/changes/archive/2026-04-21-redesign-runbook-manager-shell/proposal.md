## Why

The `runbook-manager` app currently works as a functional admin surface, but its visual language and information architecture do not follow the repository design system and they do not yet reflect the product shape the team wants to ship. This change aligns the app with the Notion-inspired design system while expanding the web experience into a clearer workspace for managing runbooks and preparing for an agent chat surface.

## What Changes

- Redesign the `runbook-manager` web app to follow the typography, color, spacing, border, and layout rules defined in `packages/runbook-manager/docs/design-system.md`.
- Replace the current single-column admin page with a workspace-style interface that separates runbook management from agent access.
- Add a runbook library experience that supports creating runbooks from markdown files, browsing the runbook list, opening a dedicated runbook detail view, and deleting runbooks.
- Limit the scope to single-file runbooks with a title, one markdown file, and optional tags. Remove revision and re-publish workflows from the current plan.
- Add an agent chat view in the navigation and layout shell that intentionally shows a `"coming soon"` placeholder instead of shipping chat functionality in this change.

## Capabilities

### New Capabilities
- `runbook-workspace-shell`: A design-system-compliant application shell with navigation between runbook management and the future agent chat experience.
- `runbook-library-management`: A runbook library that supports upload, list, detail viewing, and deletion workflows for locally managed runbooks.

### Modified Capabilities

- None.

## Impact

- Affected code includes `packages/runbook-manager/app/*` and `packages/runbook-manager/src/lib/runbooks/*`.
- New server actions, routes, or service methods will be needed for runbook creation from file upload, runbook detail retrieval, and runbook deletion.
- Styling will move toward shared design tokens and layout primitives derived from the existing design system document.
- The change is limited to the web application shell and local runbook-management flows; it does not introduce live agent chat behavior, revisions, or general editing.
