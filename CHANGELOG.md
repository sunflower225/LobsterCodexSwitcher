# Changelog

## v0.2.0

### Changes

- Rebrand the project as `LobsterCodexSwitcher` while keeping the existing `codex-switcher` and `csw` CLI commands intact
- Document the project as an enhanced fork of `mileson/CJFCodexSwitcher` for OpenClaw and Lobster workflows
- Add automatic local proxy auth synchronization after account switches
- Add automatic local `cliproxyapi` restart after proxy auth synchronization
- Add automatic proxy OAuth login fallback when the selected account has no local proxy credential yet

### Fixes

- Avoid stale `~/.cli-proxy-api` credentials staying active after switching `~/.codex/auth.json`
- Make `--switch` return machine-readable proxy sync results for agents and scripts
- Keep proxy sync available even when the selected account is already the current account
