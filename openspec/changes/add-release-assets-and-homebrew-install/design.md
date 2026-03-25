## Context

当前仓库已经具备可运行代码、项目内 Skill、非交互 CLI 和 Python console script，但在对外分发上还差最后一层产品化包装：

- README 缺少徽章和直观截图
- 还没有正式 release 文案与版本 tag
- Homebrew 安装尚未真正落地
- 虽然支持 `pipx install git+repo`，但 README 还可以进一步压缩成面向用户的一句话安装入口

## Goals / Non-Goals

**Goals:**

- 让 GitHub 仓库首页具备“第一次访问就能理解和安装”的信息密度。
- 建立首个正式版本 release 与 release notes。
- 提供一句命令的 Homebrew 安装路径。
- 保持 pip/pipx 路径也能一句命令安装。

**Non-Goals:**

- 不在本次发布中引入 PyPI 正式发布。
- 不在本次引入 CI/CD 自动发版流水线。
- 不修改核心账号切换逻辑。

## Decisions

### 1. 截图直接放入仓库并在 README 中展示

原因:
- 用户已提供可直接使用的实际界面截图。
- 放入仓库后，README 和 release notes 都可以稳定引用。

### 2. 采用 GitHub release + 本地 release notes 文件

原因:
- release 文案既要在 GitHub 页面展示，也要留在仓库中方便迭代。
- 本地文件可以作为后续版本模板复用。

### 3. Homebrew 采用独立 Tap 仓库

原因:
- 最符合 Homebrew 社区的分发方式。
- 用户可以直接通过 `brew install owner/tap/formula` 一句命令安装。

### 4. pip 路径继续使用 Git URL 安装

原因:
- 当前没有 PyPI 凭证和正式发布流程。
- `pipx install git+https://...` 仍然是标准、可执行、对外可复制的一句话安装方式。

## Risks / Trade-offs

- [Risk] Homebrew Formula 依赖 release tarball 的 SHA256，必须与 tag 保持一致 -> Mitigation: 先创建 tag，再基于远程 tarball 计算 SHA256。
- [Risk] README 徽章依赖 release/tag 存在 -> Mitigation: 先提交变更并打 tag，再用最终 tag 链接更新徽章。
- [Risk] Tap 仓库额外增加维护成本 -> Mitigation: 仅保存单个 formula，保持结构最简。

## Migration Plan

1. 更新 README，加入徽章、截图和一句命令安装路径。
2. 创建 release notes 文件。
3. 推送代码并创建版本 tag/release。
4. 创建 Homebrew Tap 仓库并写入 formula。
5. 最后再回写 README 中的 Homebrew 安装命令与发布链接。

## Open Questions

- 首个 release 版本号是否沿用 `0.1.0`。当前计划沿用现有 `pyproject.toml` 版本。
