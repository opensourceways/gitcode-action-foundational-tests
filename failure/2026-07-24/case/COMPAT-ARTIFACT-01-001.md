## 失败分诊 · COMPAT-ARTIFACT-01-001 · upload/download-artifact 跨 job 传递等价性

**判定结果**: FAIL
**失败断言**:
assertions[0] (positive, run_status) — 期望 `completed_success`，实际 job status=FAILED
assertions[1] (positive, run_logs) — 期望: "日志中应出现 ARTIFACT_TRANSFER_OK"，因 job FAILED 未通过
assertions[2] (negative, run_logs) — 期望: "日志中不应出现 ARTIFACT_TRANSFER_FAILED"，因 job FAILED 未通过
assertions[3] (negative, workflow_parse) — 期望: "不应因使用裸插件名 upload-artifact/download-artifact 而解析失败"，因 job FAILED 未通过

**根因初判**: 产品bug
**责任人**: 平台方

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
  ::error::Upload artifact failed: Artifact with name already exists: cross-job-artifact, repoId=10431328, workflowId=ca416cbd7eb8494db7e18fe9285628b0

- **预期行为**（Phase 01 文本用例 `COMPAT-ARTIFACT-01-001`，优先级 P1，维度 兼容性）:
  - 前置条件: 仓库已启用 upload-artifact 与 download-artifact 插件
  - 操作步骤:
    1. 在 job A 中使用 `uses: upload-artifact` 上传一个标记文件
    2. 在 job B 中使用 `uses: download-artifact` 下载同一文件
    3. 验证 job B 能正确读取到 job A 上传的文件内容
  - 预期结果:
    - upload-artifact 成功上传文件到 artifact 存储
    - download-artifact 成功下载并恢复文件到 job B 工作目录
    - 文件内容在跨 job 传递后保持一致
    - 裸插件名写法行为与 GitHub 全名写法等价
  - 验证点:
    - [正向] upload-artifact 步骤成功，无报错
    - [正向] download-artifact 步骤成功，无报错
    - [正向] job B 中文件内容与 job A 上传时一致
    - [负向] 不应因使用裸插件名而解析失败

- **实际行为**:
  - Job "Upload artifact" status=FAILED
  - Job "Download and verify artifact" status=IGNORED
  - **失败传导链**: **Upload artifact** (FAILED) → **Download and verify artifact** (IGNORED)

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** `phase02/classify-experiment/2026-07-23/VALID/COMPAT-ARTIFACT-01-001.yaml` 中 workflow 定义:
    ```yaml
      on:
        workflow_dispatch:
      jobs:
        job-upload:
          name: Upload artifact
          runs-on: [dedicate-hosted, x64, large]
          steps:
            - name: (TC) create artifact file
              run: |
                mkdir -p artifacts
                echo "CROSS_JOB_MARKER_$(date +%s)" > artifacts/marker.txt
            - name: (TC) upload artifact
              uses: upload-artifact
              with:
                name: cross-job-artifact
                path: artifacts/marker.txt
        job-download:
          name: Download and verify artifact
          runs-on: [dedicate-hosted, x64, large]
          needs: job-upload
          steps:
            - name: (TC) download artifact
              uses: download-artifact
              with:
                name: cross-job-artifact
                path: downloaded
            - name: (TC) verify artifact content
              run: |
                if grep -q "CROSS_JOB_MARKER" downloaded/marker.txt; then
                  echo "ARTIFACT_TRANSFER_OK"
                else
                  echo "ARTIFACT_TRANSFER_FAILED"
                  exit 1
                fi
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
    - 测试 `run_logs` (negative断言) → 规格定义了预期日志输出，测试在步骤输出中验证
    - 测试 `workflow_parse` (negative断言) → 规格定义了工作流解析规则
    - 测试用例设计源自规格 `inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md`，测试步骤与规格文档化行为一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (as maintainer)
  - Phase 01 前置条件: 仓库已启用 upload-artifact 与 download-artifact 插件

**置信度**: 高（job status=FAILED 且下游 IGNORED，平台执行层明确故障）

**影响**:
- **阻塞性**: 🔴阻塞 — 上游 job FAILED 导致下游全部跳过，功能不可用
- **静默性**: 🟡可察觉 — 通过 job status=FAILED 可见，但 shell 诊断输出有限
- **影响面**: 🔴跨维度 — 两端传播（上游 FAILED + 下游 IGNORED），平台核心功能故障
- **综合**: 基于上述证据，COMPAT-ARTIFACT-01-001 的失败根因初步判定为 **产品bug**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 否 — 平台功能缺陷

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMPAT-ARTIFACT-01-001.log`
- 修复后重新验跑 COMPAT-ARTIFACT-01-001
- 相关用例: COMPAT-ARTIFACT-01-002
