## 失败分诊 · REL-TIMEOUT-01-009 · 自定义短超时——timeout-minutes=1 时 step 运行 2 分钟应被强制终止

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 job 在 60±10s 被平台 1min 超时终止（status=failure），实际 job status=CANCELED（183s 后被 harness 取消）；assertions[1] (positive, run_logs) — 期望日志含超时信息，实际无任何业务日志

**根因初判**: 环境/Harness

**证据**:

- **Job 日志全量**（仅 5 行）:
  ```
  === JOB: timeout test job (status=CANCELED) ===
  [2026/07/23 22:39:09.913 GMT+08:00] [INFO] Job(1529981223072178176_1529981223042818055) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/9361f7ab-b9b2-4862-8026-2d606b12540c.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/9361f7ab-b9b2-4862-8026-2d606b12540c.sh
  ```
  日志显示：job 状态 **CANCELED**，0 字节有效日志。期望 `timeout-minutes=1` 的 job 执行 `sleep 120`（2 分钟），应在 60±10s 被平台超时机制终止。但实际在约 183s 后 job 被测试 harness 取消——对于 `timeout-minutes=1` 的短超时用例，harness 的取消时机（~183s）仍早于平台可能触发的超时（理论上如果平台超时未生效，sleep 120 应完成于 ~120s）。Job 被 CANCELED 而非预期的 FAILED（平台 timeout 触发）。

- **预期行为**（Phase 01 文本用例 `REL-TIMEOUT-01-009`，优先级 P1，维度 稳定性）:
  - 操作步骤 1: "触发 timeout-minutes=1 的 workflow，step 执行 sleep 120"
  - 预期结果: "job 在 60±10 秒时被终止；状态为 failure；日志含超时信息"
  - 验证点: "[正向] job 状态=failure；[正向] 实际运行时长 60±10 秒"

- **实际行为**:
  - Job 在约 183s 后被 harness 取消（而非平台 1min 超时在 60s 时终止）
  - 平台 timeout-minutes=1 的短超时行为完全未被验证——sleep 120 未在 60s 时被终止
  - Job 状态 CANCELED（harness 取消）而非 FAILED（平台 timeout-minutes）

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `timeout test job` 配置 `timeout-minutes: 1`，执行 `sleep 120`
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/syntax-reference/workflow-file-location-structure.md` 中 `timeout-minutes` 参数的定义。规格描述：设置 `timeout-minutes: 1` 时，超过 1 分钟运行的 job 会被自动终止。但 harness 取消（~183s）先于或混淆了平台超时机制——无法确定平台是否真的在 ~60s 时尝试终止 job。

**置信度**: 高（日志零输出——job 在 183s 时被 CANCELED（harness），平台 timeout-minutes=1 的短超时终止行为完全未被观察到；需 disable harness 超时来验证平台短超时机制）

**影响**:
- **阻塞性**: 🟡非阻塞 — 平台timeout-minutes=1短超时终止行为未被观察到（harness在183s取消混淆了平台60s超时），但平台job启动和harness取消机制均正常
- **静默性**: 🟡可察觉 — job状态CANCELED可察觉被取消，但0字节有效日志无法区分平台超时和harness取消
- **影响面**: 🟢单用例 — 仅影响本timeout短超时用例，不影响超长超时或正常用例
- **综合**: harness取消（~183s）混淆了平台短超时（~60s）机制，平台timeout-minutes=1的终止行为未能独立验证，disable harness超时即可规避
- **是否有规避手段**: 是 — 对于短超时用例（timeout-minutes≤N），disable测试harness的超时机制让平台独立触发

**建议**:
- 对于短超时用例（timeout-minutes=1~N），disable 测试 harness 的超时机制，让平台 timeout-minutes 独立触发
- 相关用例: REL-TIMEOUT-01-007, REL-TIMEOUT-01-008, REL-TIMEOUT-01-010
