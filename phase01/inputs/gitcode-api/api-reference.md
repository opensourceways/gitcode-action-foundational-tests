<!-- source: https://docs.gitcode.com/docs/apis/ | fetched: 2026-07-20 via Playwright browser rendering -->

# GitCode Actions API 参考手册

> 来源: https://docs.gitcode.com/docs/apis/ (Actions 分类)
> 抓取方式: Playwright 浏览器渲染（页面为 Docusaurus 交互式 API 浏览器，需 JS 执行）
> 本文为 agent 使用的 API 组装参考——agent 基于此文档组装参数调用平台接口辅助测试。

## 基础信息

| 项目 | 值 |
|---|---|
| Base URL | `https://api.gitcode.com` |
| API 版本 | Actions 类使用 `v8`，其他资源（仓库/PR/Issues 等）使用 `v5` |
| 认证方式 | OAuth2.0 — 在 query string 中传 `access_token` 参数 |
| 认证获取 | `/docs/apis/oauth`（OAuth2.0 授权流程） |

## 通用约定

### 路径参数

所有 Actions API 共享以下路径参数模式：

| 参数 | 类型 | 位置 | 必填 | 说明 |
|---|---|---|---|---|
| `owner` | string | path | 是 | 仓库所属空间地址（组织或个人的地址 path） |
| `repo` | string | path | 是 | 仓库路径（path） |
| `run_id` | string | path | 是 | 流水线运行 ID |
| `job_id` | string | path | 是 | Job ID |
| `artifact_id` | string | path | 是 | Artifact ID |
| `archive_format` | string | path | 是 | 下载格式（如 `zip`） |
| `runner_group_id` | string | path | 是 | Runner Group ID |

### 通用查询参数（列表类接口）

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `access_token` | string | 是* | 用户授权码（OAuth2.0） |
| `per_page` | string | 否 | 每页数量，最大 100，默认 20 |
| `page` | string | 否 | 当前页码，默认 1 |

### 流水线运行记录专用过滤参数

用于 `GET /api/v8/repos/:owner/:repo/actions/runs`：

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `event` | string | 否 | 触发事件类型：`MR`（mr事件）、`Push`（推送事件）、`Manual`（手动触发） |
| `status` | string | 否 | 运行状态：`COMPLETED`（已完成）、`RUNNING`（运行中）、`FAILED`（失败）、`CANCELED`（取消）、`IGNORED`（忽略）、`PAUSED`（暂停）、`SUSPEND`（挂起） |
| `branch` | string | 否 | 分支过滤 |
| `executor` | string | 否 | 触发人用户名 |
| `pull_request_id` | string | 否 | PR 的编号 |
| `workflow_id` | string | 否 | 流水线 ID |
| `workflow_name` | string | 否 | 流水线名称 |
| `startTime` | string | 否 | 开始时间过滤 |
| `endTime` | string | 否 | 结束时间过滤 |

---

## Actions API 端点全清单（20 个）

### 流水线运行记录

#### 1. 获取仓库所有的流水线运行记录
```
GET /api/v8/repos/:owner/:repo/actions/runs
```
- **路径参数**: `owner`, `repo`
- **查询参数**: 见上方「流水线运行记录专用过滤参数」+ 通用查询参数
- **用途**: 获取指定仓库的所有流水线运行记录，支持按事件/状态/分支/触发人/PR/时间过滤分页

#### 2. 获取流水线运行详情
```
GET /api/v8/repos/:owner/:repo/actions/runs/:run_id
```
- **路径参数**: `owner`, `repo`, `run_id`
- **查询参数**: `access_token`
- **用途**: 获取单次流水线运行的详细信息（状态、耗时、触发信息等）

### Job（任务）

#### 3. 获取工作流运行的 jobs 列表
```
GET /api/v8/repos/:owner/:repo/actions/runs/:run_id/jobs
```
- **路径参数**: `owner`, `repo`, `run_id`
- **查询参数**: `access_token` + 通用查询参数
- **用途**: 获取某次运行中的所有 Job 列表（含状态、Runner 标签、耗时）

#### 4. 获取工作流运行的 job 详情
```
GET /api/v8/repos/:owner/:repo/actions/runs/:run_id/jobs/:job_id
```
- **路径参数**: `owner`, `repo`, `run_id`, `job_id`
- **查询参数**: `access_token`
- **用途**: 获取单个 Job 的完整信息（steps、日志指针等）

#### 5. 下载工作流运行的 job 日志
```
GET /api/v8/repos/:owner/:repo/actions/runs/:run_id/jobs/:job_id/download-log
```
- **路径参数**: `owner`, `repo`, `run_id`, `job_id`
- **查询参数**: `access_token`
- **用途**: 下载 Job 的完整日志文件——**测试断言的直接证据源**（检查日志中是否出现/不出现特定内容）

### Artifacts（制品）

#### 6. 列出仓库的 Artifacts
```
GET /api/v8/repos/:owner/:repo/actions/artifacts
```
- **路径参数**: `owner`, `repo`
- **查询参数**: `access_token` + 通用查询参数

#### 7. 列出特定 Run 的 Artifacts
```
GET /api/v8/repos/:owner/:repo/actions/runs/:run_id/artifacts
```
- **路径参数**: `owner`, `repo`, `run_id`
- **查询参数**: `access_token`

#### 8. 获取 Artifact 详情
```
GET /api/v8/repos/:owner/:repo/actions/artifacts/:artifact_id
```
- **路径参数**: `owner`, `repo`, `artifact_id`
- **查询参数**: `access_token`

#### 9. 删除指定 Artifact
```
DELETE /api/v8/repos/:owner/:repo/actions/artifacts/:artifact_id
```
- **路径参数**: `owner`, `repo`, `artifact_id`
- **查询参数**: `access_token`
- **用途**: 测试清理——用例 teardown 阶段用于删除测试产生的制品

#### 10. 下载指定 Artifact
```
GET /api/v8/repos/:owner/:repo/actions/artifacts/:artifact_id/:archive_format
```
- **路径参数**: `owner`, `repo`, `artifact_id`, `archive_format`（如 `zip`）
- **查询参数**: `access_token`
- **用途**: 验证制品内容是否正确生成

### Runner 管理

#### 11. 查询指定仓库下的所有主机 Runner
```
GET /api/v8/repos/:owner/:repo/actions/runners
```
- **路径参数**: `owner`, `repo`
- **查询参数**: `access_token`

#### 12. 查询分享给仓库的所有主机 Runner
```
GET /api/v8/repos/:owner/:repo/actions/runners/shared-runners
```
- **路径参数**: `owner`, `repo`
- **查询参数**: `access_token`

#### 13. 查询指定仓库下的所有 K8S Runner
```
GET /api/v8/repos/:owner/:repo/actions/runner-sets
```
- **路径参数**: `owner`, `repo`
- **查询参数**: `access_token`

#### 14. 查询分享给仓库的所有 K8S Runner
```
GET /api/v8/repos/:owner/:repo/actions/shared-runner-sets
```
- **路径参数**: `owner`, `repo`
- **查询参数**: `access_token`

### Runner Group（组织级）

#### 15. 查询指定组织下的所有 Runner Group
```
GET /api/v8/orgs/:org/actions/runner-groups
```
- **路径参数**: `org`
- **查询参数**: `access_token`

#### 16. 获取指定 Runner Group 的详细信息
```
GET /api/v8/orgs/:org/actions/runner-groups/:runner_group_id
```
- **路径参数**: `org`, `runner_group_id`
- **查询参数**: `access_token`

#### 17. 查询指定 Runner Group 下的所有主机 Runner
```
GET /api/v8/orgs/:org/actions/runner-groups/:runner_group_id/runners
```
- **路径参数**: `org`, `runner_group_id`
- **查询参数**: `access_token`

#### 18. 查询指定 Runner Group 下的所有 K8S Runner
```
GET /api/v8/orgs/:org/actions/runner-groups/:runner_group_id/runners/sets
```
- **路径参数**: `org`, `runner_group_id`
- **查询参数**: `access_token`

#### 19. 查询有权访问指定 Runner Group 的仓库列表
```
GET /api/v8/orgs/:org/actions/runner-groups/:runner_group_id/shared-namespaces
```
- **路径参数**: `org`, `runner_group_id`
- **查询参数**: `access_token`

---

## 典型 Agent 调用场景

### 场景 1：验证 workflow 运行状态

```
GET /api/v8/repos/{owner}/{repo}/actions/runs/{run_id}
→ 返回 status / conclusion / created_at / updated_at
→ 断言: status == "COMPLETED" AND conclusion == "success"
```

### 场景 2：验证 Job 日志不包含 secret

```
GET /api/v8/repos/{owner}/{repo}/actions/runs/{run_id}/jobs
→ 找到目标 job_id
GET /api/v8/repos/{owner}/{repo}/actions/runs/{run_id}/jobs/{job_id}/download-log
→ grep 日志内容
→ 断言: MUST_NOT contain secret value
```

### 场景 3：验证 fork PR 隔离

```
# 以 fork 贡献者身份触发 workflow
# 步骤 1: 确认 run 完成
GET /api/v8/repos/{owner}/{repo}/actions/runs/{run_id}
# 步骤 2: 检查 job 日志
GET /api/v8/repos/{owner}/{repo}/actions/runs/{run_id}/jobs/{job_id}/download-log
→ 断言: MUST_NOT contain secret value
```

### 场景 4：并发控制验证

```
# 触发 N 个 workflow_dispatch 后
GET /api/v8/repos/{owner}/{repo}/actions/runs?status=RUNNING&per_page=100
→ 返回当前正在运行的 runs 数量
→ 断言: count(runs) <= concurrency.max
```

### 场景 5：清理测试制品
```
DELETE /api/v8/repos/{owner}/{repo}/actions/artifacts/{artifact_id}
→ 用例 teardown 阶段清理
```

### 响应 Schema（以 runs 列表接口为例）

```json
{
  "total_count": 0,
  "workflow_runs": [
    {
      "workflow_run_id": "string",
      "workflow_id": "string",
      "workflow_name": "string",
      "file_path": "string",
      "title": "string",
      "status": "string",
      "event": "string",
      "run_number": 0,
      "head_branch": "string",
      "head_sha": "string",
      "actor": {
        "id": "string",
        "object_id": "string",
        "login": "string",
        "name": "string"
      },
      "start_time": 0,
      "end_time": 0,
      "pause_time": 0
    }
  ]
}
```

**响应字段说明：**

| 字段 | 类型 | 说明 |
|---|---|---|
| `total_count` | integer | 总数量 |
| `workflow_runs` | object[] | 流水线运行记录数组 |
| `workflow_runs[].workflow_run_id` | string | 运行记录 ID（用于获取详情） |
| `workflow_runs[].workflow_id` | string | 流水线定义 ID |
| `workflow_runs[].workflow_name` | string | 流水线名称 |
| `workflow_runs[].file_path` | string | Workflow YAML 文件路径 |
| `workflow_runs[].title` | string | 运行标题 |
| `workflow_runs[].status` | string | 运行状态（COMPLETED/RUNNING/FAILED/CANCELED/IGNORED/PAUSED/SUSPEND） |
| `workflow_runs[].event` | string | 触发事件类型（MR/Push/Manual） |
| `workflow_runs[].run_number` | integer | 运行序号 |
| `workflow_runs[].head_branch` | string | 触发分支 |
| `workflow_runs[].head_sha` | string | 触发 commit SHA |
| `workflow_runs[].actor` | object | 触发人信息 |
| `workflow_runs[].actor.id` | string | 触发人 ID |
| `workflow_runs[].actor.login` | string | 触发人用户名 |
| `workflow_runs[].actor.name` | string | 触发人显示名 |
| `workflow_runs[].start_time` | integer | 开始时间（Unix 时间戳） |
| `workflow_runs[].end_time` | integer | 结束时间（Unix 时间戳） |
| `workflow_runs[].pause_time` | integer | 暂停时间（Unix 时间戳） |

## curl 调用示例

```bash
# 列出仓库的流水线运行记录
curl -s "https://api.gitcode.com/api/v8/repos/$OWNER/$REPO/actions/runs?access_token=$TOKEN&per_page=20&status=COMPLETED"

# 获取单次运行详情
curl -s "https://api.gitcode.com/api/v8/repos/$OWNER/$REPO/actions/runs/$RUN_ID?access_token=$TOKEN"

# 下载 job 日志
curl -s "https://api.gitcode.com/api/v8/repos/$OWNER/$REPO/actions/runs/$RUN_ID/jobs/$JOB_ID/download-log?access_token=$TOKEN"
```

## 相邻 API 分类（非 Actions，但相关）

| 分类 | 版本 | 示例端点 | 可能关联的测试场景 |
|---|---|---|---|
| Pull Requests | v5 | `GET /api/v5/repos/:owner/:repo/pulls` | 验证 PR 事件触发 workflow |
| Webhooks | v5 | `GET /api/v5/repos/:owner/:repo/hooks` | 验证 webhook 与 workflow 触发关联 |
| Repositories | v5 | `GET /api/v5/repos/:owner/:repo/git/trees/:sha` | 验证 checkout 行为 |
| Issues | v5 | `POST /api/v5/repos/:owner/issues` | 验证 issue_comment 触发 |

---

## Agent 使用指引

1. **认证准备**: 需要有效的 OAuth2.0 `access_token`。建议在 `inputs/platform-config/` 或环境变量中配置测试专用 token。
2. **Base URL**: 所有请求以 `https://api.gitcode.com` 为前缀。agent 组装 URL 时必须使用完整路径。
3. **分页**: 列表类接口默认每页 20 条，最大 100 条。遍历全量数据时用 `page` 参数翻页。
4. **响应格式**: JSON。状态码遵循 HTTP 标准（200 成功，4xx/5xx 错误）。
5. **幂等性**: GET 请求幂等，DELETE 需注意后续调用可能返回 404。
