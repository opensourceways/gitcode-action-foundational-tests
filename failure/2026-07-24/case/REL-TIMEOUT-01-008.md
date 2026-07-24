## 失败分诊 · REL-TIMEOUT-01-008 · job timeout 越界触发——361 分钟应在 360 分钟被强制终止

**判定结果**: FAIL
**失败断言**: 正向/job_status expected=failure actual=CANCELED; 正向/run_logs expected=contains "timeout" actual=无法验证

**根因初判**: 环境/Harness
**责任人**: Phase 02

**证据**:

- **Job 日志全量**（5 行）:
  ```
  === JOB: timeout test job (status=CANCELED) ===
  [2026/07/23 22:38:58.894] [INFO] Job(1529981176968261632_1529981176947290119) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/4a3f6acf-b88d-4976-b0cb-d0b668337590.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/4a3f6acf-b88d-4976-b0cb-d0b668337590.sh
  ```

- **预期行为**（Phase 01 文本用例 REL-TIMEOUT-01-008，优先级 P1，维度 稳定性）:
  - 前置条件: 仓库具备 workflow 运行权限
  - 操作步骤 1: 触发 timeout-minutes=360 的 workflow，job 执行 sleep 21660
  - 预期结果: job 在 360±2 分钟时被终止; 状态为 failure; 日志含超时信息

- **实际行为**:
  - job 被 harness 标记为 CANCELED，无任何 step 执行日志
  - sleep 21660 秒 = 361 分钟，需运行约 6 小时
  - harness 在 job 开始后将其取消（而非等待 360 分钟让 platform timeout 触发）

- **对照 GitCode 规格**:
  - 同 REL-TIMEOUT-01-007

- **环境前置条件验证**: 同 REL-TIMEOUT-01-007

**置信度**: 高 (同 REL-TIMEOUT-01-007，harness 超时保护取消了长时间任务)

**影响**:
- **阻塞性**: 🟡非阻塞 — 同 REL-TIMEOUT-01-007
- **静默性**: 🟡可察觉 — CANCELED 明确
- **影响面**: 🟡同维度 — 影响所有长时间 timeout 测试
- **综合**: harness 全局超时保护前置于 platform timeout-minutes 机制，无法观测到 platform 的超时行为
- **是否有规避手段**: 是（使用加速时间模拟或为 timeout 测试去全局超时限制）

**建议**:
- 同 REL-TIMEOUT-01-007
