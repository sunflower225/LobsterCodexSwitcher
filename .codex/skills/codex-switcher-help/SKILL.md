---
name: codex-switcher-help
description: |
  This skill should be used when Claude needs to operate, explain, or automate
  the Codex Switcher tool in this repository. Use it for: (1) listing available
  accounts, (2) selecting the best account by quota, (3) switching or saving
  accounts through non-interactive CLI commands, (4) explaining the interactive
  usage flow, or (5) choosing the fastest global installation path for other users.
---

# Codex Switcher Operator

## Overview

Use this skill to prefer stable, non-interactive `codex-switcher` commands over manual TUI driving whenever an agent needs account information or account switching. Treat the repository-local CLI contract as the primary interface; use the interactive page only when the task is explicitly UI-oriented.

## Workflow

1. Decide whether the task is read-only (`--list`, `--best`, `--json`) or state-changing (`--switch`, `--save-current`).
2. Prefer the non-interactive CLI path first. Read [references/cli.md](references/cli.md) for exact commands and selector rules.
3. When recommending installation or onboarding other users, read [references/deploy.md](references/deploy.md) and choose the fastest deployment path that fits the target audience.
4. If the user asks how to use the interactive screen, cite the repository behavior briefly and use [examples/user-usage.md](examples/user-usage.md) for concrete flows.
5. If an agent needs machine-readable output, always prefer `--json`.

## Rules

- Prefer sorted CLI output over ad-hoc filtering. The ranking rule is fixed: 5-hour remaining descending, then weekly remaining descending.
- Prefer `--switch best` or `--best --json` for agent decisions instead of re-implementing ranking logic.
- Do not describe stale or cached quota as authoritative if the CLI has already performed a fresh online refresh.
- If the task is “guide the user”, keep explanations short and point to the exact command or screen action.

## References

- CLI contract and selector rules: [references/cli.md](references/cli.md)
- Global installation and distribution paths: [references/deploy.md](references/deploy.md)
- Agent-oriented examples: [examples/agent-usage.md](examples/agent-usage.md)
- User-oriented examples: [examples/user-usage.md](examples/user-usage.md)
