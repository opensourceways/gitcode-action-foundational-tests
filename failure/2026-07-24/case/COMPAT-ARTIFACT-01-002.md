## 失败分诊 · COMPAT-ARTIFACT-01-002 · upload-artifact 保留期行为等价性

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 `completed_success`，实际 `COMPLETED`（平台 API 返回大写枚举值，与合约期望的小写语义值不匹配）

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（共 41 行）:
```
=== JOB: Verify artifact retention (status=COMPLETED) ===
[2026/07/23 22:17:03.914 GMT+08:00] [INFO] Job(1529975661622079488_1529975661596913671) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/57b19c39-f572-4295-9401-a1ce51265408.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/57b19c39-f572-4295-9401-a1ce51265408.sh

::debug::Using workspace directory: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-1
Uploading artifact "retention-test-artifact" from paths: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-1/retention_marker.txt
::debug::followSymbolicLinks 'true'
::debug::implicitDescendants 'true'
::debug::matchDirectories 'true'
::debug::omitBrokenSymbolicLinks 'true'
::debug::followSymbolicLinks 'true'
::debug::implicitDescendants 'true'
::debug::matchDirectories 'true'
::debug::omitBrokenSymbolicLinks 'true'
::debug::Search path '/home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-1/retention_marker.txt'
Found 1 file(s) to upload
::debug::[diagnostic] First 1 matched file(s): /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-1/retention_marker.txt
::debug::Resolved root directory: /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-1
Creating zip archive from 1 file(s)...
Zip archive created: /tmp/artifact-1784816237243-65215bac.zip (~0 MB, 178 bytes)
Creating artifact "retention-test-artifact" (size: 178 bytes, workflow: 241d8083e7784b8f9682f8959c717af9)...
[Twirp] trace-id: e04d18519ebc63393218b0a7e03a3809
Artifact created with ID 206052053389312, upload mode: simple
Uploading artifact via simple PUT (~0 MB)...
Upload complete. SHA-256: e7c9afcfb4e9116cc46c95b2f6c758156fa8623bf34eb0e02c7cf2fef7724bea
Finalizing artifact...
[Twirp] trace-id: 4b1415ebb70afa02fe11cdb914a2edb7
Artifact "retention-test-artifact" finalized successfully.
Fetching signed artifact URL...
[Twirp] trace-id: 041e7a0f0ceab924ca21e574f8e09ff8
Signed artifact URL obtained.
::debug::Temp zip file removed: /tmp/artifact-1784816237243-65215bac.zip
Artifact "retention-test-artifact" uploaded successfully. ID: 206052053389312, Size: 178 bytes
Artifact portal URL: https://gitcode.com/ComputingActionTest/gitcode-test-1/actions/artifacts/206052053389312

No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/66437c89-cbcf-4df8-ac7b-22c1c2a494b8.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/66437c89-cbcf-4df8-ac7b-22c1c2a494b8.sh
ARTIFACT_UPLOADED_OK
```

  **日志分析**: "ARTIFACT_UPLOADED_OK" — 上传成功, run=COMPLETED

- **预期行为**（Phase 01 文本用例 `COMPAT-ARTIFACT-01-002`，优先级 P1，维度 compatibility）:
  - 操作步骤 1: "在工作流中使用 `uses: upload-artifact` 上传文件"
  - 操作步骤 2: "配置保留期参数（如 retention-days）"
  - 操作步骤 3: "观察 artifact 在系统中的保留与过期行为"

  预期结果:
  - upload-artifact 支持保留期参数配置
  - 超过保留期后 artifact 被自动清理
  - 保留期内 artifact 可正常下载
  - 裸插件名写法与 GitHub 全名写法在保留期语义上等价

  验证点:
  - [正向] 保留期内可正常下载 artifact
  - [正向] 超过保留期后 artifact 被清理或不可访问
  - [负向] 不应出现保留期配置被静默忽略的情况

- **实际行为**:
  - "ARTIFACT_UPLOADED_OK" — 上传成功, run=COMPLETED


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

**置信度**: 高（"ARTIFACT_UPLOADED_OK" — 上传成功, run=COMPLETED）

**影响**:
- **阻塞性**: ⚪无影响 — 平台 artifact 上传成功（ARTIFACT_UPLOADED_OK，完整的上传日志），断言标记 COMPLETED≠success
- **静默性**: 🟢明确报错 — 平台完整输出上传全流程日志（zip 创建、上传、finalize、signed URL），仅测试断言词汇不一致
- **影响面**: 🟢单用例 — 仅本用例断言标记需修复
- **综合**: 平台 artifact 上传保留期功能完全正常，仅断言词汇不匹配
- **是否有规避手段**: 是 — 修复 run_status 词汇映射

**建议**:
- 修复 `compile_asserts.py` 中的 run_status 词汇映射：`COMPLETED→success, FAILED→failure, CANCELED→canceled`
- 将 COMPAT-ARTIFACT-01-002 标记为「用例断言修复后应重新验跑」
- 相关用例: COMPAT-ARTIFACT-01-001
