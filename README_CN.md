# LobsterCodexSwitcher

面向小龙虾 / OpenClaw 工作流的 Codex 多账号切换与本地代理联动工具。

[English](./README.md)

[![License](https://img.shields.io/github/license/sunflower225/LobsterCodexSwitcher)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-3776AB?logo=python&logoColor=white)](./pyproject.toml)
[![GitHub Stars](https://img.shields.io/github/stars/sunflower225/LobsterCodexSwitcher?style=social)](https://github.com/sunflower225/LobsterCodexSwitcher/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/sunflower225/LobsterCodexSwitcher)](https://github.com/sunflower225/LobsterCodexSwitcher/commits/main)

![LobsterCodexSwitcher Screenshot](docs/images/overview.png)

## 项目来源

这个项目基于开源项目 [mileson/CJFCodexSwitcher](https://github.com/mileson/CJFCodexSwitcher) 增强而来。

这一版主要补了小龙虾 / OpenClaw 场景下真正缺的能力：

- 切换 `~/.codex/auth.json`
- 同步 `~/.cli-proxy-api`
- 自动重启本地 `cliproxyapi`
- 目标账号没有代理凭据时，自动触发 proxy OAuth 登录

## 它能做什么

`LobsterCodexSwitcher` 适合这类场景：

- 你有多个 Codex 账号
- 你要查看每个账号的 5 小时 / 每周余量
- 你要快速切换账号
- 你还要保证本地 `CLIProxyAPI` 跟着一起切，不再手动处理代理凭据

## 功能亮点

- 启动后直接进入账号列表页
- 当前账号固定显示在最前
- 实时查看 5 小时 / 每周额度与重置时间
- 当前账号自动归档
- 可以直接复用官方 `codex login` 增加账号
- 提供 Agent 友好的 CLI：`--list`、`--json`、`--best`、`--switch`、`--save-current`
- `--switch` 后自动同步本地代理凭据
- 自动重启 `com.user.cliproxyapi`
- 缺少代理凭据时自动拉起 proxy OAuth 登录

## 技术栈

| 层级 | 技术 |
|------|------|
| Runtime | Python 3 |
| Network | Python 标准库 `urllib` |
| Packaging | `pyproject.toml` + `setuptools` |
| UI | Terminal TUI |

## 安装

```bash
git clone https://github.com/sunflower225/LobsterCodexSwitcher.git
cd LobsterCodexSwitcher
python3 install.py
source ~/.zshrc  # 或 ~/.bashrc
codex-switcher
```

前置要求：

- Python 3.8+
- 本机有可用的 `codex` 命令
- 如果你要联动代理，本机还需要可用的 `cliproxyapi`

## 交互使用

工具启动后会直接进入实时账号列表。

核心字段：

- `邮箱`：账号邮箱
- `SPACE`：主要 workspace / organization 标识
- `PLAN`：计划类型，例如 `TEAM`
- `5小时`：5 小时余量与重置时间
- `每周`：每周余量与重置时间
- `[当前]`：当前正在使用的账号

底部操作：

- `Enter`：刷新页面
- `a`：调用官方 `codex login` 添加账号
- 输入 `#` 序号：切到对应账号
- `0`：退出

## CLI 命令

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

## 代理联动行为

现在执行：

```bash
codex-switcher --switch flow14662@gmail.com --json
```

除了切 `~/.codex/auth.json`，还会额外执行：

1. 在 `~/.cli-proxy-api` 里查找目标邮箱的代理凭据
2. 启用最新的一份匹配凭据
3. 禁用其它活跃代理凭据
4. 重启 `com.user.cliproxyapi`
5. 如果没有找到目标邮箱的代理凭据，就自动拉起 proxy OAuth 登录，再重试一次同步

`--json` 输出里会带一个 `proxy` 字段，包含：

- 代理联动是否成功
- 启用了哪份 auth 文件
- 是否触发了自动 proxy 登录
- 代理重启是否成功

## 项目结构

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

## 安全说明

见 [SECURITY.md](./SECURITY.md)

## 贡献方式

见 [CONTRIBUTING.md](./CONTRIBUTING.md)

## License

MIT
