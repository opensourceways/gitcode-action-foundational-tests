## 失败分诊 · REL-TIMEOUT-01-007 · job timeout 边界值——359 分钟运行应在 360 分钟边界前完成

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 job 在 359 分钟前 success，实际 job status=CANCELED（369s 后被 harness 强制取消，远低于 359min）；assertions[1] (positive, run_logs) — 期望日志含 sleep 21540 完成标记，实际不存在

**根因初判**: 环境/Harness

**证据**:

- **Job 日志全量**（仅 5 行）:
  ```
  === JOB: timeout test job (status=CANCELED) ===
  [2026/07/23 22:38:47.849 GMT+08:00] [INFO] Job(1529981130642173952_1529981130621202439) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/76228aa7-941d-4842-8876-04918777d9d6.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/76228aa7-941d-4842-8876-04918777d9d6.sh
  ```
  日志显示：job 状态 **CANCELED**，**无任何 shell 业务输出**（无 `sleep` 开始/结束标记，无退出错误）。脚本被执行但无输出——job 被外部取消。期望 `timeout-minutes=360` 的 job 执行 `sleep 21540`（约 359 分钟），但实际在仅约 369s 后就被取消——这是**测试 harness 的 300s 全局超时**，而非平台的 `timeout-minutes` 机制。Harness 超时先于 `sleep 21540` 完成前触发，强制取消了 job。

- **预期行为**（Phase 01 文本用例 `REL-TIMEOUT-01-007`，优先级 P1，维度 稳定性）:
  - 操作步骤 1: "触发 timeout-minutes=360 的 workflow，job 执行 sleep 21540"
  - 预期结果: "job 在 359 分钟前成功完成；状态为 success"
  - 验证点: "[正向] job 状态=success；[负向] 不应在 358 分钟前被强制终止"

- **实际行为**:
  - Job 在约 369s（而非 359min）后被测试 harness 的超时机制取消
  - 平台 timeout-minutes=360 的边界行为未被测试到——harness 层超时（~300s）远低于平台超时
  - sleep 21540 从未被执行这么久，job 状态 CANCELED 而非预期的 COMPLETED

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `timeout test job` 配置 `timeout-minutes: 360`，执行 `sleep 21540`
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/syntax-reference/workflow-file-location-structure.md` 中 `jobs.<job_id>.timeout-minutes` 参数的定义。规格描述：`timeout-minutes` 默认 360 分钟，在边界值（如 359 分钟）时 job 应正常完成。但测试 harness 的 300s 超时机制先于平台 timeout 触发——**harness 层不应覆盖平台超时设置**。

**置信度**: 高（harness 300s 超时在 ~369s 时触发取消——`sleep 21540` 对应的 359min 远未到达；日志 0 字节有效输出证明 job 被外部取消而非平台 timeout 机制触发）

**建议**:
- 针对超长 sleep 用例（如 sleep 21540=359min），测试 harness 的超时上限应设置为大于平台 timeout-minutes 的值（如 370min），或 disable harness 超时
- 相关用例: REL-TIMEOUT-01-008, REL-TIMEOUT-01-009, REL-TIMEOUT-01-010
