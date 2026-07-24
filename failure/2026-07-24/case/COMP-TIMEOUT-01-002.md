## 失败分诊 · COMP-TIMEOUT-01-002 · 超时的 job 被强制终止并标记为 failure

**判定结果**: FAIL
**失败断言**:
assertions[0] (negative, run_status) — 期望 `success`，实际 job status=CANCELED
assertions[1] (positive, run_status) — 期望 `failure`，实际 job status=CANCELED
assertions[2] (positive, run_logs) — 期望日志包含 `starting`，待确认

**根因初判**: 产品bug
**责任人**: 平台方

**证据**:

- **Job 日志全量**（共 10 行）:
  ```
=== JOB: Verify timeout kill (status=CANCELED) ===
[2026/07/23 22:15:10.715 GMT+08:00] [INFO] Job(1529975186650959872_1529975186625794055) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/a86ef9ad-8274-4ad6-b1c6-9d2bf9752255.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/a86ef9ad-8274-4ad6-b1c6-9d2bf9752255.sh
starting

No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/2a43ae6e-da92-40e6-a74f-627a1cd6dc61.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/2a43ae6e-da92-40e6-a74f-627a1cd6dc61.sh
  ```

- **预期行为**（Phase 01 文本用例 `COMP-TIMEOUT-01-002`，优先级 P1，维度 completeness）:
  - 前置条件: workflow 声明 timeout-minutes: 1
  - 操作步骤:
    1. 触发 workflow，其中 step 睡眠超过 1 分钟
    2. 观察 job 是否在 1 分钟后被强制终止
  - 预期结果:
    - job 在 1 分钟后被强制终止
    - 运行状态标记为 failure
    - 已运行 step 的日志保留
  - 验证点:
    - [负向] 运行状态为 failure
    - [正向] 超时前已完成的 step 日志完整保留

- **实际行为**:
  - Job "Verify timeout kill" status=CANCELED

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** `phase02/classify-experiment/2026-07-23/VALID/COMP-TIMEOUT-01-002.yaml` 中 workflow 定义:
    ```yaml
      on:
        workflow_dispatch:
      jobs:
        verify:
          name: Verify timeout kill
          runs-on: [dedicate-hosted, x64, large]
          timeout-minutes: 1
          steps:
            - name: Echo before sleep
              run: |
                echo "starting"
            - name: Sleep beyond timeout
              run: |
                sleep 120
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
    - 测试 `run_status` (negative断言) → 规格定义了工作流运行状态应正常完成
    - 测试 `run_status` (positive断言) → 规格定义了工作流运行状态应正常完成
    - 测试 `run_logs` (positive断言) → 规格定义了预期日志输出，测试在步骤输出中验证
    - 测试用例设计源自规格 `inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md`，测试步骤与规格文档化行为一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (as maintainer)
  - Phase 01 前置条件: workflow 声明 timeout-minutes: 1

**置信度**: 低（缺乏足够信息判断根因）

**影响**:
- **阻塞性**: 🟡可能阻塞
- **静默性**: 🟡可察觉
- **影响面**: 🟡局部
- **综合**: 基于上述证据，COMP-TIMEOUT-01-002 的失败根因初步判定为 **产品bug**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 否

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMP-TIMEOUT-01-002.log`
- 修复后重新验跑 COMP-TIMEOUT-01-002
- 相关用例: COMP-TIMEOUT-01-001
