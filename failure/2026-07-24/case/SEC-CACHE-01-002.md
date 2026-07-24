## 失败分诊 · SEC-CACHE-01-002 · 主仓 cache restore 对 fork cache miss

**判定结果**: FAIL
**失败断言**: 
- negative, cache_restore, must_not_hit "fork_cache_key" — 无法验证，cache 步骤被跳过
- positive, run_logs, equals "cache_miss" — 日志中无 cache_miss，只有事件校验拒绝

**根因初判**: 用例问题
**责任人**: Phase 02

**证据**:

- **Job 日志全量** (4 行):
  ```
  === JOB: Restore cache from main repo (status=COMPLETED) ===
  [2026/07/23 22:05:10.573 GMT+08:00] [INFO] Job(1529972669225377792_1529972669187629063) duration check: true
  ::warning::Event Validation Error: The event type Manual (normalized: manual) is not supported because it's not tied to a branch or tag ref.
  ::warning::[cache eventValidation] normalized=manual allowlistMatch=false allowlist=[push|pull_request|merge_request] ATOMGIT_EVENT_NAME=Manual GITHUB_EVENT_NAME=Manual ATOMGIT_REF=main GITHUB_REF=main | hint: EVENT_NAME normalized "Manual" -> "manual" for allowlist check; event not in allowlist [push|pull_request|merge_request]
  ```

- **预期行为** (Phase 01 文本用例 SEC-CACHE-01-002, 优先级 P0, 维度 security):
  - 前置条件: fork PR 已写入 cache
  - 操作步骤 1: 在主仓触发 workflow，使用与 fork PR 相同的 cache key 尝试 restore
  - 操作步骤 2: 查看 restore 结果
  - 预期结果: cache restore 结果为 miss；日志中显示未找到对应缓存

- **实际行为**:
  - Cache 步骤被平台事件校验层拒绝执行
  - 原因: 测试 YAML 使用 `workflow_dispatch` 触发（事件名 "Manual"），但 cache action 仅支持 `push | pull_request | merge_request`
  - 系统输出明确的 allowlist 校验警告，cache restore 未实际执行

- **对照 GitCode 规格** `security-permissions/pr-mr-pipeline-security.md`:
  - 第 12 行: "执行代码来源 | fork 仓库的代码（PR 提交）"
  - 第 13 行: "ATOMGIT_TOKEN 权限 | 仅 read 权限（安全限制）"
  - 第 14 行: "Secrets 可访问性 | fork 来源不可访问项目 Secret"
  - Cache 隔离是 fork PR 安全机制的一部分，触发事件应为 `pull_request`

- **环境前置条件验证**: YAML `setup.repo_fixture: with-cache`，无 secrets 字段，无 config_probe。触发事件为 `workflow_dispatch` 而非 cache 支持的 push/PR/MR 事件。

**置信度**: 高 (cache action 的 allowlist 校验逻辑明确输出在日志中)

**影响**:
- **阻塞性**: 🟡非阻塞 — 可通过切换触发事件修复测试
- **静默性**: 🟢明确报错 — 平台给出了清晰的 Event Validation Error
- **影响面**: 🟢单用例 — 仅此用例因触发事件选择不当失败
- **综合**: 测试 YAML 的 trigger.event 选择错误，应使用 push 或 pull_request 事件
- **是否有规避手段**: 是

**建议**:
- 修改测试 YAML 的 `trigger.event` 为 `push` 或 `pull_request`（需对应 fork PR 场景）
- 或使用 `push` 事件模拟主仓触发场景
