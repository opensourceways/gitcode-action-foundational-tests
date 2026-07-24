## 失败分诊 · REL-IGNORE-01-004 · concurrency IGNORE 策略——超上限运行应直接执行

**判定结果**: FAIL
**失败断言**: 正向/run_status expected=completed(success) actual=仅1个run记录; 负向/run_status expected=NOT queued actual=无法验证

**根因初判**: 环境/Harness
**责任人**: Phase 02

**证据**:

- **Job 日志全量**（5 行）:
  ```
  === JOB: concurrency test job (status=COMPLETED) ===
  [2026/07/23 22:29:52.595] [INFO] Job(1529978885519450112_1529978885485895687) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/1969b61c-ad5d-4fe1-9b68-d4a69501aa45.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/1969b61c-ad5d-4fe1-9b68-d4a69501aa45.sh
  ```

- **预期行为**（Phase 01 文本用例 REL-IGNORE-01-004，优先级 P1，维度 稳定性）:
  - 前置条件: 仓库已配置 concurrency.max=2 exceed-action=IGNORE 的 workflow
  - 操作步骤 1: 同时触发 4 次该 workflow
  - 预期结果: 4 个运行全部进入 in_progress; 无 queued 状态

- **实际行为**:
  - 日志仅显示 1 个 run 的 1 个 job 完成（sleep 30 执行完毕）
  - 无法验证 4 个 run 是否同时进入 in_progress、是否出现 queued
  - harness 未正确编排多 run 并发场景

- **对照 GitCode 规格**:
  - 同 REL-CONC-01-001，concurrency 测试均需 harness 的多 run 编排支持

- **环境前置条件验证**: 单个 job 正常执行，多 run 编排缺失

**置信度**: 中 (与 REL-CONC-01-001 相同模式，harness 多 run 触发能力缺失)

**影响**:
- **阻塞性**: 🔴阻塞 — IGNORE 策略行为无法验证
- **静默性**: 🔴静默错误 — 仅 1 个 run 执行
- **影响面**: 🟡同维度 — 影响所有 concurrency 策略测试
- **综合**: harness 未实现批量 run 触发编排，concurrency IGNORE/QUEUE/max 策略均无法验证
- **是否有规避手段**: 是（harness 实现多 run 编排）

**建议**:
- 同 REL-CONC-01-001，Phase 02 需实现 concurrency 测试所需的批量 run 触发和状态聚合机制
