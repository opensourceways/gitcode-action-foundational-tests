## 失败分诊 · REL-FAULT-01-032 · 故障注入——artifact 上传时网络分区 30 秒后应失败并报网络错误

**判定结果**: FAIL
**失败断言**: 正向/step_status expected=failure actual=COMPLETED; 正向/run_logs expected=contains "network" actual=日志无网络错误

**根因初判**: 环境/Harness
**责任人**: Phase 02

**证据**:

- **Job 日志全量**（39 行）:
  ```
  === JOB: fault injection network partition (status=COMPLETED) ===
  [2026/07/23 22:28:39.155] [INFO] Job(1529978577598689280_1529978577577717767) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/9f2ac65c-70bb-4b3a-b290-1d758dbb7c1b.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/9f2ac65c-70bb-4b3a-b290-1d758dbb7c1b.sh
  10+0 records in
  10+0 records out
  10485760 bytes (10 MB, 10 MiB) copied, 0.0335674 s, 312 MB/s
  
  ::debug::Using workspace directory: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-4
  Uploading artifact "net-fault-artifact" from paths: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-4/artifact.bin
  ...
  Creating zip archive from 1 file(s)...
  Zip archive created: /tmp/artifact-1784816931991-fa0ea7b4.zip (~10 MB, 10489098 bytes)
  Creating artifact "net-fault-artifact" (size: 10489098 bytes, workflow: 9cc44d40850241b4aa58705d88462e1c)...
  [Twirp] trace-id: a8b986132aaaa3d8b0974fca320b0625
  Artifact created with ID 206054968430592, upload mode: simple
  Uploading artifact via simple PUT (~10 MB)...
  Upload complete. SHA-256: 96a82fcb46014b1dae4f366dc3209c77b1c35e17e5fe84ea2a73e23a62d5582b
  Finalizing artifact...
  [Twirp] trace-id: ff4245c8643cfe9e412c9006a9834487
  Artifact "net-fault-artifact" finalized successfully.
  Fetching signed artifact URL...
  [Twirp] trace-id: c2065fe1c2b16355f262b6cea6ff81ed
  Signed artifact URL obtained.
  ::debug::Temp zip file removed: /tmp/artifact-1784816931991-fa0ea7b4.zip
  Artifact "net-fault-artifact" uploaded successfully. ID: 206054968430592, Size: 10489098 bytes
  Artifact portal URL: https://gitcode.com/ComputingActionTest/gitcode-test-4/actions/artifacts/206054968430592
  ```

- **预期行为**（Phase 01 文本用例 REL-FAULT-01-032，优先级 P1，维度 稳定性）:
  - 前置条件: 具备故障注入能力; fixture 仓库可接受破坏性测试
  - 操作步骤 1: 触发含 upload-artifact step 的 workflow，在 upload 期间注入网络分区 30 秒
  - 预期结果: upload-artifact step 状态=failure; 日志含 network/connection/timeout 或中文等价词; 不应无限挂起超过 120 秒

- **实际行为**:
  - artifact 上传完全正常：10MB 文件生成 → zip → simple PUT → finalize → signed URL 获取，全流程成功
  - 无任何网络分区迹象，无网络错误日志
  - fault_injection 配置（at: mid_job, action: network_partition, duration_seconds: 30）未生效

- **对照 GitCode 规格**:
  - 无直接相关规格段落；依赖 harness 的 network_partition 注入能力

- **环境前置条件验证**: artifact 服务正常（simple PUT 成功），但故障注入未触发

**置信度**: 高 (artifact 上传全流程成功，网络分区明显未注入)

**影响**:
- **阻塞性**: 🔴阻塞 — network_partition 故障注入能力缺失
- **静默性**: 🔴静默错误 — 无任何故障注入执行的日志
- **影响面**: 🔴跨维度 — 同 REL-FAULT-01-031，故障注入能力整体缺失
- **综合**: harness network_partition 故障注入未实现或未触发，artifact 上传在无干扰环境下正常完成
- **是否有规避手段**: 否（harness 需实现真实的网络分区机制）

**建议**:
- Phase 02 确认故障注入 infrastructure（iptables/tc 规则注入、SIGKILL 信号发送等）是否已在 runner 上部署
- 故障注入模块应在日志中明确标注注入开始/结束时间戳与结果
