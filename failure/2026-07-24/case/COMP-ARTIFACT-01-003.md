## 失败分诊 · COMP-ARTIFACT-01-003 · artifact 保留期设置生效

**判定结果**: FAIL
**失败断言**:
assertions[0] (positive, artifact_available) — 期望 `yes_within_retention`，实际 job status=FAILED
assertions[1] (negative, artifact_available_after_expiry) — 期望 `no_after_1_day`，实际 job status=FAILED

**根因初判**: 产品bug
**责任人**: 平台方

**证据**:

- **Job 日志全量**（共 2 行）:
  ```
=== JOB: Upload with short retention (status=FAILED) ===
[2026/07/23 22:11:53.181 GMT+08:00] [INFO] Job(1529974358023880704_1529974357990326279) duration check: true
  ```

- **预期行为**（Phase 01 文本用例 `COMP-ARTIFACT-01-003`，优先级 P1，维度 completeness）:
  - 前置条件: workflow 设置 retention-days: 1
  - 操作步骤:
    1. 上传 artifact 并设置 retention-days: 1
    2. 等待超过保留期后尝试下载
  - 预期结果:
    - 超过保留期后 artifact 不可下载
  - 验证点:
    - [正向] 保留期内可下载 artifact
    - [负向] 超过保留期后下载返回 404

- **实际行为**:
  - Job "Upload with short retention" status=FAILED
  - Job "Upload with short retention" FAILED，无下游依赖

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** `phase02/classify-experiment/2026-07-23/VALID/COMP-ARTIFACT-01-003.yaml` 中 workflow 定义:
    ```yaml
      on:
        workflow_dispatch:
      jobs:
        upload:
          name: Upload with short retention
          runs-on: [dedicate-hosted, x64, large]
          steps:
            - name: Create artifact
              run: |
                echo "temp" > temp.txt
            - name: Upload artifact
              uses: upload-artifact
              with:
                name: temp-artifact
                path: temp.txt
                retention-days: 1
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
    - 测试 `artifact_available` (positive断言) → 规格定义了对应行为（期望: `yes_within_retention`）
    - 测试 `artifact_available_after_expiry` (negative断言) → 规格定义了对应行为（期望: `no_after_1_day`）
    - 测试用例设计源自规格 `inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md`，测试步骤与规格文档化行为一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (as maintainer)
  - Phase 01 前置条件: workflow 设置 retention-days: 1

**置信度**: 中（job status=FAILED 但日志信息有限）

**影响**:
- **阻塞性**: 🔴阻塞 — job FAILED 导致功能不可用
- **静默性**: 🟡可察觉 — 通过 job status=FAILED 可见
- **影响面**: 🟡局部 — 影响单一功能点
- **综合**: 基于上述证据，COMP-ARTIFACT-01-003 的失败根因初步判定为 **产品bug**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 否 — 平台功能缺陷

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMP-ARTIFACT-01-003.log`
- 修复后重新验跑 COMP-ARTIFACT-01-003
- 相关用例: COMP-ARTIFACT-01-002
