## 失败分诊 · REL-TIMEOUT-01-008 · job timeout 越界触发——361 分钟应在 360 分钟被强制终止

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 job 在 360±2 分钟被平台 timeout 终止（status=failure），实际 job status=CANCELED（366s 后被 harness 取消）；assertions[1] (positive, run_logs) — 期望日志含 timeout/超时，实际无任何业务日志

**根因初判**: 环境/Harness

**证据**:

- **Job 日志全量**（仅 5 行）:
  ```
  === JOB: timeout test job (status=CANCELED) ===
  [2026/07/23 22:38:58.894 GMT+08:00] [INFO] Job(1529981176968261632_1529981176947290119) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/4a3f6acf-b88d-4976-b0cb-d0b668337590.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/4a3f6acf-b88d-4976-b0cb-d0b668337590.sh
  ```
  日志显示：job 状态 **CANCELED**，0 字节有效日志。与 REL-TIMEOUT-01-007 相同模式——期望 `timeout-minutes=360` 的 job 执行 `sleep 21660`（约 361 分钟），在平台 360 分钟超时后应被标记为 `failure` 且日志含超时信息。但实际在约 366s 后就被测试 harness 取消——harness 300s 全局超时先于平台 timeout-minutes 触发。

- **预期行为**（Phase 01 文本用例 `REL-TIMEOUT-01-008`，优先级 P1，维度 稳定性）:
  - 操作步骤 1: "触发 timeout-minutes=360 的 workflow，job 执行 sleep 21660"
  - 预期结果: "job 在 360±2 分钟时被终止；状态为 failure；日志含超时信息"
  - 验证点: "[正向] job 状态=failure；[正向] 日志含 timeout 或 超时；[负向] 不应运行超过 365 分钟"

- **实际行为**:
  - Job 在约 366s 后（而非 361min）被 harness 超时取消
  - 平台 timeout-minutes=360 的越界触发行为完全未被测试到——sleep 21660 从未执行到平台超时点
  - Job 状态 CANCELED（harness 取消）而非预期的 FAILED（平台 timeout-minutes）

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `timeout test job` 配置 `timeout-minutes: 360`，执行 `sleep 21660`
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/syntax-reference/workflow-file-location-structure.md` 中 `jobs.<job_id>.timeout-minutes` 的越界行为定义。规格描述：当 job 运行时间超过 `timeout-minutes` 时，job 被终止且标记为 failure。但 harness 300s 超时阻断了此验证——sleep 21660（361min）远未到达时就被 harness 取消。

**置信度**: 高（harness 300s 超时在 ~366s 时触发取消——`sleep 21660` 对应的 361min 远未到达；平台 timeout-minutes 越界触发行为完全未被测试）

**影响**:
- **阻塞性**: 🟡非阻塞 — 平台timeout-minutes越界触发行为未被测试（sleep 21660从未执行到超时点），但平台job启动和harness取消机制均正常
- **静默性**: 🟡可察觉 — job状态CANCELED可察觉被取消，但0字节有效日志无法判断是平台timeout触发还是harness取消
- **影响面**: 🟢单用例 — 仅影响超长sleep的timeout边界测试用例（REL-TIMEOUT-01-007/008/010），不影响短时用例
- **综合**: harness 300s全局超时先于平台360min timeout触发导致越界终止行为未被验证，调整harness超时配置即可规避
- **是否有规避手段**: 是 — 将超长sleep用例的harness超时上限设置为大于平台timeout-minutes的值（如370min）

**建议**:
- 测试 harness 的超时上限需远大于平台 timeout-minutes（建议 400min 以上或 disable）
- 相关用例: REL-TIMEOUT-01-007, REL-TIMEOUT-01-009, REL-TIMEOUT-01-010
