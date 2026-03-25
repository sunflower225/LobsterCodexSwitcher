# CLI Reference

## Priority

Prefer these non-interactive commands before driving the TUI:

- `codex-switcher --list`
- `codex-switcher --list --json`
- `codex-switcher --best`
- `codex-switcher --best --json`
- `codex-switcher --switch <selector>`
- `codex-switcher --save-current [NAME]`
- `codex-switcher --refresh`

## Sorting Rule

All agent-facing ranking uses:

1. 5-hour remaining percentage descending
2. Weekly remaining percentage descending
3. Email ascending as final tie-breaker

## Selector Rules

`--switch <selector>` accepts:

- ranked index from the sorted list, for example `1`
- exact email, for example `user@example.com`
- explicit identity key
- `best`

## JSON Output

When `--json` is present, the tool returns structured fields such as:

- `rank`
- `email`
- `plan_type`
- `is_current`
- `is_saved`
- `identity`
- `switch_path`
- `hourly_remaining_pct`
- `weekly_remaining_pct`
- `hourly_reset_at`
- `weekly_reset_at`
- `hourly_reset`
- `weekly_reset`

For switching commands, the JSON payload also includes:

- `ok`
- `message`
- `account`
- `restart`

## Recommended Agent Usage

- Need all accounts: `codex-switcher --list --json`
- Need top candidate: `codex-switcher --best --json`
- Need direct switch: `codex-switcher --switch best`
- Need structured switch result: `codex-switcher --switch best --json`
- Need save current login snapshot: `codex-switcher --save-current`
