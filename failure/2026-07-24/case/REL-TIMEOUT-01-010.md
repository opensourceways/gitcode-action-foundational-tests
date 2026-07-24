## 失败分诊 · REL-TIMEOUT-01-010 · 默认超时——未声明 timeout-minutes 运行 361 分钟应被强制终止

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 job 在默认 360 分钟被终止（status=failure），实际 job status=CANCELED（346s 后被 harness 取消）；assertions[1] (positive, run_logs) — 期望日志含超时信息，实际无任何业务日志

**根因初判**: 环境/Harness

**证据**:

- **Job 日志全量**（仅 5 行）:
  ```
  === JOB: reliability test job (status=CANCELED) ===
  [2026/07/23 22:39:20.453 GMT+08:00] [INFO] Job(1529981267208966144_1529981267187994631) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/450fce2f-10bf-4da6-afe7-252b7e442e8d.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/450fce2f-10bf-4da6-afe7-252b7e442e8d.sh
  ```
  日志显示：job 状态 **CANCELED**，0 字节有效日志。与 REL-TIMEOUT-01-007/008/009 相同模式——期望不声明 `timeout-minutes`（使用默认 360min）的 job 执行 `sleep 21660`（约 361 分钟），应在 360 分钟被平台超时终止。但实际在约 346s 后就被测试 harness 取消——harness 300s 全局超时完全覆盖了平台默认 timeout-minutes 的验证。

- **预期行为**（Phase 01 文本用例 `REL-TIMEOUT-01-010`，优先级 P1，维度 稳定性）:
  - 操作步骤 1: "触发未声明 timeout-minutes 的 workflow，job 执行 sleep 21660"
  - 预期结果: "job 在 360 分钟时被终止；状态为 failure；日志含超时信息"
  - 验证点: "[正向] job 状态=failure；[负向] 不应无限运行"

- **实际行为**:
  - Job 在约 346s 后（而非 360min）被 harness 取消
  - 平台默认 timeout-minutes=360 的强制终止行为完全未被测试到
  - Job 状态 CANCELED 而非 FAILED

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `reliability test job` 未声明 `timeout-minutes`（使用默认 360 分钟），执行 `sleep 21660`
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/syntax-reference/workflow-file-location-structure.md` 中 `jobs.<job_id>.timeout-minutes` 的默认值定义。规格描述：默认 timeout 为 360 分钟（GitHub Actions 兼容默认值）。平台应在此默认超时后终止超长 job。Harness 300s 超时完全阻断了此验证。

**置信度**: 高（harness 300s 超时在 ~346s 时触发取消——`sleep 21660` 对应的 361min 远未到达；平台默认 timeout-minutes 强制终止行为完全未被测试）

**影响**:
- **阻塞性**: 🟡非阻塞 — 平台默认timeout-minutes=360强制终止行为未被测试（sleep 21660从未执行到超时点），但平台job启动和harness取消机制均正常
- **静默性**: 🟡可察觉 — job状态CANCELED可察觉被取消，但0字节有效日志无法判断是平台默认超时触发还是harness取消
- **影响面**: 🟢单用例 — 仅影响超长sleep的timeout边界测试用例（REL-TIMEOUT-01-007/008/010），不影响短时用例
- **综合**: harness 300s全局超时完全覆盖了平台默认360min timeout的验证，调整harness超时配置即可规避
- **是否有规避手段**: 是 — 将超长sleep用例的harness超时上限设置为大于平台默认timeout（如400min）

**建议**:
- 测试 harness 的超时上限需远大于平台默认 timeout-minutes（建议 400min 以上或 disable）
- 相关用例: REL-TIMEOUT-01-007, REL-TIMEOUT-01-008, REL-TIMEOUT-01-009
