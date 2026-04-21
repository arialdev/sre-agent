## ADDED Requirements

### Requirement: Users SHALL be able to upload runbooks from the web application
The system SHALL allow users to create a runbook from the web application by submitting a title, one markdown file, and optional tags through a dedicated creation view. The creation form SHALL not accept pasted markdown content or a summary field.

#### Scenario: User creates a new runbook
- **WHEN** the user submits a valid title and markdown file from the create view
- **THEN** the system SHALL create the runbook, index its content, and navigate the user to the dedicated runbook view

### Requirement: Users SHALL be able to browse and open managed runbooks
The system SHALL present a runbook library view that lists managed runbooks and allows a user to open a specific runbook in a dedicated view to inspect its title, optional tags, source file name, and readable content.

#### Scenario: User views a runbook from the library
- **WHEN** the user selects a runbook from the runbook management view
- **THEN** the application SHALL navigate to a dedicated runbook view with the selected runbook’s content and visible metadata needed for reading

### Requirement: Users SHALL be able to delete a managed runbook
The system SHALL allow a user to delete a runbook from the web application, and the deletion SHALL remove the runbook from metadata storage together with its locally stored content and indexed knowledge entries only after the user confirms the action by typing the runbook slug.

#### Scenario: User confirms runbook deletion
- **WHEN** the user enters the matching runbook slug in the confirmation popup and confirms deletion for an existing runbook
- **THEN** the system SHALL remove the runbook from the library and SHALL delete the corresponding local content and knowledge-index records

### Requirement: The runbook library SHALL separate listing from creation
The system SHALL keep the list view focused on browsing existing runbooks and SHALL expose a `Publish` navigation action that opens a separate create view for new runbooks.

#### Scenario: User starts creating a runbook from the library
- **WHEN** the user selects the `Publish` action in the list view
- **THEN** the application SHALL navigate to a dedicated create view instead of rendering the creation form inline in the library
