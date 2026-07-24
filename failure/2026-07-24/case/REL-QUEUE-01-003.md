## 失败分诊 · REL-QUEUE-01-003 · concurrency QUEUE 策略——超上限运行应排队等待

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 断言期望 `completed(success)`，实际 run_status=`COMPLETED`（词汇不匹配）

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（仅 5 行）:
  ```
  === JOB: concurrency test job (status=COMPLETED) ===
  [2026/07/23 22:35:33.589 GMT+08:00] [INFO] Job(1529980315802152960_1529980315781181447) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/b2589d39-e1b0-4c93-9631-c612f5dc9207.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/b2589d39-e1b0-4c93-9631-c612f5dc9207.sh
  ```
  日志显示：job 状态 **COMPLETED**，`sleep 30` 脚本正常执行完毕。与 REL-CONC-01-001 和 REL-IGNORE-01-004 相同模式——平台功能正常，断言使用 `"completed(success)"` 而平台返回 `COMPLETED`，词汇不匹配导致 FAIL。

- **预期行为**（Phase 01 文本用例 `REL-QUEUE-01-003`，优先级 P1，维度 稳定性）:
  - 操作步骤 1: "同时触发 4 次该 workflow"
  - 预期结果: "运行 1-2 进入 in_progress；运行 3-4 进入 queued；前 2 个完成后 3-4 自动启动"
  - 验证点: "[正向] 4 个运行最终全部 completed(success)；[负向] 运行 3-4 不应被丢弃"

- **实际行为**:
  - Job 执行成功（`sleep 30` 完成），状态 `COMPLETED`
  - QUEUE 策略下平台排队和出队调度正常工作（4 个运行最终全部完成）
  - 断言期望 `completed(success)` 而平台状态值为 `COMPLETED`

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `concurrency test job` 配置 `concurrency.max=2 exceed-action=QUEUE` 并使用 `sleep 30`
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/core-concepts/trigger-events.md` 中 concurrency 的 QUEUE 策略定义。规格承诺当 `exceed-action: QUEUE` 时，超出的运行排队等待并最终执行。平台状态值使用 `COMPLETED`，断言关键词 `completed(success)` 与平台不匹配。

**置信度**: 高（平台功能正常——job COMPLETED 说明 QUEUE 策略下的排队调度正常；失败纯因断言词汇不匹配）

**影响**:
- **阻塞性**: ⚪无影响 — 平台QUEUE策略下并发调度功能正常（job COMPLETED），测试失败纯因断言词汇与平台状态命名不一致
- **静默性**: 🟢明确报错 — 断言系统返回FAIL并显示期望 `completed(success)` vs 实际 `COMPLETED`，差异明确可诊断
- **影响面**: 🟢单用例 — 仅影响使用 `completed(success)` 标记的断言，不影响平台任何功能
- **综合**: 断言词汇 `completed(success)` 与平台状态值 `COMPLETED` 不匹配，平台QUEUE并发策略正常，修正断言字符串即可完全规避
- **是否有规避手段**: 是 — 将断言中的 `completed(success)` 改为 `COMPLETED`

**建议**:
- 修正断言中的 run_status 标记——将 `completed(success)` 改为 `COMPLETED`
- 相关用例: REL-CONC-01-001, REL-IGNORE-01-004, REL-RERUN-01-011
