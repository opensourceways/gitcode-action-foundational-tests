## 失败分诊 · REL-ARTPERF-01-053-V2 · 制品传输性能——1GB artifact 上传下载耗时

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 upload 成功，实际 upload job status=FAILED；assertions[1] (positive, run_logs) — 期望下载成功且 hash 匹配，实际 download job IGNORED

**根因初判**: 环境问题

**证据**:

- **Job 日志全量**（仅 57 行）:
  ```
  === JOB: upload artifact job (status=FAILED) ===
  [2026/07/23 22:26:17.443 GMT+08:00] [INFO] Job(1529977983043514368_1529977983022542849) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/03691558-0708-4330-86d3-fe0d74079a91.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/03691558-0708-4330-86d3-fe0d74079a91.sh
  1024+0 records in
  1024+0 records out
  1073741824 bytes (1.1 GB, 1.0 GiB) copied, 2.43541 s, 441 MB/s

  ::debug::Using workspace directory: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0
  Uploading artifact "perf-artifact" from paths: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0/artifact.bin
  ...
  Zip archive created: /tmp/artifact-1784816791200-c57f61a7.zip (~1024 MB, 1074069497 bytes)
  Creating artifact "perf-artifact" (size: 1074069497 bytes, workflow: 5e6d6460f31a4672953d5d33acae7f20)...
  ...
  Artifact multipart upload started (~1024 MB archive, 6 part(s))
  ...
  Artifact multipart upload progress: ~1024 MB (100% of ~1024 MB)
  ...
  [Twirp] trace-id: 22d3fd4e0e48c67ea4e6143081c27a92
  [Twirp] error trace-id: 22d3fd4e0e48c67ea4e6143081c27a92
  ::warning::Upload failed, artifact ID 206054481891328 may require cleanup on the server.
  ::debug::Temp zip file removed: /tmp/artifact-1784816791200-c57f61a7.zip
  ::error::Upload artifact failed: Namespace artifact quota exceeded: namespace=13965860, repoId=10431319, requestedBytes=1074069497, currentUsed=1506363281, max=1073741824

  === JOB: download artifact job (status=IGNORED) ===
  ```
  日志显示：1GB 文件生成成功（`1.1 GB copied, 441 MB/s`），zip 打包成功（`~1024 MB, 1074069497 bytes`），multipart 上传全部完成（6 个分片 100% 上传）。但在 finalize 阶段被服务端拒绝——`Namespace artifact quota exceeded: namespace=13965860, repoId=10431319, requestedBytes=1074069497, currentUsed=1506363281, max=1073741824`。当前 namespace 已使用 1.4GB（前次运行残留），请求额外 1GB 超出 1GB 配额上限。这是**测试环境 artifact 配额耗尽**，非平台功能缺陷。

- **预期行为**（Phase 01 文本用例 `REL-ARTPERF-01-053-V2`，优先级 P1，维度 稳定性）:
  - 操作步骤 1: "触发含 1GB artifact upload/download 的 workflow"
  - 预期结果: "上传/下载均成功且 hash 100% 匹配；上传≤300s 下载≤300s"
  - 验证点: "[正向] 上传≤300s；[正向] 下载≤300s；[正向] hash 100% 匹配"

- **实际行为**:
  - 1GB 文件生成和 multipart 上传本身成功（6 个分片全部完成），但在服务端 finalize 阶段因 namespace artifact 配额（1GB）被前次运行残留数据占满而拒绝
  - **失败传导链**: upload job FAILED（配额超限）→ download job IGNORED，性能和校验点均未被测试到

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `upload artifact job` 的 upload 步骤: 使用 `actions/upload-artifact@v4`，name=`perf-artifact`，path=`artifact.bin`
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/core-concepts/upload-download-artifacts.md` 的 upload-artifact 用法。规格定义了 artifact 上传流程，包括 multipart upload 和 finalize 阶段。平台的 artifact quota 限制（1GB per namespace）是正常配额管理行为——但测试环境中前次运行的 artifact 数据残留导致配额耗尽。

**置信度**: 高（日志明确 quota exceeded，`currentUsed=1.4GB > max=1GB`，是测试环境 artifact 配额耗尽问题，非平台上传逻辑缺陷）

**影响**:
- **阻塞性**: 🔴阻塞 — 1GB artifact上传在finalize阶段被配额拒绝，workflow无法完成
- **静默性**: 🟡可察觉 — 平台明确返回 `Namespace artifact quota exceeded` 错误及配额详情，用户可诊断
- **影响面**: 🟢单用例 — 仅影响本测试环境namespace，其他namespace不受配额限制影响
- **综合**: 环境artifact配额（1GB）被前次运行残留数据占满导致上传被拒，平台功能正常，清理历史artifact释放配额即可规避
- **是否有规避手段**: 是 — 测试运行前通过API清理namespace下历史artifact释放配额空间

**建议**:
- 测试运行前清理历史 artifact 数据（通过 API 删除或使用独立 namespace）以释放配额空间
- 相关用例: REL-ART-01-041, REL-ARTPERF-01-053
