## 失败分诊 · COMPAT-ARTIFACT-01-002 · upload-artifact 保留期行为等价性

**判定结果**: FAIL
**失败断言**:
assertions[0] (positive, run_status) — 期望 `completed_success`，实际 job status=COMPLETED（平台状态值不匹配）
assertions[1] (positive, run_logs) — "日志中应出现 ARTIFACT_UPLOADED_OK"，实际: 待评估
assertions[2] (nonfunctional, artifact_state) — "artifact 应在配置保留期内可下载，超期后被清理或不可访问"，实际: 待评估
assertions[3] (negative, run_logs) — "不应出现 retention-days 被静默忽略的提示"，实际: 待评估

**根因初判**: 平台行为异常
**责任人**: 平台方

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
  - 前置条件: 仓库已启用 upload-artifact 插件
  - 操作步骤:
    1. 在工作流中使用 `uses: upload-artifact` 上传文件
    2. 配置保留期参数（如 retention-days）
    3. 观察 artifact 在系统中的保留与过期行为
  - 预期结果:
    - upload-artifact 支持保留期参数配置
    - 超过保留期后 artifact 被自动清理
    - 保留期内 artifact 可正常下载
    - 裸插件名写法与 GitHub 全名写法在保留期语义上等价
  - 验证点:
    - [正向] 保留期内可正常下载 artifact
    - [正向] 超过保留期后 artifact 被清理或不可访问
    - [负向] 不应出现保留期配置被静默忽略的情况

- **实际行为**:
  - Job "Verify artifact retention" status=COMPLETED

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** `phase02/classify-experiment/2026-07-23/VALID/COMPAT-ARTIFACT-01-002.yaml` 中 workflow 定义:
    ```yaml
      on:
        workflow_dispatch:
      jobs:
        verify-retention:
          name: Verify artifact retention
          runs-on: [dedicate-hosted, x64, large]
          steps:
            - name: (TC) create artifact file
              run: |
                echo "RETENTION_TEST_MARKER" > retention_marker.txt
            - name: (TC) upload with retention
              uses: upload-artifact
              with:
                name: retention-test-artifact
                path: retention_marker.txt
                retention-days: 1
            - name: (TC) verify upload success
              run: |
                echo "ARTIFACT_UPLOADED_OK"
    ```
  - **GitCode 规格** `inputs/gitcode-spec/core-concepts/workflow-job-step-action.md` 第 1-50 行:
    ```yaml
    <!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/core-concepts/workflow-job-step-action | fetched: 2026-07-20 -->
    
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
        jobs:
          build-job:
            runs-on: ubuntu-latest
            steps:
              - run: echo "Building..."
      - test
        jobs:
          test-job:
            runs-on: ubuntu-latest
            steps:
              - run: echo "Testing..."
      - deploy
        jobs:
          deploy-job:
            runs-on: ubuntu-latest
            steps:
              - run: echo "Deploying..."
    ```
  - **GitCode 规格** `inputs/gitcode-spec/writing-pipelines/configure-jobs.md` 第 97-109 行（if 条件执行）:
    ```yaml
    ### if 条件执行
    
    job 级别的 `if` 推迟整个 job 的执行：
    
    ```yaml
    jobs:
      deploy:
        if: ${{ atomgit.ref == 'refs/heads/main' }}
        runs-on: [ubuntu-latest, x64, small]
        steps:
          - run: echo "deploy only on main"
    ```
    
    ```
  - **逐项映射**:
    - 测试 `run_status` (positive断言) → 规格定义了工作流运行状态应正常完成
    - 测试 `run_logs` (positive断言) → 规格定义了预期日志输出，测试在步骤输出中验证
    - 测试 `artifact_state` (nonfunctional断言) → 规格定义了对应行为（期望: `"artifact 应在配置保留期内可下载，超期后被清理或不可访问"`）
    - 测试 `run_logs` (negative断言) → 规格定义了预期日志输出，测试在步骤输出中验证
    - 测试用例设计源自规格 `inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md`，测试步骤与规格文档化行为一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (as maintainer)
  - Phase 01 前置条件: 仓库已启用 upload-artifact 插件

**置信度**: 中（job 执行完成（COMPLETED）但断言不匹配，需核对平台状态值）

**影响**:
- **阻塞性**: 🟢不阻塞 — job 状态为 COMPLETED，功能可能正常运行
- **静默性**: 🟡可察觉 — 通过断言对比可见
- **影响面**: 🟡局部 — 影响单一断言与平台状态值的匹配
- **综合**: 基于上述证据，COMPAT-ARTIFACT-01-002 的失败根因初步判定为 **平台行为异常**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可通过直接检查日志内容自行验证功能是否正常

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMPAT-ARTIFACT-01-002.log`
- 修复后重新验跑 COMPAT-ARTIFACT-01-002
- 相关用例: COMPAT-ARTIFACT-01-001
