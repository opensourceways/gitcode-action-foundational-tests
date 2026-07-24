## 失败分诊 · REL-ART-01-041 · 超大 artifact——100 MB artifact 上传后下游 job 应成功下载

**判定结果**: FAIL
**失败断言**: 正向/upload_status expected=success actual=FAILED; 正向/download_status expected=success actual=IGNORED; 正向/md5_match expected=true actual=N/A

**根因初判**: 产品bug
**责任人**: 平台方

**证据**:

- **Job 日志全量**（34 行）:
  ```
  === JOB: upload artifact job (status=FAILED) ===
  [2026/07/23 22:24:54.483] [INFO] Job(1529977634954158080_1529977634916409351) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/2b2bd817-068c-4ab5-9d10-4f85b9025bbc.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/2b2bd817-068c-4ab5-9d10-4f85b9025bbc.sh
  100+0 records in
  100+0 records out
  104857600 bytes (105 MB, 100 MiB) copied, 0.333898 s, 314 MB/s
  
  ::debug::Using workspace directory: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-4
  Uploading artifact "perf-artifact" from paths: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-4/artifact.bin
  ::debug::followSymbolicLinks 'true'
  ::debug::implicitDescendants 'true'
  ::debug::matchDirectories 'true'
  ::debug::omitBrokenSymbolicLinks 'true'
  ::debug::followSymbolicLinks 'true'
  ::debug::implicitDescendants 'true'
  ::debug::matchDirectories 'true'
  ::debug::omitBrokenSymbolicLinks 'true'
  ::debug::Search path '/home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-4/artifact.bin'
  Found 1 file(s) to upload
  ::debug::[diagnostic] First 1 matched file(s): /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-4/artifact.bin
  ::debug::Resolved root directory: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-4
  Creating zip archive from 1 file(s)...
  Zip archive progress tracking enabled (~100 MB source data)
  Zip archive created: /tmp/artifact-1784816707118-368d6406.zip (~100 MB, 104889728 bytes)
  Creating artifact "perf-artifact" (size: 104889728 bytes, workflow: 2604461c200e4c16b3eb4493b77328f5)...
  [Twirp] trace-id: 15a18a736f54aaf0872160258f1c1128
  [Twirp] error trace-id: 15a18a736f54aaf0872160258f1c1128
  ::debug::Temp zip file removed: /tmp/artifact-1784816707118-368d6406.zip
  ::error::Upload artifact failed: Artifact with name already exists: perf-artifact, repoId=10431338, workflowId=2604461c200e4c16b3eb4493b77328f5


  === JOB: download artifact job (status=IGNORED) ===
  ```

- **预期行为**（Phase 01 文本用例 REL-ART-01-041，优先级 P1，维度 稳定性）:
  - 前置条件: 仓库具备 artifact 使用权限
  - 操作步骤 1: 触发含 upload-artifact(100MB) 和 download-artifact 的 workflow
  - 预期结果: upload 成功; download 成功; 下载后文件 MD5 与上传前一致

- **实际行为**:
  - upload job 生成了 100MB zip，但在创建 artifact 时平台返回 `Artifact with name already exists: perf-artifact`
  - download job 因 upload 失败被直接 IGNORED
  - **失败传导链**: upload FAILED → download IGNORED → 所有正向断言不满足

- **对照 GitCode 规格**:
  - 无直接相关规格段落；artifact 名称应在同一 workflow run 内唯一，但平台拒绝了同名 artifact，说明 artifact 命名空间未正确隔离（可能是跨 run 残留）

- **环境前置条件验证**: runner 可用（100MB 文件成功生成），artifact 服务可达（Twirp 调用成功），但平台名称空间检查失败

**置信度**: 高 (artifact 名称冲突是明确的平台行为，非用例或环境问题)

**影响**:
- **阻塞性**: 🔴阻塞 — 同一 repo 下同名 artifact 无法重复上传，影响任何流程
- **静默性**: 🟢明确报错 — `error::Upload artifact failed` 明确提示
- **影响面**: 🔴跨维度 — 影响所有 artifact 上传相关用例
- **综合**: 平台 artifact 命名空间隔离不完善，同名 artifact 跨运行冲突导致上传失败
- **是否有规避手段**: 是（每次使用唯一 artifact 名称，或在测试前清理历史 artifact）

**建议**:
- 平台方需排查 artifact 命名空间隔离逻辑，确认 artifact 名称是否应在 workflow run 级别唯一
- 测试方可临时使用带 UUID 的 artifact 名称作为 workaround
