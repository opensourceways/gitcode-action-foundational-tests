## 失败分诊 · COMP-TIMEOUT-01-001 · 未声明 timeout-minutes 的 job 在 360 分钟内正常完成

**判定结果**: FAIL
**失败断言**:
assertions[0] (positive, run_status) — 期望 `success`，实际 job status=COMPLETED（平台状态值不匹配）
assertions[1] (nonfunctional, run_duration) — 期望通过，实际待验证

**根因初判**: 平台行为异常
**责任人**: 平台方

**证据**:

- **Job 日志全量**（共 6 行）:
  ```
=== JOB: Verify default timeout (status=COMPLETED) ===
[2026/07/23 22:14:59.297 GMT+08:00] [INFO] Job(1529975138676383744_1529975138642829319) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/0850d2a0-1db9-47e0-a3df-bc88b583695b.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/0850d2a0-1db9-47e0-a3df-bc88b583695b.sh
done
  ```

- **预期行为**（Phase 01 文本用例 `COMP-TIMEOUT-01-001`，优先级 P1，维度 completeness）:
  - 前置条件: workflow 未声明 timeout-minutes
  - 操作步骤:
    1. 触发 workflow
    2. 观察运行是否成功
  - 预期结果:
    - job 在默认 360 分钟超时范围内成功完成
  - 验证点:
    - [正向] 运行状态为 success
    - [非功能] 运行耗时远小于 360 分钟

- **实际行为**:
  - Job "Verify default timeout" status=COMPLETED

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** `phase02/classify-experiment/2026-07-23/VALID/COMP-TIMEOUT-01-001.yaml` 中 workflow 定义:
    ```yaml
      on:
        workflow_dispatch:
      jobs:
        verify:
          name: Verify default timeout
          runs-on: [dedicate-hosted, x64, large]
          steps:
            - name: Quick step
              run: |
                echo "done"
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
  - **GitCode 规格** `inputs/gitcode-spec/writing-pipelines/configure-jobs.md` 第 110-122 行（timeout-minutes 超时时间）:
    ```yaml
    ### timeout-minutes 超时时间
    
    ```yaml
    jobs:
      build:
        runs-on: [ubuntu-latest, x64, small]
        timeout-minutes: 30
        steps:
          - run: ./build.sh
    ```
    
    默认超时时间为 360 分钟（6 小时）。超时后 job 将被强制终止。
    
    ```
  - **逐项映射**:
    - 测试 `run_status` (positive断言) → 规格定义了工作流运行状态应正常完成
    - 测试 `run_duration` (nonfunctional断言) → 规格定义了默认超时限制
    - 测试用例设计源自规格 `inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md`，测试步骤与规格文档化行为一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (as maintainer)
  - Phase 01 前置条件: workflow 未声明 timeout-minutes

**置信度**: 中（job 执行完成（COMPLETED）但断言不匹配，需核对平台状态值）

**影响**:
- **阻塞性**: 🟢不阻塞 — job 状态为 COMPLETED，功能可能正常运行
- **静默性**: 🟡可察觉 — 通过断言对比可见
- **影响面**: 🟡局部 — 影响单一断言与平台状态值的匹配
- **综合**: 基于上述证据，COMP-TIMEOUT-01-001 的失败根因初步判定为 **平台行为异常**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可通过直接检查日志内容自行验证功能是否正常

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMP-TIMEOUT-01-001.log`
- 修复后重新验跑 COMP-TIMEOUT-01-001
- 相关用例: COMP-TIMEOUT-01-002
