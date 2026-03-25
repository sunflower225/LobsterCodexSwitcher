## ADDED Requirements

### Requirement: CLI SHALL support non-interactive account listing

The tool SHALL support a non-interactive command mode for listing available accounts without entering the TUI.

#### Scenario: List accounts in terminal

- **WHEN** a caller runs the list command
- **THEN** the tool MUST print accounts sorted by 5-hour remaining descending and weekly remaining descending

### Requirement: CLI SHALL support machine-readable output

The tool SHALL support JSON output for agent consumption.

#### Scenario: Request JSON output

- **WHEN** a caller requests JSON output
- **THEN** the tool MUST return structured account records including identity, plan, remaining quota, reset times, and current-account status

### Requirement: CLI SHALL support best-account selection and switching

The tool SHALL support selecting the highest-ranked account and switching accounts without entering the TUI.

#### Scenario: Query best account

- **WHEN** a caller requests the best account
- **THEN** the tool MUST return the top-ranked account according to the configured sorting rule

#### Scenario: Switch account by selector

- **WHEN** a caller provides an index, email, or explicit best selector
- **THEN** the tool MUST resolve the target account and perform the switch operation non-interactively

### Requirement: CLI SHALL support saving current account non-interactively

The tool SHALL support saving the current active account without entering the TUI.

#### Scenario: Save current account

- **WHEN** a caller invokes the save-current command
- **THEN** the tool MUST save the current account snapshot and report the result in CLI output
