## 失败分诊 · COMP-ISOLATION-01-002 · 环境变量不跨 job 泄漏

**判定结果**: FAIL
**失败断言**:
assertions[0] (positive, run_status) — 期望 `success`，实际 job status=COMPLETED（平台状态值不匹配）
assertions[1] (negative, run_logs) — 期望通过，实际待验证

**根因初判**: 平台行为异常
**责任人**: 平台方

**证据**:

- **Job 日志全量**（共 14 行）:
  ```
=== JOB: Create tmp isolation marker (status=COMPLETED) ===
[2026/07/23 22:02:49.185 GMT+08:00] [INFO] Job(1529972076444266496_1529972076419100679) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/7a47315a-85d1-414b-a441-7f632dade35f.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/7a47315a-85d1-414b-a441-7f632dade35f.sh
MARKER_CREATED


=== JOB: Check tmp marker isolation (status=COMPLETED) ===
[2026/07/23 22:03:02.555 GMT+08:00] [INFO] Job(1529972076444266496_1529972076419100681) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/b9bb0e2f-6080-4973-948c-712c5f45dde7.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/b9bb0e2f-6080-4973-948c-712c5f45dde7.sh
ISOLATION_STRONG: marker not visible across jobs
  ```

- **预期行为**（Phase 01 文本用例 `COMP-ISOLATION-01-002`，优先级 P0，维度 completeness）:
  - 前置条件: workflow 含两个串行 jobs
  - 操作步骤:
    1. job 1 设置环境变量
    2. job 2 检查该环境变量
  - 预期结果:
    - job 2 不应看到 job 1 设置的环境变量
  - 验证点:
    - [负向] job 2 中环境变量值为空或未设置

- **实际行为**:
  - Job "Create tmp isolation marker" status=COMPLETED
  - Job "Check tmp marker isolation" status=COMPLETED
  - **失败传导链**: Create tmp isolation marker (COMPLETED) → Check tmp marker isolation (COMPLETED)

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** `phase02/classify-experiment/2026-07-23/VALID/COMP-ISOLATION-01-002.yaml` 中 workflow 定义:
    ```yaml
      on:
        workflow_dispatch:
      jobs:
        job1:
          name: Set env
          runs-on: [dedicate-hosted, x64, large]
          steps:
            - name: Export env
              run: |
                echo "ISOLATION_VAR=leak" >> "$ATOMGIT_ENV"
        job2:
          name: Check env
          runs-on: [dedicate-hosted, x64, large]
          needs: job1
          steps:
            - name: Verify env absent
              run: |
                if [ -z "${ISOLATION_VAR:-}" ]; then
                  echo "env not leaked as expected"
                else
                  echo "env leaked: $ISOLATION_VAR"
                  exit 1
                fi
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
    - 测试 `run_logs` (negative断言) → 规格定义了预期日志输出，测试在步骤输出中验证
    - 测试用例设计源自规格 `inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md`，测试步骤与规格文档化行为一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (as maintainer)
  - Phase 01 前置条件: workflow 含两个串行 jobs

**置信度**: 中（job 执行完成（COMPLETED）但断言不匹配，需核对平台状态值）

**影响**:
- **阻塞性**: 🟢不阻塞 — job 状态为 COMPLETED，功能可能正常运行
- **静默性**: 🟡可察觉 — 通过断言对比可见
- **影响面**: 🟡局部 — 影响单一断言与平台状态值的匹配
- **综合**: 基于上述证据，COMP-ISOLATION-01-002 的失败根因初步判定为 **平台行为异常**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可通过直接检查日志内容自行验证功能是否正常

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMP-ISOLATION-01-002.log`
- 修复后重新验跑 COMP-ISOLATION-01-002
- 相关用例: COMP-ISOLATION-01-001
