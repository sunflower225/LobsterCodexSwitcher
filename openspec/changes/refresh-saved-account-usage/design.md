## Context

当前脚本把“查看所有账号余量”实现为一次批量 usage 刷新，但刷新输入仅来自各档案里现成的 `access_token` 和 `account_id`。这对当前活跃账号通常有效，对长期未切换的存档账号则会因为 `access_token` 过期而失败。虽然本地 auth 档案保留了 `refresh_token` 和 `last_refresh`，但现有逻辑没有利用它们。

同时，界面展示的 5 小时 / 每周重置时间依赖 usage API 返回的 `reset_at`。一旦刷新失败，界面会继续显示旧缓存，但缺少明确状态区分，用户会误以为所有账号都被实时刷新过。

## Goals / Non-Goals

**Goals:**

- 支持未激活的已存档账号在后台独立刷新 token 和 usage。
- 将刷新后的 token 持久化回原账号档案，避免每次都依赖过期 `access_token`。
- 统一输出 5 小时 / 每周窗口的具体重置时间与剩余时长。
- 在刷新失败时保留旧缓存，但明确标识刷新结果，避免误导。

**Non-Goals:**

- 不改造账号切换流程。
- 不接入 `~/.codex/sessions/**/rollout-*.jsonl` 的本地 usage 推断逻辑。
- 不引入第三方依赖，继续只使用 Python 标准库。

## Decisions

### 1. 为每个账号引入“先刷新 token，再拉 usage”的两段式流程

原因:
- 官方 `openai/codex` 已明确使用 `https://auth.openai.com/oauth/token`、`client_id=app_EMoamEEZ73f0CkXaXp7hrann`、`grant_type=refresh_token` 进行 ChatGPT token 刷新。
- 这允许我们在不切换当前活跃登录态的前提下，为单个存档账号换新 `access_token`。

备选方案:
- 仅继续使用现有 `access_token` 请求 usage。缺点是未切换账号会持续失效。
- 读取本地 rollout 文件推断 usage。缺点是无法归属到离线账号，且数据延迟较大。

### 2. 仅在需要时刷新 token，但允许对离线账号做主动刷新

原因:
- 如果 `access_token` 看起来仍有效，可直接请求 usage，减少不必要的 refresh。
- 一旦 usage 返回 `401` / `403` 或 token 已过期，则立即执行 refresh token 流程。
- 对未激活账号，“主动刷新 token”比“盲目请求 usage 后失败”更稳定。

备选方案:
- 每次都先 refresh token。实现最简单，但会增加不必要的 refresh 次数。

### 3. 回写账号档案时只更新 token 相关字段和 `last_refresh`

原因:
- 当前账号档案本身就是 auth 快照，更新 `tokens.id_token/access_token/refresh_token/account_id` 与 `last_refresh` 就足够。
- 避免覆盖其他未知字段，兼容未来 auth.json 扩展。

### 4. 为账号信息增加显式刷新状态

原因:
- 需要把“已刷新成功”“仅使用缓存”“认证失效需要重新登录”区分开。
- 这样表格和详情页能解释为什么某个账号不是最新数据。

### 5. 批量刷新使用有界并发，而不是串行刷新

原因:
- 当前性能瓶颈主要是多个账号的网络请求串行执行，总耗时近似等于每个账号 refresh token / usage 请求时间之和。
- 将去重后的账号刷新任务并发执行，可以在不牺牲实时性的前提下明显缩短“查看余量”页面等待时间。
- 仍然保持“每个账号都请求最新在线数据”，缓存只在失败时回退，不参与主刷新路径。

备选方案:
- 继续串行请求。实现简单，但账号变多时等待时间线性增长。
- 以缓存优先。速度更快，但与“必须获取最新核心数据”的目标冲突。

## Risks / Trade-offs

- [Risk] refresh token 已过期、已失效或被轮换后旧值失效 -> Mitigation: 捕获错误并保留旧缓存，同时在 UI 中显示认证失效状态。
- [Risk] 同一账号可能同时存在当前登录档案与存档档案 -> Mitigation: 以账号文件路径为写回目标，刷新时按邮箱去重，但当前 `auth.json` 与存档文件分别独立更新。
- [Risk] OpenAI 返回的计划类型与 JWT claim 不一致 -> Mitigation: usage 成功时以 API 返回的 `plan_type` 为展示值，JWT 仅作为回退。
- [Risk] 并发刷新时多个线程同时写本地账号档案或缓存 -> Mitigation: 仅对去重后的账号身份提交一个刷新任务，避免同一账号被多个线程同时写入。

## Migration Plan

1. 新增 token refresh 帮助函数与 auth 档案写回逻辑。
2. 改造“查看所有账号余量”批量刷新逻辑，支持从文件路径刷新离线账号。
3. 为 `get_account_info` / 列表展示补充刷新状态字段。
4. 更新 README，说明未激活账号也会后台刷新以及失败时的状态含义。

## Open Questions

- 是否需要在主菜单单独增加“刷新所有账号 token”命令。目前先复用“查看所有账号余量”触发刷新。
- 当前列表是否要展示更细粒度的失败原因。先保留简短状态，避免表格过宽。
