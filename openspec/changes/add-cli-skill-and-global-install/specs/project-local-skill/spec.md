## ADDED Requirements

### Requirement: Project SHALL include a local codex-switcher skill

The project SHALL include a repository-local Skill that explains how users and agents should operate codex-switcher in both interactive and non-interactive modes.

#### Scenario: Skill is stored in project

- **WHEN** the repository is opened by a user or agent
- **THEN** a project-local Skill MUST exist under the repository so the usage guidance is versioned with the tool

### Requirement: Skill SHALL document agent-first workflows

The Skill SHALL document the preferred agent workflows for listing accounts, selecting the best account, switching accounts, and saving the current account.

#### Scenario: Agent needs best account workflow

- **WHEN** an agent needs to choose the best available account
- **THEN** the Skill MUST explain the ranking rule and the preferred CLI command path
