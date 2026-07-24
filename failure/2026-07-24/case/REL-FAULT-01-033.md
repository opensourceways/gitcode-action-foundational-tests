## 失败分诊 · REL-FAULT-01-033 · 故障注入——runner 磁盘接近满时写入操作应失败并报磁盘满

**判定结果**: FAIL
**失败断言**: 正向/job_status expected=failure actual=COMPLETED; 正向/run_logs contains "No space left on device" actual=not found

**根因初判**: 环境/Harness（磁盘预填充未使磁盘满——额外 2GB 写入成功）
**责任人**: Phase 02

**证据**:

- **Job 日志全量**:
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

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 具备故障注入能力; fixture 仓库可接受破坏性测试
  - 操作步骤: 在 small runner 上预填充 49.5 GB 数据，job 再尝试写入 2 GB artifact
  - 预期结果: 写入失败; 日志含 No space left on device 或平台等价错误; job 状态=failure

- **实际行为**:
  - 预填充 step（fallocate 49.5G）未输出内容
  - 写入 step 成功写入 2GB（`dd bs=1M count=2048` → 2048+0 records），status=COMPLETED
  - 无 "No space left on device" 错误
  - 说明预填充 49.5GB 后 runner 磁盘仍有足够空间写入额外的 2GB
  - **失败传导链**: 磁盘未满 → 2GB 写入成功 → job COMPLETED → 所有断言不满足

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `test` 的 steps:
    ```yaml
    - name: prefill disk
      run: |
        fallocate -l 49.5G prefill.bin || dd if=/dev/zero of=prefill.bin bs=1M count=50688
    - name: write additional 2GB
      run: |
        dd if=/dev/zero of=extra.bin bs=1M count=2048
    ```
  - **测试 YAML** 中 fault_injection 和 runs-on:
    ```yaml
    runs-on: [ubuntu-latest, x64, small]
    ...
    fault_injection:
      at: pre_job
      action: disk_full
      params:
        pre_fill_gb: 49.5
        append_gb: 2
    ```
  - **GitCode 规格** `writing-pipelines/configure-jobs.md` 第 43-53 行:
    ```yaml
    runs-on: [ubuntu-latest, x64, small]
    ```
  - **逐项映射**: `runs-on: [ubuntu-latest, x64, small]` → 匹配规格（small flavor）; `fallocate -l 49.5G` → 预填充逻辑正确; `dd count=2048 bs=1M` (2GB) → 写入量正确。但 small runner 的实际磁盘空间可能大于预期（>51.5GB），导致填充后仍有空间。fault_injection 声明 `pre_fill_gb: 49.5` 和 `append_gb: 2` 但实际执行依赖于 runner 真实磁盘容量。

- **环境前置条件验证**: runner 可用（ubuntu-latest, x64, small），49.5G 预填充和 2GB 写入均成功；小型 runner 实际磁盘空间大于 51.5GB

**置信度**: 高（2GB 写入成功证明磁盘空间充足；预填充量不足或 runner 实际磁盘容量大于预期）

**影响**:
- **阻塞性**: 🟢不阻塞 — 不影响正常功能，仅故障注入场景不满足
- **静默性**: 🟡中等 — 预填充和写入均静默成功
- **影响面**: 🟡同用例 — 仅影响磁盘满载入用例
- **综合**: small runner 实际磁盘空间大于用例假设的 50GB，预填充 49.5G 后仍有 2GB+ 剩余空间
- **是否有规避手段**: 是（增大预填充量至接近 runner 实际磁盘容量；或使用 tmpfs/loopback 设备限制空间）

**建议**:
- 检查 small runner 实例的实际磁盘容量（df -h），调整预填充量
- 考虑使用 `dd if=/dev/zero of=prefill.bin bs=1M count=<剩余MB-100>` 动态计算填充量
- 对于不满足的测试，改用 loopback mount 固定大小文件系统来精确控制磁盘空间
