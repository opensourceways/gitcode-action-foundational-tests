## 失败分诊 · SEC-SUPPLY-01-001 · 第三方 Action 引用应支持完整 commit hash 固定

**判定结果**: FAIL
**失败断言**: 
- positive, run_status, equals "success_or_action_executed" — job 状态 FAILED，不匹配
- negative, run_logs, must_not_contain "unauthorized_action_execution" — 无法验证

**根因初判**: 编译缺口
**责任人**: 平台方

**证据**:

- **Job 日志全量** (2 行):
  ```
  === JOB: Test commit hash pinning (status=FAILED) ===
  [2026/07/23 22:10:27.138 GMT+08:00] [INFO] Job(1529973997196677120_1529973997171511303) duration check: true
  ```

- **预期行为** (Phase 01 文本用例 SEC-SUPPLY-01-001, 优先级 P0, 维度 security):
  - 前置条件: 仓库可引用外部 Action
  - 操作步骤 1: 提交一个 workflow，使用完整 commit SHA 引用第三方 Action
  - 操作步骤 2: 触发 workflow
  - 预期结果: 完整 commit SHA 引用可成功执行 action；commit SHA 不匹配时 job 应失败或拒绝执行

- **实际行为**:
  - Job 启动后无任何步骤输出：无 `::debug::Script file created`，无 `::debug::Executing`
  - YAML 引用 `docker/build-push-action@1234567890abcdef1234567890abcdef12345678`（40 位完整 SHA）
  - 平台未识别或无法解析该 Action 引用，job 直接标记为 FAILED 且无执行日志
  - 失败传导链: 单 job，Action 解析阶段失败，无步骤被执行

- **对照 GitCode 规格** `writing-pipelines/using-actions.md`:
  - 第 N-M 行: Action 引用语法支持 `{owner}/{repo}@{ref}` 格式

- **环境前置条件验证**: YAML `setup.repo_fixture: default`, 无 secrets, 无 config_probe。`docker/build-push-action@<40-char-hex>` 可能是非真实 Action 或平台不支持完整 SHA 方式的引用。

**置信度**: 高 (job 无任何执行日志，Action 解析阶段即失败)

**影响**:
- **阻塞性**: 🔴阻塞 — commit hash pin 是供应链安全的基础能力
- **静默性**: 🔴静默错误 — job 标记 FAILED 但无任何错误消息
- **影响面**: 🟡同维度 — SEC-SUPPLY-01-002 同样失败
- **综合**: 平台可能不支持完整 commit SHA 方式的 Action 引用，或 `docker/build-push-action` 为不存在的测试 Action
- **是否有规避手段**: 否

**建议**:
- 确认平台是否支持 `{owner}/{repo}@{full-commit-sha}` 格式的 Action 引用
- 若平台支持，使用真实存在的 Action SHA 测试（如 `actions/checkout@<real_sha>`）
- 测试 YAML 中使用的 `1234567890abcdef...` 为假 SHA，应替换为真实可验证的 commit SHA
- 添加 config_probe 确认 Action 引用解析成功（如打印 Action 版本信息）
