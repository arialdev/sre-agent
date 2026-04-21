## ADDED Requirements

### Requirement: The application SHALL provide a workspace shell aligned to the design system
The system SHALL render the `runbook-manager` web app inside a persistent workspace shell that follows `packages/runbook-manager/docs/design-system.md`, including the specified warm neutral palette, typography hierarchy, spacing rhythm, whisper borders, and soft card elevation.

#### Scenario: User opens the web app
- **WHEN** the user loads the `runbook-manager` application
- **THEN** the page SHALL present a navigation shell and content areas styled according to the design system rather than the previous ad hoc visual treatment

### Requirement: The application SHALL provide separate navigation targets for runbooks and agent chat
The system SHALL expose dedicated navigation destinations for runbook management and agent chat so that the information architecture clearly separates current functionality from future agent interactions.

#### Scenario: User navigates between primary areas
- **WHEN** the user selects a primary navigation item
- **THEN** the application SHALL display the corresponding runbook management or agent chat view within the shared shell

### Requirement: The agent chat area SHALL render a placeholder state
The system SHALL provide an agent chat view that clearly communicates that the chat capability is not implemented yet.

#### Scenario: User opens the agent chat view
- **WHEN** the user navigates to the agent chat area
- **THEN** the application SHALL display a placeholder message containing the text `coming soon`
