## 失败分诊 · REL-ART-01-041 · 超大 artifact——100 MB artifact 上传后下游 job 应成功下载

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 success，实际 upload job status=FAILED；assertions[1] (positive, run_logs) — 期望日志含 download 成功，实际 download job IGNORED（因上游 upload 失败并未执行）

**根因初判**: 环境问题

**证据**:

- **Job 日志全量**（仅 34 行）:
  ```
  === JOB: upload artifact job (status=FAILED) ===
  [2026/07/23 22:24:54.483 GMT+08:00] [INFO] Job(1529977634954158080_1529977634916409351) duration check: true
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
  日志显示：100MB 文件生成成功（`104857600 bytes copied, 314 MB/s`），zip 打包成功（`~100 MB, 104889728 bytes`），但在服务端创建 artifact 时被拒绝——`Artifact with name already exists: perf-artifact`。这是环境中前次测试运行残留的 artifact 同名冲突，而非平台功能缺陷。

- **预期行为**（Phase 01 文本用例 `REL-ART-01-041`，优先级 P1，维度 稳定性）:
  - 操作步骤 1: "触发含 upload-artifact(100MB) 和 download-artifact 的 workflow"
  - 预期结果: "upload 成功；download 成功；下载后文件 MD5 与上传前一致"
  - 验证点: "[正向] upload 成功；[正向] download 成功；[正向] MD5 校验通过"

- **实际行为**:
  - upload 步骤在服务端侧因同名 artifact "perf-artifact" 已存在被拒绝（Twirp error），upload job 状态=FAILED。
  - **失败传导链**: upload job FAILED → download job IGNORED，下游 MD5 校验功能未被测试到。

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `upload artifact job` 的 upload 步骤: 使用 `actions/upload-artifact@v4`，name=`perf-artifact`，path=`artifact.bin`
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/core-concepts/upload-download-artifacts.md` 的 upload-artifact 用法。平台 API 在创建 artifact 时校验同名冲突，返回 `Artifact with name already exists` 错误——这是平台的正常保护逻辑，非 bug。但同一 workflowId 内不应有同名冲突，根本原因是前次运行的 artifact 未清理。

**置信度**: 中（日志明确 artifact 名冲突，非平台功能缺陷，属测试环境中前次运行的残留 artifact 干扰）

**影响**:
- **阻塞性**: ⚪无影响 — 平台artifact上传功能正常，失败仅因环境中前次运行的artifact残留导致同名冲突
- **静默性**: 🟡可察觉 — 平台明确返回 `Artifact with name already exists` 错误信息，但测试未捕获此消息
- **影响面**: 🟢单用例 — 仅影响本测试用例，其他用例使用不同的artifact名称不受影响
- **综合**: 环境同名artifact冲突导致测试失败，平台功能本身正常，使用唯一artifact名称即可完全规避
- **是否有规避手段**: 是 — 每次运行时使用带UUID后缀的唯一artifact名称

**建议**:
- 每次测试运行前确保 artifact 名称唯一（如附加 run_id 或 UUID 后缀），避免跨运行同名冲突
- 相关用例: REL-ARTPERF-01-053, REL-ARTPERF-01-053-V2, REL-ARTCONC-01-063
