## 失败分诊 · COMPAT-INPUTS-01-002 · workflow_dispatch inputs 类型限制 - string 正常通过

**判定结果**: FAIL
**失败断言**:
assertions (string input) — job COMPLETED，ENV=production STRING_INPUT_OK 正确输出

**根因初判**: 标记不匹配
**责任人**: Phase 01

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
  - 前置条件: - 仓库已启用 Actions
    - 测试分支存在
  - 操作步骤: 1. 在 workflow 中定义 workflow_dispatch inputs 并指定 type: string
    2. 提交并推送该 workflow
    3. 触发 workflow 并传入参数
  - 预期结果: - workflow 应被平台接受，不报错
    - string 类型的 input 应能正常接收和输出
  - 验证点: - [正向] workflow 校验通过
    - [正向] string 类型 input 能正常传递和使用

- **实际行为**:
  - Job "Verify string input acceptance" status=COMPLETED

- **对照 GitCode 规格** `phase01/inputs/gitcode-spec/core-concepts/trigger-events.md`:
  - 规格摘要:
    ```
# 触发事件
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
| `schedule` | 定时触发 | `on: schedule: - cron: '0 2 *
    ```
  - 测试 YAML 工作流模式与此规格承诺一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (manual)
  - Phase 01 前置条件: - 仓库已启用 Actions
    - 测试分支存在

**置信度**: 中（job 执行成功但断言评判未通过，需进一步确认断言逻辑）

**影响**:
- **阻塞性**: 🟡非阻塞 — job 执行成功，功能正常
- **静默性**: 🟢明确报错 — 断言差异可通过 logs/assertions 定位
- **影响面**: 🟢单用例 — 仅本用例断言未通过
- **综合**: 基于上述证据，COMPAT-INPUTS-01-002 的失败根因初步判定为 **标记不匹配**（责任人: **Phase 01**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可调整断言评判规则或补充环境配置

**建议**:
- 复查断言评判器对 COMPAT-INPUTS-01-002 的判断逻辑
