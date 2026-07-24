## 失败分诊 · COMPAT-ARTIFACT-01-001 · upload/download-artifact 跨 job 传递等价性

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 `completed_success`，实际 `FAILED`（平台缺陷导致 job 执行失败）

**根因初判**: 产品bug

**证据**:

- **Job 日志全量**（共 30 行）:
```
=== JOB: Upload artifact (status=FAILED) ===
[2026/07/23 22:16:53.204 GMT+08:00] [INFO] Job(1529975616432521216_1529975616398966791) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/1bf65fa1-5d0e-4bdb-9619-e8fc68a51e0c.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/1bf65fa1-5d0e-4bdb-9619-e8fc68a51e0c.sh

::debug::Using workspace directory: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-1
Uploading artifact "cross-job-artifact" from paths: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-1/artifacts/marker.txt
::debug::followSymbolicLinks 'true'
::debug::implicitDescendants 'true'
::debug::matchDirectories 'true'
::debug::omitBrokenSymbolicLinks 'true'
::debug::followSymbolicLinks 'true'
::debug::implicitDescendants 'true'
::debug::matchDirectories 'true'
::debug::omitBrokenSymbolicLinks 'true'
::debug::Search path '/home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-1/artifacts/marker.txt'
Found 1 file(s) to upload
::debug::[diagnostic] First 1 matched file(s): /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-1/artifacts/marker.txt
::debug::Resolved root directory: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-1/artifacts
Creating zip archive from 1 file(s)...
Zip archive created: /tmp/artifact-1784816227356-bead89b4.zip (~0 MB, 164 bytes)
Creating artifact "cross-job-artifact" (size: 164 bytes, workflow: ca416cbd7eb8494db7e18fe9285628b0)...
[Twirp] trace-id: 12bc6206e2fe41bde000e039912805e8
[Twirp] error trace-id: 12bc6206e2fe41bde000e039912805e8
::debug::Temp zip file removed: /tmp/artifact-1784816227356-bead89b4.zip
::error::Upload artifact failed: Artifact with name already exists: cross-job-artifact, repoId=10431328, workflowId=ca416cbd7eb8494db7e18fe9285628b0


=== JOB: Download and verify artifact (status=IGNORED) ===
```

  **日志分析**: "Artifact with name already exists: cross-job-artifact" + "[Twirp] error" — 制品名冲突

- **预期行为**（Phase 01 文本用例 `COMPAT-ARTIFACT-01-001`，优先级 P1，维度 compatibility）:
  - 操作步骤 1: "在 job A 中使用 `uses: upload-artifact` 上传一个标记文件"
  - 操作步骤 2: "在 job B 中使用 `uses: download-artifact` 下载同一文件"
  - 操作步骤 3: "验证 job B 能正确读取到 job A 上传的文件内容"

  预期结果:
  - upload-artifact 成功上传文件到 artifact 存储
  - download-artifact 成功下载并恢复文件到 job B 工作目录
  - 文件内容在跨 job 传递后保持一致
  - 裸插件名写法行为与 GitHub 全名写法等价

  验证点:
  - [正向] upload-artifact 步骤成功，无报错
  - [正向] download-artifact 步骤成功，无报错
  - [正向] job B 中文件内容与 job A 上传时一致
  - [负向] 不应因使用裸插件名而解析失败

- **实际行为**:
  - "Artifact with name already exists: cross-job-artifact" + "[Twirp] error" — 制品名冲突
  - **失败传导链**: **Upload artifact** → FAILED → **Download and verify artifact** → IGNORED（因上游失败而跳过），下游 xxx 功能未被测试到

- **测试 YAML 与规格精确对照**:
  - 规格文件: `upload-download-artifacts.md` (路径: `phase01/inputs/gitcode-spec/writing-pipelines/upload-download-artifacts.md`)
  - 规格节选:
```yaml
steps:
  - uses: upload-artifact
    with:
      name: app-dist
      path: dist/
```
    该规格明确声明: 15-18行的上传制品示例，使用了 `uses: upload-artifact` 裸插件名

  测试 YAML 的写法与规格示例一致，证明平台文档确凿承诺了该行为。

**置信度**: 高（"Artifact with name already exists: cross-job-artifact" + "[Twirp] error" — 制品名冲突）

**影响**:
- **阻塞性**: 🔴阻塞 — 制品上传因名称冲突失败（"Artifact with name already exists"），下游 Download 被 IGNORED，跨 job artifact 传递功能完全断裂
- **静默性**: 🟡可察觉 — 平台清楚报错 "Artifact with name already exists" 含 Twirp trace-id，但该错误非正常业务流程（名称应唯一），暗示制品名管理不健全
- **影响面**: 🔴跨维度 — artifact 名称冲突影响所有依赖 artifact 的 workflow，非孤立问题
- **综合**: 制品存储层名称冲突导致跨 job artifact 传递失败，虽报错清晰但平台应独立管理制品命名空间
- **是否有规避手段**: 否 — 需平台修复制品名称冲突管理机制

**建议**:
- 将此缺陷提交给平台工程团队，附上日志文件 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMPAT-ARTIFACT-01-001.log`
- 建议修复后重新验跑 COMPAT-ARTIFACT-01-001
- 相关用例: COMPAT-ARTIFACT-01-002
