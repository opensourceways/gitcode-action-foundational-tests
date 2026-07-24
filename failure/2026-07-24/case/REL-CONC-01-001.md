## 失败分诊 · REL-CONC-01-001 · concurrency.max=5 时同时触发 5 个运行应全部进入执行态

**判定结果**: FAIL
**失败断言**: 正向/run_status expected=completed(success) actual=仅1个run记录; 非功能/queued_to_running_latency ≤60s actual=无法验证

**根因初判**: 环境/Harness
**责任人**: Phase 02

**证据**:

- **Job 日志全量**（5 行）:
  ```
  === JOB: concurrency test job (status=COMPLETED) ===
  [2026/07/23 22:27:10.892] [INFO] Job(1529978207228936192_1529978207195381767) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/dd24ba4a-9120-473f-abbc-4663e320e1bb.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/dd24ba4a-9120-473f-abbc-4663e320e1bb.sh
  ```

- **预期行为**（Phase 01 文本用例 REL-CONC-01-001，优先级 P1，维度 稳定性）:
  - 前置条件: 仓库已配置 concurrency.max=5 的 workflow
  - 操作步骤 1: 同时通过 API 触发 5 次该 workflow
  - 预期结果: 5 个运行均进入 in_progress 状态; 全部在合理时间内完成

- **实际行为**:
  - 日志中仅出现 1 个 job（1 个 run），未体现 5 次并发触发
  - 无法验证 5 个 run 是否均进入 in_progress、是否在合理时间内完成
  - harness 未正确触发多 run 场景或未聚合多 run 的日志

- **对照 GitCode 规格** `phase01/inputs/gitcode-spec/core-concepts/trigger-events.md`:
  - 无直接相关规格段落；concurrency 功能测试需 harness 支持多 run 编排

- **环境前置条件验证**: 单个 job 可正常执行（sleep 10 完成），但多 run 触发失败

**置信度**: 中 (可能是 harness 未触发多 run，也可能是 platform concurrency 机制问题，但日志无多 run 迹象更指向 harness)

**影响**:
- **阻塞性**: 🔴阻塞 — 无法验证 concurrency 功能
- **静默性**: 🔴静默错误 — 仅 1 个 run 执行，其他 4 个未被触发或未被记录
- **影响面**: 🟡同维度 — 影响所有 concurrency 相关测试（REL-QUEUE-01-003, REL-IGNORE-01-004）
- **综合**: harness 未能正确编排多 run 并发触发场景，日志仅体现单一 run
- **是否有规避手段**: 是（harness 实现批量 API 触发 + run 状态轮询聚合）

**建议**:
- Phase 02 harness 实现 concurrency 测试的专用编排：通过 API 同时触发 N 个 run，轮询所有 run 状态并聚合日志
