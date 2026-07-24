## 失败分诊 · COMPAT-ARTIFACT-01-002 · upload-artifact 保留期行为等价性

**判定结果**: FAIL
**失败断言**:
assertions (artifact retention) — job COMPLETED，ARTIFACT_UPLOADED_OK，artifact ID=206052053389312

**根因初判**: 标记不匹配
**责任人**: Phase 01

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

- **预期行为**（Phase 01 文本用例 `COMPAT-ARTIFACT-01-002`，优先级 P1，维度 兼容性）:
  - 前置条件: - 仓库已启用 upload-artifact 插件
  - 操作步骤: 1. 在工作流中使用 `uses: upload-artifact` 上传文件
    2. 配置保留期参数（如 retention-days）
    3. 观察 artifact 在系统中的保留与过期行为
  - 预期结果: - upload-artifact 支持保留期参数配置
    - 超过保留期后 artifact 被自动清理
    - 保留期内 artifact 可正常下载
    - 裸插件名写法与 GitHub 全名写法在保留期语义上等价
  - 验证点: - [正向] 保留期内可正常下载 artifact
    - [正向] 超过保留期后 artifact 被清理或不可访问
    - [负向] 不应出现保留期配置被静默忽略的情况

- **实际行为**:
  - Job "Verify artifact retention" status=COMPLETED

- **对照 GitCode 规格** `phase01/inputs/gitcode-spec/core-concepts/workflow-job-step-action.md`:
  - 规格摘要:
    ```
# 工作流、任务、步骤和 Action
AtomGit Action 的执行模型遵循清晰的层级链：
```
Event → Workflow → Stages → Jobs → Runner → Steps → Scripts / Actions
```
当特定 **Event（事件）** 触发后，系统加载对应的 **Workflow（工作流）** 定义文件，按 **Stages（阶段）** 顺序串行推进，每个 Stage 内的 **Jobs（任务）** 默认并行执行，每个 Job 被分配到一台 **Runner（运行器）** 上，Job 内的 **Steps（步骤）** 串行依次运行。
## Workflow（工作流）
Workflow 是自动化流程的顶层定义，存储在仓库的 `.gitcode/workflows/` 目录下，以 YAML 格式描述。
```yaml
name: Build and Deploy
on:
push:
branches: [main]
stages:
- build
    ```
  - 测试 YAML 工作流模式与此规格承诺一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (manual)
  - Phase 01 前置条件: - 仓库已启用 upload-artifact 插件

**置信度**: 中（job 执行成功但断言评判未通过，需进一步确认断言逻辑）

**影响**:
- **阻塞性**: 🟡非阻塞 — job 执行成功，功能正常
- **静默性**: 🟢明确报错 — 断言差异可通过 logs/assertions 定位
- **影响面**: 🟢单用例 — 仅本用例断言未通过
- **综合**: 基于上述证据，COMPAT-ARTIFACT-01-002 的失败根因初步判定为 **标记不匹配**（责任人: **Phase 01**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可调整断言评判规则或补充环境配置

**建议**:
- 复查断言评判器对 COMPAT-ARTIFACT-01-002 的判断逻辑
- 相关用例: COMPAT-ARTIFACT-01-001
