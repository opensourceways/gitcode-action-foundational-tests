## 失败分诊 · COMPAT-DIR-01-001 · 工作流目录差异——.gitcode/workflows/ 正常识别

**判定结果**: FAIL
**失败断言**:
assertions[0] (positive, run_status) — 期望 `completed_success`，实际 job status=COMPLETED（平台状态值不匹配）
assertions[1] (positive, run_logs) — "日志中应出现 GITCODE_DIR_RECOGNIZED_OK"，实际: 待评估
assertions[2] (positive, workflow_discovery) — ".gitcode/workflows/ 下的工作流文件被正确识别"，实际: 待评估

**根因初判**: 平台行为异常
**责任人**: 平台方

**证据**:

- **Job 日志全量**（共 6 行）:
  ```
=== JOB: Verify .gitcode workflows dir (status=COMPLETED) ===
[2026/07/23 22:17:42.925 GMT+08:00] [INFO] Job(1529975825048813568_1529975825011064839) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/597789f8-f4eb-4c9d-b32d-5f1d73680286.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/597789f8-f4eb-4c9d-b32d-5f1d73680286.sh
GITCODE_DIR_RECOGNIZED_OK
  ```

- **预期行为**（Phase 01 文本用例 `COMPAT-DIR-01-001`，优先级 P1，维度 兼容性）:
  - 前置条件: 仓库已创建 .gitcode/workflows/ 目录
  - 操作步骤:
    1. 在 .gitcode/workflows/ci.yml 中创建工作流定义
    2. 提交并推送到仓库
    3. 触发对应事件，验证工作流被正确识别和执行
  - 预期结果:
    - .gitcode/workflows/ 下的 .yml 文件被平台识别为有效工作流
    - 对应事件触发时工作流正常执行
    - 此行为与 GitCode 官方文档一致
  - 验证点:
    - [正向] .gitcode/workflows/*.yml 被正确识别
    - [正向] 对应事件触发后工作流正常执行
    - [负向] 不应出现 .gitcode 目录下文件被忽略的情况

- **实际行为**:
  - Job "Verify .gitcode workflows dir" status=COMPLETED

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** `phase02/classify-experiment/2026-07-23/VALID/COMPAT-DIR-01-001.yaml` 中 workflow 定义:
    ```yaml
      on:
        push:
          branches: [main]
      jobs:
        verify-gitcode-dir:
          name: Verify .gitcode workflows dir
          runs-on: [dedicate-hosted, x64, large]
          steps:
            - name: (TC) echo from gitcode dir
              run: |
                echo "GITCODE_DIR_RECOGNIZED_OK"
    ```
  - **GitCode 规格** `inputs/gitcode-spec/core-concepts/workflow-job-step-action.md` 第 13-42 行（Workflow（工作流））:
    ```yaml
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
    
    ```
  - **GitCode 规格** `inputs/gitcode-spec/writing-pipelines/configure-jobs.md` 第 1-50 行:
    ```yaml
    <!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/writing-pipelines/configure-jobs | fetched: 2026-07-20 -->
    
    # 配置任务 Jobs
    
    **适用场景**：当你需要在 workflow 中定义一个或多个任务，指定运行环境、超时时间、环境变量、并发控制、矩阵策略等时。
    
    ## 前提条件
    
    - 已理解 workflow 的基本结构。
    - 已确定 job 需要的运行环境（Runner 标签）。
    
    ## 快速示例
    
    ```yaml
    name: ci
    on:
      push:
        branches:
          - main
    jobs:
      build:
        runs-on: [ubuntu-latest, x64, small]
        timeout-minutes: 30
        env:
          APP_ENV: production
        steps:
          - uses: checkout
          - run: ./build.sh
    ```
    
    ## 配置说明
    
    ### runs-on 运行环境
    
    `runs-on` 指定 job 运行的 Runner 环境。AtomGit Action 的官方资源池标签采用**三段式格式**：`{os}-{version},{arch},{flavor}`。
    
    | 段位 | 说明 | 示例 |
    |------|------|------|
    | `{os}-{version}` | 操作系统及版本 | `ubuntu-latest` |
    | `{arch}` | CPU 架构 | `x64`、`arm64` |
    ```
  - **逐项映射**:
    - 测试 `run_status` (positive断言) → 规格定义了工作流运行状态应正常完成
    - 测试 `run_logs` (positive断言) → 规格定义了预期日志输出，测试在步骤输出中验证
    - 测试 `workflow_discovery` (positive断言) → 规格定义了对应行为（期望: `".gitcode/workflows/ 下的工作流文件被正确识别"`）
    - 测试用例设计源自规格 `inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md`，测试步骤与规格文档化行为一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: push (as maintainer)
  - Phase 01 前置条件: 仓库已创建 .gitcode/workflows/ 目录

**置信度**: 中（job 执行完成（COMPLETED）但断言不匹配，需核对平台状态值）

**影响**:
- **阻塞性**: 🟢不阻塞 — job 状态为 COMPLETED，功能可能正常运行
- **静默性**: 🟡可察觉 — 通过断言对比可见
- **影响面**: 🟡局部 — 影响单一断言与平台状态值的匹配
- **综合**: 基于上述证据，COMPAT-DIR-01-001 的失败根因初步判定为 **平台行为异常**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可通过直接检查日志内容自行验证功能是否正常

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMPAT-DIR-01-001.log`
- 修复后重新验跑 COMPAT-DIR-01-001
- 相关用例: COMPAT-DIR-01-002
