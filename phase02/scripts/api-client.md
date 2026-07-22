# API Client（api-client）

## 类型
确定性脚本（Bash + curl + jq）

## 职责
封装所有 GitCode API 调用，为其他脚本提供统一、可测试的接口。隔离 API 细节（Base URL、认证、分页、错误处理），让上层脚本不直接拼 curl。

## 依赖
- `curl`（HTTP 请求）
- `jq`（JSON 解析）
- 环境变量：`GITCODE_API_BASE_URL`（默认 `https://api.gitcode.com`）、`GITCODE_ACCESS_TOKEN`

## API 方法清单

### 流水线运行记录

```bash
# 获取仓库所有 run（支持分页与过滤）
api_list_runs <owner> <repo> [event] [status] [branch] [per_page] [page]
# GET /api/v8/repos/:owner/:repo/actions/runs

# 获取单次 run 详情
api_get_run <owner> <repo> <run_id>
# GET /api/v8/repos/:owner/:repo/actions/runs/:run_id
# 返回: { id, status, conclusion, created_at, updated_at, ... }
```

### Job（任务）

```bash
# 获取 run 的 job 列表
api_list_jobs <owner> <repo> <run_id> [per_page] [page]
# GET /api/v8/repos/:owner/:repo/actions/runs/:run_id/jobs

# 获取单个 job 详情
api_get_job <owner> <repo> <run_id> <job_id>
# GET /api/v8/repos/:owner/:repo/actions/runs/:run_id/jobs/:job_id

# 下载 job 日志（★ 端点名是 download_log 下划线，不是 download-log 连字符）
api_download_job_log <owner> <repo> <run_id> <job_id> [output_file]
# GET /api/v8/repos/:owner/:repo/actions/runs/:run_id/jobs/:job_id/download_log
# ✅ 2026-07-21 实测可用：返回 302 → raw.gitcode.com → 200 application/zip
#    zip 内每个 step 一个 `{seq}_{step_name}.log`（UTF-8 无 BOM），内容为完整 runner 输出。
```

> **日志正文取法（已跑通，用 OAuth token，无需浏览器会话）**
>
> ```
> GET /api/v8/repos/:owner/:repo/actions/runs/:run_id/jobs/:job_id/download_log?access_token=<TOKEN>
> → 302 重定向到 raw.gitcode.com → 200 application/zip
> → 解压：每 step 一个 .log 文件
> ```
> **三个坑（都踩过）**：
> 1. 端点名 **`download_log`（下划线）** 才对；`download-log`（连字符）恒 404——早期只测连字符导致误判"平台缺陷"。
> 2. 必须**跟随 302 重定向**（curl -L / urllib 默认跟随）；不跟只看到 302 空响应。
> 3. job id：`/actions/runs/{run}/jobs` 的 `jobs[].id` 在某些场景为空串；以 **run detail 的 `stages.jobs[].id`** 为准更可靠。
>
> - 鉴权：**OAuth token**（`?access_token=`），不需要浏览器 cookie，不受 WAF、不会几天过期。
> - 封装见 **`log_fetcher.py`**（`list_jobs` / `download_job_log_zip` / `fetch_job_logs` / `render_job_logs`）。
> - 已验证**掩码真实生效**（secret 值在日志显示为 `***`）→ 负向 `must_not_contain_secret` 与掩码类用例可确定性判定。
>
> ⚠️ 旧方案（web-api.gitcode.com + 浏览器 Bearer/cookie + 过 WAF）**已废弃**——它能用但依赖会过期的浏览器会话。zip 方案只需 OAuth token，更稳，取代之。

### Artifacts（制品）

```bash
# 列出仓库 artifacts
api_list_artifacts <owner> <repo> [per_page] [page]
# GET /api/v8/repos/:owner/:repo/actions/artifacts

# 列出某 run 的 artifacts
api_list_run_artifacts <owner> <repo> <run_id>
# GET /api/v8/repos/:owner/:repo/actions/runs/:run_id/artifacts

# 获取 artifact 详情
api_get_artifact <owner> <repo> <artifact_id>
# GET /api/v8/repos/:owner/:repo/actions/artifacts/:artifact_id

# 下载 artifact
api_download_artifact <owner> <repo> <artifact_id> <archive_format> [output_dir]
# GET /api/v8/repos/:owner/:repo/actions/artifacts/:artifact_id/:archive_format

# 删除 artifact（teardown 用）
api_delete_artifact <owner> <repo> <artifact_id>
# DELETE /api/v8/repos/:owner/:repo/actions/artifacts/:artifact_id
```

### Runner 管理

```bash
# 列出仓库所有主机 Runner
api_list_runners <owner> <repo>
# GET /api/v8/repos/:owner/:repo/actions/runners

# 列出仓库所有 K8S Runner
api_list_runner_sets <owner> <repo>
# GET /api/v8/repos/:owner/:repo/actions/runner-sets
```

## 实现示意

```bash
#!/bin/bash
# api-client.sh — include 后提供上述函数
# 全局配置
: ${GITCODE_API_BASE_URL:="https://api.gitcode.com"}
: ${GITCODE_ACCESS_TOKEN:?请设置 GITCODE_ACCESS_TOKEN 环境变量}

# 统一请求封装
# ★ 认证：Authorization: Bearer 请求头（不是 ?access_token= 查询参数——后者会报 PARAMETER_ERROR）
# ★ 列 run 用 per_page=10 较稳；部分节点偶发 PARAMETER_ERROR(codeArtsIds)，需重试穿透（见下 _gitcode_api_retry）
_gitcode_api() {
  local method="$1" path="$2" qs="$3"
  local url="${GITCODE_API_BASE_URL}${path}"
  [ -n "$qs" ] && url="${url}?${qs}"
  curl -s -X "$method" -H "Authorization: Bearer ${GITCODE_ACCESS_TOKEN}" "$url"
}

# 带重试的封装：穿透偶发 PARAMETER_ERROR（见 PLATFORM-NOTES.md §3）
_gitcode_api_retry() {
  local i
  for i in $(seq 1 15); do
    local out; out=$(_gitcode_api "$@")
    if ! echo "$out" | grep -q 'PARAMETER_ERROR'; then echo "$out"; return 0; fi
    sleep 3
  done
  echo "$out"; return 1
}

api_get_run() {
  local owner="$1" repo="$2" run_id="$3"
  _gitcode_api GET "/api/v8/repos/${owner}/${repo}/actions/runs/${run_id}"
}

api_list_jobs() {
  local owner="$1" repo="$2" run_id="$3" per_page="${4:-20}" page="${5:-1}"
  _gitcode_api GET "/api/v8/repos/${owner}/${repo}/actions/runs/${run_id}/jobs" \
    "per_page=${per_page}&page=${page}"
}

api_download_job_log() {
  local owner="$1" repo="$2" run_id="$3" job_id="$4" output="${5:-/dev/stdout}"
  _gitcode_api GET "/api/v8/repos/${owner}/${repo}/actions/runs/${run_id}/jobs/${job_id}/download-log" \
    "" > "$output"
}

# ...其他函数类似
```

## 错误处理
- **认证**：`Authorization: Bearer <token>` 请求头；`?access_token=` 查询参数会报 `PARAMETER_ERROR`。
- **偶发 `PARAMETER_ERROR(codeArtsIds)`**：list runs 时部分后端节点会返回，非参数真错——用 `_gitcode_api_retry` 重试穿透。
- **run 校验错误 API 看不到**：编译失败的 run，v8 API 的 `message` 是 `null`、job 数为 0、`event=PUSH`、耗时 1s。
  具体 Validation Error 只在**网页 run 详情页**「N 个错误」处可见（见 PLATFORM-NOTES.md §3）。
- HTTP 4xx → 记录错误响应，调用方据此判断（401=token 过期，404=资源不存在）
- HTTP 5xx → 重试最多 2 次（间隔 2s），仍失败则返回错误
- 网络超时 → curl `--connect-timeout 10 --max-time 30`

## 质量要求
- 所有函数有明确的输入/输出契约
- 错误时输出 JSON `{ "error": "message", "http_status": nnn }`
- 不写日志文件（调用方自己 redirect）
