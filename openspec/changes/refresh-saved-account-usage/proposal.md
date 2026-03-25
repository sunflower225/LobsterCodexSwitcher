## Why

当前“查看所有账号余量”只会直接拿各账号档案里的 `access_token` 请求 usage API。当前登录账号通常 token 较新，因此看起来能刷新；未切换到前台的存档账号随着 `access_token` 过期，只能显示旧缓存，导致余量和 5 小时 / 每周重置时间长期不准。

## What Changes

- 为已存档账号增加独立的 token 刷新链路：在不切换当前登录态的前提下，优先用存档里的 `refresh_token` 换取最新 token。
- 统一把刷新后的 token 回写到对应账号档案，避免后续继续使用过期 `access_token`。
- 在 usage 请求成功后，为所有账号写入最新的 5 小时 / 每周余量与精确重置时间。
- 当账号无法完成 token 刷新或 usage 请求失败时，保留最近一次缓存，并向界面暴露刷新状态而不是静默表现成“已刷新”。

## Capabilities

### New Capabilities

- `archived-account-usage-refresh`: 允许已存档但未激活的账号独立刷新 token、usage 和重置时间。

### Modified Capabilities

- None.

## Impact

- 影响文件: `codex-switcher.py`, `README.md`
- 新增 OpenAI OAuth refresh token 请求逻辑，调用 `https://auth.openai.com/oauth/token`
- 账号档案会在后台刷新时更新 `tokens.*` 与 `last_refresh`
- usage 缓存会包含更可靠的 `reset_at_hourly` / `reset_at_weekly` 与格式化展示字段
