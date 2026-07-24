## 失败分诊 · REL-QUEUE-01-003 · concurrency QUEUE 策略——超上限运行应排队等待

**判定结果**: FAIL
**失败断言**: 正向/run_status expected=completed(success) actual=仅1个run记录; 非功能/queued_count expected=2 actual=无法验证

**根因初判**: 环境/Harness
**责任人**: Phase 02

**证据**:

- **Job 日志全量**（5 行）:
  ```
  === JOB: concurrency test job (status=COMPLETED) ===
  [2026/07/23 22:35:33.589] [INFO] Job(1529980315802152960_1529980315781181447) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/b2589d39-e1b0-4c93-9631-c612f5dc9207.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/b2589d39-e1b0-4c93-9631-c612f5dc9207.sh
  ```

- **预期行为**（Phase 01 文本用例 REL-QUEUE-01-003，优先级 P1，维度 稳定性）:
  - 前置条件: 仓库已配置 concurrency.max=2 exceed-action=QUEUE 的 workflow
  - 操作步骤 1: 同时触发 4 次该 workflow
  - 预期结果: 运行 1-2 进入 in_progress; 运行 3-4 进入 queued; 前 2 个完成后 3-4 自动启动

- **实际行为**:
  - 日志仅显示 1 个 run 的 1 个 job 完成
  - 无法验证运行 3-4 是否进入 queued、前 2 个完成后是否自动启动
  - harness 未正确编排 4 次并发触发

- **对照 GitCode 规格**:
  - 同 REL-CONC-01-001、REL-IGNORE-01-004

- **环境前置条件验证**: 单个 job 正常，多 run 编排缺失

**置信度**: 中 (同 REL-CONC-01-001 模式，harness 多 run 能力缺失)

**影响**:
- **阻塞性**: 🔴阻塞 — QUEUE 策略行为无法验证
- **静默性**: 🔴静默错误 — 仅 1 个 run 执行
- **影响面**: 🟡同维度 — 影响所有 concurrency 策略测试
- **综合**: 同 REL-CONC-01-001 和 REL-IGNORE-01-004，harness 多 run 触发编排能力缺失
- **是否有规避手段**: 是（harness 实现多 run 编排）

**建议**:
- 参考 REL-CONC-01-001 的建议
