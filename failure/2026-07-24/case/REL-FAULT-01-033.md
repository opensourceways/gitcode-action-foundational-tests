## 失败分诊 · REL-FAULT-01-033 · 故障注入——runner 磁盘接近满时写入操作应失败并报磁盘满

**判定结果**: FAIL
**失败断言**: 正向/job_status expected=failure actual=COMPLETED; 正向/run_logs expected=contains "No space left on device" actual=日志无磁盘满错误

**根因初判**: 环境/Harness
**责任人**: Phase 02

**证据**:

- **Job 日志全量**（12 行）:
  ```
  === JOB: fault injection disk full (status=COMPLETED) ===
  [2026/07/23 22:28:50.082] [INFO] Job(1529978623182512128_1529978623153152001) duration check: true
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

- **预期行为**（Phase 01 文本用例 REL-FAULT-01-033，优先级 P1，维度 稳定性）:
  - 前置条件: 具备故障注入能力; fixture 仓库可接受破坏性测试
  - 操作步骤 1: 在 small runner 上预填充 49.5 GB 数据，job 再尝试写入 2 GB artifact
  - 预期结果: 写入失败，日志含 No space left on device 或平台等价错误; job 状态=failure

- **实际行为**:
  - job 以 COMPLETED 状态完成
  - prefill step 静默执行（无输出），write 2GB step 成功写入 2.1 GB（2.5 GB/s 写入速度）
  - 磁盘空间充足，未触发任何磁盘满错误
  - fault_injection 配置（at: pre_job, action: disk_full, pre_fill_gb: 49.5）未生效

- **对照 GitCode 规格**:
  - 无直接相关规格段落；依赖 harness 的 disk_full 注入能力

- **环境前置条件验证**: 磁盘空间充足（2 GB 写入成功），故障注入未触发

**置信度**: 高 (2 GB 数据成功写入，磁盘满故障注入明显未生效)

**影响**:
- **阻塞性**: 🔴阻塞 — disk_full 故障注入能力缺失
- **静默性**: 🔴静默错误 — 无故障注入日志，无磁盘使用警告
- **影响面**: 🔴跨维度 — 同 REL-FAULT-01-031，故障注入能力整体缺失
- **综合**: harness disk_full 故障注入（pre-fill 49.5 GB）未执行，runner 磁盘充足，写入正常完成
- **是否有规避手段**: 否（harness 需实现 pre-fill 磁盘空间的故障注入）

**建议**:
- Phase 02 确认磁盘满故障注入是否在 runner 上实施（如 fallocate/tmpfs 限制）
- 三类故障注入（SIGKILL, network_partition, disk_full）均失败，可能是统一注入框架未部署
