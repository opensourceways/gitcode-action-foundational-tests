## 失败分诊 · COMPAT-OUTCOME-01-001 · continue-on-error false 时 outcome 与 conclusion 应均为 failure

**判定结果**: FAIL
**失败断言**:
assertions[0] (positive, step_status) — 期望 `failure`，实际 job status=FAILED
assertions[1] (positive, step_conclusion) — 期望 `failure`，实际 job status=FAILED
assertions[2] (positive, run_status) — 期望 `failure`，实际 job status=FAILED

**根因初判**: 产品bug
**责任人**: 平台方

**证据**:

- **Job 日志全量**（共 58 行）:
  ```
=== JOB: Test outcome with continue on error false (status=FAILED) ===
[2026/07/23 22:23:05.278 GMT+08:00] [INFO] Job(1529977177305133056_1529977177284161543) duration check: true
[2026/07/23 14:23:16.991 GMT+00:00] [INFO] repository dist full path is /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0
Getting Git version info >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:16.995 GMT+00:00] [INFO] run git command --> git version
[2026/07/23 14:23:17.005 GMT+00:00] [INFO] run git command stdout --> git version 2.43.0

[2026/07/23 14:23:17.006 GMT+00:00] [INFO] Deleting the contents of '/home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0'
initialize git repository >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:17.007 GMT+00:00] [INFO] run git command --> git init
[2026/07/23 14:23:17.013 GMT+00:00] [INFO] run git command stdout --> Initialized empty Git repository in /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0/.git/
[2026/07/23 14:23:17.014 GMT+00:00] [INFO] run git command --> git remote add origin https://gitcode.com/ComputingActionTest/gitcode-test-0.git
[2026/07/23 14:23:17.018 GMT+00:00] [INFO] git repository initialized at /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0

Disabling automatic garbage collection >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:17.019 GMT+00:00] [INFO] run git command --> git config --local gc.auto 0

Setting up auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:17.022 GMT+00:00] [INFO] Removing SSH command configuration
[2026/07/23 14:23:17.023 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
[2026/07/23 14:23:17.027 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
[2026/07/23 14:23:17.050 GMT+00:00] [INFO] Removing HTTP extra header
[2026/07/23 14:23:17.051 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
[2026/07/23 14:23:17.055 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
[2026/07/23 14:23:17.075 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
[2026/07/23 14:23:17.083 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'
[2026/07/23 14:23:17.103 GMT+00:00] [INFO] configuring token
[2026/07/23 14:23:17.109 GMT+00:00] [INFO] configuring token config local

Start fetch git repo >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:17.120 GMT+00:00] [INFO] run git command --> git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --progress --depth=1 origin +refs/heads/main*:refs/remotes/origin/main* +refs/tags/main*:refs/tags/main*

Checking out the ref >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:17.648 GMT+00:00] [INFO] run git command --> git branch --list --remote origin/main
[2026/07/23 14:23:17.652 GMT+00:00] [INFO] run git command stdout -->   origin/main
[2026/07/23 14:23:17.653 GMT+00:00] [INFO] run git command --> git checkout --progress --force -B main refs/remotes/origin/main
[2026/07/23 14:23:17.659 GMT+00:00] [INFO] run git command stdout --> branch 'main' set up to track 'origin/main'.

Removing auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:17.669 GMT+00:00] [INFO] Removing SSH command configuration
[2026/07/23 14:23:17.669 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
[2026/07/23 14:23:17.672 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
[2026/07/23 14:23:17.693 GMT+00:00] [INFO] Removing HTTP extra header
[2026/07/23 14:23:17.694 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
[2026/07/23 14:23:17.698 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
[2026/07/23 14:23:17.719 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
[2026/07/23 14:23:17.744 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'


No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/8891abb1-c0e1-467c-acc5-7a1c90ae5398.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/8891abb1-c0e1-467c-acc5-7a1c90ae5398.sh
::error::Process exited with code 1

No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/d1ee7d63-bf63-43b2-bdd5-b8b1a2c2dae7.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/d1ee7d63-bf63-43b2-bdd5-b8b1a2c2dae7.sh
Check step outcome and conclusion
  ```
  ::error::Process exited with code 1

- **预期行为**（Phase 01 文本用例 `COMPAT-OUTCOME-01-001`，优先级 P1，维度 兼容性）:
  - 前置条件: 仓库已启用 workflow
  - 操作步骤:
    1. 创建一个 workflow_dispatch 触发的 workflow
    2. 配置一个 step，显式设置 `continue-on-error: false`（或默认不写）
    3. 该 step 的 run 脚本以非零退出码结束（如 `exit 1`）
    4. 在后续 step 中通过 `${{ atomgit.step.status }}` 或上下文读取该 step 的状态
    5. 手动触发该 workflow
  - 预期结果:
    - 该 step 失败后，job 整体标记为失败
    - outcome（执行结果）与 conclusion（最终判定）均为 failure
    - 由于 continue-on-error 为 false，两者不应出现差异
  - 验证点:
    - [正向] 失败 step 的 outcome 为 failure
    - [正向] 失败 step 的 conclusion 为 failure
    - [正向] job 整体状态为 failure

- **实际行为**:
  - Job "Test outcome with continue on error false" status=FAILED
  - Job "Test outcome with continue on error false" FAILED，无下游依赖

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** `phase02/classify-experiment/2026-07-23/VALID/COMPAT-OUTCOME-01-001.yaml` 中 workflow 定义:
    ```yaml
      on:
        workflow_dispatch:
      jobs:
        outcome-false:
          name: Test outcome with continue on error false
          runs-on: [dedicate-hosted, x64, large]
          steps:
            - name: checkout source
              uses: checkout
            - name: failing step
              continue-on-error: false
              run: |
                exit 1
            - name: check status
              if: ${{ always() }}
              run: |
                echo "Check step outcome and conclusion"
    ```
  - **GitCode 规格** `inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md` 第 1-50 行:
    ```yaml
    <!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/core-concepts/variables-secrets-context-expressions | fetched: 2026-07-20 -->
    <!-- 注意：本页 WebFetch 返回为英文（模型转译），内容忠实但语言待统一为中文，勘误时可重抓。 -->
    
    # Variables, Secrets, Context and Expressions
    
    AtomGit Action provides a four-level variable system using `env`, `vars`, `secrets`, and `inputs`, enabling flexible workflow configuration through context (primarily `atomgit`) and expressions (`${{ expression }}`).
    
    ## Four-Level Variable System
    
    | Type | Suitable For | Sensitive | Reference Method |
    |------|-------------|-----------|-------------------|
    | `env` | Temporary variables within workflow | No | `$VAR_NAME` or `${{ env.VAR }}` |
    | `vars` | Repository/organization-level regular variables | No | `${{ vars.VAR }}` |
    | `secrets` | Passwords, tokens, private keys | Yes | `${{ secrets.NAME }}` |
    | `inputs` | Workflow input parameters | No | `${{ inputs.NAME }}` |
    
    ## Variable Priority
    
    ```
    Step env  >  Job env  >  Workflow env
    ```
    
    ## Context
    
    AtomGit Action supports 12 contexts, with the core context being **`atomgit`**:
    
    | Context | Description | Typical Properties |
    |---------|-------------|-------------------|
    | `atomgit` | Core workflow run information | `atomgit.sha`, `atomgit.ref`, `atomgit.event_name` |
    | `env` | Environment variables | `env.VAR_NAME` |
    | `vars` | Configuration variables | `vars.VAR_NAME` |
    | `secrets` | Secrets | `secrets.NAME` |
    | `job` | Current job information | `job.status` |
    | `steps` | Step information and outputs | `steps.id.outputs.result` |
    | `runner` | Runner information | `runner.os`, `runner.arch` |
    | `inputs` | Input parameters | `inputs.NAME` |
    | `matrix` | Matrix parameters | `matrix.os` |
    | `strategy` | Matrix strategy information | `strategy.fail-fast` |
    
    ## Expressions
    ```
  - **GitCode 规格** `inputs/gitcode-spec/syntax-reference/expressions.md` 第 1-50 行:
    ```yaml
    <!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/syntax-reference/expressions | fetched: 2026-07-20 -->
    
    # 表达式
    
    AtomGit Action 使用 `${{ expression }}` 语法在工作流中编写表达式。表达式可在 `if` 条件、变量赋值、步骤参数等位置使用。
    
    ## 3.1 字面量
    
    | 类型 | 语法 | 示例 |
    |------|------|------|
    | 布尔值 | `true` / `false` | `${{ true }}` |
    | null | `null` | `${{ null }}` |
    | 数字 | 整数或浮点数 | `${{ 42 }}`, `${{ 3.14 }}` |
    | 字符串 | 单引号包裹 | `${{ 'hello' }}` |
    
    ## 3.2 运算符
    
    | 运算符 | 说明 | 示例 |
    |--------|------|------|
    | `==` | 等于 | `${{ atomgit.ref == 'refs/heads/main' }}` |
    | `!=` | 不等于 | `${{ atomgit.event_name != 'schedule' }}` |
    | `!` | 逻辑非 | `${{ !success }}` |
    | `&&` | 逻辑与 | `${{ success && atomgit.ref == 'refs/heads/main' }}` |
    | `\|\|` | 逻辑或 | `${{ failed \|\| cancelled }}` |
    | `>` | 大于 | `${{ matrix.version > 12 }}` |
    | `<` | 小于 | `${{ matrix.version < 14 }}` |
    | `>=` | 大于等于 | `${{ strategy.job-total >= 3 }}` |
    | `<=` | 小于等于 | `${{ inputs.count <= 10 }}` |
    
    > **运算符优先级（从高到低）：** `` → `!` → `<`, `>`, `<=`, `>=` → `==`, `!=` → `&&` → `||`
    
    ## 3.3 函数
    
    | 函数 | 说明 | 示例 |
    |------|------|------|
    | `success` | 所有前置步骤成功时返回 `true` | `if: ${{ success }}` |
    | `always` | 无论前置步骤结果如何始终返回 `true` | `if: ${{ always }}` |
    | `cancelled` | 工作流被取消时返回 `true` | `if: ${{ cancelled }}` |
    | `failed` | 任一前置步骤失败时返回 `true` | `if: ${{ failed }}` |
    | `contains(search, item)` | 判断 search 是否包含 item | `${{ contains(atomgit.ref, 'release') }}` |
    ```
  - **逐项映射**:
    - 测试 `step_status` (positive断言) → 规格定义了对应行为（期望: `failure`）
    - 测试 `step_conclusion` (positive断言) → 规格定义了对应行为（期望: `failure`）
    - 测试 `run_status` (positive断言) → 规格定义了工作流运行状态应正常完成
    - 测试用例设计源自规格 `inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md`，测试步骤与规格文档化行为一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (as maintainer)
  - Phase 01 前置条件: 仓库已启用 workflow

**置信度**: 高（job status=FAILED 且有明确错误输出）

**影响**:
- **阻塞性**: 🔴阻塞 — job FAILED 导致功能不可用
- **静默性**: 🟡可察觉 — 通过 job status=FAILED 可见
- **影响面**: 🟡局部 — 影响单一功能点
- **综合**: 基于上述证据，COMPAT-OUTCOME-01-001 的失败根因初步判定为 **产品bug**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 否 — 平台功能缺陷

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMPAT-OUTCOME-01-001.log`
- 修复后重新验跑 COMPAT-OUTCOME-01-001
- 相关用例: COMPAT-OUTCOME-01-002
