# Phase 02 API 缺口分析

对照 `phase01/inputs/gitcode-api/api-reference.md`（20 个 Actions API），分析全部阻断项的 API 缺口。

## 总体

- 总 case: 197
- 可直接跑 (full_scriptable): 107
- 部分可跑 (partial_scriptable): 59
- 无法跑 (not_scriptable): 31

## 🔴 完全缺失的 API（api-reference 中无对应端点）

| 阻断 | 影响 case | 缺失的 API |
|------|----------|-----------|
| fork_pr | 13 | POST /api/v5/repos/:owner/:repo/forks （创建 fork）<br>POST /api/v5/repos/:owner/:repo/pulls （从 fork 分支向目标仓开 PR）<br><small>第二 GitCode 账号的 OAuth token api-reference 未提及 fork API；v5 PR 只提示了 GET 端点</small> |
| manual | 5 | POST /api/v8/repos/:owner/:repo/actions/workflows/:workflow_id/dispatch<br><small>api-reference 的 run 过滤参数有 event=Manual，说明平台支持 manual 触发，dispatch 端点路径待确认</small> |
| pr | 5 | POST /api/v5/repos/:owner/:repo/pulls （创建 PR）<br><small>api-reference 相邻 API 提示 v5 pull requests 存在，但未列出 POST 端点</small> |
| pull_request_comment | 1 | POST /api/v5/repos/:owner/:repo/pulls/:number/comments （PR comment）<br><small>api-reference 提及 v5 Issues 但未提及 PR comments</small> |
| pull_request_target | 1 | POST /api/v5/repos/:owner/:repo/pulls （创建 PR）<br><small>需额外验证 target 上下文中 fork PR 无法访问 secrets</small> |
| pull_request | 1 | POST /api/v5/repos/:owner/:repo/pulls （创建 PR）<br><small>同 pr 触发</small> |

## 🟡 API 已存在但未集成到 assertion_engine / workflow_runner

| 阻断 | 影响 case | 已有 API | 缺失的动作 |
|------|----------|---------|-----------|
| artifacts | 1 | GET /api/v8/.../actions/artifacts + download — API 已有，只需集成到 assertion_engine |  |
| run_duration | 2 | GET /api/v8/.../actions/runs/:run_id — 已有 start_time/end_time，只需计算差值 |  |
| runner_schedulable | 2 | GET /api/v8/.../actions/runners — API 已有，只需检查 runner 在线状态 |  |
| runner_scheduling | 1 |  | 同 runner_schedulable — API 已有 |
| step_summary | 1 | GET /api/v8/.../actions/runs/:run_id/jobs/:job_id — Job detail 已有 steps 信息，只需扩展 assertion_engine |  |
| workflow_validation | 2 | POST /api/v2/projects/:project/actions/valid — validate_workflow.py 已实现 |  |

## 🟢 非 API 问题

| 阻断 | 影响 case | 解决方式 |
|------|----------|---------|
| llm_assisted | 44 | 非 API 问题 — 需 LLM 辅助判定通道集成到 assertion_engine 44 条中 27 条 target=error_message（可诊断性评估），其余在 run_logs/run_ui 等 |
| schedule | 5 | 非 API 问题。cron 由平台按时调度，外部无法触发。变通：push trigger + ATOMGIT_EVENT_NAME=schedule |
| badge | 3 | 非 GitCode API — HTTP GET badge URL 即可，直接用 curl/libcurl |
| pr_ui | 1 | 同 run_ui — 需 Playwright |
| run_ui | 3 | 非 API 问题 — 需 Playwright 浏览器自动化检查 Web UI |
| untrusted | 17 | 第二 GitCode 账号 + OAuth token（非 API 缺口，是账号资源） 即使 trigger=push 也需以 untrusted 身份 push 到 fork → 开 PR |

## 🔴 fault_injection 特例

| 阻断 | 影响 case | 需要的能力 |
|------|----------|-----------|
| fault_injection | 5 | POST /api/v8/repos/:owner/:repo/actions/runs/:run_id/cancel （kill_runner 模拟） network_partition 需 infra 层操作（无标准 API） concurrent_flood 可用 workflow_dispatch API 批量触发模拟 |

## ⚠️ 未知 repo_fixture

- **未知 repo_fixture 'branch-protected'，需确认测试仓前置资源**: 1 cases (SEC-REFPROT-02-001)
- **未知 repo_fixture 'container-ci'，需确认测试仓前置资源**: 1 cases (COMP-CONTAINER-02-001)
- **未知 repo_fixture 'container-isolation'，需确认测试仓前置资源**: 1 cases (SEC-CONT-ISOLATE-02-001)
- **未知 repo_fixture 'matrix-ci'，需确认测试仓前置资源**: 3 cases (COMP-MATRIX-02-005, COMP-MATRIX-02-006, COMP-MATRIX-02-007)
- **未知 repo_fixture 'matrix-compat'，需确认测试仓前置资源**: 1 cases (COMPAT-MATRIX-02-001)
- **未知 repo_fixture 'preemption-ci'，需确认测试仓前置资源**: 2 cases (REL-PREEMPT-02-001, REL-PREEMPT-02-002)
- **未知 repo_fixture 'with-permissions'，需确认测试仓前置资源**: 2 cases (SEC-PERMS-02-001, USE-MIGR-02-003)
- **未知 repo_fixture 'with-pr-trigger'，需确认测试仓前置资源**: 6 cases (SEC-INJECT-02-001, SEC-INJECT-02-002, SEC-INJECT-02-003, SEC-INJECT-02-004, SEC-INJECT-02-005...)
- **未知 repo_fixture 'with-target-workflow'，需确认测试仓前置资源**: 1 cases (SEC-FORK-02-003)

> 解决方式：在测试组织下预先创建对应 fixture 仓，配置好 secrets/variables/branch_protection。非 API 缺口。
## 📋 需要向 GitCode 侧确认/申请的端点清单

| 优先级 | API 端点 | 方法 | 用途 | 影响 case 数 |
|--------|---------|------|------|-------------|
| P0 | `/api/v5/repos/:owner/:repo/pulls` | POST | 创建 PR（解锁 20 case） | 20 |
| P0 | `/api/v8/repos/:owner/:repo/actions/workflows/:workflow_id/dispatch` | POST | workflow_dispatch（解锁 5 manual case + 故障注入 flood） | 5+5 |
| P1 | `/api/v5/repos/:owner/:repo/forks` | POST | 创建 fork（解锁 13 fork_pr case） | 13 |
| P1 | `/api/v8/repos/:owner/:repo/actions/runs/:run_id/cancel` | POST | 取消运行（调试 + 5 chaos case） | 5 |
| P2 | `/api/v5/repos/:owner/:repo/pulls/:number/comments` | POST | PR comment 触发（1 case） | 1 |
