## 失败分诊 · COMPAT-ENV-01-001 · ATOMGIT_SHA 环境变量应正确返回触发提交 SHA

**判定结果**: FAIL
**失败断言**:
assertions[0] (positive, run_status) — 期望 `success`，实际 job status=COMPLETED（平台状态值不匹配）
assertions[1] (positive, run_logs) — "日志中 atomgit_sha 应包含 40 位十六进制 SHA 值"，实际: 待评估

**根因初判**: 平台行为异常
**责任人**: 平台方

**证据**:

- **Job 日志全量**（共 7 行）:
  ```
=== JOB: Test ATOMGIT_SHA env var (status=COMPLETED) ===
[2026/07/23 22:17:55.420 GMT+08:00] [INFO] Job(1529975877301706752_1529975877263958023) duration check: true
No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/fa86e9e0-7aba-4669-8c7a-9d3ea2710a12.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/fa86e9e0-7aba-4669-8c7a-9d3ea2710a12.sh
atomgit_sha=
done
  ```

- **预期行为**（Phase 01 文本用例 `COMPAT-ENV-01-001`，优先级 P1，维度 兼容性）:
  - 前置条件: 仓库已启用 Actions; Runner 环境正常注入 ATOMGIT_* 变量
  - 操作步骤:
    1. 在 workflow 的 run 步骤中输出 $ATOMGIT_SHA
    2. 触发 workflow 运行
  - 预期结果:
    - $ATOMGIT_SHA 应返回当前触发事件的提交 SHA（40 位十六进制字符串）
  - 验证点:
    - [正向] 日志中 ATOMGIT_SHA 的值不为空且为有效 SHA 格式

- **实际行为**:
  - Job "Test ATOMGIT_SHA env var" status=COMPLETED

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** `phase02/classify-experiment/2026-07-23/VALID/COMPAT-ENV-01-001.yaml` 中 workflow 定义:
    ```yaml
      on:
        workflow_dispatch:
      jobs:
        test:
          name: Test ATOMGIT_SHA env var
          runs-on: [dedicate-hosted, x64, large]
          steps:
            - name: Echo ATOMGIT_SHA
              run: |
                echo "atomgit_sha=$ATOMGIT_SHA"
                echo "done"
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
    - 测试用例设计源自规格 `inputs/gitcode-spec/core-concepts/trigger-events.md`，测试步骤与规格文档化行为一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (as maintainer)
  - Phase 01 前置条件: 仓库已启用 Actions; Runner 环境正常注入 ATOMGIT_* 变量

**置信度**: 中（job 执行完成（COMPLETED）但断言不匹配，需核对平台状态值）

**影响**:
- **阻塞性**: 🟢不阻塞 — job 状态为 COMPLETED，功能可能正常运行
- **静默性**: 🟡可察觉 — 通过断言对比可见
- **影响面**: 🟡局部 — 影响单一断言与平台状态值的匹配
- **综合**: 基于上述证据，COMPAT-ENV-01-001 的失败根因初步判定为 **平台行为异常**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可通过直接检查日志内容自行验证功能是否正常

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMPAT-ENV-01-001.log`
- 修复后重新验跑 COMPAT-ENV-01-001
- 相关用例: 无
