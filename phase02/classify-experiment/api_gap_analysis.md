# Phase 02 所需但缺失的 API

对照 `phase01/inputs/gitcode-api/api-reference.md`（20 个 Actions API + 4 个相邻 API hint），
分析 197 个 case 的全部阻断项 → API 缺口。

## 结论摘要：需要的新 API / 确认的端点

### 🔴 完全缺失的 API（api-reference 中无任何提及）

| API | 用途 | 影响 case 数 |
|-----|------|-------------|
| `POST /api/v5/repos/:owner/:repo/forks` | 创建 fork | 13 (fork_pr trigger) |
| `POST /api/v5/repos/:owner/:repo/pulls` | 创建 PR（pr/pull_request 触发） | 13 fork + 5 pr + 1 pull_request + 1 pull_request_target = 20 |
| `POST /api/v8/repos/:owner/:repo/actions/workflows/:workflow_id/dispatch` | workflow_dispatch (manual 触发) | 5 |
| `POST /api/v5/repos/:owner/:repo/pulls/:number/comments` | PR comment (pull_request_comment 触发) | 1 |
| `POST /api/v8/repos/:owner/:repo/actions/runs/:run_id/cancel` | 取消运行 (fault_injection kill_runner) | 2 (CHAOS cases) |

### 🟡 API 已存在但未集成到 assertion_engine

| 已有 API | 当前用途 | 缺失的 assertion kind |
|----------|----------|----------------------|
| `GET .../actions/artifacts` + download | 只在 api-reference 中有，log_fetcher 未调用 | artifact 内容断言 (1 case) |
| `GET .../actions/runners` | 只在 api-reference 中有，未集成 | runner_schedulable / runner_scheduling (3 cases) |
| `POST /api/v2/.../actions/valid` | validate_workflow.py 已实现，未入 assertion_engine | workflow_validation (2 cases) |
| `GET .../actions/runs/:id` (start_time/end_time) | workflow_runner 已调用但不计算 duration | run_duration (2 cases) |

### 🟢 非 API 问题（infra / 账号 / LLM / UI）

| 阻断 | 数量 | 解决方式 |
|------|------|---------|
| `trigger.as=untrusted_contributor` | 17 | 需第二 GitCode 账号 + OAuth token（非 API，是账号资源） |
| `schedule` trigger | 5 | cron 无法按需触发；变通：push trigger + 手动设 ATOMGIT_EVENT_NAME=schedule |
| `eval=llm_assisted` | 44 | 需 LLM 集成到 assertion_engine（非 API） |
| `target=run_ui / pr_ui` | 4 | 需 Playwright 浏览器自动化（非 API） |
| `target=badge_response` | 3 | HTTP GET badge URL，非 GitCode API，直接 curl 即可 |
| `fault_injection` / `network_partition` / `concurrent_flood` | 3+2 | 需 infra 层能力（kill runner、断网、并发 flood） |
| `setup.repo_fixture` 未知 | ~18 | 需预先创建配置好的测试仓 |

## 按 Case 明细：哪些 case 需要什么 API

### `POST /api/v5/repos/:owner/:repo/pulls` (18 cases)

- COMPAT-PR-TYPES-02-001
- SEC-ENV-POLLUTE-02-001
- SEC-FORK-02-001
- SEC-FORK-02-002
- SEC-FORK-02-003
- SEC-FORK-02-004
- SEC-FORK-02-005
- SEC-INJECT-02-001
- SEC-INJECT-02-002
- SEC-INJECT-02-003
- SEC-INJECT-02-004
- SEC-INJECT-02-005
- SEC-INJECT-02-006
- SEC-SUPPLY-02-002
- SEC-TOCTOU-02-001
- SEC-TOKEN-02-001
- USE-ERR-MSG-02-002
- USE-PR-CHECKS-02-001

### `POST /api/v5/repos/:owner/:repo/forks` (13 cases)

- SEC-FORK-02-001
- SEC-FORK-02-002
- SEC-FORK-02-003
- SEC-FORK-02-004
- SEC-FORK-02-005
- SEC-INJECT-02-001
- SEC-INJECT-02-002
- SEC-INJECT-02-003
- SEC-INJECT-02-004
- SEC-INJECT-02-005
- SEC-INJECT-02-006
- SEC-SUPPLY-02-002
- SEC-TOKEN-02-001

### `需要第二 GitCode 账号的 OAuth token` (13 cases)

- SEC-FORK-02-001
- SEC-FORK-02-002
- SEC-FORK-02-003
- SEC-FORK-02-004
- SEC-FORK-02-005
- SEC-INJECT-02-001
- SEC-INJECT-02-002
- SEC-INJECT-02-003
- SEC-INJECT-02-004
- SEC-INJECT-02-005
- SEC-INJECT-02-006
- SEC-SUPPLY-02-002
- SEC-TOKEN-02-001

### `POST /api/v8/repos/:owner/:repo/actions/workflows/:workflow_id/dispatch` (5 cases)

- COMP-CONCUR-02-001
- COMPAT-CONCUR-02-001
- REL-CONCUR-02-002
- REL-CONCUR-02-003
- USE-INPUTS-DEFAULT-02-001

### `` (5 cases)

- COMP-CONCUR-02-001
- COMPAT-CONCUR-02-001
- REL-CONCUR-02-002
- REL-CONCUR-02-003
- USE-INPUTS-DEFAULT-02-001

### `（run 列表过滤参数有 event=Manual，说明平台已支持 manual 触发；` (5 cases)

- COMP-CONCUR-02-001
- COMPAT-CONCUR-02-001
- REL-CONCUR-02-002
- REL-CONCUR-02-003
- USE-INPUTS-DEFAULT-02-001

### `dispatch API 需从 GitCode 侧确认端点路径、请求体格式）` (5 cases)

- COMP-CONCUR-02-001
- COMPAT-CONCUR-02-001
- REL-CONCUR-02-002
- REL-CONCUR-02-003
- USE-INPUTS-DEFAULT-02-001

### `(api-reference 相邻 API 中提及 v5 pull requests，但未列出完整端点；需确认参数格式、PR 创建后 run 关联方式)` (5 cases)

- COMPAT-PR-TYPES-02-001
- SEC-ENV-POLLUTE-02-001
- SEC-TOCTOU-02-001
- USE-ERR-MSG-02-002
- USE-PR-CHECKS-02-001

### `POST /api/v8/repos/:owner/:repo/actions/runs/:run_id/cancel` (5 cases)

- REL-CHAOS-02-001
- REL-CHAOS-02-002
- REL-CHAOS-02-003
- REL-CONCUR-02-004
- REL-RACE-02-001

### `无标准 API 可模拟 network_partition（需 infra 层操作）` (5 cases)

- REL-CHAOS-02-001
- REL-CHAOS-02-002
- REL-CHAOS-02-003
- REL-CONCUR-02-004
- REL-RACE-02-001

### `无标准 API 可模拟 concurrent_flood（需大量并发 dispatch 调用）` (5 cases)

- REL-CHAOS-02-001
- REL-CHAOS-02-002
- REL-CHAOS-02-003
- REL-CONCUR-02-004
- REL-RACE-02-001

### `POST /api/v5/repos/:owner/:repo/pulls/:number/comments` (1 cases)

- COMPAT-PR-COMM-02-001

### `（api-reference 提及 v5 Issues 但未提及 PR comments 端点）` (1 cases)

- COMPAT-PR-COMM-02-001
