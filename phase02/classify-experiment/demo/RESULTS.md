# Demo Results — PR Trigger Automation Test (Final)

**时间**: 2026-07-23  
**脚本**: `demo_pr_trigger.py`, `demo_fork_pr.py`

## Summary

| 测试 | 类型 | API | 结果 |
|------|------|-----|------|
| PR #1 | same-repo | `POST /pulls` (bot token) | ❌ 无触发 |
| PR #2 | same-repo | `POST /pulls` (bot token, workflow on base first) | ❌ 无触发 |
| PR #3 | same-repo | `POST /pulls` (bot token, 30s wait + git pull sync) | ❌ 无触发 |
| **PR #4** | **fork → upstream** | **`POST /pulls` (contributor token, `head: teamfi:branch`)** | **❌ 无触发** |
| **PR #5** | **fork → upstream** | **same, no cleanup** | **❌ 无触发 (Web UI pending)** |
| **issue_comment #1** | **issue + comment** | **`POST /issues` + `POST /comments` (contributor)** | **❌ 无触发** |

## What Works

| 能力 | 状态 |
|------|------|
| `POST /api/v5/repos/.../forks` — 创建 fork | ✅ |
| Contributor token clone fork + push 分支 | ✅ |
| `POST /api/v5/repos/.../pulls` 跨仓库 PR (`head: owner:branch`) | ✅ |
| `PATCH .../pulls/:id` 关闭 PR | ✅ |
| Bot 推 workflow 到 upstream main | ✅ |
| Fork 检测与复用 | ✅ |
| `on: push` workflow 触发 (bot push) | ✅ |

## What Fails

| 能力 | 尝试次数 | 原因 |
|------|----------|------|
| **`on: pull_request` 触发** | 4 (same-repo ×3 + fork ×1) | **平台不触发** |
| `pull_request_id` filter on v8 runs API | 4 | 始终返回 0 |

## Root Cause

**GitCode 的 `POST /api/v5/repos/.../pulls` API 创建的 PR 不会自动触发 `on: pull_request` workflow。** 平台可能仅对 Web UI 创建的 PR 触发，或需要其他触发机制（webhook push event）。

This is a **platform limitation**, not an automation bug. The full fork→PR pipeline is scriptable, but the platform doesn't fire the trigger.

## Next Steps

1. **Web UI 手动创建 PR** — 验证 Web UI 创建的 PR 是否会触发 `on: pull_request` workflow
2. **Push-triggered workaround** — 用 `on: push` 替代 `on: pull_request`，在 PR 分支 push 时触发
3. **联系平台方** — 确认 API 创建的 PR 是否应该触发 workflow，或是否需要额外参数
