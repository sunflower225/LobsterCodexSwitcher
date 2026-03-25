## ADDED Requirements

### Requirement: Archived accounts SHALL refresh usage without becoming active

The system SHALL refresh authentication data and usage for archived inactive accounts during account list viewing without requiring those accounts to become the active login.

#### Scenario: Refresh archived account with valid refresh token

- **WHEN** 用户执行“查看所有账号余量”，且某个已存档账号具备 `refresh_token` 与 `account_id`
- **THEN** 系统必须能够在不替换当前 `~/.codex/auth.json` 的前提下，为该账号获取可用 token 并拉取最新 usage

### Requirement: Refreshed tokens SHALL be persisted back to the source auth snapshot

The system SHALL persist refreshed token fields back to the source auth snapshot after a successful refresh-token exchange so later refreshes do not rely on stale access tokens.

#### Scenario: Persist refreshed tokens

- **WHEN** 某个账号的 refresh token 请求成功并返回新的 `access_token`、`refresh_token` 或 `id_token`
- **THEN** 系统必须更新该账号源文件中的对应 token 字段与 `last_refresh`

### Requirement: Usage refresh SHALL expose both 5-hour and weekly reset times

The system SHALL store and present both the 5-hour and weekly reset timestamps returned by the usage API so users can see current quota and the next recovery time.

#### Scenario: Format reset times from usage response

- **WHEN** usage API 返回 `primary_window.reset_at` 或 `secondary_window.reset_at`
- **THEN** 系统必须保存原始时间戳，并生成用户可读的“今天 HH:MM (剩余时长)”格式展示文本

#### Scenario: Render compact reset times in account list

- **WHEN** 账号列表展示 5 小时和每周剩余量
- **THEN** 系统必须在剩余百分比后追加紧凑的下次重置时间，例如 `剩余16%(18:55)`，并在跨天时显示带日期的紧凑时间

### Requirement: Failed archived refresh SHALL fall back to cached usage with explicit status

The system MUST preserve the last known cached usage when an archived-account refresh fails, and it MUST expose a non-success refresh status instead of implying the account was refreshed successfully.

#### Scenario: Keep cache on refresh failure

- **WHEN** 存档账号的 refresh token 已失效，或 usage API 请求失败
- **THEN** 系统必须保留已有 usage 缓存，并在账号状态中标记该账号使用的是缓存或需要重新登录

### Requirement: Usage view SHALL merge the active account into the main list

The system SHALL render the current active account inside the same account table as archived accounts instead of showing a separate current-account detail block at the top.

#### Scenario: Render unified account list

- **WHEN** 用户进入“查看所有账号余量”
- **THEN** 系统必须输出单一账号列表，并在当前激活账号所在行标记其为 `[当前]`

### Requirement: Usage view SHALL provide plan and inline actions

The system SHALL include a plan column in the unified list, and it SHALL provide inline actions for saving the current unsaved account and switching accounts by row number.

#### Scenario: Show plan column

- **WHEN** 系统渲染账号列表
- **THEN** 每一行必须包含计划类型列，例如 `TEAM`、`PLUS`

#### Scenario: Offer save action for current unsaved account

- **WHEN** 当前登录账号尚未存档
- **THEN** 列表底部必须显示可直接确认的存档操作入口

#### Scenario: Switch by list index

- **WHEN** 用户在查看余量页面输入某个 `#` 序号
- **THEN** 系统必须根据该行对应账号执行切换登录，而不要求先进入单独的切换菜单

#### Scenario: Show refresh progress as a progress bar

- **WHEN** 系统正在批量刷新账号 usage
- **THEN** 界面必须显示紧凑的刷新进度条和已完成数量，而不是逐行输出 bullet 列表

#### Scenario: Refresh accounts concurrently with live data

- **WHEN** 系统批量刷新多个账号的 usage
- **THEN** 系统必须并发请求各账号的最新在线 usage 数据，而不是按账号串行阻塞刷新

#### Scenario: Restart Codex sessions after switching

- **WHEN** 用户切换到另一个账号且切换成功
- **THEN** 系统必须安排后台任务关闭当前运行中的 Codex Desktop 与 Codex CLI，并且只按检测到的客户端实例数量重新拉起 Codex Desktop

#### Scenario: Open directly into usage view

- **WHEN** 用户启动工具
- **THEN** 系统必须直接进入查看余量页面，而不是先显示主菜单

#### Scenario: Refresh or exit from usage view

- **WHEN** 用户位于查看余量页面
- **THEN** 系统必须允许用户通过 `Enter` 刷新当前页面，并通过 `0` 直接退出工具

#### Scenario: Stay in usage view after switching

- **WHEN** 用户在查看余量页面切换账号成功
- **THEN** 系统不得主动退出当前工具进程，而是应在提示后保持或刷新当前页面

#### Scenario: Auto refresh after successful switch

- **WHEN** 用户切换账号成功且重启任务已安排
- **THEN** 系统不得等待用户按回车确认，而是应自动回到查看余量页面并刷新，以便新账号被识别为 `[当前]`
