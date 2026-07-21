# Workflow Runner（workflow-runner）

## 类型
确定性脚本（Bash + git + api-client）

## 职责
执行用例链路中的「③ 部署 + 触发」和「④ 等待 + 采集」。负责将 yaml-compiler 产出的 workflow YAML 部署到测试仓库、按 trigger 方式触发执行、轮询等待完成、采集全量结果。

## 依赖
- `api-client` 脚本（调用 GitCode API）
- `env-manager` 脚本（提供测试仓库上下文）
- `git`（push workflow YAML、创建分支/tag/PR）
- `jq`（JSON 解析）

## 输入
- 用例 YAML（单条）
- 编译后的 workflow YAML 文件内容（由 yaml-compiler 产出）
- 测试仓库上下文：`{ owner, repo, branch, fixture_type }`（由 env-manager 提供）
- API token（环境变量）

## 处理逻辑

### 阶段一：部署

```bash
# 1. clone 测试仓库
git clone <repo_url> /tmp/test-repo-<case-id>
cd /tmp/test-repo-<case-id>

# 2. 确保 .gitcode/workflows/ 目录存在
mkdir -p .gitcode/workflows/

# 3. 写入编译后的 workflow YAML
#    文件名从用例 id 派生，如 SEC-FORK-01-001 → sec-fork-001.yml
echo "$COMPILED_YAML" > .gitcode/workflows/<name>.yml

# 4. commit + push
git add .gitcode/workflows/<name>.yml
git commit -m "test: Phase 02 case <id>"
git push origin <branch>
```

### 阶段二：触发

> ⚠️ **实测约束（见 `phase02/PLATFORM-NOTES.md` §2）**：在测试仓库上 **push 不会可靠自动触发**流水线
> （所有 `event=PUSH` 的 run 都 ~1s 失败或不创建 run），**只有手动触发 / `workflow_dispatch` 能真正跑起来**
> （PILOT-BASIC #1、USE-DOC-02-003 #2 均为 Manual → COMPLETED）。而 `workflow_dispatch` 的 dispatch API
> 目前全部 404、PAT 只能读不能触发。**批量执行前触发方式必须先定**。下方 `push` 分支按现状不可靠。

根据 `trigger.event` 选择触发方式：

```bash
case "$TRIGGER_EVENT" in
  push)
    # git push 即自然触发，记录 push 后最新 run_id
    RUN_ID=$(api_get_latest_run "$OWNER" "$REPO" "$BRANCH")
    ;;
  pr|fork_pr)
    # 创建 PR（按 trigger.as 切换身份）
    # maintainer: 直接用主身份创建 PR
    # untrusted_contributor: 在 fork 仓库创建 PR（如不可行则模拟）
    PR_ID=$(create_pr "$OWNER" "$REPO" "$BRANCH" "target_branch")
    RUN_ID=$(api_get_run_by_pr "$OWNER" "$REPO" "$PR_ID")
    ;;
  manual)
    # 调 API 手动触发 workflow_dispatch
    # ★ 实测：dispatch API 全部 404（v8/v5 均试），PAT 触发不了。当前只能网页登录后点「运行工作流」。
    #   平台真正的 dispatch 接口待确认；确认前 manual 无法脚本化。见 PLATFORM-NOTES.md §2。
    RUN_ID=$(trigger_manual "$OWNER" "$REPO" "$WORKFLOW_ID")
    ;;
  schedule)
    # 无法立即触发，等待 cron 到点
    # 实际执行中可能需要等待或改用 manual 替代
    ;;
  tag)
    git tag "test-<case-id>-$(date +%s)"
    git push origin "test-<case-id>-$(date +%s)"
    RUN_ID=$(api_get_latest_run "$OWNER" "$REPO")
    ;;
esac

echo "$RUN_ID"  # 输出给下游
```

### 阶段三：等待完成

```bash
# 轮询等待 run 完成，有超时控制
TIMEOUT=${CASE_TIMEOUT:-1800}  # 默认 30 分钟
INTERVAL=10                     # 每 10 秒检测一次
ELAPSED=0

while [ $ELAPSED -lt $TIMEOUT ]; do
  STATUS=$(api_get_run "$OWNER" "$REPO" "$RUN_ID" | jq -r '.status')
  case "$STATUS" in
    COMPLETED|FAILED|CANCELED) break ;;
    *) sleep $INTERVAL; ELAPSED=$((ELAPSED + INTERVAL)) ;;
  esac
done

if [ $ELAPSED -ge $TIMEOUT ]; then
  echo "TIMEOUT" && exit 124
fi
```

### 阶段四：采集

```bash
# 1. Run 详情
RUN_DETAIL=$(api_get_run "$OWNER" "$REPO" "$RUN_ID")

# 2. Job 列表 + 每个 job 详情
JOBS=$(api_list_jobs "$OWNER" "$REPO" "$RUN_ID")
for job_id in $(echo "$JOBS" | jq -r '.[].id'); do
  JOB_DETAIL=$(api_get_job "$OWNER" "$REPO" "$RUN_ID" "$job_id")
  JOB_LOG=$(api_download_job_log "$OWNER" "$REPO" "$RUN_ID" "$job_id")
done

# 3. Artifacts 列表
ARTIFACTS=$(api_list_run_artifacts "$OWNER" "$REPO" "$RUN_ID")

# 4. 如有 fault_injection：在指定时机执行注入动作
if [ "$FAULT_INJECTION" != "null" ]; then
  # 见 fault_injection 处理逻辑
fi

# 5. 汇总为 RunResult JSON
jq -n \
  --arg run_id "$RUN_ID" \
  --arg status "$STATUS" \
  --arg run_detail "$RUN_DETAIL" \
  --arg jobs "$JOBS" \
  --arg logs "$JOB_LOGS" \
  --arg artifacts "$ARTIFACTS" \
  '{run_id: $run_id, status: $status, detail: $run_detail, jobs: $jobs, logs: $logs, artifacts: $artifacts}'

# 输出：RunResult JSON
```

## 故障注入处理

当 `fault_injection != null` 时：

```bash
case "$FAULT_ACTION" in
  kill_runner)
    # 在 mid_job 时 kill runner 进程
    # 需要有对 runner 实例的操作权限
    ;;
  network_partition)
    # iptables 阻断网络
    ;;
  disk_full)
    # dd 填满磁盘
    ;;
  cpu_saturate)
    # stress 打满 CPU
    ;;
  concurrent_flood)
    # 并发触发 N 个 workflow
    for i in $(seq 1 $CONCURRENCY); do
      trigger_workflow &  # 后台并发
    done
    wait
    ;;
esac
```

## 输出
- **RunResult JSON**：`{ run_id, status, conclusion, duration, jobs: [...], logs: "...", artifacts: [...], fault_injection_result }`
- 写入 `runs/<run-id>/results/<case-id>.json`（供 assertion-engine 消费）

## 超时与重试
- 默认超时 30 min（用例 YAML 可覆盖）
- API 调用重试（由 api-client 处理）
- 超时未完成的 run 输出 `TIMEOUT` 状态

## 质量要求
- 触发方式必须与 trigger.event 完全对应
- 日志完整抓取（不截断，负向断言依赖全文扫描）
- 身份切换正确（maintainer vs untrusted_contributor）
- Clone 的临时目录在完成后清理
