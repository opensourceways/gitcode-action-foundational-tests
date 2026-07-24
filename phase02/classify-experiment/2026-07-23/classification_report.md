# Case 可脚本化分类报告 — 2026-07-23 VALID

**数据源**: `phase02/classify-experiment/2026-07-23/VALID/` (平台校验通过的 cases)
**分类规则**: `phase02/classify-experiment/quick-start.md` (基于 demo 实测)

## 总体统计

| 分类 | 数量 | 占比 | 含义 |
|------|------|------|------|
| `scriptable` | **13** | 4.4% | push trigger + 全部断言可映射 |
| `api_blocked` | **35** | 11.8% | API 调用可行，平台不触发 (非代码问题) |
| `untested` | **243** | 81.8% | API 尚未验证可行性 |
| `fixture_gap` | **2** | 0.7% | trigger 可触发但缺 repo fixture |
| `fault_gap` | **0** | 0.0% | 需故障注入基础设施 |
| `assertion_gap` | **4** | 1.3% | trigger 可触发但断言需新 kind |

## 按维度 × 分类

| 维度 | scriptable | api_blocked | untested | fixture_gap | fault_gap | assertion_gap | 合计 |
|------|------|------|------|------|------|------|------|
| completeness | 6 | 10 | 57 | 0 | 0 | 2 | 75 |
| compatibility | 1 | 8 | 66 | 2 | 0 | 1 | 78 |
| reliability | 3 | 0 | 65 | 0 | 0 | 1 | 69 |
| security | 1 | 15 | 27 | 0 | 0 | 0 | 43 |
| usability | 2 | 2 | 28 | 0 | 0 | 0 | 32 |
| **合计** |  | **13 | **35 | **243 | **2 | **0 | **4** | **297** |

---

## 阻断项汇总（按唯一 case 去重）

### Trigger 层

| 阻断 | Cases | 说明 |
|------|-------|------|
| trigger workflow_dispatch: API not yet tested | 243 | (待 API 验证)
| trigger pull_request: API works, platform does NOT fire trigger | 17 | (API 已打通，平台不触发)
| trigger pull_request_target: API works, platform does NOT fire trigger | 10 | (API 已打通，平台不触发)
| trigger issue_comment: API works, platform does NOT fire trigger | 6 | (API 已打通，平台不触发)
| trigger pull_request_comment: API works, platform does NOT fire trigger | 1 | (API 已打通，平台不触发)
| trigger pr: unknown/unmapped trigger event | 1 |
| trigger fork_pr: API works, platform does NOT fire trigger | 1 | (API 已打通，平台不触发)
| trigger.as=untrusted_contributor: needs second account token | 1 |

### 断言层 — 需新 assertion kind

| 新 assertion kind | Cases | 示例 target |
|------|-------|------|
| `metric` | 19 | `success_rate` |
| `job_status` | 16 | `parent_status` |
| `workflow_validation` | 10 | `workflow_parse` |
| `cache` | 6 | `cache_step` |
| `run_detail` | 6 | `run_file_path` |
| `rerun` | 6 | `rerun_context` |
| `artifact_ops` | 6 | `upload_status` |
| `resource_metric` | 6 | `max_running_count` |
| `artifacts` | 4 | `artifact_available` |
| `step_summary` | 4 | `step_summary` |
| `failure_attribution` | 3 | `failure_attribution` |
| `log_detail` | 3 | `log_integrity` |
| `runner_spec` | 2 | `runner_label` |
| `http_metric` | 2 | `http_200_ratio` |
| `infra` | 2 | `pod_count` |
| `doc` | 2 | `error_stack` |
| `step_summary_html` | 1 | `step_summary_html` |
| `run_duration` | 1 | `run_duration` |
| `cancel` | 1 | `cancel_queued_status` |
| `artifact_expiry` | 1 | `download_day90_status` |

### 断言层 — LLM 辅助判定
- 65 cases 包含 `eval=llm_assisted` 断言

### 其他

| 阻断 | Cases |
|------|-------|

---

## 逐 Case 明细

### ✓ COMP-ATOMGIT-01-048 — scriptable
- 维度: completeness | 优先级: P1
- 标题: atomgit 事件相关属性可访问性
- Trigger: OK
- 断言: 3 total / 3 mappable / 0 LLM / 0 unmappable
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ✓ COMP-BOUND-01-084 — scriptable
- 维度: completeness | 优先级: P1
- 标题: 路径与分支过滤组合及否定模式边界验证
- Trigger: OK
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ✓ COMP-DIR-01-001 — scriptable
- 维度: completeness | 优先级: P1
- 标题: .gitcode/workflows/ 下的 YAML 被正确识别并触发
- Trigger: OK
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  ⬜ [1] type=positive target=run_file_path eval=deterministic → needs run detail assertion kind

### ✓ COMP-PUSH-01-001 — scriptable
- 维度: completeness | 优先级: P1
- 标题: 匹配 branches 的 push 正确触发 workflow
- Trigger: OK
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  ⬜ [1] type=positive target=run_event eval=deterministic → needs run detail assertion kind

### ✓ COMP-TRIG-01-072 — scriptable
- 维度: completeness | 优先级: P1
- 标题: push 事件关键字段与过滤验证
- Trigger: OK
- 断言: 3 total / 3 mappable / 0 LLM / 0 unmappable
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ✓ COMP-TRIG-01-078 — scriptable
- 维度: completeness | 优先级: P1
- 标题: 多事件组合与分支路径过滤验证
- Trigger: OK
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ✓ COMPAT-DIR-01-001 — scriptable
- 维度: compatibility | 优先级: P1
- 标题: 工作流目录差异——.gitcode/workflows/ 正常识别
- Trigger: OK
- 断言: 3 total / 2 mappable / 0 LLM / 1 unmappable
  ✅ [0] type=positive target=run_status eval=deterministic → equals='completed_success'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ⬜ [2] type=positive target=workflow_discovery eval=deterministic → needs workflow validation kind

### ✓ REL-FLOOD-01-036 — scriptable
- 维度: reliability | 优先级: P1
- 标题: 并发洪泛——同一仓库 10 个 push 同时触发 10 个 workflow 运行应无丢失
- Trigger: OK
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
  ⬜ [0] type=positive target=created_runs_count eval=deterministic → needs job-level status assertion kind
  ✅ [1] type=positive target=run_status eval=deterministic → equals='completed(success)'

### ✓ REL-PATHS-01-014 — scriptable
- 维度: reliability | 优先级: P1
- 标题: paths 匹配边界值——变更恰好 300 个文件时 paths 过滤应生效
- Trigger: OK
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
  ✅ [0] type=positive target=run_status eval=deterministic → equals='completed(success)'

### ✓ REL-PATHS-01-015 — scriptable
- 维度: reliability | 优先级: P1
- 标题: paths 匹配越界值——第 301 个变更文件不参与 paths 匹配判断
- Trigger: OK
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
  ✅ [0] type=positive target=run_status eval=deterministic → equals='not_triggered'

### ✓ SEC-INJ-01-004 — scriptable
- 维度: security | 优先级: P0
- 标题: 不可信 commit message 不可直接插进 run 脚本导致命令注入
- Trigger: OK
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger.as=untrusted_contributor: needs second account token
  ✅ [0] type=negative target=run_logs eval=deterministic → must_not_contain='injected_command_executed'
  ✅ [1] type=positive target=run_status eval=deterministic → equals='success'

### ✓ USE-BADGE-01-001 — scriptable
- 维度: usability | 优先级: P1
- 标题: workflow 运行完成后状态徽标及时回写且语义清晰
- Trigger: OK
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
  ✅ [0] type=positive target=run_status eval=deterministic → equals='COMPLETED'
  🤖 [1] type=nonfunctional target=ui_visual eval=llm_assisted → LLM辅助

### ✓ USE-DIR-01-001 — scriptable
- 维度: usability | 优先级: P1
- 标题: workflow 放置于 .gitcode/workflows/ 下可正常触发
- Trigger: OK
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
  ✅ [0] type=positive target=run_status eval=deterministic → equals='COMPLETED'

### ⬜ COMP-PUSH-01-002 — assertion_gap
- 维度: completeness | 优先级: P1
- 标题: 不匹配 branches 的 push 不触发 workflow
- Trigger: OK
- 断言: 1 total / 0 mappable / 0 LLM / 1 unmappable
  ⬜ [0] type=negative target=run_created eval=deterministic → needs run detail assertion kind

### ⬜ COMP-PUSH-01-003 — assertion_gap
- 维度: completeness | 优先级: P1
- 标题: paths 过滤匹配前 300 个变更文件行为符合预期
- Trigger: OK
- 断言: 1 total / 0 mappable / 0 LLM / 1 unmappable
  ⬜ [0] type=negative target=run_created eval=deterministic → needs run detail assertion kind

### ⬜ COMPAT-DIR-01-003 — assertion_gap
- 维度: compatibility | 优先级: P1
- 标题: .github/workflows 目录不应被识别且应给出迁移提示
- Trigger: OK
- 断言: 2 total / 0 mappable / 2 LLM / 2 unmappable
  🤖 [0] type=negative target=run_status eval=llm_assisted → LLM辅助
  🤖 [1] type=positive target=error_message eval=llm_assisted → LLM辅助

### ⬜ REL-FLOOD-01-037 — assertion_gap
- 维度: reliability | 优先级: P1
- 标题: 并发洪泛——同一仓库 50 个 push 同时触发应正确排队/限流不崩溃
- Trigger: OK
- 断言: 3 total / 0 mappable / 0 LLM / 3 unmappable
  ⬜ [0] type=positive target=created_runs_count eval=deterministic → needs job-level status assertion kind
  ⬜ [1] type=positive target=api_status eval=deterministic → needs HTTP metric assertion kind
  ⬜ [2] type=negative target=api_status eval=deterministic → needs HTTP metric assertion kind

### ⬜ COMPAT-CACHE-01-002 — fixture_gap
- 维度: compatibility | 优先级: P0
- 标题: cache 行为等价性——fork PR 写隔离
- Trigger: BLOCKED
- 断言: 3 total / 3 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger pr: unknown/unmapped trigger event
  - unknown repo_fixture 'with-fork-pr'
  ✅ [0] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=negative target=run_status eval=deterministic → equals='leaked_cache_to_fork'

### ⬜ COMPAT-DIR-01-002 — fixture_gap
- 维度: compatibility | 优先级: P1
- 标题: 工作流目录差异——.github/workflows/ 不应被识别
- Trigger: OK
- 断言: 3 total / 2 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - unknown repo_fixture 'with-github-dir'
  ⬜ [0] type=negative target=workflow_discovery eval=deterministic → needs workflow validation kind
  ✅ [1] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=positive target=run_status eval=deterministic → status check

### ❓ COMP-ARTIFACT-01-001 — untested
- 维度: completeness | 优先级: P1
- 标题: artifact 可在同 workflow 的 job 间正确传递
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  ✅ [1] type=positive target=run_logs eval=deterministic → contains='hello artifact'

### ❓ COMP-ARTIFACT-01-002 — untested
- 维度: completeness | 优先级: P1
- 标题: 下载全部制品功能正常
- Trigger: BLOCKED
- 断言: 3 total / 3 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  ✅ [1] type=positive target=run_logs eval=deterministic → contains='app'
  ✅ [2] type=positive target=run_logs eval=deterministic → contains='report'

### ❓ COMP-ARTIFACT-01-003 — untested
- 维度: completeness | 优先级: P1
- 标题: artifact 保留期设置生效
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=artifact_available eval=deterministic → needs artifact assertion kind
  ❌ [1] type=negative target=artifact_available_after_expiry eval=deterministic → unmapped target='artifact_available_after_expiry'

### ❓ COMP-ATOMGIT-01-047 — untested
- 维度: completeness | 优先级: P1
- 标题: atomgit 核心上下文属性可访问性
- Trigger: BLOCKED
- 断言: 3 total / 3 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-ATOMGIT-01-049 — untested
- 维度: completeness | 优先级: P1
- 标题: atomgit 边界格式校验
- Trigger: BLOCKED
- 断言: 3 total / 3 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-BOUND-01-086 — untested
- 维度: completeness | 优先级: P1
- 标题: 矩阵构建 include exclude 与单值边界验证
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-BOUND-01-087 — untested
- 维度: completeness | 优先级: P1
- 标题: 步骤输出与跨 job 传递边界验证
- Trigger: BLOCKED
- 断言: 3 total / 3 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-BOUND-01-088 — untested
- 维度: completeness | 优先级: P1
- 标题: 工作流命令 set-env add-path 与文件写入边界验证
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-CACHE-01-001 — untested
- 维度: completeness | 优先级: P0
- 标题: cache hit 时恢复缓存内容正确
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  ⬜ [1] type=positive target=cache_step eval=deterministic → needs cache assertion kind

### ❓ COMP-CACHE-01-002 — untested
- 维度: completeness | 优先级: P0
- 标题: restore-keys 前缀匹配兜底生效
- Trigger: BLOCKED
- 断言: 1 total / 0 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=cache_step eval=deterministic → needs cache assertion kind

### ❓ COMP-CALL-01-001 — untested
- 维度: completeness | 优先级: P1
- 标题: 2 层 workflow_call 嵌套正常执行
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  - unknown repo_fixture 'reusable-workflow'
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'

### ❓ COMP-CALL-01-002 — untested
- 维度: completeness | 优先级: P1
- 标题: 3 层 workflow_call 嵌套应被拒绝
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  - unknown repo_fixture 'reusable-workflow-3layer'
  ✅ [0] type=negative target=run_status eval=deterministic → equals='success'
  🤖 [1] type=nonfunctional target=error_message eval=llm_assisted → LLM辅助

### ❓ COMP-CTX-01-051 — untested
- 维度: completeness | 优先级: P1
- 标题: 上下文在 workflow job step 各级注入验证
- Trigger: BLOCKED
- 断言: 3 total / 3 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-CTX-01-052 — untested
- 维度: completeness | 优先级: P1
- 标题: 上下文在条件表达式 if 中注入验证
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-CTX-01-053 — untested
- 维度: completeness | 优先级: P1
- 标题: 上下文在 Action 插件参数中注入验证
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'

### ❓ COMP-ENVCTX-01-050 — untested
- 维度: completeness | 优先级: P1
- 标题: env 优先级链 step 大于 job 大于 workflow
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-EXPR-01-054 — untested
- 维度: completeness | 优先级: P1
- 标题: 字符串函数 contains startsWith endsWith 边界行为
- Trigger: BLOCKED
- 断言: 3 total / 3 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-EXPR-01-055 — untested
- 维度: completeness | 优先级: P1
- 标题: hashFiles 函数边界行为
- Trigger: BLOCKED
- 断言: 3 total / 3 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-EXPR-01-056 — untested
- 维度: completeness | 优先级: P1
- 标题: toJson 函数边界行为
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-EXPR-01-057 — untested
- 维度: completeness | 优先级: P1
- 标题: format substring replace 函数边界行为
- Trigger: BLOCKED
- 断言: 3 total / 3 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-ISOLATION-01-001 — untested
- 维度: completeness | 优先级: P0
- 标题: 同一 workflow 先后 job 的文件系统相互隔离
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  ✅ [1] type=negative target=run_logs eval=deterministic → must_not_contain='secret data'

### ❓ COMP-ISOLATION-01-002 — untested
- 维度: completeness | 优先级: P0
- 标题: 环境变量不跨 job 泄漏
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  ✅ [1] type=negative target=run_logs eval=deterministic → must_not_contain='env leaked'

### ❓ COMP-JOB-01-066 — untested
- 维度: completeness | 优先级: P1
- 标题: job 必填字段 name runs-on steps 验证
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-JOB-01-067 — untested
- 维度: completeness | 优先级: P1
- 标题: job 可选字段 env if timeout-minutes needs 验证
- Trigger: BLOCKED
- 断言: 3 total / 3 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-JOB-01-068 — untested
- 维度: completeness | 优先级: P1
- 标题: job strategy 矩阵与 continue-on-error 验证
- Trigger: BLOCKED
- 断言: 3 total / 3 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-PERMS-01-001 — untested
- 维度: completeness | 优先级: P0
- 标题: permissions 空对象时 ATOMGIT_TOKEN 仅 repository read
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_status eval=deterministic → equals='success'
  ✅ [1] type=positive target=run_logs eval=deterministic → contains='403'

### ❓ COMP-PERMS-01-002 — untested
- 维度: completeness | 优先级: P0
- 标题: 声明 repository write 后 TOKEN 可推送代码
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'

### ❓ COMP-RERUN-01-001 — untested
- 维度: completeness | 优先级: P1
- 标题: rerun 后 atomgit.sha 保持原始值 run_number 递增
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=rerun_context eval=deterministic → needs rerun assertion kind
  ⬜ [1] type=positive target=rerun_context eval=deterministic → needs rerun assertion kind

### ❓ COMP-RERUN-01-002 — untested
- 维度: completeness | 优先级: P1
- 标题: 第 4 次 rerun 应被系统拒绝
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 1 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=negative target=rerun_result eval=deterministic → needs rerun assertion kind
  🤖 [1] type=nonfunctional target=error_message eval=llm_assisted → LLM辅助

### ❓ COMP-RERUN-01-003 — untested
- 维度: completeness | 优先级: P1
- 标题: 超过 6 小时的运行不可 rerun
- Trigger: BLOCKED
- 断言: 1 total / 0 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=negative target=rerun_result eval=deterministic → needs rerun assertion kind

### ❓ COMP-RUNNER-01-001 — untested
- 维度: completeness | 优先级: P1
- 标题: 三段式标签正确调度到对应规格 Runner
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  ⬜ [1] type=positive target=runner_label eval=deterministic → needs runner spec assertion kind

### ❓ COMP-RUNNER-01-002 — untested
- 维度: completeness | 优先级: P1
- 标题: runs-on default 等效 ubuntu-latest x64 small
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  ⬜ [1] type=positive target=runner_spec eval=deterministic → needs runner spec assertion kind

### ❓ COMP-RUNNER-01-080 — untested
- 维度: completeness | 优先级: P1
- 标题: runner 上下文属性可访问性验证
- Trigger: BLOCKED
- 断言: 4 total / 4 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [3] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-SCRIPT-01-081 — untested
- 维度: completeness | 优先级: P1
- 标题: 仓库内脚本执行与路径验证
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-SCRIPT-01-082 — untested
- 维度: completeness | 优先级: P1
- 标题: 脚本权限设置与直接执行验证
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'

### ❓ COMP-SECRET-01-001 — untested
- 维度: completeness | 优先级: P0
- 标题: echo secret 在日志中被脱敏为 ***
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='***'
  ✅ [1] type=negative target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-SECRET-01-002 — untested
- 维度: completeness | 优先级: P0
- 标题: secret 原始值不应以明文出现在标准日志中
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-SECRET-01-003 — untested
- 维度: completeness | 优先级: P0
- 标题: base64 编码后的 secret 是否仍被脱敏
- Trigger: BLOCKED
- 断言: 1 total / 0 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=nonfunctional target=run_logs eval=llm_assisted → LLM辅助

### ❓ COMP-STATUS-01-001 — untested
- 维度: completeness | 优先级: P1
- 标题: 运行状态机 queued 到 completed 转换正确
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=run_status_sequence eval=deterministic → needs run detail assertion kind
  ✅ [1] type=positive target=run_status eval=deterministic → equals='success'

### ❓ COMP-STATUS-01-002 — untested
- 维度: completeness | 优先级: P1
- 标题: 失败 step 的日志完整保留且可查看
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='BEFORE_FAILURE_MARKER'
  ✅ [1] type=positive target=run_logs eval=deterministic → contains='ERROR_MARKER'

### ❓ COMP-STEP-01-069 — untested
- 维度: completeness | 优先级: P1
- 标题: step 必填与核心字段 name run uses 验证
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_status eval=deterministic → equals='success'

### ❓ COMP-STEP-01-070 — untested
- 维度: completeness | 优先级: P1
- 标题: step 可选字段 id env if with 验证
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-STEP-01-071 — untested
- 维度: completeness | 优先级: P1
- 标题: step 执行控制 shell working-directory continue-on-error timeout-minutes 验证
- Trigger: BLOCKED
- 断言: 4 total / 4 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [3] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-SUMMARY-01-001 — untested
- 维度: completeness | 优先级: P1
- 标题: ATOMGIT_STEP_SUMMARY Markdown 表格与标题正确渲染
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=step_summary eval=deterministic → needs step summary assertion kind
  ⬜ [1] type=positive target=step_summary_html eval=deterministic → needs HTML parse kind

### ❓ COMP-SUMMARY-01-002 — untested
- 维度: completeness | 优先级: P1
- 标题: summary 中不应暴露系统内部路径
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=negative target=step_summary eval=deterministic → needs step summary assertion kind
  ⬜ [1] type=negative target=step_summary eval=deterministic → needs step summary assertion kind

### ❓ COMP-SYSENV-01-059 — untested
- 维度: completeness | 优先级: P1
- 标题: ATOMGIT 系统环境变量关键变量存在性
- Trigger: BLOCKED
- 断言: 6 total / 6 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [3] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [4] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [5] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-SYSENV-01-060 — untested
- 维度: completeness | 优先级: P1
- 标题: ATOMGIT 系统环境变量值正确性
- Trigger: BLOCKED
- 断言: 3 total / 3 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-TIMEOUT-01-001 — untested
- 维度: completeness | 优先级: P1
- 标题: 未声明 timeout-minutes 的 job 在 360 分钟内正常完成
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  ⬜ [1] type=nonfunctional target=run_duration eval=deterministic → needs duration assertion kind

### ❓ COMP-TIMEOUT-01-002 — untested
- 维度: completeness | 优先级: P1
- 标题: 超时的 job 被强制终止并标记为 failure
- Trigger: BLOCKED
- 断言: 3 total / 3 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_status eval=deterministic → equals='success'
  ✅ [1] type=positive target=run_status eval=deterministic → equals='failure'
  ✅ [2] type=positive target=run_logs eval=deterministic → contains='starting'

### ❓ COMP-TRIG-01-074 — untested
- 维度: completeness | 优先级: P1
- 标题: workflow_dispatch 事件关键字段与 inputs 验证
- Trigger: BLOCKED
- 断言: 3 total / 3 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-TRIG-01-079 — untested
- 维度: completeness | 优先级: P1
- 标题: 触发事件 types 取值与过滤边界验证
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-UNKNOWN-01-002 — untested
- 维度: completeness | 优先级: P1
- 标题: 不应静默忽略未知字段导致用户误以为配置生效
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_status eval=deterministic → equals='success_with_unknown_field_silently_ignored'

### ❓ COMP-VARREF-01-083 — untested
- 维度: completeness | 优先级: P1
- 标题: YAML 表达式与 Shell 环境变量引用方式验证
- Trigger: BLOCKED
- 断言: 3 total / 3 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-WFLOW-01-061 — untested
- 维度: completeness | 优先级: P1
- 标题: workflow name 与 on 字段必填与类型验证
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-WFLOW-01-062 — untested
- 维度: completeness | 优先级: P1
- 标题: workflow env 与 defaults 字段验证
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-WFLOW-01-063 — untested
- 维度: completeness | 优先级: P1
- 标题: workflow concurrency 并发控制字段验证
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMP-WFLOW-01-064 — untested
- 维度: completeness | 优先级: P1
- 标题: workflow stages 阶段结构字段验证
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMPAT-ACTION-01-001 — untested
- 维度: compatibility | 优先级: P1
- 标题: checkout 短名等价性——ref 参数支持
- Trigger: BLOCKED
- 断言: 4 total / 3 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='completed_success'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  ⬜ [3] type=negative target=workflow_parse eval=deterministic → needs workflow validation kind

### ❓ COMPAT-ACTION-01-002 — untested
- 维度: compatibility | 优先级: P1
- 标题: checkout 短名等价性——path 参数支持
- Trigger: BLOCKED
- 断言: 4 total / 3 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='completed_success'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  ⬜ [3] type=negative target=workflow_parse eval=deterministic → needs workflow validation kind

### ❓ COMPAT-ARTIFACT-01-001 — untested
- 维度: compatibility | 优先级: P1
- 标题: upload/download-artifact 跨 job 传递等价性
- Trigger: BLOCKED
- 断言: 4 total / 3 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='completed_success'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  ⬜ [3] type=negative target=workflow_parse eval=deterministic → needs workflow validation kind

### ❓ COMPAT-ARTIFACT-01-002 — untested
- 维度: compatibility | 优先级: P1
- 标题: upload-artifact 保留期行为等价性
- Trigger: BLOCKED
- 断言: 4 total / 3 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='completed_success'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ⬜ [2] type=nonfunctional target=artifact_state eval=deterministic → needs artifact assertion kind
  ✅ [3] type=negative target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMPAT-CACHE-01-001 — untested
- 维度: compatibility | 优先级: P1
- 标题: cache 行为等价性——缓存命中场景
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=negative target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMPAT-CONTAINER-01-001 — untested
- 维度: compatibility | 优先级: P1
- 标题: container 字段不被支持时应明确报错而非静默忽略
- Trigger: BLOCKED
- 断言: 3 total / 0 mappable / 3 LLM / 3 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=negative target=validation_error eval=llm_assisted → LLM辅助
  🤖 [1] type=negative target=run_status eval=llm_assisted → LLM辅助
  🤖 [2] type=positive target=error_message eval=llm_assisted → LLM辅助

### ❓ COMPAT-CONTAINER-01-002 — untested
- 维度: compatibility | 优先级: P1
- 标题: container 自定义镜像被拒绝时应给出替代指引
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 2 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=negative target=validation_error eval=llm_assisted → LLM辅助
  🤖 [1] type=positive target=error_message eval=llm_assisted → LLM辅助

### ❓ COMPAT-CTX-01-001 — untested
- 维度: compatibility | 优先级: P1
- 标题: 使用 github.ref 上下文应报错或求值为空
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 2 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=negative target=run_logs eval=llm_assisted → LLM辅助
  🤖 [1] type=nonfunctional target=error_message eval=llm_assisted → LLM辅助

### ❓ COMPAT-CTX-01-002 — untested
- 维度: compatibility | 优先级: P1
- 标题: 使用 atomgit.ref 上下文应正确返回触发引用
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  🤖 [1] type=positive target=run_logs eval=llm_assisted → LLM辅助

### ❓ COMPAT-CTX-01-003 — untested
- 维度: compatibility | 优先级: P1
- 标题: github 上下文嵌套属性访问应报错而非返回空
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  🤖 [1] type=positive target=run_logs eval=llm_assisted → LLM辅助

### ❓ COMPAT-DEPR-01-001 — untested
- 维度: compatibility | 优先级: P1
- 标题: ::set-env:: 废弃命令应被拒绝或给出迁移指引
- Trigger: BLOCKED
- 断言: 3 total / 0 mappable / 3 LLM / 3 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=negative target=run_status eval=llm_assisted → LLM辅助
  🤖 [1] type=positive target=error_message eval=llm_assisted → LLM辅助
  🤖 [2] type=positive target=error_message eval=llm_assisted → LLM辅助

### ❓ COMPAT-DEPR-01-002 — untested
- 维度: compatibility | 优先级: P1
- 标题: ::add-path:: 废弃命令应被拒绝或给出迁移指引
- Trigger: BLOCKED
- 断言: 3 total / 0 mappable / 3 LLM / 3 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=negative target=run_status eval=llm_assisted → LLM辅助
  🤖 [1] type=positive target=error_message eval=llm_assisted → LLM辅助
  🤖 [2] type=positive target=error_message eval=llm_assisted → LLM辅助

### ❓ COMPAT-ENV-01-001 — untested
- 维度: compatibility | 优先级: P1
- 标题: ATOMGIT_SHA 环境变量应正确返回触发提交 SHA
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  🤖 [1] type=positive target=run_logs eval=llm_assisted → LLM辅助

### ❓ COMPAT-ENV-01-002 — untested
- 维度: compatibility | 优先级: P1
- 标题: GITHUB_SHA 环境变量在 GitCode 中应为空或未定义
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 2 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=negative target=run_logs eval=llm_assisted → LLM辅助
  🤖 [1] type=nonfunctional target=error_message eval=llm_assisted → LLM辅助

### ❓ COMPAT-ENV-01-003 — untested
- 维度: compatibility | 优先级: P1
- 标题: GITHUB_ENV 环境变量不应被静默映射到 ATOMGIT_ENV
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 2 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=negative target=run_logs eval=llm_assisted → LLM辅助
  🤖 [1] type=positive target=run_logs eval=llm_assisted → LLM辅助

### ❓ COMPAT-EXPR-01-001 — untested
- 维度: compatibility | 优先级: P1
- 标题: success 关键字在条件表达式中的可用性
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='implicit success confirmed'

### ❓ COMPAT-EXPR-01-002 — untested
- 维度: compatibility | 优先级: P1
- 标题: success() 函数的处理行为差异
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='Job B ran after Job A success'
  ✅ [1] type=positive target=run_status eval=deterministic → equals='success'

### ❓ COMPAT-EXPR-01-003 — untested
- 维度: compatibility | 优先级: P1
- 标题: failure() 与 failed 关键字的处理行为差异
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='Cleanup ran after failure'
  ✅ [1] type=positive target=run_status eval=deterministic → equals='failure'

### ❓ COMPAT-EXPR-01-004 — untested
- 维度: compatibility | 优先级: P1
- 标题: contains 表达式大小写敏感边界
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='exact case match: true'

### ❓ COMPAT-EXPR-01-005 — untested
- 维度: compatibility | 优先级: P1
- 标题: contains 表达式空值与空字符串边界
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='empty needle:'

### ❓ COMPAT-EXPR-01-006 — untested
- 维度: compatibility | 优先级: P1
- 标题: hashFiles 表达式无匹配路径边界
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='hash no match:'

### ❓ COMPAT-EXPR-01-007 — untested
- 维度: compatibility | 优先级: P1
- 标题: hashFiles 表达式多路径组合边界
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='hash multi:'

### ❓ COMPAT-EXPR-01-008 — untested
- 维度: compatibility | 优先级: P1
- 标题: toJson 表达式输出格式差异（pretty-print vs compact）
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  🤖 [1] type=nonfunctional target=run_logs eval=llm_assisted → LLM辅助

### ❓ COMPAT-EXPR-01-009 — untested
- 维度: compatibility | 优先级: P1
- 标题: loose equality 跨类型强制求值差异
- Trigger: BLOCKED
- 断言: 3 total / 2 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  🤖 [2] type=nonfunctional target=run_logs eval=llm_assisted → LLM辅助

### ❓ COMPAT-EXPR-01-010 — untested
- 维度: compatibility | 优先级: P1
- 标题: loose equality null 与空字符串及零的等价性差异
- Trigger: BLOCKED
- 断言: 3 total / 2 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  🤖 [2] type=nonfunctional target=run_logs eval=llm_assisted → LLM辅助

### ❓ COMPAT-EXPR-01-011 — untested
- 维度: compatibility | 优先级: P1
- 标题: join() 函数缺失时的降级行为
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_logs eval=deterministic → must_not_contain='join-result=a-b-c'
  🤖 [1] type=nonfunctional target=error_message eval=llm_assisted → LLM辅助

### ❓ COMPAT-EXPR-01-012 — untested
- 维度: compatibility | 优先级: P1
- 标题: fromJSON() 函数缺失时的降级行为
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_logs eval=deterministic → must_not_contain='fromjson-result=1'
  🤖 [1] type=nonfunctional target=error_message eval=llm_assisted → LLM辅助

### ❓ COMPAT-IF-01-001 — untested
- 维度: compatibility | 优先级: P1
- 标题: step 失败后后续 step 默认跳过行为
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='failure'
  ✅ [1] type=negative target=run_logs eval=deterministic → contains='This should not appear'

### ❓ COMPAT-IF-01-002 — untested
- 维度: compatibility | 优先级: P1
- 标题: continue-on-error 标记后失败 step 不阻断后续执行
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='This should appear'
  ✅ [1] type=positive target=run_status eval=deterministic → equals='success'

### ❓ COMPAT-INPUTS-01-001 — untested
- 维度: compatibility | 优先级: P1
- 标题: workflow_dispatch inputs 类型限制 - boolean 应报错
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_status eval=deterministic → equals='success'
  🤖 [1] type=nonfunctional target=error_message eval=llm_assisted → LLM辅助

### ❓ COMPAT-INPUTS-01-002 — untested
- 维度: compatibility | 优先级: P1
- 标题: workflow_dispatch inputs 类型限制 - string 正常通过
- Trigger: BLOCKED
- 断言: 3 total / 3 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMPAT-ISOLATE-01-001 — untested
- 维度: compatibility | 优先级: P1
- 标题: Runner 环境隔离——跨 job 文件隔离
- Trigger: BLOCKED
- 断言: 4 total / 4 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [3] type=negative target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMPAT-ISOLATE-01-002 — untested
- 维度: compatibility | 优先级: P1
- 标题: Runner 环境隔离——跨 job 环境变量隔离
- Trigger: BLOCKED
- 断言: 3 total / 3 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMPAT-MASK-01-001 — untested
- 维度: compatibility | 优先级: P0
- 标题: 直接 echo secrets 值应在日志中被脱敏
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  🤖 [1] type=positive target=run_logs eval=llm_assisted → LLM辅助

### ❓ COMPAT-MASK-01-002 — untested
- 维度: compatibility | 优先级: P0
- 标题: 通过 env 注入 secret 后输出应在日志中被脱敏
- Trigger: BLOCKED
- 断言: 3 total / 2 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  🤖 [1] type=positive target=run_logs eval=llm_assisted → LLM辅助
  ✅ [2] type=positive target=run_status eval=deterministic → equals='success'

### ❓ COMPAT-MATRIX-01-003 — untested
- 维度: compatibility | 优先级: P2
- 标题: matrix 三维展开不被支持时的差异
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 2 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=positive target=run_status eval=llm_assisted → LLM辅助
  🤖 [1] type=negative target=run_status eval=llm_assisted → LLM辅助

### ❓ COMPAT-MATRIX-01-004 — untested
- 维度: compatibility | 优先级: P2
- 标题: matrix include 无基础变量不被支持时的差异
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 2 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=positive target=run_status eval=llm_assisted → LLM辅助
  🤖 [1] type=negative target=run_status eval=llm_assisted → LLM辅助

### ❓ COMPAT-MATRIX-01-005 — untested
- 维度: compatibility | 优先级: P2
- 标题: matrix exclude 全排除不被支持时的差异
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 2 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=positive target=validation_error eval=llm_assisted → LLM辅助
  🤖 [1] type=negative target=run_status eval=llm_assisted → LLM辅助

### ❓ COMPAT-NEST-01-001 — untested
- 维度: compatibility | 优先级: P1
- 标题: workflow_call 嵌套层数 - 2 层正常执行
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  - unknown repo_fixture 'reusable-workflow'
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'

### ❓ COMPAT-NEST-01-002 — untested
- 维度: compatibility | 优先级: P1
- 标题: workflow_call 嵌套层数 - 3 层越界应报错
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  - unknown repo_fixture 'reusable-workflow-3layer'
  ✅ [0] type=negative target=run_status eval=deterministic → equals='success'
  🤖 [1] type=nonfunctional target=error_message eval=llm_assisted → LLM辅助

### ❓ COMPAT-OUTCOME-01-001 — untested
- 维度: compatibility | 优先级: P1
- 标题: continue-on-error false 时 outcome 与 conclusion 应均为 failure
- Trigger: BLOCKED
- 断言: 3 total / 1 mappable / 2 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=positive target=step_status eval=llm_assisted → LLM辅助
  🤖 [1] type=positive target=step_conclusion eval=llm_assisted → LLM辅助
  ✅ [2] type=positive target=run_status eval=deterministic → equals='failure'

### ❓ COMPAT-OUTCOME-01-002 — untested
- 维度: compatibility | 优先级: P1
- 标题: continue-on-error true 时 outcome 应为 failure 而 conclusion 应为 success
- Trigger: BLOCKED
- 断言: 3 total / 1 mappable / 2 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=positive target=step_status eval=llm_assisted → LLM辅助
  🤖 [1] type=positive target=step_conclusion eval=llm_assisted → LLM辅助
  ✅ [2] type=positive target=run_status eval=deterministic → equals='success'

### ❓ COMPAT-OUTCOME-01-003 — untested
- 维度: compatibility | 优先级: P1
- 标题: outcome 与 conclusion 在 job 条件判断中不应互换语义
- Trigger: BLOCKED
- 断言: 3 total / 0 mappable / 3 LLM / 3 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=positive target=job_status eval=llm_assisted → LLM辅助
  🤖 [1] type=positive target=step_status eval=llm_assisted → LLM辅助
  🤖 [2] type=negative target=semantic_swap eval=llm_assisted → LLM辅助

### ❓ COMPAT-OUTPUT-01-001 — untested
- 维度: compatibility | 优先级: P1
- 标题: 跨 Job 引用未声明 output 时返回空值的差异
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  🤖 [1] type=positive target=run_logs eval=llm_assisted → LLM辅助

### ❓ COMPAT-PERM-01-001 — untested
- 维度: compatibility | 优先级: P0
- 标题: 未声明 permissions 时默认 TOKEN 读操作权限范围
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  ✅ [1] type=positive target=run_logs eval=deterministic → contains='README'

### ❓ COMPAT-PERM-01-004 — untested
- 维度: compatibility | 优先级: P0
- 标题: permissions 命名差异——GitCode repository 权限项正常生效
- Trigger: BLOCKED
- 断言: 4 total / 3 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='completed_success'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [2] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  ⬜ [3] type=negative target=workflow_parse eval=deterministic → needs workflow validation kind

### ❓ COMPAT-PERM-01-005 — untested
- 维度: compatibility | 优先级: P0
- 标题: permissions 空对象时 ATOMGIT_TOKEN 默认权限范围差异
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 2 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=positive target=run_logs eval=llm_assisted → LLM辅助
  🤖 [1] type=negative target=run_logs eval=llm_assisted → LLM辅助

### ❓ COMPAT-RUNNER-01-001 — untested
- 维度: compatibility | 优先级: P1
- 标题: runner.os 在 Linux Runner 上应返回 Linux
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  🤖 [1] type=positive target=run_logs eval=llm_assisted → LLM辅助

### ❓ COMPAT-RUNNER-01-002 — untested
- 维度: compatibility | 优先级: P1
- 标题: runner.arch 在 x86_64 Runner 上应返回 X64
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  🤖 [1] type=positive target=run_logs eval=llm_assisted → LLM辅助

### ❓ COMPAT-RUNNER-01-003 — untested
- 维度: compatibility | 优先级: P2
- 标题: self-hosted 标签不被支持时应明确报错
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 2 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=positive target=error_message eval=llm_assisted → LLM辅助
  🤖 [1] type=negative target=run_status eval=llm_assisted → LLM辅助

### ❓ COMPAT-RUNNER-01-006 — untested
- 维度: compatibility | 优先级: P2
- 标题: Runner 未预装 Java 工具链与 GitHub 差异
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 2 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=positive target=run_logs eval=llm_assisted → LLM辅助
  🤖 [1] type=positive target=error_message eval=llm_assisted → LLM辅助

### ❓ COMPAT-RUNSON-01-001 — untested
- 维度: compatibility | 优先级: P1
- 标题: runs-on 标签体系——三段式数组正常匹配
- Trigger: BLOCKED
- 断言: 3 total / 2 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='completed_success'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ⬜ [2] type=negative target=workflow_parse eval=deterministic → needs workflow validation kind

### ❓ COMPAT-RUNSON-01-002 — untested
- 维度: compatibility | 优先级: P1
- 标题: runs-on 标签体系——单标签字符串应报错
- Trigger: BLOCKED
- 断言: 3 total / 1 mappable / 1 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=negative target=workflow_parse eval=deterministic → needs workflow validation kind
  🤖 [1] type=positive target=run_logs eval=llm_assisted → LLM辅助
  ✅ [2] type=negative target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMPAT-SHELL-01-001 — untested
- 维度: compatibility | 优先级: P1
- 标题: 默认 shell 隐式行为差异 - 未显式声明时是否为 bash
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='bash'

### ❓ COMPAT-SHELL-01-002 — untested
- 维度: compatibility | 优先级: P1
- 标题: 默认工作目录隐式行为差异 - 未显式声明时是否为仓库根目录
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='README'

### ❓ COMPAT-TOKEN-01-001 — untested
- 维度: compatibility | 优先级: P0
- 标题: ATOMGIT_TOKEN 应正确返回有效令牌
- Trigger: BLOCKED
- 断言: 3 total / 2 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  🤖 [1] type=positive target=run_logs eval=llm_assisted → LLM辅助
  ✅ [2] type=negative target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ COMPAT-TOKEN-01-002 — untested
- 维度: compatibility | 优先级: P0
- 标题: GITHUB_TOKEN 在 GitCode 中应为空且不应被静默映射
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 2 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=negative target=run_logs eval=llm_assisted → LLM辅助
  🤖 [1] type=nonfunctional target=error_message eval=llm_assisted → LLM辅助

### ❓ COMPAT-TOKEN-01-003 — untested
- 维度: compatibility | 优先级: P0
- 标题: GITHUB_TOKEN 不应被静默映射为 ATOMGIT_TOKEN
- Trigger: BLOCKED
- 断言: 3 total / 0 mappable / 3 LLM / 3 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=negative target=run_logs eval=llm_assisted → LLM辅助
  🤖 [1] type=positive target=run_logs eval=llm_assisted → LLM辅助
  🤖 [2] type=negative target=run_logs eval=llm_assisted → LLM辅助

### ❓ COMPAT-VARS-01-001 — untested
- 维度: compatibility | 优先级: P1
- 标题: vars 上下文若支持应正确返回值
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  🤖 [1] type=positive target=run_logs eval=llm_assisted → LLM辅助

### ❓ COMPAT-VARS-01-002 — untested
- 维度: compatibility | 优先级: P1
- 标题: vars 上下文若不支持应报错而非静默为空
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 2 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=negative target=run_logs eval=llm_assisted → LLM辅助
  🤖 [1] type=nonfunctional target=error_message eval=llm_assisted → LLM辅助

### ❓ COMPAT-VARS-01-003 — untested
- 维度: compatibility | 优先级: P1
- 标题: vars 项目级覆盖组织级的优先级差异
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 2 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=positive target=run_logs eval=llm_assisted → LLM辅助
  🤖 [1] type=negative target=run_logs eval=llm_assisted → LLM辅助

### ❓ COMPAT-VARS-01-004 — untested
- 维度: compatibility | 优先级: P1
- 标题: vars 与 env 同名时的优先级差异
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 2 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=positive target=run_logs eval=llm_assisted → LLM辅助
  🤖 [1] type=positive target=run_logs eval=llm_assisted → LLM辅助

### ❓ COMPAT-VARS-01-006 — untested
- 维度: compatibility | 优先级: P1
- 标题: vars 在 Action 中的可用性差异
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 2 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=positive target=run_status eval=llm_assisted → LLM辅助
  🤖 [1] type=negative target=run_logs eval=llm_assisted → LLM辅助

### ❓ COMPAT-WCMD-01-001 — untested
- 维度: compatibility | 优先级: P2
- 标题: ::add-mask:: 不被支持时应静默降级而非报错
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  🤖 [1] type=negative target=run_logs eval=llm_assisted → LLM辅助

### ❓ COMPAT-WCMD-01-002 — untested
- 维度: compatibility | 优先级: P2
- 标题: ::group:: 不被支持时应静默降级而非报错
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  🤖 [1] type=negative target=run_logs eval=llm_assisted → LLM辅助

### ❓ COMPAT-WCMD-01-003 — untested
- 维度: compatibility | 优先级: P2
- 标题: ::stop-commands:: 不被支持时应静默降级而非报错
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  🤖 [1] type=negative target=run_logs eval=llm_assisted → LLM辅助

### ❓ REL-API-01-065 — untested
- 维度: reliability | 优先级: P2
- 标题: API 限流与一致性——10 QPS 高频查询 run/job 状态不丢数据
- Trigger: BLOCKED
- 断言: 3 total / 0 mappable / 0 LLM / 3 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=http_200_ratio eval=deterministic → needs HTTP metric assertion kind
  ⬜ [1] type=negative target=http_error_codes eval=deterministic → needs HTTP metric assertion kind
  ⬜ [2] type=nonfunctional target=response_time_p95_seconds eval=deterministic → needs HTTP metric assertion kind

### ❓ REL-ART-01-041 — untested
- 维度: reliability | 优先级: P1
- 标题: 超大 artifact——100 MB artifact 上传后下游 job 应成功下载
- Trigger: BLOCKED
- 断言: 3 total / 0 mappable / 0 LLM / 3 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=upload_status eval=deterministic → needs artifact operation assertion kind
  ⬜ [1] type=positive target=download_status eval=deterministic → needs artifact operation assertion kind
  ⬜ [2] type=positive target=md5_match eval=deterministic → needs artifact operation assertion kind

### ❓ REL-ARTCONC-01-063 — untested
- 维度: reliability | 优先级: P1
- 标题: 制品并发写一致性——多 job 同时 upload-artifact 同名 artifact
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=download_content eval=deterministic → needs artifact operation assertion kind
  ⬜ [1] type=negative target=download_content eval=deterministic → needs artifact operation assertion kind

### ❓ REL-ARTPERF-01-053 — untested
- 维度: reliability | 优先级: P1
- 标题: 制品传输性能——100MB artifact 上传下载耗时
- Trigger: BLOCKED
- 断言: 3 total / 0 mappable / 0 LLM / 3 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=nonfunctional target=upload_time_seconds eval=deterministic → needs artifact operation assertion kind
  ⬜ [1] type=nonfunctional target=download_time_seconds eval=deterministic → needs artifact operation assertion kind
  ⬜ [2] type=positive target=hash_match eval=deterministic → needs artifact operation assertion kind

### ❓ REL-ARTPERF-01-053-V2 — untested
- 维度: reliability | 优先级: P1
- 标题: 制品传输性能——1GB artifact 上传下载耗时
- Trigger: BLOCKED
- 断言: 3 total / 0 mappable / 0 LLM / 3 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=nonfunctional target=upload_time_seconds eval=deterministic → needs artifact operation assertion kind
  ⬜ [1] type=nonfunctional target=download_time_seconds eval=deterministic → needs artifact operation assertion kind
  ⬜ [2] type=positive target=hash_match eval=deterministic → needs artifact operation assertion kind

### ❓ REL-BIGRUNNER-01-066 — untested
- 维度: reliability | 优先级: P1
- 标题: 大规格资源调度稳定性——xlarge/2xlarge 反复编译成功率
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=success_rate eval=deterministic → needs metric assertion kind
  ⬜ [1] type=positive target=failure_attribution eval=deterministic → needs failure attribution kind

### ❓ REL-CACHE-01-046 — untested
- 维度: reliability | 优先级: P1
- 标题: 缓存 LRU 淘汰压力——连续写入 10 个大缓存后最旧缓存应被正确淘汰
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=latest_cache_status eval=deterministic → needs cache assertion kind
  ⬜ [1] type=positive target=oldest_cache_status eval=deterministic → needs cache assertion kind

### ❓ REL-CACHEPERF-01-054 — untested
- 维度: reliability | 优先级: P2
- 标题: 缓存加速比——cache 命中 vs 未命中构建耗时对比
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=nonfunctional target=speedup_ratio eval=deterministic → needs metric assertion kind
  ⬜ [1] type=nonfunctional target=restore_time_seconds eval=deterministic → needs metric assertion kind

### ❓ REL-CANCEL-01-028 — untested
- 维度: reliability | 优先级: P1
- 标题: 手动取消 workflow——运行中取消时 always() cleanup step 仍应执行
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=cleanup_step_status eval=deterministic → needs metric assertion kind
  ✅ [1] type=positive target=run_status eval=deterministic → equals='canceled'

### ❓ REL-CANCELREL-01-061 — untested
- 维度: reliability | 优先级: P1
- 标题: 取消操作可靠性——queued/running/post 各阶段取消状态正确过渡
- Trigger: BLOCKED
- 断言: 4 total / 0 mappable / 0 LLM / 4 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=cancel_queued_status eval=deterministic → needs cancel assertion kind
  ⬜ [1] type=positive target=cancel_running_status eval=deterministic → needs cancel assertion kind
  ⬜ [2] type=positive target=cancel_post_main_status eval=deterministic → needs cancel assertion kind
  ⬜ [3] type=nonfunctional target=cancel_stabilization_seconds eval=deterministic → needs cancel assertion kind

### ❓ REL-CHILDSTATE-01-064 — untested
- 维度: reliability | 优先级: P0
- 标题: 子任务状态传播——workflow_call 失败时父 workflow 不应假阳性完成
- Trigger: BLOCKED
- 断言: 3 total / 0 mappable / 0 LLM / 3 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=parent_status eval=deterministic → needs job-level status assertion kind
  ⬜ [1] type=positive target=downstream_status eval=deterministic → needs job-level status assertion kind
  ⬜ [2] type=negative target=parent_status eval=deterministic → needs job-level status assertion kind

### ❓ REL-CHILDSTATE-01-064-V2 — untested
- 维度: reliability | 优先级: P0
- 标题: 子任务状态传播——workflow_call 未拉起时父 workflow 不应假阳性完成
- Trigger: BLOCKED
- 断言: 3 total / 0 mappable / 0 LLM / 3 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=parent_status eval=deterministic → needs job-level status assertion kind
  ⬜ [1] type=positive target=downstream_status eval=deterministic → needs job-level status assertion kind
  ⬜ [2] type=negative target=parent_status eval=deterministic → needs job-level status assertion kind

### ❓ REL-CONC-01-001 — untested
- 维度: reliability | 优先级: P1
- 标题: concurrency.max=5 时同时触发 5 个运行应全部进入执行态
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='completed(success)'
  ⬜ [1] type=nonfunctional target=queued_to_running_latency eval=deterministic → needs metric assertion kind

### ❓ REL-CONC-01-002 — untested
- 维度: reliability | 优先级: P1
- 标题: concurrency.max=6 配置应被系统拒绝
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=yaml_validation eval=deterministic → needs workflow validation kind
  ✅ [1] type=negative target=run_status eval=deterministic → equals='should_not_start'

### ❓ REL-CONTINUE-01-030 — untested
- 维度: reliability | 优先级: P1
- 标题: continue-on-error=true——job 失败后 workflow 不应终止
- Trigger: BLOCKED
- 断言: 3 total / 0 mappable / 0 LLM / 3 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=job_a_status eval=deterministic → needs job-level status assertion kind
  ⬜ [1] type=positive target=job_b_status eval=deterministic → needs job-level status assertion kind
  ⬜ [2] type=positive target=workflow_status eval=deterministic → needs workflow validation kind

### ❓ REL-CPU-01-022 — untested
- 维度: reliability | 优先级: P1
- 标题: Runner CPU 饱和——small runner 运行 4 个 CPU 密集型进程应完成但耗时延长
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=job_status eval=deterministic → equals='success'
  ⬜ [1] type=nonfunctional target=job_duration_seconds eval=deterministic → needs metric assertion kind

### ❓ REL-DISK-01-018 — untested
- 维度: reliability | 优先级: P1
- 标题: Runner 磁盘边界——small runner 写入 49 GB 应成功
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=job_status eval=deterministic → equals='success'

### ❓ REL-DISK-01-019 — untested
- 维度: reliability | 优先级: P1
- 标题: Runner 磁盘越界——small runner 写入 51 GB 应失败并报磁盘满
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=job_status eval=deterministic → equals='failure'
  ✅ [1] type=positive target=run_logs eval=deterministic → contains='No space left on device'

### ❓ REL-FAIR-01-044 — untested
- 维度: reliability | 优先级: P1
- 标题: 并发资源公平性——2 个 workflow 各 3 个 jobs 应被公平调度
- Trigger: BLOCKED
- 断言: 1 total / 0 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=nonfunctional target=startup_time_diff_seconds eval=deterministic → needs metric assertion kind

### ❓ REL-FAULT-01-031 — untested
- 维度: reliability | 优先级: P1
- 标题: 故障注入——job 执行中 runner 进程被 SIGKILL 后应记录失败并保留已执行日志
- Trigger: BLOCKED
- 断言: 3 total / 3 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  - fault_injection.action=kill_runner
  ✅ [0] type=positive target=job_status eval=deterministic → equals='failure'
  ✅ [1] type=positive target=run_logs eval=deterministic → contains='step_one_marker'
  ✅ [2] type=negative target=run_logs eval=deterministic → contains='step_four_marker'

### ❓ REL-FAULT-01-032 — untested
- 维度: reliability | 优先级: P1
- 标题: 故障注入——artifact 上传时网络分区 30 秒后应失败并报网络错误
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  - fault_injection.action=network_partition
  ✅ [0] type=positive target=step_status eval=deterministic → equals='failure'
  ✅ [1] type=positive target=run_logs eval=deterministic → contains='network'

### ❓ REL-FAULT-01-033 — untested
- 维度: reliability | 优先级: P1
- 标题: 故障注入——runner 磁盘接近满时写入操作应失败并报磁盘满
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  - fault_injection.action=disk_full
  ✅ [0] type=positive target=job_status eval=deterministic → equals='failure'
  ✅ [1] type=positive target=run_logs eval=deterministic → contains='No space left on device'

### ❓ REL-FAULT-01-034 — untested
- 维度: reliability | 优先级: P1
- 标题: 故障注入——cache 服务 503 不可用时 job 应优雅降级为 cache miss
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  - fault_injection.action=concurrent_flood
  ✅ [0] type=positive target=job_status eval=deterministic → equals='success'
  ✅ [1] type=positive target=run_logs eval=deterministic → contains='cache miss'

### ❓ REL-FAULT-01-035 — untested
- 维度: reliability | 优先级: P1
- 标题: 故障注入——artifact 下载服务 503 不可用时 job 应失败并报依赖服务错误
- Trigger: BLOCKED
- 断言: 3 total / 3 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  - fault_injection.action=concurrent_flood
  ✅ [0] type=positive target=step_status eval=deterministic → equals='failure'
  ✅ [1] type=positive target=run_logs eval=deterministic → contains='503'
  ✅ [2] type=positive target=job_status eval=deterministic → equals='failure'

### ❓ REL-IGNORE-01-004 — untested
- 维度: reliability | 优先级: P1
- 标题: concurrency IGNORE 策略——超上限运行应直接执行
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='completed(success)'
  ✅ [1] type=negative target=run_status eval=deterministic → equals='queued'

### ❓ REL-IMAGE-01-052 — untested
- 维度: reliability | 优先级: P1
- 标题: 镜像拉取性能——500MB 自定义 container 环境准备耗时基准
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=nonfunctional target=image_pull_time_seconds eval=deterministic → needs metric assertion kind
  ✅ [1] type=positive target=job_status eval=deterministic → equals='success'

### ❓ REL-IMAGE-01-052-V2 — untested
- 维度: reliability | 优先级: P1
- 标题: 镜像拉取性能——5GB 自定义 container 环境准备耗时基准
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=nonfunctional target=image_pull_time_seconds eval=deterministic → needs metric assertion kind
  ✅ [1] type=positive target=job_status eval=deterministic → equals='success'

### ❓ REL-K8S-01-045 — untested
- 维度: reliability | 优先级: P1
- 标题: 自托管 K8s Runner 弹性伸缩——min=1/max=1 时并发 3 个 jobs 应排队执行
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=pod_count eval=deterministic → needs infra assertion kind
  ⬜ [1] type=positive target=max_concurrent_jobs eval=deterministic → needs job-level status assertion kind

### ❓ REL-LATENCY-01-050 — untested
- 维度: reliability | 优先级: P1
- 标题: 调度延迟基准——queued→running P50/P95 等待时间
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=nonfunctional target=p95_latency_seconds eval=deterministic → needs metric assertion kind
  ⬜ [1] type=nonfunctional target=p50_latency_seconds eval=deterministic → needs metric assertion kind

### ❓ REL-LATENCY-01-050-V2 — untested
- 维度: reliability | 优先级: P1
- 标题: 调度延迟压力——并发 20 个 job 的排队延迟与完成率
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=completed_jobs_count eval=deterministic → needs job-level status assertion kind
  ⬜ [1] type=nonfunctional target=max_queued_time_seconds eval=deterministic → needs metric assertion kind

### ❓ REL-LOG-01-040 — untested
- 维度: reliability | 优先级: P1
- 标题: 超长日志——单 job 输出 100 MB 日志应完整保留且可下载查看
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ❌ [0] type=positive target=log_size_mb eval=deterministic → unmapped target='log_size_mb'
  ❌ [1] type=positive target=log_download eval=deterministic → unmapped target='log_download'

### ❓ REL-LOGPERF-01-051 — untested
- 维度: reliability | 优先级: P1
- 标题: 日志加载性能——50MB 日志下载与查看耗时
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=nonfunctional target=download_time_seconds eval=deterministic → needs artifact operation assertion kind
  ⬜ [1] type=positive target=log_integrity eval=deterministic → needs log detail assertion kind

### ❓ REL-LOGPERF-01-051-V2 — untested
- 维度: reliability | 优先级: P1
- 标题: 日志加载性能——200MB 日志下载与查看耗时
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=nonfunctional target=download_time_seconds eval=deterministic → needs artifact operation assertion kind
  ⬜ [1] type=positive target=log_integrity eval=deterministic → needs log detail assertion kind

### ❓ REL-LOGSTABLE-01-059 — untested
- 维度: reliability | 优先级: P1
- 标题: 日志系统稳定性——6 万行日志无乱序/无丢失/无截断
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=log_line_count eval=deterministic → needs log detail assertion kind
  ⬜ [1] type=positive target=log_order eval=deterministic → needs log detail assertion kind

### ❓ REL-LONG-01-043 — untested
- 维度: reliability | 优先级: P1
- 标题: 长时运行接近 timeout 边界——350 分钟运行应成功且心跳保活正常
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=job_status eval=deterministic → equals='success'
  ⬜ [1] type=nonfunctional target=heartbeat_interval_seconds eval=deterministic → needs metric assertion kind

### ❓ REL-MATRIX-01-026 — untested
- 维度: reliability | 优先级: P1
- 标题: matrix fail-fast=true——任意 job 实例失败应立即取消其余实例
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=job_status eval=deterministic → equals='failure'
  ⬜ [1] type=positive target=cancelled_jobs_count eval=deterministic → needs job-level status assertion kind

### ❓ REL-MATRIX-01-027 — untested
- 维度: reliability | 优先级: P1
- 标题: matrix max-parallel=4——9 个组合应最多同时运行 4 个
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=max_concurrent_jobs eval=deterministic → needs job-level status assertion kind
  ✅ [1] type=positive target=run_status eval=deterministic → equals='completed(success)'

### ❓ REL-MATRIX-01-038 — untested
- 维度: reliability | 优先级: P1
- 标题: 大规模 matrix——20 个组合应全部生成并正确调度
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=generated_jobs_count eval=deterministic → needs job-level status assertion kind
  ✅ [1] type=positive target=run_status eval=deterministic → equals='completed(success)'

### ❓ REL-MATRIX-01-039 — untested
- 维度: reliability | 优先级: P1
- 标题: 大规模 matrix——50 个组合应全部生成并正确调度
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=generated_jobs_count eval=deterministic → needs job-level status assertion kind
  ⬜ [1] type=nonfunctional target=scheduling_latency_seconds eval=deterministic → needs metric assertion kind

### ❓ REL-MATRIXFAIR-01-056 — untested
- 维度: reliability | 优先级: P1
- 标题: 矩阵调度公平性——20 实例 matrix 配 max-parallel=4 的无饿死验证
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=completed_jobs_count eval=deterministic → needs job-level status assertion kind
  ⬜ [1] type=nonfunctional target=queued_delay_ratio eval=deterministic → needs metric assertion kind

### ❓ REL-MEM-01-020 — untested
- 维度: reliability | 优先级: P1
- 标题: Runner 内存边界——small runner 分配 7.5 GB 应成功
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=job_status eval=deterministic → equals='success'

### ❓ REL-MEM-01-021 — untested
- 维度: reliability | 优先级: P1
- 标题: Runner 内存越界——small runner 分配 9 GB 应被 OOM kill
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=job_status eval=deterministic → equals='failure'
  ✅ [1] type=positive target=run_logs eval=deterministic → contains='Killed'

### ❓ REL-NEEDS-01-025 — untested
- 维度: reliability | 优先级: P1
- 标题: needs 失败传播——上游 job 失败时下游 job 应被 skip
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=job_a_status eval=deterministic → needs job-level status assertion kind
  ⬜ [1] type=positive target=job_b_status eval=deterministic → needs job-level status assertion kind

### ❓ REL-NEST-01-023 — untested
- 维度: reliability | 优先级: P1
- 标题: workflow_call 嵌套边界——2 层嵌套调用应成功执行
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='completed(success)'

### ❓ REL-NEST-01-024 — untested
- 维度: reliability | 优先级: P1
- 标题: workflow_call 嵌套越界——3 层嵌套调用应被拒绝
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='completed(failure)'
  ✅ [1] type=positive target=run_logs eval=deterministic → contains='嵌套'

### ❓ REL-NETFAULT-01-062 — untested
- 维度: reliability | 优先级: P2
- 标题: 网络依赖容错——workflow 中访问不可达地址的明确失败与有界超时
- Trigger: BLOCKED
- 断言: 3 total / 0 mappable / 0 LLM / 3 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=reachable_status eval=deterministic → needs infra assertion kind
  ⬜ [1] type=positive target=unreachable_timeout_seconds eval=deterministic → needs infra assertion kind
  ⬜ [2] type=positive target=failure_attribution eval=deterministic → needs failure attribution kind

### ❓ REL-OUTPUT-01-016 — untested
- 维度: reliability | 优先级: P1
- 标题: step output 边界值——ATOMGIT_OUTPUT 写入 1 MB 参数应成功传递
- Trigger: BLOCKED
- 断言: 1 total / 0 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=step_output_length eval=deterministic → needs metric assertion kind

### ❓ REL-OUTPUT-01-017 — untested
- 维度: reliability | 优先级: P1
- 标题: step output 越界值——ATOMGIT_OUTPUT 写入 1 MB+1 byte 应被拒绝或报错
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='1MB'
  ✅ [1] type=positive target=job_status eval=deterministic → equals='failure'

### ❓ REL-PRESSURE-01-055 — untested
- 维度: reliability | 优先级: P1
- 标题: 并发压测——concurrency.max=5 时触发 20 个 workflow 的排队与完成率
- Trigger: BLOCKED
- 断言: 3 total / 0 mappable / 0 LLM / 3 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=completed_count eval=deterministic → needs job-level status assertion kind
  ⬜ [1] type=nonfunctional target=max_running_count eval=deterministic → needs resource metric assertion kind
  ⬜ [2] type=nonfunctional target=total_duration_seconds eval=deterministic → needs resource metric assertion kind

### ❓ REL-PROJLIMIT-01-067 — untested
- 维度: reliability | 优先级: P1
- 标题: 项目级 workflow 并发上限——200 条同时触发时全部完成无丢失
- Trigger: BLOCKED
- 断言: 5 total / 0 mappable / 0 LLM / 5 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=completed_count eval=deterministic → needs job-level status assertion kind
  ❌ [1] type=positive target=failed_count eval=deterministic → unmapped target='failed_count'
  ⬜ [2] type=positive target=queued_count eval=deterministic → needs resource metric assertion kind
  ⬜ [3] type=nonfunctional target=total_duration_seconds eval=deterministic → needs resource metric assertion kind
  ❌ [4] type=nonfunctional target=lost_count eval=deterministic → unmapped target='lost_count'

### ❓ REL-PROJLIMIT-01-068 — untested
- 维度: reliability | 优先级: P1
- 标题: 项目级 workflow 并发上限越界——201 条同时触发时至少一条进入排队
- Trigger: BLOCKED
- 断言: 5 total / 0 mappable / 0 LLM / 5 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=completed_count eval=deterministic → needs job-level status assertion kind
  ❌ [1] type=positive target=failed_count eval=deterministic → unmapped target='failed_count'
  ⬜ [2] type=positive target=queued_count eval=deterministic → needs resource metric assertion kind
  ⬜ [3] type=nonfunctional target=total_duration_seconds eval=deterministic → needs resource metric assertion kind
  ❌ [4] type=nonfunctional target=lost_count eval=deterministic → unmapped target='lost_count'

### ❓ REL-QUEUE-01-003 — untested
- 维度: reliability | 优先级: P1
- 标题: concurrency QUEUE 策略——超上限运行应排队等待
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='completed(success)'
  ⬜ [1] type=nonfunctional target=queued_count eval=deterministic → needs resource metric assertion kind

### ❓ REL-RERUN-01-011 — untested
- 维度: reliability | 优先级: P1
- 标题: rerun 边界值——单条运行连续重新运行 3 次应全部成功
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=rerun_count eval=deterministic → needs rerun assertion kind
  ✅ [1] type=positive target=run_status eval=deterministic → equals='completed(success)'

### ❓ REL-RERUN-01-012 — untested
- 维度: reliability | 优先级: P1
- 标题: rerun 越界值——尝试第 4 次重新运行应被系统拒绝
- Trigger: BLOCKED
- 断言: 1 total / 0 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=rerun_request eval=deterministic → needs rerun assertion kind

### ❓ REL-RERUN-01-013 — untested
- 维度: reliability | 优先级: P1
- 标题: rerun 6 小时年龄限制——超期运行不可重新运行
- Trigger: BLOCKED
- 断言: 1 total / 0 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=rerun_request eval=deterministic → needs rerun assertion kind

### ❓ REL-RETAIN-01-047 — untested
- 维度: reliability | 优先级: P1
- 标题: artifact 保留期 90 天边界——第 91 天应不可下载
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=download_day90_status eval=deterministic → needs artifact expiry check kind
  ⬜ [1] type=positive target=download_day91_status eval=deterministic → needs artifact expiry check kind

### ❓ REL-RUNNER-01-049 — untested
- 维度: reliability | 优先级: P1
- 标题: Runner 规格真实性——small/medium/large 实际 CPU/内存/磁盘 vs 声明值
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=resource_ratio eval=deterministic → needs resource metric assertion kind
  ⬜ [1] type=nonfunctional target=queued_to_running_minutes eval=deterministic → needs metric assertion kind

### ❓ REL-RUNNER-01-049-V2 — untested
- 维度: reliability | 优先级: P1
- 标题: Runner 规格真实性——xlarge/2xlarge 实际 CPU/内存/磁盘 vs 声明值
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=resource_ratio eval=deterministic → needs resource metric assertion kind
  ⬜ [1] type=positive target=failure_attribution eval=deterministic → needs failure attribution kind

### ❓ REL-SCHED-01-057 — untested
- 维度: reliability | 优先级: P1
- 标题: 资源调度状态一致性——空闲 runner 存在时 job 不应死等
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=nonfunctional target=max_queued_to_running_seconds eval=deterministic → needs metric assertion kind
  ⬜ [1] type=nonfunctional target=avg_queued_to_running_seconds eval=deterministic → needs metric assertion kind

### ❓ REL-STATE-01-058 — untested
- 维度: reliability | 优先级: P1
- 标题: Runner 状态机正确性——空闲/运行/离线转换与时序一致性
- Trigger: BLOCKED
- 断言: 3 total / 0 mappable / 0 LLM / 3 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=state_sequence eval=deterministic → needs metric assertion kind
  ⬜ [1] type=nonfunctional target=idle_to_running_seconds eval=deterministic → needs metric assertion kind
  ⬜ [2] type=nonfunctional target=running_to_idle_seconds eval=deterministic → needs metric assertion kind

### ❓ REL-TIMEOUT-01-007 — untested
- 维度: reliability | 优先级: P1
- 标题: job timeout 边界值——359 分钟运行应在 360 分钟边界前完成
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=job_status eval=deterministic → equals='success'
  ⬜ [1] type=nonfunctional target=job_duration_minutes eval=deterministic → needs metric assertion kind

### ❓ REL-TIMEOUT-01-008 — untested
- 维度: reliability | 优先级: P1
- 标题: job timeout 越界触发——361 分钟应在 360 分钟被强制终止
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=job_status eval=deterministic → equals='failure'
  ✅ [1] type=positive target=run_logs eval=deterministic → contains='timeout'

### ❓ REL-TIMEOUT-01-009 — untested
- 维度: reliability | 优先级: P1
- 标题: 自定义短超时——timeout-minutes=1 时 step 运行 2 分钟应被强制终止
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=job_status eval=deterministic → equals='failure'
  ⬜ [1] type=nonfunctional target=job_duration_seconds eval=deterministic → needs metric assertion kind

### ❓ REL-TIMEOUT-01-010 — untested
- 维度: reliability | 优先级: P1
- 标题: 默认超时——未声明 timeout-minutes 运行 361 分钟应被强制终止
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=job_status eval=deterministic → equals='failure'
  ✅ [1] type=positive target=run_logs eval=deterministic → contains='timeout'

### ❓ REL-YAMLCACHE-01-060 — untested
- 维度: reliability | 优先级: P1
- 标题: Workflow YAML 缓存失效——修改后无旧代码残留
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='marker_v2'
  ✅ [1] type=negative target=run_logs eval=deterministic → contains='marker_v1'

### ❓ SEC-ARTF-01-002 — untested
- 维度: security | 优先级: P0
- 标题: 跨仓库 artifact 下载返回 403 或 404
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  - unknown repo_fixture 'with-artifacts'
  ✅ [0] type=negative target=run_logs eval=deterministic → must_not_contain='200'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ SEC-CACHE-01-002 — untested
- 维度: security | 优先级: P0
- 标题: 主仓 cache restore 对 fork cache miss
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  - unknown repo_fixture 'with-cache'
  ⬜ [0] type=negative target=cache_restore eval=deterministic → needs cache assertion kind
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ SEC-DEFPERM-01-001 — untested
- 维度: security | 优先级: P0
- 标题: ATOMGIT_TOKEN 默认权限范围与 job 级覆盖必须正确生效
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_logs eval=deterministic → must_not_contain='write_successful'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ SEC-DOS-01-001 — untested
- 维度: security | 优先级: P0
- 标题: 大 artifact / 大 cache 必须受配额与边界限制
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_status eval=deterministic → status check
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ SEC-INJ-01-005 — untested
- 维度: security | 优先级: P0
- 标题: 表达式求值必须防止双重模板渲染（二次求值）
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_logs eval=deterministic → must_not_contain='2'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ SEC-MASK-01-001 — untested
- 维度: security | 优先级: P0
- 标题: Secret 值在运行日志中必须被自动脱敏为 ***
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ SEC-MASK-01-002 — untested
- 维度: security | 优先级: P0
- 标题: Secret 值在 step summary 和错误堆栈中必须被脱敏
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=negative target=step_summary eval=deterministic → needs step summary assertion kind
  ⬜ [1] type=negative target=error_stack eval=deterministic → needs doc check kind

### ❓ SEC-MASK-01-003 — untested
- 维度: security | 优先级: P0
- 标题: Secret 日志脱敏不可通过 base64 编码绕过
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  🤖 [1] type=negative target=run_logs eval=llm_assisted → LLM辅助

### ❓ SEC-MASK-01-004 — untested
- 维度: security | 优先级: P0
- 标题: Secret 日志脱敏不可通过字符串拼接或插值绕过
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  🤖 [1] type=negative target=run_logs eval=llm_assisted → LLM辅助

### ❓ SEC-MASK-01-005 — untested
- 维度: security | 优先级: P0
- 标题: Secret 日志脱敏不可通过多行值输出绕过
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ SEC-MASK-01-006 — untested
- 维度: security | 优先级: P0
- 标题: Secret 日志脱敏不可通过分片输出绕过
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  🤖 [1] type=negative target=run_logs eval=llm_assisted → LLM辅助

### ❓ SEC-NAME-01-001 — untested
- 维度: security | 优先级: P0
- 标题: Secret/变量名含特殊字符时不可导致意外求值或权限绕过
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_status eval=deterministic → equals='success_or_yaml_error'

### ❓ SEC-NAME-01-002 — untested
- 维度: security | 优先级: P0
- 标题: 通过 printenv 或进程枚举获取 ATOMGIT_TOKEN/secrets 时日志中必须保持脱敏
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ SEC-NET-01-001 — untested
- 维度: security | 优先级: P0
- 标题: Runner 网络出站必须受控，防止 SSRF 与内网跳板
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_logs eval=deterministic → must_not_contain='metadata_service_response'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ SEC-OIDC-01-001 — untested
- 维度: security | 优先级: P1
- 标题: OIDC / 短时凭据支持若缺失，必须明确标注为平台限制并提供替代安全方案
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=negative target=platform_docs eval=deterministic → needs doc check kind
  ⬜ [1] type=positive target=platform_docs eval=deterministic → needs doc check kind

### ❓ SEC-PERM-01-003 — untested
- 维度: security | 优先级: P0
- 标题: 未声明 permissions 时 ATOMGIT_TOKEN 默认权限必须最小化（read-only）
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_logs eval=deterministic → must_not_contain='write_permission_granted'
  ✅ [1] type=positive target=run_status eval=deterministic → equals='completed'

### ❓ SEC-PERM-01-004 — untested
- 维度: security | 优先级: P0
- 标题: 默认状态下写操作被 403 拒绝
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_logs eval=deterministic → must_not_contain='push_successful'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ SEC-RUN-01-001 — untested
- 维度: security | 优先级: P0
- 标题: Job 结束后 workspace 与临时文件必须被彻底清理
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_logs eval=deterministic → must_not_contain='residual found'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ SEC-RUN-01-002 — untested
- 维度: security | 优先级: P0
- 标题: Runner 环境变量与共享目录必须跨 job 隔离
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_logs eval=deterministic → must_not_contain='isolation broken'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ SEC-RUN-01-003 — untested
- 维度: security | 优先级: P0
- 标题: 自托管 Runner 跨项目残留必须被隔离
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  - unknown repo_fixture 'self-hosted-shared'
  ✅ [0] type=negative target=run_logs eval=deterministic → must_not_contain='cross project leak'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ SEC-SIDE-01-001 — untested
- 维度: security | 优先级: P0
- 标题: Secret 不经 output 侧信道绕过脱敏外泄
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  ❌ [1] type=negative target=step_output eval=deterministic → unmapped target='step_output'

### ❓ SEC-SIDE-01-002 — untested
- 维度: security | 优先级: P0
- 标题: Secret 不经 artifact 侧信道绕过脱敏外泄
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=negative target=artifact_content eval=deterministic → needs artifact assertion kind
  ✅ [1] type=positive target=run_status eval=deterministic → equals='blocked_or_masked'

### ❓ SEC-SUPPLY-01-001 — untested
- 维度: security | 优先级: P0
- 标题: 第三方 Action 引用应支持完整 commit hash 固定
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success_or_action_executed'
  ✅ [1] type=negative target=run_logs eval=deterministic → must_not_contain='unauthorized_action_execution'

### ❓ SEC-SUPPLY-01-002 — untested
- 维度: security | 优先级: P0
- 标题: commit hash 不匹配时第三方 Action 应被拒绝执行
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_status eval=deterministic → status check
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ SEC-TOCTOU-01-001 — untested
- 维度: security | 优先级: P0
- 标题: 审批后推送新 commit 不应被已授权特权运行执行
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_logs eval=deterministic → must_not_contain='unapproved_commit_executed'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ SEC-WCMD-01-001 — untested
- 维度: security | 优先级: P0
- 标题: Workflow 命令（如 add-mask）的响应本身不可泄露被遮蔽前的 secret 值
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ SEC-WCMD-01-002 — untested
- 维度: security | 优先级: P0
- 标题: 跨运行 artifact 必须被视为不可信数据
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  - unknown repo_fixture 'with-artifacts'
  ✅ [0] type=negative target=run_logs eval=deterministic → must_not_contain='auto_executed'
  ✅ [1] type=positive target=run_status eval=deterministic → equals='completed'

### ❓ USE-ACT-01-001 — untested
- 维度: usability | 优先级: P1
- 标题: 使用裸插件名 checkout 时正常拉取官方 Action
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='COMPLETED'

### ❓ USE-ACT-01-002 — untested
- 维度: usability | 优先级: P1
- 标题: 使用 actions/checkout@v4 时报错应给出迁移指引
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_status eval=deterministic → equals='COMPLETED'
  ❌ [1] type=nonfunctional target=error_message eval=deterministic → error_message (unmappable)

### ❓ USE-ANNOT-01-001 — untested
- 维度: usability | 优先级: P1
- 标题: workflow 命令 ::error:: 与 ::warning:: 在日志中保留原文
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='::error file=src/main.js,line=10::Missing semicolon'
  ✅ [1] type=positive target=run_logs eval=deterministic → contains='::warning file=src/util.js,line=5::Deprecated function'

### ❓ USE-CONC-01-001 — untested
- 维度: usability | 优先级: P1
- 标题: concurrency.max 配置 0 或 10 时报错应提示有效范围 1-5
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_status eval=deterministic → equals='COMPLETED'
  ❌ [1] type=nonfunctional target=error_message eval=deterministic → error_message (unmappable)

### ❓ USE-CTX-01-001 — untested
- 维度: usability | 优先级: P1
- 标题: 使用 atomgit 上下文时表达式正常求值
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='ref=refs/heads/'

### ❓ USE-CTX-01-002 — untested
- 维度: usability | 优先级: P1
- 标题: 使用 github 上下文时报错应提示 atomgit 替代
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_status eval=deterministic → equals='COMPLETED'
  ❌ [1] type=nonfunctional target=error_message eval=deterministic → error_message (unmappable)

### ❓ USE-DEPR-01-001 — untested
- 维度: usability | 优先级: P1
- 标题: 使用 ATOMGIT_OUTPUT 文件协议时正常生效
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='val=myvalue'

### ❓ USE-DEPR-01-002 — untested
- 维度: usability | 优先级: P1
- 标题: 使用 ::set-output 时应给出弃用警告与替代示例
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=nonfunctional target=run_logs eval=deterministic → run_logs (implicit value)

### ❓ USE-DISP-01-001 — untested
- 维度: usability | 优先级: P1
- 标题: workflow_dispatch 必填参数未提供时应给出明确校验错误
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_status eval=deterministic → equals='COMPLETED'
  ❌ [1] type=nonfunctional target=error_message eval=deterministic → error_message (unmappable)

### ❓ USE-DISP-01-002 — untested
- 维度: usability | 优先级: P1
- 标题: workflow_dispatch 未提供参数但存在 default 时应使用默认值运行
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='env=staging'

### ❓ USE-ENV-01-001 — untested
- 维度: usability | 优先级: P1
- 标题: 使用 ATOMGIT_SHA 环境变量时正常取值
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='sha='

### ❓ USE-ENV-01-002 — untested
- 维度: usability | 优先级: P1
- 标题: 引用 GITHUB_SHA 时日志应给出环境变量映射提示
- Trigger: BLOCKED
- 断言: 1 total / 0 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=nonfunctional target=error_message eval=llm_assisted → LLM辅助

### ❓ USE-EXPR-01-001 — untested
- 维度: usability | 优先级: P1
- 标题: 引用不存在的上下文属性时报错应包含原始表达式与错误类型
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_status eval=deterministic → equals='COMPLETED'
  ❌ [1] type=nonfunctional target=error_message eval=deterministic → error_message (unmappable)

### ❓ USE-INPT-01-001 — untested
- 维度: usability | 优先级: P1
- 标题: 使用 string 类型 input 时正常通过校验
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='COMPLETED'

### ❓ USE-INPT-01-002 — untested
- 维度: usability | 优先级: P1
- 标题: 使用 boolean 类型 input 时报错应提示仅支持 string
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_status eval=deterministic → equals='COMPLETED'
  ❌ [1] type=nonfunctional target=error_message eval=deterministic → error_message (unmappable)

### ❓ USE-LBL-01-002 — untested
- 维度: usability | 优先级: P1
- 标题: runs-on 标签因容量不足排队时应提示排队状态而非无可用 runner
- Trigger: BLOCKED
- 断言: 1 total / 0 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=nonfunctional target=run_logs eval=llm_assisted → LLM辅助

### ❓ USE-LOG-01-001 — untested
- 维度: usability | 优先级: P1
- 标题: 多 step 日志按时间线组织且边界清晰
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='step one prepare'
  🤖 [1] type=nonfunctional target=ui_layout eval=llm_assisted → LLM辅助

### ❓ USE-MASK-01-001 — untested
- 维度: usability | 优先级: P0
- 标题: secret 脱敏文档描述与实际行为一致并给出缓解建议
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  🤖 [1] type=nonfunctional target=documentation eval=llm_assisted → LLM辅助

### ❓ USE-MASK-01-002 — untested
- 维度: usability | 优先级: P0
- 标题: 直接 echo secrets 值时文档描述的绕过风险与实际一致
- Trigger: BLOCKED
- 断言: 1 total / 0 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  🤖 [0] type=nonfunctional target=run_logs eval=llm_assisted → LLM辅助

### ❓ USE-MD-01-001 — untested
- 维度: usability | 优先级: P1
- 标题: ATOMGIT_STEP_SUMMARY 写入的 Markdown 正确渲染为 HTML
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 1 LLM / 2 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ⬜ [0] type=positive target=step_summary eval=deterministic → needs step summary assertion kind
  🤖 [1] type=nonfunctional target=ui_visual eval=llm_assisted → LLM辅助

### ❓ USE-OS-01-001 — untested
- 维度: usability | 优先级: P1
- 标题: runner.os 返回值与文档声明的平台支持一致
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='os=Linux'
  🤖 [1] type=nonfunctional target=documentation eval=llm_assisted → LLM辅助

### ❓ USE-PERM-01-001 — untested
- 维度: usability | 优先级: P1
- 标题: 使用 GitCode 权限域命名时正常生效
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='COMPLETED'

### ❓ USE-RUN-01-001 — untested
- 维度: usability | 优先级: P1
- 标题: 使用三段式标签时 job 正常调度
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_status eval=deterministic → equals='COMPLETED'

### ❓ USE-SEARCH-01-001 — untested
- 维度: usability | 优先级: P1
- 标题: 日志搜索与下载功能可用且交互流畅
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='ERROR: mock failure line 1'
  🤖 [1] type=nonfunctional target=ui_interaction eval=llm_assisted → LLM辅助

### ❓ USE-SECNAME-01-001 — untested
- 维度: usability | 优先级: P1
- 标题: Secret 名称以 ATOMGIT_ 开头时应给出命名规则错误
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_status eval=deterministic → equals='COMPLETED'
  ❌ [1] type=nonfunctional target=error_message eval=deterministic → error_message (unmappable)

### ❓ USE-SECNAME-01-002 — untested
- 维度: usability | 优先级: P1
- 标题: Secret 名称以数字开头时应给出命名规则错误
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=negative target=run_status eval=deterministic → equals='COMPLETED'
  ❌ [1] type=nonfunctional target=error_message eval=deterministic → error_message (unmappable)

### ❓ USE-STAT-01-001 — untested
- 维度: usability | 优先级: P1
- 标题: 使用 always() 带括号时若被接受则正常执行
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='cleanup executed'

### ❓ USE-UNKN-01-002 — untested
- 维度: usability | 优先级: P1
- 标题: 未知字段报错若识别为 GitHub 特有应追加迁移提示
- Trigger: BLOCKED
- 断言: 1 total / 0 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger workflow_dispatch: API not yet tested
  ❌ [0] type=nonfunctional target=error_message eval=deterministic → error_message (unmappable)

### ✗ COMP-CACHE-01-003 — api_blocked
- 维度: completeness | 优先级: P0
- 标题: fork PR 不应覆盖或污染主分支 cache
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger pull_request: API works, platform does NOT fire trigger
  - unknown repo_fixture 'with-cache'
  ⬜ [0] type=negative target=cache_pollution eval=deterministic → needs cache assertion kind
  ⬜ [1] type=positive target=main_cache_content eval=deterministic → needs cache assertion kind

### ✗ COMP-PERMS-01-003 — api_blocked
- 维度: completeness | 优先级: P0
- 标题: fork PR 的 pull_request 下声明 write 仍仅 read
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger pull_request: API works, platform does NOT fire trigger
  ✅ [0] type=negative target=run_status eval=deterministic → equals='success_with_write'
  ✅ [1] type=positive target=run_logs eval=deterministic → contains='write failed as expected'

### ✗ COMP-PR-01-001 — api_blocked
- 维度: completeness | 优先级: P0
- 标题: fork PR 触发 pull_request 时不可读取项目 secrets
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger pull_request: API works, platform does NOT fire trigger
  ✅ [0] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_status eval=deterministic → equals='success_or_blocked'

### ✗ COMP-PR-01-002 — api_blocked
- 维度: completeness | 优先级: P0
- 标题: pull_request_target 可访问 secrets 且 TOKEN 拥有写权限
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger pull_request_target: API works, platform does NOT fire trigger
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_status eval=deterministic → equals='success'

### ✗ COMP-PR-01-003 — api_blocked
- 维度: completeness | 优先级: P0
- 标题: fork PR 的 pull_request workflow ATOMGIT_TOKEN 仅 read 权限
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger pull_request: API works, platform does NOT fire trigger
  ⬜ [0] type=negative target=run_step_result eval=deterministic → needs run detail assertion kind
  ✅ [1] type=positive target=run_status eval=deterministic → equals='success_or_failure'

### ✗ COMP-PRTARGET-01-001 — api_blocked
- 维度: completeness | 优先级: P0
- 标题: pull_request_target 默认使用 base 分支 workflow 版本
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger pull_request_target: API works, platform does NOT fire trigger
  ✅ [0] type=positive target=run_logs eval=deterministic → contains='BASE_VERSION_MARKER'
  ✅ [1] type=negative target=run_logs eval=deterministic → must_not_contain='FORK_VERSION_MARKER'

### ✗ COMP-PRTARGET-01-002 — api_blocked
- 维度: completeness | 优先级: P0
- 标题: 显式 checkout head.sha 后执行不可信代码的风险可控
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger pull_request_target: API works, platform does NOT fire trigger
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  ✅ [1] type=positive target=run_logs eval=deterministic → contains='BASE_VERSION_MARKER'

### ✗ COMP-TRIG-01-073 — api_blocked
- 维度: completeness | 优先级: P1
- 标题: pull_request 事件关键字段与 types 验证
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger pull_request: API works, platform does NOT fire trigger
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ✗ COMP-TRIG-01-076 — api_blocked
- 维度: completeness | 优先级: P1
- 标题: issue_comment 事件关键字段与 types 验证
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger issue_comment: API works, platform does NOT fire trigger
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ✗ COMP-TRIG-01-077 — api_blocked
- 维度: completeness | 优先级: P1
- 标题: pull_request_comment 事件关键字段与过滤验证
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger pull_request_comment: API works, platform does NOT fire trigger
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ✗ COMPAT-COMM-01-001 — api_blocked
- 维度: compatibility | 优先级: P1
- 标题: issue_comment types 命名差异 - GitCode 合法 types 应被接受
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger issue_comment: API works, platform does NOT fire trigger
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  🤖 [1] type=negative target=validation_error eval=llm_assisted → LLM辅助

### ✗ COMPAT-COMM-01-002 — api_blocked
- 维度: compatibility | 优先级: P1
- 标题: issue_comment types:created 不支持时应给出降级指引
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 2 LLM / 2 unmappable
- 阻断项:
  - trigger issue_comment: API works, platform does NOT fire trigger
  🤖 [0] type=negative target=run_status eval=llm_assisted → LLM辅助
  🤖 [1] type=positive target=error_message eval=llm_assisted → LLM辅助

### ✗ COMPAT-PERM-01-002 — api_blocked
- 维度: compatibility | 优先级: P0
- 标题: 未声明 permissions 时 fork PR 写操作隔离
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger fork_pr: API works, platform does NOT fire trigger
  ✅ [0] type=negative target=run_status eval=deterministic → equals='success'
  ✅ [1] type=negative target=run_logs eval=deterministic → run_logs (implicit value)

### ✗ COMPAT-PR-01-001 — api_blocked
- 维度: compatibility | 优先级: P0
- 标题: pull_request types 命名差异 - GitCode 合法 types 应被接受
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger pull_request: API works, platform does NOT fire trigger
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ✗ COMPAT-PR-01-006 — api_blocked
- 维度: compatibility | 优先级: P1
- 标题: PR 目标分支过滤行为差异
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger pull_request: API works, platform does NOT fire trigger
  ✅ [0] type=positive target=run_status eval=deterministic → equals='success'
  🤖 [1] type=negative target=run_status eval=llm_assisted → LLM辅助

### ✗ COMPAT-TARGET-01-001 — api_blocked
- 维度: compatibility | 优先级: P0
- 标题: pull_request_target 默认 checkout 应为 base 分支而非 head 分支
- Trigger: BLOCKED
- 断言: 3 total / 1 mappable / 2 LLM / 2 unmappable
- 阻断项:
  - trigger pull_request_target: API works, platform does NOT fire trigger
  - unknown repo_fixture 'with-fork-pr'
  🤖 [0] type=negative target=run_logs eval=llm_assisted → LLM辅助
  🤖 [1] type=positive target=run_logs eval=llm_assisted → LLM辅助
  ✅ [2] type=positive target=run_status eval=deterministic → equals='success'

### ✗ COMPAT-TARGET-01-002 — api_blocked
- 维度: compatibility | 优先级: P0
- 标题: pull_request_target 在 fork 场景下应保持 secret 隔离
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger pull_request_target: API works, platform does NOT fire trigger
  - unknown repo_fixture 'with-fork-pr'
  ✅ [0] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_status eval=deterministic → equals='success'

### ✗ COMPAT-TARGET-01-003 — api_blocked
- 维度: compatibility | 优先级: P0
- 标题: pull_request_target 默认 types 与 GitHub 差异
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 2 LLM / 2 unmappable
- 阻断项:
  - trigger pull_request_target: API works, platform does NOT fire trigger
  🤖 [0] type=positive target=run_status eval=llm_assisted → LLM辅助
  🤖 [1] type=positive target=run_status eval=llm_assisted → LLM辅助

### ✗ SEC-ARTF-01-001 — api_blocked
- 维度: security | 优先级: P0
- 标题: fork PR 上传的 artifact 必须不可被主仓 workflow 下载或执行
- Trigger: BLOCKED
- 断言: 2 total / 0 mappable / 0 LLM / 2 unmappable
- 阻断项:
  - trigger pull_request: API works, platform does NOT fire trigger
  - unknown repo_fixture 'with-artifacts'
  ⬜ [0] type=negative target=artifact_download eval=deterministic → needs artifact assertion kind
  ⬜ [1] type=positive target=artifact_download eval=deterministic → needs artifact assertion kind

### ✗ SEC-BASE-01-001 — api_blocked
- 维度: security | 优先级: P0
- 标题: pull_request_target 使用 base 分支的 workflow 版本
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger pull_request_target: API works, platform does NOT fire trigger
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=negative target=run_logs eval=deterministic → must_not_contain='fork_injected_step'

### ✗ SEC-BASE-01-002 — api_blocked
- 维度: security | 优先级: P0
- 标题: fork PR 改 workflow 不被 pull_request_target 采用
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger pull_request_target: API works, platform does NOT fire trigger
  ✅ [0] type=negative target=run_logs eval=deterministic → must_not_contain='fork_injected_step'
  ✅ [1] type=positive target=run_status eval=deterministic → equals='success_with_base_workflow'

### ✗ SEC-CACHE-01-001 — api_blocked
- 维度: security | 优先级: P0
- 标题: fork PR 写入的 cache 必须不可被主仓后续 workflow 读取
- Trigger: BLOCKED
- 断言: 2 total / 1 mappable / 0 LLM / 1 unmappable
- 阻断项:
  - trigger pull_request: API works, platform does NOT fire trigger
  - unknown repo_fixture 'with-cache'
  ⬜ [0] type=negative target=cache_restore eval=deterministic → needs cache assertion kind
  ✅ [1] type=positive target=run_status eval=deterministic → equals='completed'

### ✗ SEC-COMM-01-001 — api_blocked
- 维度: security | 优先级: P0
- 标题: issue_comment / pull_request_comment 触发关键字过滤必须不可被绕过
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger issue_comment: API works, platform does NOT fire trigger
  ✅ [0] type=negative target=run_status eval=deterministic → status check
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ✗ SEC-FORK-01-001 — api_blocked
- 维度: security | 优先级: P0
- 标题: fork PR 触发 pull_request 时不可读取项目 secrets
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger pull_request: API works, platform does NOT fire trigger
  ✅ [0] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_status eval=deterministic → equals='completed_or_blocked'

### ✗ SEC-FORK-01-002 — api_blocked
- 维度: security | 优先级: P0
- 标题: fork PR 中 secrets 引用返回空值且 job 不崩溃
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger pull_request: API works, platform does NOT fire trigger
  ✅ [0] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_status eval=deterministic → equals='success'

### ✗ SEC-INJ-01-001 — api_blocked
- 维度: security | 优先级: P0
- 标题: 不可信 PR 标题不可直接插进 run 脚本导致命令注入
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger pull_request: API works, platform does NOT fire trigger
  ✅ [0] type=negative target=run_logs eval=deterministic → must_not_contain='injected_command_executed'
  ✅ [1] type=positive target=run_status eval=deterministic → equals='success'

### ✗ SEC-INJ-01-002 — api_blocked
- 维度: security | 优先级: P0
- 标题: 不可信分支名不可直接插进 run 脚本导致命令注入
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger pull_request: API works, platform does NOT fire trigger
  ✅ [0] type=negative target=run_logs eval=deterministic → must_not_contain='injected_command_executed'
  ✅ [1] type=positive target=run_status eval=deterministic → equals='success'

### ✗ SEC-INJ-01-003 — api_blocked
- 维度: security | 优先级: P0
- 标题: 不可信 issue/PR 评论内容不可直接插进 run 脚本导致命令注入
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger issue_comment: API works, platform does NOT fire trigger
  ✅ [0] type=negative target=run_logs eval=deterministic → must_not_contain='injected_command_executed'
  ✅ [1] type=positive target=run_status eval=deterministic → equals='success'

### ✗ SEC-PRTGT-01-001 — api_blocked
- 维度: security | 优先级: P0
- 标题: pull_request_target 下显式 checkout 不可信 PR 时 secrets 仍应受控
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger pull_request_target: API works, platform does NOT fire trigger
  ✅ [0] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_status eval=deterministic → equals='blocked_or_pending'

### ✗ SEC-PRTGT-01-002 — api_blocked
- 维度: security | 优先级: P0
- 标题: pull_request_target 无审批不执行 fork PR 代码
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger pull_request_target: API works, platform does NOT fire trigger
  ✅ [0] type=negative target=run_status eval=deterministic → status check
  ✅ [1] type=positive target=run_status eval=deterministic → equals='pending_or_blocked'

### ✗ SEC-TOCTOU-01-002 — api_blocked
- 维度: security | 优先级: P0
- 标题: 评论触发不应绕过代码固定与 PR 审批
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger issue_comment: API works, platform does NOT fire trigger
  ✅ [0] type=negative target=run_logs eval=deterministic → must_not_contain='new_commit_after_trigger'
  ✅ [1] type=positive target=run_logs eval=deterministic → run_logs (implicit value)

### ✗ SEC-TOKEN-01-001 — api_blocked
- 维度: security | 优先级: P0
- 标题: fork PR 触发 pull_request 时 ATOMGIT_TOKEN 必须仅拥有 read 权限
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger pull_request: API works, platform does NOT fire trigger
  ✅ [0] type=positive target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=negative target=run_logs eval=deterministic → must_not_contain='write_permission_granted'

### ✗ SEC-TOKEN-01-002 — api_blocked
- 维度: security | 优先级: P0
- 标题: fork PR 中 ATOMGIT_TOKEN 写操作被平台拒绝
- Trigger: BLOCKED
- 断言: 2 total / 2 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger pull_request: API works, platform does NOT fire trigger
  ✅ [0] type=negative target=run_logs eval=deterministic → run_logs (implicit value)
  ✅ [1] type=positive target=run_status eval=deterministic → equals='completed'

### ✗ USE-ANNOT-01-002 — api_blocked
- 维度: usability | 优先级: P1
- 标题: ::error:: 生成的 PR annotation 具备文件路径、行号与可点击跳转
- Trigger: BLOCKED
- 断言: 1 total / 0 mappable / 1 LLM / 1 unmappable
- 阻断项:
  - trigger pull_request: API works, platform does NOT fire trigger
  🤖 [0] type=nonfunctional target=pr_ui eval=llm_assisted → LLM辅助

### ✗ USE-TYPE-01-001 — api_blocked
- 维度: usability | 优先级: P1
- 标题: 使用 GitCode types 命名时正常触发
- Trigger: BLOCKED
- 断言: 1 total / 1 mappable / 0 LLM / 0 unmappable
- 阻断项:
  - trigger pull_request: API works, platform does NOT fire trigger
  ✅ [0] type=positive target=run_status eval=deterministic → equals='COMPLETED'
