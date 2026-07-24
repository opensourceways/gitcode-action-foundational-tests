## 失败分诊 · REL-CANCEL-01-028 · 手动取消 workflow——运行中取消时 always() cleanup step 仍应执行

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 workflow 状态=cancelled，实际 job status=COMPLETED；assertions[1] (positive, run_logs) — 期望日志出现 "canceled"，实际未出现取消标记

**根因初判**: 用例问题

**证据**:

- **Job 日志全量**（仅 10 行）:
  ```
  === JOB: cancel semantics test job (status=COMPLETED) ===
  [2026/07/23 22:26:49.936 GMT+08:00] [INFO] Job(1529978119413174272_1529978119388008455) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/9ba3c7a9-e8da-440c-adcb-78eef9857334.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/9ba3c7a9-e8da-440c-adcb-78eef9857334.sh

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/57a424b2-69c1-4f3a-b2c1-b663a18b280c.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/57a424b2-69c1-4f3a-b2c1-b663a18b280c.sh
  cleanup executed
  ```
  日志显示：两个 shell 步骤都执行完毕——第一个 step 无业务输出（可能是 sleep 类操作），第二个 step 输出 `cleanup executed`（即 `if: ${{ always() }}` 的 cleanup step 被执行）。但 job 状态为 **COMPLETED**（非 cancelled），说明整个 job 完整执行完毕，并未在运行中被取消。测试框架未能在运行时注入取消操作。

- **预期行为**（Phase 01 文本用例 `REL-CANCEL-01-028`，优先级 P1，维度 稳定性）:
  - 操作步骤 1: "手动取消该 workflow"
  - 预期结果: "非 always step 被终止；if: ${{ always() }} 的 cleanup step 被执行；workflow 最终状态=cancelled"
  - 验证点: "[正向] 非 always step 被终止；[正向] cleanup step 日志存在且 completed；[正向] workflow 状态=cancelled"

- **实际行为**:
  - 两步骤全执行完毕，cleanup step 正常输出 `cleanup executed`，job 状态 COMPLETED——说明 workflow 从未被取消
  - 测试框架未能成功向平台发送取消请求，导致取消行为未被触发。`always()` cleanup 本身工作正常，但整个"取消"前提条件未达成。

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `cancel semantics test job` 配置了 `if: ${{ always() }}` 的 cleanup step 和一个前置的非 always step
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/syntax-reference/expressions.md` 中 `always()` 函数的行为定义——`always()` 使 step 在任何情况下执行，包括取消。但测试框架未实际触发取消操作，因此本次测试仅验证了正常流程（两个 step 均执行），未验证取消路径。

**置信度**: 中（日志确认 cancel 从未发生——job COMPLETED 而非 CANCELED，测试 harness 未注入取消操作；平台 `always()` 功能本身正常）

**影响**:
- **阻塞性**: 🟡非阻塞 — workflow完整执行完毕（COMPLETED），平台功能正常，仅取消路径未被覆盖
- **静默性**: 🟡可察觉 — job COMPLETED而非CANCELED可察觉取消未发生，但测试断言未区分"未取消"和"取消后行为异常"
- **影响面**: 🟢单用例 — 仅本用例的取消注入未触发，不影响其他用例
- **综合**: 测试harness未在job执行中成功发送取消请求，平台always()功能正常，修复harness取消注入时机即可规避
- **是否有规避手段**: 是 — 确保取消API在job进入`in_progress`状态后立即发送

**建议**:
- 修复测试 harness 的取消注入逻辑——确保在 job 执行中通过 API 发送取消请求，而非在 job 完成后
- 相关用例: 无直接关联，但与其他取消/超时类用例共享 harness 取消机制
