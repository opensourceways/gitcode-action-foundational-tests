## 失败分诊 · REL-TIMEOUT-01-007 · job timeout 边界值——359 分钟运行应在 360 分钟边界前完成

**判定结果**: FAIL
**失败断言**: 正向/job_status expected=success actual=CANCELED; 非功能/job_duration_minutes ≤359 actual=harness取消

**根因初判**: 环境/Harness
**责任人**: Phase 02

**证据**:

- **Job 日志全量**（5 行）:
  ```
  === JOB: timeout test job (status=CANCELED) ===
  [2026/07/23 22:38:47.849] [INFO] Job(1529981130642173952_1529981130621202439) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/76228aa7-941d-4842-8876-04918777d9d6.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/76228aa7-941d-4842-8876-04918777d9d6.sh
  ```

- **预期行为**（Phase 01 文本用例 REL-TIMEOUT-01-007，优先级 P1，维度 稳定性）:
  - 前置条件: 仓库具备 workflow 运行权限
  - 操作步骤 1: 触发 timeout-minutes=360 的 workflow，job 执行 sleep 21540
  - 预期结果: job 在 359 分钟前成功完成; 状态为 success

- **实际行为**:
  - job 被标记为 CANCELED，无任何 step 执行日志
  - timeout-minutes=360, sleep 21540（359 分钟）是需要运行数小时的超长任务
  - harness 在 job 开始执行后将其取消（而非等待数小时让 sleep 自然完成）
  - 此行为属于 harness 的超时保护机制：对于动辄数小时的 timeout 测试，harness 主动取消了 job

- **对照 GitCode 规格** `phase01/inputs/gitcode-spec/core-concepts/workflow-job-step-action.md`:
  - 无直接相关规格段落；timeout-minutes 为 job 级别超时，21540 秒 sleep 理论上需运行约 6 小时

- **环境前置条件验证**: job 被调度但被 harness 提前取消

**置信度**: 高 (job 状态为 CANCELED 且无执行内容，是 harness 主动取消的结果)

**影响**:
- **阻塞性**: 🟡非阻塞 — harness 超时保护合理，但阻塞了真实 timeout 场景测试
- **静默性**: 🟡可察觉 — CANCELED 状态明确
- **影响面**: 🟡同维度 — 影响所有长时间 timeout 测试（REL-TIMEOUT-01-008/009/010）
- **综合**: harness 有整体运行超时保护，对单 job 需运行 6 小时的测试自动取消，无法验证 timeout-minutes 机制
- **是否有规避手段**: 是（缩短测试的 sleep 时间，或用加速时钟模拟长时间运行）

**建议**:
- 对 timeout 测试使用加速时间或 mock：将 sleep 时间缩短但调整 timeout-minutes 保持相对比例
- 或为 timeout 测试用例配置独立的不受全局超时保护的 harness 通道
