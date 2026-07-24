## 失败分诊 · REL-FAULT-01-033 · 故障注入——runner 磁盘接近满时写入操作应失败并报磁盘满

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 job 状态=failure（磁盘满拒绝写入），实际 job status=COMPLETED，2GB 写入成功

**根因初判**: 平台缺陷

**证据**:

- **Job 日志全量**（仅 12 行）:
  ```
  === JOB: fault injection disk full (status=COMPLETED) ===
  [2026/07/23 22:28:50.082 GMT+08:00] [INFO] Job(1529978623182512128_1529978623153152001) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/8152ff3d-2caf-440c-bc72-b2d3acaf10f8.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/8152ff3d-2caf-440c-bc72-b2d3acaf10f8.sh

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/165d32cc-03b5-48f4-9513-5d7774890842.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/165d32cc-03b5-48f4-9513-5d7774890842.sh
  2048+0 records in
  2048+0 records out
  2147483648 bytes (2.1 GB, 2.0 GiB) copied, 0.858863 s, 2.5 GB/s
  ```
  日志显示：job 状态 **COMPLETED**，2GB 数据写入成功——`2147483648 bytes (2.1 GB, 2.0 GiB) copied, 2.5 GB/s`。**磁盘满故障注入从未施加**——在"预填充 49.5 GB"的前提下，2GB 写入应触发 `No space left on device`，但实际写入在 0.86s 内以 2.5 GB/s 的速度完成，磁盘空间充足。

- **预期行为**（Phase 01 文本用例 `REL-FAULT-01-033`，优先级 P1，维度 稳定性）:
  - 操作步骤 1: "在 small runner 上预填充 49.5 GB 数据，job 再尝试写入 2 GB artifact"
  - 预期结果: "写入失败，日志含 No space left on device 或平台等价错误；job 状态=failure"
  - 验证点: "[正向] job 状态=failure；[正向] 日志含磁盘满错误"

- **实际行为**:
  - 2GB 文件在 0.86s 内以 2.5 GB/s 速度正常写入
  - 无任何磁盘满错误——`No space left on device` 未出现
  - **故障注入未生效**——磁盘预填充未被执行，或 runner 磁盘空间远大于 50GB

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `fault injection disk full` job 设计为 step_1 预填充磁盘，step_2 尝试写入 2GB 数据
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/core-concepts/runner-and-environment.md` 中 runner 资源限制和错误处理的行为。规格描述当磁盘空间不足时 job 应报告 `No space left on device` 错误。但本次测试中预填充步骤被静默跳过或 runner 磁盘容量远超预期——2GB 写入在 0.86s 内成功，磁盘满故障注入机制未生效。

**置信度**: 高（日志确凿——2GB 写入成功 `2.1 GB copied, 2.5 GB/s`，磁盘满故障注入完全未生效）

**影响**:
- **阻塞性**: 🔴阻塞 — 平台无法在runner上施加磁盘满故障，磁盘空间耗尽时的job错误处理能力完全未验证
- **静默性**: 🔴静默错误 — 2GB写入在0.86s内以2.5GB/s速度成功完成，无任何磁盘满错误，无日志表明预填充未执行
- **影响面**: 🟡同维度 — 影响全部故障注入类用例（REL-FAULT-01-031/032/033），磁盘满故障注入机制整体失效
- **综合**: 磁盘预填充步骤静默跳过，2GB写入在充足空间中成功完成，job磁盘满错误处理能力完全未被测试，需平台修复故障注入基础设施
- **是否有规避手段**: 否 — 磁盘满模拟需要平台/harness层在runner节点上预填充磁盘空间

**建议**:
- 检查 step_1 预填充 49.5GB 的脚本是否实际执行（日志显示 step_1 无输出——可能为空步骤或失败后静默继续）
- 确认 runner 磁盘容量和故障注入 harness 的预填充逻辑
- 相关用例: REL-FAULT-01-031, REL-FAULT-01-032
