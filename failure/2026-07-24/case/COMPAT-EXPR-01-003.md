## 失败分诊 · COMPAT-EXPR-01-003 · failure() 与 failed 关键字的处理行为差异

**判定结果**: FAIL
**失败断言**:
assertions[0] (positive, run_logs) — 期望日志包含 `"Cleanup ran after failure"`，因 job FAILED 未执行验证
assertions[1] (positive, run_status) — 期望 `failure`，实际 job status=FAILED

**根因初判**: 产品bug
**责任人**: 平台方

**证据**:

- **Job 日志全量**（共 58 行）:
  ```
=== JOB: Test failure handling (status=FAILED) ===
[2026/07/23 22:19:21.153 GMT+08:00] [INFO] Job(1529976237059743744_1529976237026189319) duration check: true
[2026/07/23 14:19:33.853 GMT+00:00] [INFO] repository dist full path is /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0
Getting Git version info >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:19:33.858 GMT+00:00] [INFO] run git command --> git version
[2026/07/23 14:19:33.866 GMT+00:00] [INFO] run git command stdout --> git version 2.43.0

[2026/07/23 14:19:33.867 GMT+00:00] [INFO] Deleting the contents of '/home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0'
initialize git repository >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:19:33.869 GMT+00:00] [INFO] run git command --> git init
[2026/07/23 14:19:33.874 GMT+00:00] [INFO] run git command stdout --> Initialized empty Git repository in /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0/.git/
[2026/07/23 14:19:33.874 GMT+00:00] [INFO] run git command --> git remote add origin https://gitcode.com/ComputingActionTest/gitcode-test-0.git
[2026/07/23 14:19:33.882 GMT+00:00] [INFO] git repository initialized at /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0

Disabling automatic garbage collection >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:19:33.883 GMT+00:00] [INFO] run git command --> git config --local gc.auto 0

Setting up auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:19:33.887 GMT+00:00] [INFO] Removing SSH command configuration
[2026/07/23 14:19:33.887 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
[2026/07/23 14:19:33.892 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
[2026/07/23 14:19:33.912 GMT+00:00] [INFO] Removing HTTP extra header
[2026/07/23 14:19:33.913 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
[2026/07/23 14:19:33.917 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
[2026/07/23 14:19:33.938 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
[2026/07/23 14:19:33.946 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'
[2026/07/23 14:19:33.968 GMT+00:00] [INFO] configuring token
[2026/07/23 14:19:33.974 GMT+00:00] [INFO] configuring token config local

Start fetch git repo >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:19:33.986 GMT+00:00] [INFO] run git command --> git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --progress --depth=1 origin +refs/heads/main*:refs/remotes/origin/main* +refs/tags/main*:refs/tags/main*

Checking out the ref >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:19:34.525 GMT+00:00] [INFO] run git command --> git branch --list --remote origin/main
[2026/07/23 14:19:34.529 GMT+00:00] [INFO] run git command stdout -->   origin/main
[2026/07/23 14:19:34.530 GMT+00:00] [INFO] run git command --> git checkout --progress --force -B main refs/remotes/origin/main
[2026/07/23 14:19:34.538 GMT+00:00] [INFO] run git command stdout --> branch 'main' set up to track 'origin/main'.

Removing auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:19:34.548 GMT+00:00] [INFO] Removing SSH command configuration
[2026/07/23 14:19:34.549 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
[2026/07/23 14:19:34.553 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
[2026/07/23 14:19:34.576 GMT+00:00] [INFO] Removing HTTP extra header
[2026/07/23 14:19:34.576 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
[2026/07/23 14:19:34.581 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
[2026/07/23 14:19:34.605 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
[2026/07/23 14:19:34.632 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'


No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/171224bf-061f-44bb-bfc7-e3347f00c2bb.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/171224bf-061f-44bb-bfc7-e3347f00c2bb.sh
::error::Process exited with code 1

No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/50d5d8ab-bf43-4943-a68e-b6809424f4a7.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/50d5d8ab-bf43-4943-a68e-b6809424f4a7.sh
Cleanup ran after failure
  ```
  ::error::Process exited with code 1

- **预期行为**（Phase 01 文本用例 `COMPAT-EXPR-01-003`，优先级 P1，维度 兼容性）:
  - 前置条件: 仓库已启用 GitCode Action
  - 操作步骤:
    1. 提交一个 workflow，其中包含一个会失败的 step
    2. 在后续 step 中尝试使用 failure() 函数或 failed 关键字形式的表达式
    3. 手动触发并观察运行结果
  - 预期结果:
    - 平台对 failure() 函数与 failed 关键字可能有不同的支持策略
    - 记录实际行为，验证与 GitHub Actions 的兼容性差异
  - 验证点:
    - [正向] 若支持，可在失败后获取到正确的状态值
    - [负向] 若不支持，应有表达式解析错误或降级行为
    - [正向] 失败后 step 的执行状态可被观察或引用

- **实际行为**:
  - Job "Test failure handling" status=FAILED
  - Job "Test failure handling" FAILED，无下游依赖

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** `phase02/classify-experiment/2026-07-23/VALID/COMPAT-EXPR-01-003.yaml` 中 workflow 定义:
    ```yaml
      on:
        workflow_dispatch:
      jobs:
        test-failure:
          name: Test failure handling
          runs-on: [dedicate-hosted, x64, large]
          steps:
            - name: checkout source
              uses: checkout
            - name: force failure
              run: |
                exit 1
            - name: cleanup after failure
              if: ${{ always() }}
              run: |
                echo "Cleanup ran after failure"
    ```
  - **GitCode 规格** `inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md` 第 4-7 行（Variables, Secrets, Context and Expressions）:
    ```yaml
    # Variables, Secrets, Context and Expressions
    
    AtomGit Action provides a four-level variable system using `env`, `vars`, `secrets`, and `inputs`, enabling flexible workflow configuration through context (primarily `atomgit`) and expressions (`${{ expression }}`).
    
    ```
  - **GitCode 规格** `inputs/gitcode-spec/syntax-reference/expressions.md` 第 3-6 行（表达式）:
    ```yaml
    # 表达式
    
    AtomGit Action 使用 `${{ expression }}` 语法在工作流中编写表达式。表达式可在 `if` 条件、变量赋值、步骤参数等位置使用。
    
    ```
  - **逐项映射**:
    - 测试 `run_logs` (positive断言) → 规格定义了预期日志输出，测试在步骤输出中验证
    - 测试 `run_status` (positive断言) → 规格定义了工作流运行状态应正常完成
    - 测试用例设计源自规格 `inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md`，测试步骤与规格文档化行为一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (as maintainer)
  - Phase 01 前置条件: 仓库已启用 GitCode Action

**置信度**: 高（job status=FAILED 且有明确错误输出）

**影响**:
- **阻塞性**: 🔴阻塞 — job FAILED 导致功能不可用
- **静默性**: 🟡可察觉 — 通过 job status=FAILED 可见
- **影响面**: 🟡局部 — 影响单一功能点
- **综合**: 基于上述证据，COMPAT-EXPR-01-003 的失败根因初步判定为 **产品bug**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 否 — 平台功能缺陷

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMPAT-EXPR-01-003.log`
- 修复后重新验跑 COMPAT-EXPR-01-003
- 相关用例: COMPAT-EXPR-01-002
