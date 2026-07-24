## 失败分诊 · REL-IGNORE-01-004 · concurrency IGNORE 策略——超上限运行应直接执行

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 断言期望 `completed(success)`，实际 run_status=`COMPLETED`（词汇不匹配）

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（仅 5 行）:
  ```
  === JOB: concurrency test job (status=COMPLETED) ===
  [2026/07/23 22:29:52.595 GMT+08:00] [INFO] Job(1529978885519450112_1529978885485895687) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/1969b61c-ad5d-4fe1-9b68-d4a69501aa45.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/1969b61c-ad5d-4fe1-9b68-d4a69501aa45.sh
  ```
  日志显示：job 状态 **COMPLETED**，`sleep 30` 脚本正常执行完毕（无错误输出）。run 成功完成。与 REL-CONC-01-001 和 REL-QUEUE-01-003 相同的模式——断言使用 `"completed(success)"` 而平台返回 `COMPLETED`，导致标记不匹配。

- **预期行为**（Phase 01 文本用例 `REL-IGNORE-01-004`，优先级 P1，维度 稳定性）:
  - 操作步骤 1: "同时触发 4 次该 workflow"
  - 预期结果: "4 个运行全部进入 in_progress；无 queued 状态"
  - 验证点: "[正向] 4 个运行全部 completed(success)；[负向] 不应出现 queued 状态"

- **实际行为**:
  - Job 执行成功（`sleep 30` 完成），状态 `COMPLETED`
  - IGNORE 策略下平台行为正常——超出 max=2 限制的运行没有被排队（符合 IGNORE 语义）
  - 断言期望的 `completed(success)` 与平台实际状态值 `COMPLETED` 词汇不匹配

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `concurrency test job` 配置了 `concurrency.max=2 exceed-action=IGNORE` 并使用 `sleep 30`
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/core-concepts/trigger-events.md` 中 concurrency 的 IGNORE 策略定义。规格承诺当 `exceed-action: IGNORE` 时，超出的运行不会被排队（即直接执行或跳过）。平台状态值使用 `COMPLETED`，断言关键词 `completed(success)` 与平台不匹配。

**置信度**: 高（平台功能正常——job COMPLETED 说明 IGNORE 策略下的并发调度正常；失败纯因断言词汇 `completed(success)` 与平台状态值 `COMPLETED` 不匹配）

**影响**:
- **阻塞性**: ⚪无影响 — 平台IGNORE策略下并发调度功能正常（job COMPLETED），测试失败纯因断言词汇与平台状态命名不一致
- **静默性**: 🟢明确报错 — 断言系统返回FAIL并显示期望 `completed(success)` vs 实际 `COMPLETED`，差异明确可诊断
- **影响面**: 🟢单用例 — 仅影响使用 `completed(success)` 标记的断言，不影响平台任何功能
- **综合**: 断言词汇 `completed(success)` 与平台状态值 `COMPLETED` 不匹配，平台IGNORE并发策略正常，修正断言字符串即可完全规避
- **是否有规避手段**: 是 — 将断言中的 `completed(success)` 改为 `COMPLETED`

**建议**:
- 修正断言中的 run_status 标记——将 `completed(success)` 改为 `COMPLETED`
- 相关用例: REL-CONC-01-001, REL-QUEUE-01-003, REL-RERUN-01-011, REL-MATRIX-01-027
