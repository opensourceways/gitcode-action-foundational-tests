## 失败分诊 · COMPAT-ENV-01-001 · ATOMGIT_SHA 环境变量应正确返回触发提交 SHA

**判定结果**: FAIL
**失败断言**:
assertions (ATOMGIT_SHA) — job COMPLETED，但 atomgit_sha= 为空，平台未注入 commit SHA

**根因初判**: 产品bug
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
  - 前置条件: - 仓库已启用 Actions
    - Runner 环境正常注入 ATOMGIT_* 变量
  - 操作步骤: 1. 在 workflow 的 run 步骤中输出 $ATOMGIT_SHA
    2. 触发 workflow 运行
  - 预期结果: - $ATOMGIT_SHA 应返回当前触发事件的提交 SHA（40 位十六进制字符串）
  - 验证点: - [正向] 日志中 ATOMGIT_SHA 的值不为空且为有效 SHA 格式

- **实际行为**:
  - Job "Test ATOMGIT_SHA env var" status=COMPLETED
  - ATOMGIT_SHA 为空，workflow_dispatch 事件未注入 commit SHA

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
    - Runner 环境正常注入 ATOMGIT_* 变量

**置信度**: 中（job 执行成功但断言评判未通过，需进一步确认断言逻辑）

**影响**:
- **阻塞性**: 🟡非阻塞 — job 执行成功，功能正常
- **静默性**: 🟢明确报错 — 断言差异可通过 logs/assertions 定位
- **影响面**: 🟢单用例 — 仅本用例断言未通过
- **综合**: 基于上述证据，COMPAT-ENV-01-001 的失败根因初步判定为 **产品bug**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可调整断言评判规则或补充环境配置

**建议**:
- 复查断言评判器对 COMPAT-ENV-01-001 的判断逻辑
