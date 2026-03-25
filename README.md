# CJFCodexSwitcher

Fast switching and quota inspection for multiple Codex accounts.

[简体中文](./README_CN.md)

[![Release](https://img.shields.io/github/v/release/mileson/CJFCodexSwitcher?display_name=tag)](https://github.com/mileson/CJFCodexSwitcher/releases)
[![License](https://img.shields.io/github/license/mileson/CJFCodexSwitcher)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-3776AB?logo=python&logoColor=white)](./pyproject.toml)
[![Homebrew](https://img.shields.io/badge/Homebrew-installable-FBB040?logo=homebrew&logoColor=black)](https://github.com/mileson/homebrew-cjfcodexswitcher)
[![GitHub Stars](https://img.shields.io/github/stars/mileson/CJFCodexSwitcher?style=social)](https://github.com/mileson/CJFCodexSwitcher/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/mileson/CJFCodexSwitcher)](https://github.com/mileson/CJFCodexSwitcher/commits/main)
[![Downloads](https://img.shields.io/github/downloads/mileson/CJFCodexSwitcher/total)](https://github.com/mileson/CJFCodexSwitcher/releases)

![CJFCodexSwitcher Screenshot](docs/images/overview.png)

## Features

- View live 5-hour and weekly quota windows for multiple Codex accounts
- Start directly in the account list page without a separate main menu
- Highlight the active account and keep it visually separated from the rest
- Auto-refresh the page after switching accounts
- Concurrent live refresh for better response time
- Agent-friendly CLI commands: `--list`, `--json`, `--best`, `--switch`, `--save-current`
- Repository-local skill for guided agent usage

## Tech Stack

| Layer | Technology |
|-------|------------|
| Runtime | Python 3 |
| Network | Python stdlib `urllib` |
| Packaging | `pyproject.toml` + `setuptools` |
| UI | Terminal TUI |

## One-Line Install

```bash
brew tap mileson/cjfcodexswitcher && brew install cjfcodexswitcher
```

```bash
pipx install git+https://github.com/mileson/CJFCodexSwitcher.git
```

If you do not use `pipx`:

```bash
python3 -m pip install "git+https://github.com/mileson/CJFCodexSwitcher.git"
```

## Quick Start

Requirements:

- Python 3.8+
- An existing local Codex login (`~/.codex/auth.json`)

Install from source:

```bash
git clone https://github.com/mileson/CJFCodexSwitcher.git
cd CJFCodexSwitcher
python3 install.py
source ~/.zshrc  # or ~/.bashrc
codex-switcher
```

## Interactive Usage

The tool opens directly into the live account view.

Key fields:

- `邮箱`: account email
- `5小时`: 5-hour remaining quota and next reset time
- `每周`: weekly remaining quota and next reset time
- `PLAN`: plan type such as `TEAM`
- `[当前]`: the active account, rendered at the top with visual separation

Bottom actions:

- `Enter`: refresh current page
- `#`: switch to the selected account
- `0`: exit the tool

The current account is auto-saved when it first appears in the live view.

## Agent / CLI Commands

```bash
codex-switcher --list
codex-switcher --list --json
codex-switcher --best
codex-switcher --best --json
codex-switcher --switch 2
codex-switcher --switch user@example.com
codex-switcher --switch best
codex-switcher --switch best --json
codex-switcher --save-current
codex-switcher --refresh
```

Ranking rule:

1. Sort by 5-hour remaining count descending
2. If tied, sort by weekly remaining count descending
3. Use email ascending as the final tie-breaker

## Agent Prompt

Use the repository-local skill:

```text
/Users/mileson/codex-switcher/.codex/skills/codex-switcher-help/SKILL.md
```

Then prefer non-interactive commands such as `--list --json`, `--best --json`, and `--switch best --json`.

## Project Structure

```text
CJFCodexSwitcher/
├── codex_switcher.py
├── codex-switcher.py
├── install.py
├── pyproject.toml
├── README.md
├── README_CN.md
├── .codex/skills/codex-switcher-help/
└── docs/
```

## Security

- Local account snapshots, usage caches, backups, and runtime scripts must stay out of version control
- Real account data remains local on your machine
- See [SECURITY.md](./SECURITY.md) for disclosure guidance

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for contribution guidelines.

## Release

Current recommended release notes:

- [v0.1.2 Release Notes](docs/releases/v0.1.2.md)

## License

MIT
