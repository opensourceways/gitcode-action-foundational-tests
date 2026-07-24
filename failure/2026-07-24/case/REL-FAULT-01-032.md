## 失败分诊 · REL-FAULT-01-032 · 故障注入——artifact 上传时网络分区 30 秒后应失败并报网络错误

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 upload-artifact step 状态=failure（网络分区阻断），实际 job status=COMPLETED，上传完全成功

**根因初判**: 平台缺陷

**证据**:

- **Job 日志全量**（仅 39 行）:
  ```
  === JOB: fault injection network partition (status=COMPLETED) ===
  [2026/07/23 22:28:39.155 GMT+08:00] [INFO] Job(1529978577598689280_1529978577577717767) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/9f2ac65c-70bb-4b3a-b290-1d758dbb7c1b.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/9f2ac65c-70bb-4b3a-b290-1d758dbb7c1b.sh
  10+0 records in
  10+0 records out
  10485760 bytes (10 MB, 10 MiB) copied, 0.0335674 s, 312 MB/s

  ::debug::Using workspace directory: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-4
  Uploading artifact "net-fault-artifact" from paths: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-4/artifact.bin
  ...
  Creating artifact "net-fault-artifact" (size: 10489098 bytes, workflow: 9cc44d40850241b4aa58705d88462e1c)...
  ...
  Artifact "net-fault-artifact" finalized successfully.
  ...
  Artifact "net-fault-artifact" uploaded successfully. ID: 206054968430592, Size: 10489098 bytes
  Artifact portal URL: https://gitcode.com/ComputingActionTest/gitcode-test-4/actions/artifacts/206054968430592
  ```
  日志显示：job 状态 **COMPLETED**，10MB 文件生成成功（`10 MiB copied, 312 MB/s`），artifact 创建→上传→finalize 全流程成功——`uploaded successfully. ID: 206054968430592, Size: 10489098 bytes`。**网络分区故障注入从未施加**——整个上传流程在无网络故障情况下正常完成。

- **预期行为**（Phase 01 文本用例 `REL-FAULT-01-032`，优先级 P1，维度 稳定性）:
  - 操作步骤 1: "触发含 upload-artifact step 的 workflow，在 upload 期间注入网络分区 30 秒"
  - 预期结果: "upload-artifact step 状态=failure；日志含 network/connection/timeout 或中文等价词；不应无限挂起超过 120 秒"
  - 验证点: "[正向] upload-artifact step 状态=failure；[正向] 日志含网络错误；[负向] 不应无限挂起超过 120 秒"

- **实际行为**:
  - 上传全程无网络分区影响，10MB artifact 在 0.03s 内创建并完整上传
  - job COMPLETED，无任何网络错误日志
  - **故障注入未生效**——网络分区从未被施加到 runner 或 artifact 存储端点

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `fault injection network partition` job 的 upload-artifact step 使用 `net-fault-artifact` 名称上传 10MB 文件
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/core-concepts/runner-and-environment.md` 中故障恢复和网络容错的行为。规格期望平台在网络分区期间应报告网络错误。但本次测试中网络分区故障注入机制未生效—artifact 上传在无故障条件下成功。

**置信度**: 高（日志确凿——artifact `uploaded successfully`，网络分区故障注入机制完全未生效）

**影响**:
- **阻塞性**: 🔴阻塞 — 平台无法在artifact上传期间注入网络分区，网络故障下的artifact传输容错能力完全未验证
- **静默性**: 🔴静默错误 — artifact `uploaded successfully` 在无故障条件下完成，无任何错误，无任何日志表明故障注入未生效
- **影响面**: 🟡同维度 — 影响全部故障注入类用例（REL-FAULT-01-031/032/033），网络分区故障注入机制整体失效
- **综合**: 网络分区故障注入机制整体未生效，artifact在无网络故障条件下成功上传，平台网络容错能力完全未被测试，需平台修复故障注入基础设施
- **是否有规避手段**: 否 — 网络分区注入需要平台/harness层在runner节点上配置iptables/nftables规则

**建议**:
- 检查网络分区故障注入 harness 的实现——确认 iptables/nftables 规则是否在正确的时间点在正确的 runner 上注入
- 相关用例: REL-FAULT-01-031, REL-FAULT-01-033
