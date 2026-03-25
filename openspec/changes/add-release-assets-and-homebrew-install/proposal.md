## Why

仓库已经公开，但还缺少发布级资产：README 徽章、直观截图、正式 release 文案，以及真正可以“一句命令安装”的 Homebrew / pip 路径。这些缺口会直接影响新用户首次理解和安装成功率。

## What Changes

- 为 README 增加发布级徽章、产品截图和压缩后的安装命令。
- 新增 release notes 文案，并创建首个正式 GitHub release。
- 增加 Homebrew Tap / Formula，使 macOS 用户可以一句命令安装。
- 优化 pip / pipx 安装说明，保持面向新手和 Agent 的可复制命令。

## Capabilities

### New Capabilities

- `release-assets`: 提供截图、徽章和正式 release 文案。
- `homebrew-install`: 提供可用的 Homebrew 一句命令安装路径。

### Modified Capabilities

- `global-install-paths`: 将更快的全局安装从“准备路径”升级为用户可直接执行的一句命令。

## Impact

- 影响文件: `README.md`, `pyproject.toml`
- 新增文件: `docs/images/**`, `docs/releases/**`
- 新增远程仓库: Homebrew Tap 仓库
- 影响 GitHub 发布流程：新增 tag 和 release
