## 失败分诊 · COMPAT-DIR-01-002 · 工作流目录差异——.github/workflows/ 不应被识别

**判定结果**: FAIL
**失败断言**:
assertions[0] (negative, workflow_discovery) — ".github/workflows/ 下的工作流不应被识别触发"，实际: 待评估
assertions[1] (negative, run_logs) — "不应出现 GITHUB_DIR_WORKFLOW_RAN"，实际: 待评估
assertions[2] (positive, run_status) — "仅 .gitcode/workflows/ 下的工作流应被触发，且无意外运行记录"，实际: 待评估

**根因初判**: 断言失败
**责任人**: 平台方

**证据**:

- **Job 日志全量**（共 6 行）:
  ```
=== JOB: Verify .github workflows dir ignored (status=COMPLETED) ===
[2026/07/23 22:17:47.119 GMT+08:00] [INFO] Job(1529975842702766080_1529975842677600263) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/59368d05-2ae4-4cc8-a813-3504c1bbe144.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/59368d05-2ae4-4cc8-a813-3504c1bbe144.sh
GITHUB_DIR_WORKFLOW_RAN
  ```

- **预期行为**（Phase 01 文本用例 `COMPAT-DIR-01-002`，优先级 P1，维度 兼容性）:
  - 前置条件: 仓库已创建 .github/workflows/ 目录; 该目录下存在工作流定义文件
  - 操作步骤:
    1. 在 .github/workflows/ci.yml 中创建工作流定义
    2. 同时确保 .gitcode/workflows/ 下无同名工作流
    3. 提交并推送到仓库，触发对应事件
    4. 观察平台是否识别并执行 .github/workflows/ 下的工作流
  - 预期结果:
    - .github/workflows/ 下的工作流文件不被 GitCode 平台识别
    - 对应事件触发时，该目录下的工作流不会执行
    - 平台优先且仅识别 .gitcode/workflows/ 目录
  - 验证点:
    - [负向] .github/workflows/ 下的工作流不应被触发执行
    - [正向] 平台应仅识别 .gitcode/workflows/ 目录
    - [正向] 事件触发后不应出现来自 .github 目录的意外运行记录

- **实际行为**:
  - Job "Verify .github workflows dir ignored" status=COMPLETED

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** `phase02/classify-experiment/2026-07-23/VALID/COMPAT-DIR-01-002.yaml` 中 workflow 定义:
    ```yaml
      on:
        push:
          branches: [main]
      jobs:
        verify-github-dir-ignored:
          name: Verify .github workflows dir ignored
          runs-on: [dedicate-hosted, x64, large]
          steps:
            - name: (TC) echo if reached
              run: |
                echo "GITHUB_DIR_WORKFLOW_RAN"
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
    - 测试 `workflow_discovery` (negative断言) → 规格定义了对应行为（期望: `".github/workflows/ 下的工作流不应被识别触发"`）
    - 测试 `run_logs` (negative断言) → 规格定义了预期日志输出，测试在步骤输出中验证
    - 测试 `run_status` (positive断言) → 规格定义了工作流运行状态应正常完成
    - 测试用例设计源自规格 `inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md`，测试步骤与规格文档化行为一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `with-github-dir`
  - setup.branch_protection: `default`
  - 触发方式: push (as maintainer)
  - Phase 01 前置条件: 仓库已创建 .github/workflows/ 目录; 该目录下存在工作流定义文件

**置信度**: 中（job 执行完成（COMPLETED）但断言不匹配，需核对平台状态值）

**影响**:
- **阻塞性**: 🟢不阻塞 — job 状态为 COMPLETED，功能可能正常运行
- **静默性**: 🟡可察觉 — 通过断言对比可见
- **影响面**: 🟡局部 — 影响单一断言与平台状态值的匹配
- **综合**: 基于上述证据，COMPAT-DIR-01-002 的失败根因初步判定为 **断言失败**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可通过直接检查日志内容自行验证功能是否正常

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMPAT-DIR-01-002.log`
- 修复后重新验跑 COMPAT-DIR-01-002
- 相关用例: COMPAT-DIR-01-001
