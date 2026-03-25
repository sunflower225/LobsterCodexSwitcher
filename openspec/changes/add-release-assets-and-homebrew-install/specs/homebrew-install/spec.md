## ADDED Requirements

### Requirement: Project SHALL support one-line Homebrew installation

The project SHALL provide a Homebrew installation path that users can execute as a single command.

#### Scenario: Install via Homebrew tap

- **WHEN** a macOS user copies the documented Homebrew command
- **THEN** the command MUST resolve to a valid public tap and installable formula

## MODIFIED Requirements

### Requirement: Project SHALL provide a faster global installation path

The project SHALL provide installation paths that are easier to distribute to other users than manually copying the script and editing shell PATH files, including a one-line Homebrew path and a one-line standard Python path.

#### Scenario: Install via standard Python toolchain

- **WHEN** a user wants to install the tool globally
- **THEN** the project MUST expose a standard Python entry point that can be consumed by tools such as pip or pipx
