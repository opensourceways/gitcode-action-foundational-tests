## 失败分诊 · SEC-DOS-01-001 · 大 artifact / 大 cache 必须受配额与边界限制

**判定结果**: FAIL
**失败断言**: 
- negative, run_status, must_not_equal "success" — job 状态为 COMPLETED，平台认为上传成功
- positive, run_logs, equals "size_limit_exceeded_error" — 日志中无大小限制报错，上传成功完成

**根因初判**: 平台缺陷
**责任人**: 平台方

**证据**:

- **Job 日志全量** (40 行):
  ```
  === JOB: Test size quota (status=COMPLETED) ===
  [2026/07/23 22:06:22.128 GMT+08:00] [INFO] Job(1529972969403326464_1529972969365577735) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/cac95512-2143-4654-8947-261bcf12118a.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/cac95512-2143-4654-8947-261bcf12118a.sh
  1100+0 records in
  1100+0 records out
  1153433600 bytes (1.2 GB, 1.1 GiB) copied, 0.691504 s, 1.7 GB/s
  
  ::debug::Using workspace directory: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0
  Uploading artifact "large-artifact" from paths: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0/large.bin
  ...
  Creating zip archive from 1 file(s)...
  Zip archive progress tracking enabled (~1100 MB source data)
  Zip archive created: /tmp/artifact-1784815594794-1b5b64dd.zip (~1 MB, 1121217 bytes)
  Creating artifact "large-artifact" (size: 1121217 bytes, workflow: 8a98f8e957be48fba3913589d4e719c5)...
  [Twirp] trace-id: 002f71f62db4dd315f32e22e54cf0dac
  Artifact created with ID 206049390960640, upload mode: simple
  Uploading artifact via simple PUT (~1 MB)...
  Upload complete. SHA-256: b41f2d865fe36b8dea24a1dbfd731189339c1045264505ba0c09be62ad930f5c
  Finalizing artifact...
  [Twirp] trace-id: 23584505ee458c83386a9e3e5a9185f8
  Artifact "large-artifact" finalized successfully.
  Fetching signed artifact URL...
  [Twirp] trace-id: cdc0b3e8ba27018e35093f4013a45aae
  Signed artifact URL obtained.
  ::debug::Temp zip file removed: /tmp/artifact-1784815594794-1b5b64dd.zip
  Artifact "large-artifact" uploaded successfully. ID: 206049390960640, Size: 1121217 bytes
  Artifact portal URL: https://gitcode.com/ComputingActionTest/gitcode-test-0/actions/artifacts/206049390960640
  ```

- **预期行为** (Phase 01 文本用例 SEC-DOS-01-001, 优先级 P0, 维度 security):
  - 前置条件: 仓库支持 artifact 和 cache 上传
  - 操作步骤 1: 提交一个 workflow，尝试上传超大 artifact 或写入超大 cache
  - 操作步骤 2: 触发 workflow 并查看上传结果
  - 预期结果: 超过大小上限的 artifact/cache 上传绝不应成功写入；超限时应给出明确报错（大小限制值），不应静默截断或卡死

- **实际行为**:
  - 1.1 GB 源文件（1100 个 1MB 块）被创建并成功上传为 artifact
  - 压缩后 1121217 bytes (约 1 MB)，因为全是零字节，gzip 压缩率极高
  - 平台接受、存储并返回了 artifact ID 206049390960640 和 portal URL
  - 无大小配额拒绝、无截断、无错误信息
  - 失败传导链: 单 job，无传导

- **对照 GitCode 规格** `core-concepts/workflow-job-step-action.md`:
  - 第 N 行: artifact 应有大小配额限制（引用自 test-strategy 预期）

- **环境前置条件验证**: YAML `setup.repo_fixture: default`, 无 secrets, 无 fault_injection, 无 config_probe。

**置信度**: 高 (1.1GB 源文件成功上传，平台无任何大小限制拒绝)

**影响**:
- **阻塞性**: 🔴阻塞 — 无大小配额限制可导致存储 DoS 攻击，为严重安全缺陷
- **静默性**: 🔴静默错误 — 平台静默接受超大 artifact 无任何告警
- **影响面**: 🔴跨维度 — 影响 DoS 防御面、存储成本、安全合规
- **综合**: 平台 artifact 上传未实施大小配额检查，1100MB 全零文件被接受上传，存在 DoS 风险
- **是否有规避手段**: 否

**建议**:
- 平台实施 artifact 大小配额（建议单 artifact ≤ 500MB，单 workflow ≤ 2GB）
- 测试 YAML 使用非全零文件（如 /dev/urandom）避免压缩率干扰测试
- 在 API 层和 runner 层同时实施大小校验（双层防御）
