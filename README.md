# LobsterCodexSwitcher

Codex account switching and local proxy syncing for OpenClaw and Lobster workflows.

[简体中文](./README_CN.md)

[![License](https://img.shields.io/github/license/sunflower225/LobsterCodexSwitcher)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-3776AB?logo=python&logoColor=white)](./pyproject.toml)
[![GitHub Stars](https://img.shields.io/github/stars/sunflower225/LobsterCodexSwitcher?style=social)](https://github.com/sunflower225/LobsterCodexSwitcher/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/sunflower225/LobsterCodexSwitcher)](https://github.com/sunflower225/LobsterCodexSwitcher/commits/main)

![LobsterCodexSwitcher Screenshot](docs/images/overview.png)

## Origin

This project is an enhanced fork of [mileson/CJFCodexSwitcher](https://github.com/mileson/CJFCodexSwitcher).

Enhancements in this fork focus on OpenClaw and Lobster operations:

- switch `~/.codex/auth.json`
- sync `~/.cli-proxy-api` to the same account
- restart local `cliproxyapi` automatically
- trigger proxy OAuth login when the target account has no local proxy credential yet

## What It Does

`LobsterCodexSwitcher` is a CLI/TUI tool for people who use multiple Codex accounts and need to:

- inspect live 5-hour and weekly quota windows
- switch accounts quickly from a ranked list
- keep the local CLI proxy aligned with the selected Codex account
- automate account selection through stable non-interactive CLI commands

## Features

- Direct startup into the live account list
- Active account shown at the top and separated from the rest
- Live refresh of quota windows and reset times
- Automatic snapshot save for the current account when needed
- Add a new account directly from the quota view via the official `codex login` flow
- Agent-friendly CLI: `--list`, `--json`, `--best`, `--switch`, `--save-current`
- Automatic local proxy auth sync after `--switch`
- Automatic local `cliproxyapi` restart after proxy auth sync
- Automatic proxy OAuth login prompt and execution when proxy credentials are missing

## Tech Stack

| Layer | Technology |
|-------|------------|
| Runtime | Python 3 |
| Network | Python stdlib `urllib` |
| Packaging | `pyproject.toml` + `setuptools` |
| UI | Terminal TUI |

## Install

```bash
git clone https://github.com/sunflower225/LobsterCodexSwitcher.git
cd LobsterCodexSwitcher
python3 install.py
source ~/.zshrc  # or ~/.bashrc
codex-switcher
```

Requirements:

- Python 3.8+
- A working `codex` CLI on your machine
- A working local `cliproxyapi` if you want proxy sync

## Interactive Usage

The tool opens directly into the live account view.

Key fields:

- `邮箱`: account email
- `SPACE`: primary workspace / organization label for the account
- `PLAN`: plan type such as `TEAM`
- `5小时`: 5-hour remaining amount and next reset time
- `每周`: weekly remaining amount and next reset time
- `[当前]`: the active account, shown first

Bottom actions:

- `Enter`: refresh current page
- `a`: start the official `codex login` flow, then auto-save the authenticated account and keep it active
- `#`: switch to the selected account
- `0`: exit the tool

## CLI Commands

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

## Proxy Sync Behavior

After `codex-switcher --switch ...`, the tool now also handles local proxy state:

1. Finds matching auth files under `~/.cli-proxy-api`
2. Enables the newest matching auth file for the selected email
3. Disables other active auth files
4. Restarts `com.user.cliproxyapi`
5. If no proxy auth exists for that email, runs proxy OAuth login and retries sync

Example:

```bash
codex-switcher --switch flow14662@gmail.com --json
```

The JSON output includes a `proxy` block showing:

- whether proxy sync succeeded
- which auth file was enabled
- whether a proxy login attempt was triggered
- whether the local proxy restart succeeded

## OpenClaw / Lobster Example

If your OpenClaw gateway uses a local `CLIProxyAPI`, this is the practical flow:

```bash
codex-switcher --switch flow14662@gmail.com --json
```

What happens:

1. `~/.codex/auth.json` switches to the selected Codex account
2. `~/.cli-proxy-api` is reconciled to the same email
3. `com.user.cliproxyapi` is restarted
4. OpenClaw can immediately keep using the matching proxy account

This removes the old manual sequence of:

- switching the Codex account
- checking which proxy auth file is active
- disabling stale proxy auth files
- restarting `cliproxyapi`

## Project Structure

```text
LobsterCodexSwitcher/
├── codex_switcher.py
├── codex-switcher.py
├── install.py
├── pyproject.toml
├── README.md
├── README_CN.md
├── tests/
└── docs/
```

## Security

See [SECURITY.md](./SECURITY.md).

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## License

MIT
