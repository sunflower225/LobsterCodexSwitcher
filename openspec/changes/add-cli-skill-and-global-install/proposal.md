## Why

当前 `codex-switcher` 主要面向人工交互界面使用，缺少面向 Agent 的稳定 CLI 参数，也缺少项目内的专用 Skill 去指导用户或 Agent 正确调用工具。同时，现有安装方式主要依赖手动执行 `install.py`，对后续分发给其他用户做全局安装不够顺手。

## What Changes

- 新增项目内 Skill，用于指导用户或 Agent 如何查看账号、选择最佳账号、切换账号以及理解部署方式。
- 为 `codex-switcher` 增加非交互 CLI 参数，支持列出账号、JSON 输出、按规则选择最佳账号、快速切换和快速存档。
- 补充更适合对外分发的全局安装入口，为后续 `pipx` / package manager 方式铺路。

## Capabilities

### New Capabilities

- `project-local-skill`: 在项目内提供一个可复用 Skill，指导用户和 Agent 使用 codex-switcher。
- `agent-cli-commands`: 提供面向 Agent 的非交互 CLI 参数与排序/JSON 输出能力。
- `global-install-paths`: 提供更快的全局部署入口和安装文档。

### Modified Capabilities

- None.

## Impact

- 影响文件: `codex-switcher.py`, `install.py`, `README.md`
- 新增文件: `.codex/skills/codex-switcher-help/**`, `pyproject.toml`（如采用 console script）
- 影响用户与 Agent 的调用方式：从纯交互 UI 扩展到可脚本化 CLI
