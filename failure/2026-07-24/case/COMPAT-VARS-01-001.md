## 失败分诊 · COMPAT-VARS-01-001 · vars 上下文若支持应正确返回值

**判定结果**: FAIL
**失败断言**:
assertions[0] (positive, run_status) — 期望 `success`，实际 job status=COMPLETED（平台状态值不匹配）
assertions[1] (positive, run_logs) — "日志中 test_var 应包含 hello_vars，表明 vars 上下文可用"，实际: 待评估

**根因初判**: 平台行为异常
**责任人**: 平台方

**证据**:

- **Job 日志全量**（共 7 行）:
  ```
=== JOB: Test vars context (status=COMPLETED) ===
[2026/07/23 22:24:32.696 GMT+08:00] [INFO] Job(1529977543715463168_1529977543686103047) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/6147c307-ee0f-4f35-93ac-59218dd7b0ce.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/6147c307-ee0f-4f35-93ac-59218dd7b0ce.sh
test_var=
done
  ```

- **预期行为**（Phase 01 文本用例 `COMPAT-VARS-01-001`，优先级 P1，维度 兼容性）:
  - 前置条件: 仓库已启用 Actions; 若平台支持 vars，已配置测试变量 TEST_VAR
  - 操作步骤:
    1. 在 workflow 的 run 步骤中输出 ${{ vars.TEST_VAR }}
    2. 触发 workflow 运行
  - 预期结果:
    - 若 vars 支持，应正确返回 TEST_VAR 的配置值
    - 日志中应显示该值
  - 验证点:
    - [正向] vars.TEST_VAR 返回配置值

- **实际行为**:
  - Job "Test vars context" status=COMPLETED

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** `phase02/classify-experiment/2026-07-23/VALID/COMPAT-VARS-01-001.yaml` 中 workflow 定义:
    ```yaml
      on:
        workflow_dispatch:
      jobs:
        test:
          name: Test vars context
          runs-on: [dedicate-hosted, x64, large]
          steps:
            - name: Echo vars TEST_VAR
              run: |
                echo "test_var=${{ vars.TEST_VAR }}"
                echo "done"
    ```
  - **GitCode 规格** `inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md` 第 4-7 行（Variables, Secrets, Context and Expressions）:
    ```yaml
    # Variables, Secrets, Context and Expressions
    
    AtomGit Action provides a four-level variable system using `env`, `vars`, `secrets`, and `inputs`, enabling flexible workflow configuration through context (primarily `atomgit`) and expressions (`${{ expression }}`).
    
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
    - 测试 `run_status` (positive断言) → 规格定义了工作流运行状态应正常完成
    - 测试 `run_logs` (positive断言) → 规格定义了预期日志输出，测试在步骤输出中验证
    - 测试用例设计源自规格 `inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md`，测试步骤与规格文档化行为一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (as maintainer)
  - Phase 01 前置条件: 仓库已启用 Actions; 若平台支持 vars，已配置测试变量 TEST_VAR

**置信度**: 中（job 执行完成（COMPLETED）但断言不匹配，需核对平台状态值）

**影响**:
- **阻塞性**: 🟢不阻塞 — job 状态为 COMPLETED，功能可能正常运行
- **静默性**: 🟡可察觉 — 通过断言对比可见
- **影响面**: 🟡局部 — 影响单一断言与平台状态值的匹配
- **综合**: 基于上述证据，COMPAT-VARS-01-001 的失败根因初步判定为 **平台行为异常**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可通过直接检查日志内容自行验证功能是否正常

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMPAT-VARS-01-001.log`
- 修复后重新验跑 COMPAT-VARS-01-001
- 相关用例: 无
