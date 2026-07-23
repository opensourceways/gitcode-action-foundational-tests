# Phase 02 API 缺口分析 (v2 — 实测后更新)

来源：`actions_ctl.py` 实测 + api-reference.md + docs.gitcode.com

## ✅ 已验证可用（v2 web-api + v8 API）

| 端点 | 方法 | 用途 | 验证 |
|------|------|------|------|
| `/api/v2/projects/{p}/actions/workflows/list` | POST | 列出 workflow | `actions_ctl.py list` |
| `/api/v2/projects/{p}/actions/workflows/{id}/dispatch` | POST | 触发 workflow_dispatch | `actions_ctl.py dispatch` → poll → COMPLETED |
| `/api/v2/projects/{p}/actions/workflow-runs/{id}/stop` | POST | 停止/取消运行 | `actions_ctl.py stop` → `{"success": true}` |
| `/api/v2/projects/{p}/actions/valid` | POST | YAML 语法校验 | `validate_workflow.py` 已集成 |
| `/api/v8/repos/{o}/{r}/actions/runs` | GET | 列出 runs | v8 api-reference |
| `/api/v8/repos/{o}/{r}/actions/runs/{id}` | GET | run 详情 | 同上 |
| `/api/v8/repos/{o}/{r}/actions/runs/{id}/jobs` | GET | job 列表 | 同上 |
| `/api/v8/repos/{o}/{r}/actions/runs/{id}/jobs/{id}/download_log` | GET | 下载日志 | 同上 |
| `/api/v8/repos/{o}/{r}/actions/runners` | GET | runner 管理 | 同上 |
| `/api/v8/repos/{o}/{r}/actions/artifacts` | GET | 制品管理 | 同上 |

## ✅ 文档已有，harness 未集成（v5）

| 端点 | 用途 | 影响 |
|------|------|------|
| `POST /api/v5/repos/{o}/{r}/pulls` | 创建 PR | unlock pr/pull_request/pull_request_target (~7 case) |
| `POST /api/v5/repos/{o}/{r}/pulls/{n}/comments` | PR comment | unlock pull_request_comment (1 case) |
| `POST /api/v5/repos/{o}/{r}/forks` | 创建 fork | unlock fork_pr (~12 case) |

## 🔴 真正缺失

| 能力 | 说明 |
|------|------|
| schedule 触发 | cron 由平台调度，外部不可控。变通：dispatch + event_name=schedule |
| untrusted_contributor | 第二 GitCode 账号 + token（账号资源，非 API 缺口） |
| fault_injection infra | kill_runner 可用 stop API 模拟；network_partition/disk_full 需 infra 层 |

## 实测结果（2026-07-22-valid, 149 cases, dispatch 模式）

| 判定 | 说明 |
|------|------|
| PASS / FAIL | dispatch → poll → collect_logs → assert 全链路通过，15+ PASS |
| DISPATCH_FAIL | workflow YAML 有语法错误，dispatch 时被平台拒绝 |
| TIMEOUT | 长时间运行的 case（artifact 上传等） |
