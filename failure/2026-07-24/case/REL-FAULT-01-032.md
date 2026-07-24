## 失败分诊 · REL-FAULT-01-032 · 故障注入——artifact 上传时网络分区 30 秒后应失败并报网络错误

**判定结果**: FAIL
**失败断言**: 正向/step_status expected=failure actual=COMPLETED; 正向/run_logs contains "network" actual=not found

**根因初判**: 环境/Harness（网络分区注入未生效——artifact 上传顺利完成）
**责任人**: Phase 02

**证据**:

- **Job 日志全量**:
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
  Uploading artifact "net-fault-artifact" from paths: .../artifact.bin
  ...
  Artifact created with ID 206054968430592, upload mode: simple
  Uploading artifact via simple PUT (~10 MB)...
  Upload complete. SHA-256: 96a82fcb46014b1dae4f366dc3209c77b1c35e17e5fe84ea2a73e23a62d5582b
  Finalizing artifact...
  [Twirp] trace-id: ff4245c8643cfe9e412c9006a9834487
  Artifact "net-fault-artifact" finalized successfully.
  ...
  Artifact "net-fault-artifact" uploaded successfully. ID: 206054968430592, Size: 10489098 bytes
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 具备故障注入能力; fixture 仓库可接受破坏性测试
  - 操作步骤: 触发含 upload-artifact step 的 workflow，在 upload 期间注入网络分区 30 秒
  - 预期结果: upload-artifact step 状态=failure; 日志含 network/connection/timeout 或中文等价词; 不应无限挂起超过 120 秒

- **实际行为**:
  - 10MB artifact 正常生成（312 MB/s）
  - upload-artifact step 通过 simple PUT 成功完成上传并 finalized
  - 日志中无任何 network/connection/timeout 错误
  - Job status=COMPLETED（非 FAILED）
  - 说明网络分区故障注入未生效——runner 与 artifact 服务的网络连接稳定
  - **失败传导链**: network_partition 未注入 → artifact 正常上传 → step_status=COMPLETED → 断言全部失败

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `test` 的 steps:
    ```yaml
    - name: generate artifact file
      run: |
        dd if=/dev/urandom of=artifact.bin bs=1M count=10
    - name: upload artifact step
      uses: upload-artifact
      with:
        name: net-fault-artifact
        path: artifact.bin
    ```
  - **测试 YAML** 中 fault_injection:
    ```yaml
    fault_injection:
      at: mid_job
      action: network_partition
      params:
        duration_seconds: 30
        target_step: 2
      recovery_expectation: explicit_error_and_rerun_success
    ```
  - **GitCode 规格** `writing-pipelines/upload-download-artifacts.md` 第 51-58 行:
    ```yaml
    steps:
      - name: Upload artifact
        uses: upload-artifact
        with:
          name: app-dist
          path: dist/
    ```
  - **逐项映射**: upload-artifact 配置正确; fault_injection 参数配置合理（mid_job/network_partition/30s/target_step:2）。但 network_partition 注入在 runner 端未生效——可能与 REL-FAULT-01-031 同样，fault injection 对 dedicate-hosted runner 的注入机制需要检查。

- **环境前置条件验证**: runner 可用，artifact 服务正常（simple PUT 成功）；所有网络请求（Twirp API 调用）均成功

**置信度**: 高（artifact 上传完整成功，无任何网络错误；明确表明网络分区注入未生效）

**影响**:
- **阻塞性**: 🟢不阻塞 — 故障注入机制问题，不影响正常功能
- **静默性**: 🟡中等 — job 静默成功，fault 期望未被触发
- **影响面**: 🟡同机制 — 影响所有依赖 fault_injection 的用例
- **综合**: test harness 的 network_partition 注入未生效；artifact 服务本身工作正常
- **是否有规避手段**: 是（检查 fault injection 实现：network_partition 是否是 iptables/tc 规则？对 dedicate-hosted runner 是否有权限执行？）

**建议**:
- 排查 test harness 的 network_partition 实现：是使用 iptables 阻断 runner 到 artifact API 的网络，还是模拟网络延时？
- 对 dedicate-hosted runner，container 内网络规则可能受到限制
- 考虑用 upload-artifact 的超时配置替代网络分区模拟
