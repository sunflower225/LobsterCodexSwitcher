## ADDED Requirements

### Requirement: Project SHALL provide a faster global installation path

The project SHALL provide an installation path that is easier to distribute to other users than manually copying the script and editing shell PATH files.

#### Scenario: Install via standard Python toolchain

- **WHEN** a user wants to install the tool globally
- **THEN** the project MUST expose a standard Python entry point that can be consumed by tools such as pip or pipx

### Requirement: Existing install script SHALL remain supported

The project SHALL keep the existing install script path available while introducing the new global installation path.

#### Scenario: Existing user runs install.py

- **WHEN** a user continues to use the legacy install flow
- **THEN** the tool MUST remain installable through install.py without requiring the new packaging path
