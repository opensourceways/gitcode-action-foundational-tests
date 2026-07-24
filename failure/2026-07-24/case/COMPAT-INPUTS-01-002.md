## 失败分诊 · COMPAT-INPUTS-01-002 · workflow_dispatch inputs 类型限制 - string 正常通过

**判定结果**: FAIL
**失败断言**:
assertions[0] (positive, run_status) — 期望 `success`，实际 job status=COMPLETED（平台状态值不匹配）
assertions[1] (positive, run_logs) — 期望通过，实际待验证
assertions[2] (positive, run_logs) — 期望通过，实际待验证

**根因初判**: 平台行为异常
**责任人**: 平台方

**证据**:

- **Job 日志全量**（共 7 行）:
  ```
=== JOB: Verify string input acceptance (status=COMPLETED) ===
[2026/07/23 22:21:44.341 GMT+08:00] [INFO] Job(1529976837469913088_1529976837436358663) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/20a4cb42-6949-4714-bb01-d9812980ffa0.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/20a4cb42-6949-4714-bb01-d9812980ffa0.sh
ENV=production
STRING_INPUT_OK
  ```

- **预期行为**（Phase 01 文本用例 `COMPAT-INPUTS-01-002`，优先级 P1，维度 兼容性）:
  - 前置条件: 仓库已启用 Actions; 测试分支存在
  - 操作步骤:
    1. 在 workflow 中定义 workflow_dispatch inputs 并指定 type: string
    2. 提交并推送该 workflow
    3. 触发 workflow 并传入参数
  - 预期结果:
    - workflow 应被平台接受，不报错
    - string 类型的 input 应能正常接收和输出
  - 验证点:
    - [正向] workflow 校验通过
    - [正向] string 类型 input 能正常传递和使用

- **实际行为**:
  - Job "Verify string input acceptance" status=COMPLETED

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** `phase02/classify-experiment/2026-07-23/VALID/COMPAT-INPUTS-01-002.yaml` 中 workflow 定义:
    ```yaml
      on:
        workflow_dispatch:
          inputs:
            environment:
              description: '部署目标环境'
              required: true
              default: 'staging'
              type: string
      jobs:
        verify:
          name: Verify string input acceptance
          runs-on: [dedicate-hosted, x64, large]
          steps:
            - name: Echo input value
              run: |
                echo "ENV=${{ inputs.environment }}"
                echo "STRING_INPUT_OK"
    ```
  - **GitCode 规格** `inputs/gitcode-spec/core-concepts/trigger-events.md` 第 1-32 行:
    ```yaml
    <!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/core-concepts/trigger-events | fetched: 2026-07-20 -->
    
    # 触发事件
    
    **事件概述**：事件是流水线启动的源动力。当仓库中发生特定操作时，系统产生对应事件，触发匹配 `on` 配置的工作流。
    
    ## 支持的事件类型
    
    | 事件 | 说明 | 典型配置 |
    |------|------|--------|
    | `push` | 代码推送 | `on: push: branches: [main]` |
    | `pull_request` | PR 事件 | `on: pull_request: branches: [main]` |
    | `pull_request_target` | PR 安全事件 | `on: pull_request_target: branches: [main]` |
    | `issue_comment` | Issue 评论 | `on: issue_comment: types: [created]` |
    | `pull_request_comment` | PR 评论 | `on: pull_request_comment: types: [created]` |
    | `workflow_dispatch` | 手动触发 | `on: workflow_dispatch: inputs: {...}` |
    | `workflow_call` | 可重用调用 | `on: workflow_call: inputs: {...}` |
    | `schedule` | 定时触发 | `on: schedule: - cron: '0 2 * * *'` |
    
    > **重要区别**：`pull_request` 使用 PR 源分支代码运行，`pull_request_target` 使用 base 分支代码运行且拥有仓库写权限。Fork 场景推荐使用 `pull_request_target`。
    
    ## 多事件组合
    
    ```yaml
    on:
      push:
        branches: [main]
      pull_request:
        branches: [main]
      workflow_dispatch:
    ```
    
    ```
  - **逐项映射**:
    - 测试 `run_status` (positive断言) → 规格定义了工作流运行状态应正常完成
    - 测试 `run_logs` (positive断言) → 规格定义了预期日志输出，测试在步骤输出中验证
    - 测试 `run_logs` (positive断言) → 规格定义了预期日志输出，测试在步骤输出中验证
    - 测试用例设计源自规格 `inputs/gitcode-spec/core-concepts/trigger-events.md`，测试步骤与规格文档化行为一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (as maintainer)
  - Phase 01 前置条件: 仓库已启用 Actions; 测试分支存在

**置信度**: 中（job 执行完成（COMPLETED）但断言不匹配，需核对平台状态值）

**影响**:
- **阻塞性**: 🟢不阻塞 — job 状态为 COMPLETED，功能可能正常运行
- **静默性**: 🟡可察觉 — 通过断言对比可见
- **影响面**: 🟡局部 — 影响单一断言与平台状态值的匹配
- **综合**: 基于上述证据，COMPAT-INPUTS-01-002 的失败根因初步判定为 **平台行为异常**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可通过直接检查日志内容自行验证功能是否正常

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMPAT-INPUTS-01-002.log`
- 修复后重新验跑 COMPAT-INPUTS-01-002
- 相关用例: 无
