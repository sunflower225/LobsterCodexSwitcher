## Context

当前项目已经具备较完整的交互式账号查看与切换能力，但仍然存在三个明显短板：

1. Agent 若要使用本工具，只能模拟交互流程，缺少稳定的非交互命令接口。
2. 项目内没有专用 Skill，总结当前 UI/CLI 行为、排序规则和推荐用法都依赖临时上下文。
3. 安装方式以本地复制脚本加 PATH 为主，适合作者自用，不利于其他用户快速全局部署。

## Goals / Non-Goals

**Goals:**

- 提供项目内 Skill，明确用户与 Agent 的使用入口、排序规则、典型工作流。
- 增加无交互 CLI 参数，支持 Agent 直接读取账号列表、最佳账号和切换结果。
- 为全局安装增加更标准的入口，使后续对外分发更容易。

**Non-Goals:**

- 不改写现有的核心认证/usage 刷新逻辑。
- 不在本次引入外部服务端或数据库。
- 不在本次实现 Homebrew Tap 或正式 release pipeline，只为这些路径铺基础。

## Decisions

### 1. Skill 放在项目内 `.codex/skills/`

原因:
- 该 Skill 明显服务于本项目自身，和仓库一起演进最自然。
- 使用项目内 Skill 可以让后续 Agent 在进入仓库后立刻获得本工具的用法，而不需要依赖用户安装全局 Skill。

### 2. 非交互 CLI 采用 `argparse`，与当前交互模式共存

原因:
- 现有程序已是单文件 Python CLI，用 `argparse` 增加参数最小侵入。
- 可以保留默认 UI 模式，同时为 Agent 增加稳定入口。

计划加入的命令方向:
- `--list`
- `--json`
- `--best`
- `--switch <selector>`
- `--save-current [--name <name>]`
- `--refresh`

### 3. 排序规则固定为 5 小时剩余优先，其次每周剩余

原因:
- 这是用户明确要求的 Agent 视角选择逻辑。
- 固定规则后，Skill、CLI 和 UI 都可以复用同一套排序语义。

### 4. 全局安装先做 console script 兼容，再保留 install.py

原因:
- `install.py` 适合当前用户群，不能直接丢掉。
- 增加 `pyproject.toml` 和 console script 后，后续可直接支持 `pipx install`、包管理器集成、Git URL 安装。

## Risks / Trade-offs

- [Risk] 单文件脚本继续承载 UI 和 CLI，复杂度上升 -> Mitigation: 把排序、选择器解析、输出格式抽成独立函数。
- [Risk] Skill 说明与实际 CLI 行为漂移 -> Mitigation: Skill 中只保留工作流和规则，具体参数细节放到 references 文件，并在本次实现后同步验证。
- [Risk] `pipx` / console script 改造与现有 install.py 路径冲突 -> Mitigation: 保持 `python3 install.py` 可用，新增方式作为补充而非替代。

## Migration Plan

1. 创建项目内 Skill 骨架并写入说明。
2. 为脚本增加非交互 CLI 参数与排序/JSON 输出。
3. 增加 console script 所需元数据，并更新 README/安装说明。
4. 通过真实命令验证 Skill 示例与 CLI 输出一致。

## Open Questions

- 是否需要支持 `--switch best` 这种语义快捷方式。本次可一并支持。
- JSON 输出字段是否需要进一步稳定成 API contract。本次先输出高信号字段。
