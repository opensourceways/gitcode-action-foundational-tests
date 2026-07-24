## 失败分诊 · COMP-CALL-01-001 · 2 层 workflow_call 嵌套正常执行

**判定结果**: FAIL
**失败断言**:
assertions[0] (positive, run_status) — 期望 `success`，实际 job status=FAILED

**根因初判**: 产品bug
**责任人**: 平台方

**证据**:

- **Job 日志全量**（共 2 行）:
  ```
=== JOB: Call reusable workflow (status=FAILED) ===
[2026/07/23 22:12:03.980 GMT+08:00] [INFO] Job(1529974403217506304_1529974403179757575) duration check: true
  ```

- **预期行为**（Phase 01 文本用例 `COMP-CALL-01-001`，优先级 P1，维度 completeness）:
  - 前置条件: 存在可重用的子 workflow（1 层）; 主 workflow 调用子 workflow（2 层总计）
  - 操作步骤:
    1. 触发主 workflow
    2. 观察嵌套调用是否成功完成
  - 预期结果:
    - 2 层嵌套 workflow_call 成功执行
    - 子 workflow 的输出正确传递回主 workflow
  - 验证点:
    - [正向] 运行状态成功
    - [正向] 子 workflow 的 step 日志可见

- **实际行为**:
  - Job "Call reusable workflow" status=FAILED
  - Job "Call reusable workflow" FAILED，无下游依赖

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** `phase02/classify-experiment/2026-07-23/VALID/COMP-CALL-01-001.yaml` 中 workflow 定义:
    ```yaml
      on:
        workflow_dispatch:
      jobs:
        caller:
          name: Call reusable workflow
          runs-on: [dedicate-hosted, x64, large]
          steps:
            - name: Echo before call
              run: |
                echo "calling reusable workflow"
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
    - 测试用例设计源自规格 `inputs/gitcode-spec/core-concepts/trigger-events.md`，测试步骤与规格文档化行为一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `reusable-workflow`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (as maintainer)
  - Phase 01 前置条件: 存在可重用的子 workflow（1 层）; 主 workflow 调用子 workflow（2 层总计）

**置信度**: 中（job status=FAILED 但日志信息有限）

**影响**:
- **阻塞性**: 🔴阻塞 — job FAILED 导致功能不可用
- **静默性**: 🟡可察觉 — 通过 job status=FAILED 可见
- **影响面**: 🟡局部 — 影响单一功能点
- **综合**: 基于上述证据，COMP-CALL-01-001 的失败根因初步判定为 **产品bug**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 否 — 平台功能缺陷

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMP-CALL-01-001.log`
- 修复后重新验跑 COMP-CALL-01-001
- 相关用例: 无
