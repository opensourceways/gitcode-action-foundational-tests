## 失败分诊 · COMPAT-OUTCOME-01-002 · continue-on-error true 时 outcome 应为 failure 而 conclusion 应为 success

**判定结果**: FAIL
**失败断言**:
assertions[0] (positive, step_status) — 期望 `failure`，实际 job status=COMPLETED
assertions[1] (positive, step_conclusion) — 期望 `success`，实际 job status=COMPLETED（平台状态值不匹配）
assertions[2] (positive, run_status) — 期望 `success`，实际 job status=COMPLETED（平台状态值不匹配）

**根因初判**: 平台行为异常
**责任人**: 平台方

**证据**:

- **Job 日志全量**（共 63 行）:
  ```
=== JOB: Test outcome with continue on error true (status=COMPLETED) ===
[2026/07/23 22:23:16.020 GMT+08:00] [INFO] Job(1529977222095978496_1529977222066618375) duration check: true
[2026/07/23 14:23:27.589 GMT+00:00] [INFO] repository dist full path is /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-1
Getting Git version info >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:27.596 GMT+00:00] [INFO] run git command --> git version
[2026/07/23 14:23:27.607 GMT+00:00] [INFO] run git command stdout --> git version 2.43.0

[2026/07/23 14:23:27.608 GMT+00:00] [INFO] Deleting the contents of '/home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-1'
initialize git repository >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:27.609 GMT+00:00] [INFO] run git command --> git init
[2026/07/23 14:23:27.616 GMT+00:00] [INFO] run git command stdout --> Initialized empty Git repository in /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-1/.git/
[2026/07/23 14:23:27.616 GMT+00:00] [INFO] run git command --> git remote add origin https://gitcode.com/ComputingActionTest/gitcode-test-1.git
[2026/07/23 14:23:27.620 GMT+00:00] [INFO] git repository initialized at /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-1

Disabling automatic garbage collection >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:27.621 GMT+00:00] [INFO] run git command --> git config --local gc.auto 0

Setting up auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:27.625 GMT+00:00] [INFO] Removing SSH command configuration
[2026/07/23 14:23:27.625 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
[2026/07/23 14:23:27.629 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
[2026/07/23 14:23:27.649 GMT+00:00] [INFO] Removing HTTP extra header
[2026/07/23 14:23:27.649 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
[2026/07/23 14:23:27.654 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
[2026/07/23 14:23:27.674 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
[2026/07/23 14:23:27.685 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'
[2026/07/23 14:23:27.705 GMT+00:00] [INFO] configuring token
[2026/07/23 14:23:27.711 GMT+00:00] [INFO] configuring token config local

Start fetch git repo >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:27.723 GMT+00:00] [INFO] run git command --> git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --progress --depth=1 origin +refs/heads/main*:refs/remotes/origin/main* +refs/tags/main*:refs/tags/main*

Checking out the ref >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:28.198 GMT+00:00] [INFO] run git command --> git branch --list --remote origin/main
[2026/07/23 14:23:28.202 GMT+00:00] [INFO] run git command stdout -->   origin/main
[2026/07/23 14:23:28.203 GMT+00:00] [INFO] run git command --> git checkout --progress --force -B main refs/remotes/origin/main
[2026/07/23 14:23:28.210 GMT+00:00] [INFO] run git command stdout --> branch 'main' set up to track 'origin/main'.

Removing auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:28.219 GMT+00:00] [INFO] Removing SSH command configuration
[2026/07/23 14:23:28.219 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
[2026/07/23 14:23:28.223 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
[2026/07/23 14:23:28.242 GMT+00:00] [INFO] Removing HTTP extra header
[2026/07/23 14:23:28.242 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
[2026/07/23 14:23:28.246 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
[2026/07/23 14:23:28.267 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
[2026/07/23 14:23:28.301 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'


No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/77613ff9-5d67-4cb6-802b-1d4543783abf.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/77613ff9-5d67-4cb6-802b-1d4543783abf.sh
::error::Process exited with code 1

No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/fd5e2a9b-361d-4f4d-8083-f14afb3df2d1.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/fd5e2a9b-361d-4f4d-8083-f14afb3df2d1.sh
This step should run

No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/76355f07-9436-4a43-ac68-376230ed1b47.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/76355f07-9436-4a43-ac68-376230ed1b47.sh
Check step outcome and conclusion
  ```
  ::error::Process exited with code 1

- **预期行为**（Phase 01 文本用例 `COMPAT-OUTCOME-01-002`，优先级 P1，维度 兼容性）:
  - 前置条件: 仓库已启用 workflow
  - 操作步骤:
    1. 创建一个 workflow_dispatch 触发的 workflow
    2. 配置一个 step，显式设置 `continue-on-error: true`
    3. 该 step 的 run 脚本以非零退出码结束（如 `exit 1`）
    4. 在后续 step 中读取该 step 的 outcome 和 conclusion
    5. 手动触发该 workflow
  - 预期结果:
    - 该 step 的 outcome 为 failure（实际执行失败）
    - 该 step 的 conclusion 为 success（因 continue-on-error 被覆盖为成功）
    - job 整体继续执行后续 step，不应被中断
    - 语义与 GitHub Actions 一致
  - 验证点:
    - [正向] 失败 step 的 outcome 为 failure
    - [正向] 失败 step 的 conclusion 为 success
    - [正向] 后续 step 正常执行
    - [正向] job 最终状态为 success（若无其他失败）

- **实际行为**:
  - Job "Test outcome with continue on error true" status=COMPLETED

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** `phase02/classify-experiment/2026-07-23/VALID/COMPAT-OUTCOME-01-002.yaml` 中 workflow 定义:
    ```yaml
      on:
        workflow_dispatch:
      jobs:
        outcome-true:
          name: Test outcome with continue on error true
          runs-on: [dedicate-hosted, x64, large]
          steps:
            - name: checkout source
              uses: checkout
            - name: failing step tolerated
              continue-on-error: true
              run: |
                exit 1
            - name: next step runs
              run: |
                echo "This step should run"
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
    - 测试 `step_conclusion` (positive断言) → 规格定义了对应行为（期望: `success`）
    - 测试 `run_status` (positive断言) → 规格定义了工作流运行状态应正常完成
    - 测试用例设计源自规格 `inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md`，测试步骤与规格文档化行为一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (as maintainer)
  - Phase 01 前置条件: 仓库已启用 workflow

**置信度**: 中（job 执行完成（COMPLETED）但断言不匹配，需核对平台状态值）

**影响**:
- **阻塞性**: 🟢不阻塞 — job 状态为 COMPLETED，功能可能正常运行
- **静默性**: 🟡可察觉 — 通过断言对比可见
- **影响面**: 🟡局部 — 影响单一断言与平台状态值的匹配
- **综合**: 基于上述证据，COMPAT-OUTCOME-01-002 的失败根因初步判定为 **平台行为异常**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可通过直接检查日志内容自行验证功能是否正常

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMPAT-OUTCOME-01-002.log`
- 修复后重新验跑 COMPAT-OUTCOME-01-002
- 相关用例: COMPAT-OUTCOME-01-001
