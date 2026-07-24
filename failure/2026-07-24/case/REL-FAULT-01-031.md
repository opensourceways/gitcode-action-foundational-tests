## 失败分诊 · REL-FAULT-01-031 · 故障注入——job 执行中 runner 进程被 SIGKILL 后应记录失败并保留已执行日志

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 job 状态=failure（被 SIGKILL 强制终止），实际 job status=COMPLETED，所有 step 正常执行完成

**根因初判**: 平台缺陷

**证据**:

- **Job 日志全量**（仅 25 行）:
  ```
  === JOB: fault injection SIGKILL (status=COMPLETED) ===
  [2026/07/23 22:28:25.487 GMT+08:00] [INFO] Job(1529978520157822976_1529978520124268551) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/19155db2-7af6-4510-b96f-d97cab632ffa.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/19155db2-7af6-4510-b96f-d97cab632ffa.sh
  step_one_marker

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/5facc260-54cf-47de-aec2-472fe5d04f45.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/5facc260-54cf-47de-aec2-472fe5d04f45.sh
  step_two_marker

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/e0b6526d-f857-4b0c-81ce-e4d239df2596.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/e0b6526d-f857-4b0c-81ce-e4d239df2596.sh

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/814d2183-2200-4e74-ba82-cf63d7ab8243.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/814d2183-2200-4e74-ba82-cf63d7ab8243.sh
  step_four_marker

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/1d286a0d-7419-4fbc-b3fc-233882a2c14e.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/1d286a0d-7419-4fbc-b3fc-233882a2c14e.sh
  step_five_marker
  ```
  日志显示：job 状态 **COMPLETED**，step_1 到 step_5 全部正常输出 marker（`step_one_marker`、`step_two_marker`、`step_four_marker`、`step_five_marker`）。预期在第 3 个 step 时注入 SIGKILL——但 step 3 的脚本无输出（可能是 sleep 或无操作步骤），随后 step 4 和 5 继续正常执行。**SIGKILL 从未施加**，故障注入机制未生效。

- **预期行为**（Phase 01 文本用例 `REL-FAULT-01-031`，优先级 P1，维度 稳定性）:
  - 操作步骤 1: "触发 workflow，在 job 执行到第 3 个 step 时对 runner 进程注入 SIGKILL"
  - 预期结果: "job 状态=failure；step 1-2 的日志完整可查看；step 3 日志不完整或标记为中断"
  - 验证点: "[正向] job 状态=failure；[正向] step 1-2 日志完整；[负向] 不应状态=in_progress 挂起超过 5 分钟"

- **实际行为**:
  - 全部 5 个 step 完整执行完毕，step 1/2/4/5 均有日志输出
  - job 状态 COMPLETED（而非预期的 FAILED）
  - **故障注入未生效**——SIGKILL 从未被发送到 runner 进程

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `fault injection SIGKILL` job 设计了 5 个 step，预期在第 3 个 step 执行时由外部注入 SIGKILL
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/core-concepts/runner-and-environment.md` 中 runner 进程管理和故障恢复的行为。规格描述 runner 进程被异常终止时 job 应标记为失败。但本次测试中故障注入未施加——所有 step 正常完成，说明故障注入机制（harness 层或平台 API 层）未触发。

**置信度**: 高（日志确凿——step 1/2/4/5 全部输出 marker 且 job COMPLETED，SIGKILL 故障注入未生效）

**影响**:
- **阻塞性**: 🔴阻塞 — 平台无法在job运行时施加SIGKILL故障，故障恢复路径完全无法被验证，存在运行时可靠性盲区
- **静默性**: 🔴静默错误 — 所有step正常完成（COMPLETED），无任何错误、无任何日志表明故障注入未生效，静默跳过了关键安全验证
- **影响面**: 🟡同维度 — 影响全部故障注入类用例（REL-FAULT-01-031/032/033），故障注入机制整体失效
- **综合**: SIGKILL故障注入机制整体未生效，所有step在无故障条件下正常完成，job容错和故障恢复能力完全未被测试，需平台修复故障注入基础设施
- **是否有规避手段**: 否 — 故障注入是平台级能力，单用例层面无法注入SIGKILL到runner进程

**建议**:
- 检查故障注入 harness 的实现——确认 SIGKILL 发送时机（是否在正确的时间点发送到正确的 PID）和发送权限
- 相关用例: REL-FAULT-01-032, REL-FAULT-01-033
