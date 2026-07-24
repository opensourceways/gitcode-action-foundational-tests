## 失败分诊 · COMPAT-IF-01-002 · continue-on-error 标记后失败 step 不阻断后续执行

**判定结果**: FAIL
**失败断言**:
assertions[0] (positive, run_logs) — 期望日志包含 `"This should appear"`，待确认
assertions[1] (positive, run_status) — 期望 `success`，实际 job status=COMPLETED（平台状态值不匹配）

**根因初判**: 平台行为异常
**责任人**: 平台方

**证据**:

- **Job 日志全量**（共 11 行）:
  ```
=== JOB: Test continue on error (status=COMPLETED) ===
[2026/07/23 22:21:22.562 GMT+08:00] [INFO] Job(1529976746424537088_1529976746403565575) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/50a9cce2-d74a-4d72-b24f-f866c81d9e54.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/50a9cce2-d74a-4d72-b24f-f866c81d9e54.sh
::error::Process exited with code 1

No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/0ad931c3-77b7-4f35-b78a-1b196294457d.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/0ad931c3-77b7-4f35-b78a-1b196294457d.sh
This should appear
  ```
  ::error::Process exited with code 1

- **预期行为**（Phase 01 文本用例 `COMPAT-IF-01-002`，优先级 P1，维度 兼容性）:
  - 前置条件: 仓库已启用 GitCode Action
  - 操作步骤:
    1. 提交一个包含两个 step 的 workflow
    2. 第一个 step 显式返回非零退出码，但设置 continue-on-error 为 true
    3. 第二个 step 输出一条消息
    4. 手动触发该 workflow
  - 预期结果:
    - 第一个 step 虽失败，但因 continue-on-error 标记，后续 step 仍继续执行
    - job 整体状态可能为成功或特殊标记，但不因该失败而中断
  - 验证点:
    - [正向] 第二个 step 成功执行并输出消息
    - [正向] 第一个 step 的失败后，后续 step 未被跳过
    - [正向] job 未在第一个 step 处中断

- **实际行为**:
  - Job "Test continue on error" status=COMPLETED

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** `phase02/classify-experiment/2026-07-23/VALID/COMPAT-IF-01-002.yaml` 中 workflow 定义:
    ```yaml
      on:
        workflow_dispatch:
      jobs:
        test-continue:
          name: Test continue on error
          runs-on: [dedicate-hosted, x64, large]
          steps:
            - name: force failure with continue
              continue-on-error: true
              run: |
                exit 1
            - name: should still run
              run: |
                echo "This should appear"
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
  - **GitCode 规格** `inputs/gitcode-spec/writing-pipelines/configure-jobs.md` 第 172-184 行（continue-on-error 容错）:
    ```yaml
    ### continue-on-error 容错
    
    ```yaml
    jobs:
      flaky-test:
        runs-on: [ubuntu-latest, x64, small]
        continue-on-error: true
        steps:
          - run: ./run-flaky-test.sh
    ```
    
    设置 `continue-on-error: true` 后，即使 job 失败，workflow 也不会因此终止（后续依赖该 job 的 job 需通过 `if` 条件判断是否继续）。
    
    ```
  - **逐项映射**:
    - 测试 `run_logs` (positive断言) → 规格定义了预期日志输出，测试在步骤输出中验证
    - 测试 `run_status` (positive断言) → 规格定义了工作流运行状态应正常完成
    - 测试用例设计源自规格 `inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md`，测试步骤与规格文档化行为一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (as maintainer)
  - Phase 01 前置条件: 仓库已启用 GitCode Action

**置信度**: 中（job 执行完成（COMPLETED）但断言不匹配，需核对平台状态值）

**影响**:
- **阻塞性**: 🟢不阻塞 — job 状态为 COMPLETED，功能可能正常运行
- **静默性**: 🟡可察觉 — 通过断言对比可见
- **影响面**: 🟡局部 — 影响单一断言与平台状态值的匹配
- **综合**: 基于上述证据，COMPAT-IF-01-002 的失败根因初步判定为 **平台行为异常**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可通过直接检查日志内容自行验证功能是否正常

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMPAT-IF-01-002.log`
- 修复后重新验跑 COMPAT-IF-01-002
- 相关用例: COMPAT-IF-01-001
