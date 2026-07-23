# Case 可脚本化分类报告

**数据源**: `phase01/runs/2026-07-21-02/cases/yaml/` (197 cases)
**Phase 02 执行器**: `workflow_runner.py` + `assertion_engine.py`

## 总体统计（含 trigger + setup + fault + 断言）

| 分类 | 数量 | 占比 | 含义 |
|------|------|------|------|
| `full_scriptable` | **107** | 54.3% | trigger=push + 全部断言可映射 + 无 setup/fault 阻断 |
| `partial_scriptable` | **59** | 29.9% | trigger=push 但存在部分阻断（LLM、新 target、未知 fixture） |
| `not_scriptable` | **31** | 15.7% | trigger 非 push（fork_pr/manual/schedule/pr/pull_request） |

## 按维度 × 分类

| 维度 | full | partial | not | 合计 | 主要阻断 |
|------|------|---------|-----|------|---------|
| completeness | 21 | 6 | 2 | 29 | 未知 fixture、llm_assisted |
| compatibility | 39 | 16 | 6 | 61 | llm_assisted、pr/manual trigger |
| reliability | 25 | 10 | 5 | 40 | fault_injection、schedule trigger |
| security | 17 | 8 | 15 | 40 | fork_pr trigger、untrusted_contributor |
| usability | 5 | 19 | 3 | 27 | llm_assisted（大量 error_message） |

---

## 阻断项详解

### 断言层阻断（assertion_engine 不支持）

| 阻断 | 数量 | 缺什么 |
|------|------|--------|
| `eval=llm_assisted` | **44** | assertion_engine 加 LLM 辅助判定通道（27 条 target=error_message） |
| `target=run_ui / pr_ui` | **4** | Playwright 浏览器自动化 |
| `target=badge_response` | **3** | HTTP client 获取 badge URL 并解析 SVG |
| `target=runner_schedulable / runner_scheduling` | **3** | runner API 已有（`GET .../actions/runners`），加 assertion kind |
| `target=workflow_validation` | **2** | validate_workflow.py 已有（`POST /api/v2/.../valid`），接入 engine |
| `target=run_duration` | **2** | run API 已有 `start_time`/`end_time`，算差值 + 加 duration kind |
| `target=step_summary` | **1** | job API 已有 steps JSON，解析结构体而非 grep 日志 |
| `target=artifacts` | **1** | artifact API 已有（`GET .../actions/artifacts` + download），加扫描 kind |

### Trigger 层阻断

| 阻断 | 数量 | 缺什么 |
|------|------|--------|
| `fork_pr` trigger | **13** | fork API（`POST /api/v5/.../forks`）+ 第二 GitCode 账号 |
| `trigger.as=untrusted_contributor` | **17** | 第二 GitCode 账号 + OAuth token |
| `manual` trigger | **5** | dispatch API 已验证可用（`actions_ctl.py`），未集成到 runner |
| `schedule` trigger | **5** | cron 无法按需触发，变通：push + `ATOMGIT_EVENT_NAME=schedule` |
| `pr` / `pull_request` / `pull_request_target` / `pull_request_comment` | **8** | PR 创建 API（`POST /api/v5/.../pulls`）已有，未集成到 runner |

### 执行环境阻断

| 阻断 | 数量 | 缺什么 |
|------|------|--------|
| `fault_injection` 非 null | **5** | runner kill / network_partition / concurrent_flood infra |
| 未知 `repo_fixture` | **~18** | 预先创建配置好的测试仓 |

---

## API 状态

| API | 状态 | 验证方式 |
|-----|------|---------|
| `POST web-api.gitcode.com/api/v2/.../actions/workflows/{id}/dispatch` | ✅ | `actions_ctl.py` dispatch → poll → COMPLETED |
| `POST web-api.gitcode.com/api/v2/.../actions/workflow-runs/{id}/stop` | ✅ | `actions_ctl.py` stop → `{"success": true}` |
| `POST web-api.gitcode.com/api/v2/.../actions/valid` | ✅ | `validate_workflow.py` 已集成 |
| `POST api.gitcode.com/api/v5/repos/{o}/{r}/pulls` | ✅ | GitCode 文档已收录 |
| `POST api.gitcode.com/api/v5/repos/{o}/{r}/forks` | ✅ | GitCode 文档已收录 |
| `POST api.gitcode.com/api/v5/repos/{o}/{r}/pulls/{n}/comments` | ✅ | GitCode 文档已收录 |
| `POST web-api.gitcode.com/api/v2/repos/{id}/variables` | ✅ | 端点存在，需有 repo 管理权限的 cookie |

---

## 逐 Case 明细

### ✓ COMP-ACTION-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ALL_ACTIONS_EXECUTED']

### ◐ COMP-ACTOR-02-001 — partial_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 2 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ACTOR_EXPR', 'ACTOR_ENV']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ACTOR_CHECK_DONE', 'CONTEXTS_ENUMERATED']
  🤖 断言[2] type=nonfunctional target=run_logs eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMP-ARTIFACT-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ARTIFACT_CONTENT_VERIFIED']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['ARTIFACT_CONTENT_MISMATCH']

### ✓ COMP-CACHE-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['CACHE_HIT_', '日志含 CACHE_HIT_']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['CACHE_MISS']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ COMP-CONCUR-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['2']
  ✅ 断言[1] type=positive target=run_status eval=deterministic
     映射 kind: `status`

### ✓ COMP-CONTAINER-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 4 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['CONTAINER_PUBLIC_OK']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['CONTAINER_PRIVATE_OK']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['SHOULD_NOT_RUN']
  ✅ 断言[3] type=negative target=run_status eval=deterministic
     映射 kind: `status`

### ✓ COMP-CONTERR-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['JOB_C_ALWAYS_EXECUTED', 'if: always(']

### ✓ COMP-CONTEXT-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['event_name/sha/ref/workspace/run_id/repository 等']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['CONTEXT_ATTRS_DUMPED']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ COMP-DAG-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['JOB_D_ALWAYS_EXECUTED', 'if: always(']
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['PARALLEL_1_DONE', 'PARALLEL_2_DONE']

### ✓ COMP-ENV-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['输出 step-value', 'step-value']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['TEST_VAR']
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ATOMGIT_WORKSPACE']

### ✓ COMP-EXPR-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['SUCCESS_CONTEXT_TRUE', 'ALWAYS_CONTEXT_TRUE']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['FAILED_CONTEXT_TRUE']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ COMP-EXPRFN-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['CONTAINS_WORKS', 'STARTSWITH_WORKS', 'ENDSWITH_WORKS']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['hello world', 'JSON']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ COMP-FILTER-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['FILTER_MATCHED']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注

### ✓ COMP-MATIF-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ubuntu', 'MATRIX_OS', '日志含 MATRIX_OS=ubuntu']
  ✅ 断言[1] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[2] type=positive target=run_status eval=deterministic
     映射 kind: `status`

### ✓ COMP-MATRIX-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 4 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['2*3']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ubuntu, 22']
  ✅ 断言[3] type=positive target=run_status eval=deterministic
     映射 kind: `status`

### ✓ COMP-MATRIX-02-005 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 4 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ubuntu-18、ubuntu-20、centos-18、centos-20 + alpine-latest']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['EXPERIMENTAL']
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['EXPERIMENTAL']
  ✅ 断言[3] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['EXPERIMENTAL']

### ✓ COMP-MATRIX-02-006 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ubuntu-18、ubuntu-20、centos-20、centos-22']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ COMP-MATRIX-02-007 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 4 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['DYNAMIC_RUNNER_OK']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['EXTRA']
  ✅ 断言[2] type=negative target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[3] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['SHOULD_NOT_RUN']

### ✓ COMP-OUTPUT-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['OUTPUT_SET']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['NEEDS_OUTPUT']

### ◐ COMP-PARSE-02-001 — partial_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['YAML', 'WORKFLOW_PARSED_OK']
  🤖 断言[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMP-PERM-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['CLONE_OK']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['PUSH_REJECTED_AS_EXPECTED_READ_ONLY']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ COMP-POST-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['POST_CLEANUP_EXECUTED']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注

### ✓ COMP-RERUN-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 4 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['SUCCESS_JOB_DONE']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['FAIL_JOB_WILL_FAIL']
  ✅ 断言[2] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[3] type=positive target=run_status eval=deterministic
     映射 kind: `status`

### ✓ COMP-RUNNER-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ COMP-SCHEDULE-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['SCHEDULE_TRIGGERED_OK']
  ✅ 断言[1] type=nonfunctional target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['触发时间在 UTC 时区']
     ⚠️ 缺少: nonfunctional 类型语义模糊，需人工判定期望
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ COMP-STAGES-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['prep-1/2']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['build-main 在 prep 之后']
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['PREP_1_DONE', 'PREP_2_DONE', 'BUILD_MAIN_DONE']

### ✓ COMP-TIMEOUT-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=nonfunctional target=run_status eval=deterministic
     映射 kind: `status`

### ✓ COMP-TRIGGER-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['TRIGGER_TEST_RUN_OK']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=positive target=run_status eval=deterministic
     映射 kind: `status`

### ✓ COMP-WF-CALL-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['${{ inputs.input-a }} 为 value-from-caller', 'value-from-caller']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ COMPAT-ACTION-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['GITCODE_CHECKOUT_OK', 'GITCODE_SETUP_NODE_OK']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ◐ COMPAT-ACTION-INPUTS-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P2
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['INPUT_TEST_PARAM']
  🤖 断言[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMPAT-ART-CACHE-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ARTIFACT_COMPAT_VERIFIED']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ COMPAT-ARTIFACT-EQUIV-02-001 — full_scriptable
- 维度: compatibility | 优先级: P2
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=positive target=run_status eval=deterministic
     映射 kind: `status`

### ✓ COMPAT-CACHE-EQUIV-02-001 — full_scriptable
- 维度: compatibility | 优先级: P2
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['CACHE_HIT', 'CACHE_MISS']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['CACHE_HIT']

### ✓ COMPAT-CHECKOUT-EQUIV-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=positive target=run_status eval=deterministic
     映射 kind: `status`

### ✓ COMPAT-CONCUR-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['所有触发均产生可追踪的 run']

### ◐ COMPAT-CONCUR-MODEL-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=negative target=run_status eval=deterministic
     映射 kind: `status`
  🤖 断言[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMPAT-CONTEXT-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ATOMGIT_CONTEXT_DUMP_COMPLETE']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['包括 repository_owner 应可访问']

### ✓ COMPAT-CTX-AVAIL-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 4 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[3] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ COMPAT-DEF-SHELL-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 4 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['SHELL', 'SHELL 输出含 bash']
  ✅ 断言[1] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[3] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['如 sh/dash']

### ◐ COMPAT-DEPRECATED-CMD-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P2
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  🤖 断言[1] type=nonfunctional target=run_logs eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMPAT-EXPRCO-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ COMPAT-EXPRCS-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['STARTSWITH_SENSITIVE_MATCH_UPPER']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['STARTSWITH_SENSITIVE_MISMATCH_LOWER', '小写不匹配，与 GitHub 有意不同']
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['CONTAINS_WORKS', 'contains 行为明确']

### ✓ COMPAT-EXPRFN-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['输出 Hello', 'Hello']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['输出 HelloGitCode', 'HelloGitCode']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ COMPAT-EXPRFN-02-002 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 5 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['RESULT']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['RESULT']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['RESULT']
  ✅ 断言[3] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['RESULT']
  ✅ 断言[4] type=nonfunctional target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['RESULT']
     ⚠️ 缺少: nonfunctional 类型语义模糊，需人工判定期望

### ✓ COMPAT-EXPRFN-02-003 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 5 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['hello', 'RESULT', "'hello', 0, 7"]
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['aaa', 'a', 'b', 'RESULT', "'aaa', 'a', 'b'"]
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['JSON_NULL', 'JSON_TRUE', 'null', 'true']
  ✅ 断言[3] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注
  ✅ 断言[4] type=nonfunctional target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['JSON', 'atomgit.event']
     ⚠️ 缺少: nonfunctional 类型语义模糊，需人工判定期望

### ✓ COMPAT-EXPRSYN-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['SUCCESS_CONDITION_TRUE', '${{ success }} 语义等价于 GitHub ${{ success(']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ALWAYS_CONDITION_TRUE', '${{ always }} 正确求值']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ◐ COMPAT-FLAVOR-LABEL-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P2
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  🤖 断言[1] type=nonfunctional target=run_logs eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMPAT-IN-TYPE-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=negative target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ COMPAT-INJECT-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 4 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['; curl evil.com']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['whoami']
  ✅ 断言[3] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ COMPAT-MATFF-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注

### ✓ COMPAT-MATRIX-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 6 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ubuntu-18、ubuntu-20、centos-20 + alpine-edge']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['EXPERIMENTAL']
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[3] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注
  ✅ 断言[4] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注
  ✅ 断言[5] type=negative target=run_status eval=deterministic
     映射 kind: `status`

### ✓ COMPAT-MIGR-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['非 500/内部错误']

### ✓ COMPAT-MULTILINE-DELIM-02-001 — full_scriptable
- 维度: compatibility | 优先级: P2
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['MY_VAR', 'line1']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['PATH']

### ◐ COMPAT-NO-WIN-MAC-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=negative target=run_status eval=deterministic
     映射 kind: `status`
  🤖 断言[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMPAT-OUTPUT-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ATOMGIT_OUTPUT']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['version=1.2.3, status=stable']

### ◐ COMPAT-OUTPUT-LIMIT-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P2
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  🤖 断言[1] type=nonfunctional target=run_logs eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMPAT-PATHS-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['PATHS_MATCHED_AND_TRIGGERED']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=positive target=run_status eval=deterministic
     映射 kind: `status`

### ✓ COMPAT-PERMS-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['CLONE_WITH_GC_PERMS_OK', 'PUSH_REJECTED_AS_EXPECTED']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ COMPAT-POST-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=negative target=run_status eval=deterministic
     映射 kind: `status`

### ✓ COMPAT-PR-COMM-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ COMPAT-PR-TARGET-02-001 — full_scriptable
- 维度: compatibility | 优先级: P0
- 可映射断言: 4 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ATOMGIT_TOKEN']
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[3] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['YAML']

### ✓ COMPAT-PR-TYPES-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['PR_TYPE_TRIGGERED_OK', 'open/update/reopen/merge']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['opened/synchronize/reopened']

### ✓ COMPAT-RECURSIVE-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=negative target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['TRIGGER_BLOCKED']

### ✓ COMPAT-RUN-CTX-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['RUNNER_CONTEXT_DUMPED']

### ✓ COMPAT-RUN-LBL-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['THREE_PART_LABEL_MATCHED']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ COMPAT-RUNNER-NAME-02-001 — full_scriptable
- 维度: compatibility | 优先级: P2
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ARCH']

### ✓ COMPAT-RUNSON-EQUIV-02-001 — full_scriptable
- 维度: compatibility | 优先级: P2
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ARRAY_FORM_OK']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['DEFAULT_FORM_OK']

### ◐ COMPAT-RUNSON-MIGR-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P0
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=negative target=run_status eval=deterministic
     映射 kind: `status`
  🤖 断言[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMPAT-SCHEDULE-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ATOMGIT_EVENT_NAME', 'schedule']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=negative target=run_status eval=deterministic
     映射 kind: `status`

### ✓ COMPAT-SECRET-M-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 4 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注
  ✅ 断言[3] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ COMPAT-SETUP-STAR-02-001 — full_scriptable
- 维度: compatibility | 优先级: P2
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['v20']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注

### ✓ COMPAT-STAGE-FIELDS-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['PRE_BUILD', 'BUILD_DONE']
  ✅ 断言[1] type=positive target=run_status eval=deterministic
     映射 kind: `status`

### ✓ COMPAT-STAGES-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=positive target=run_status eval=deterministic
     映射 kind: `status`

### ✓ COMPAT-STAGES-ORCH-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['BUILD_DONE', 'TEST_DONE']
  ✅ 断言[1] type=positive target=run_status eval=deterministic
     映射 kind: `status`

### ◐ COMPAT-STAGES-SYNTAX-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P2
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  🤖 断言[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMPAT-SYSENV-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ATOMGIT_', 'ATOMGIT_SYSENV_DUMP_COMPLETE']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ATOMGIT_REPOSITORY_OWNER']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['GITHUB_TOKEN']

### ◐ COMPAT-SYSENV-MAP-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ATOMGIT_ENV']
  🤖 断言[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ COMPAT-TOOLCHAIN-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P2
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  🤖 断言[1] type=nonfunctional target=run_logs eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ COMPAT-UNKNOWN-TOP-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=negative target=run_status eval=deterministic
     映射 kind: `status`
  🤖 断言[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMPAT-UNSUPP-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['container.image / environment / services']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['BASIC_EXECUTION_OK']

### ◐ COMPAT-USES-REF-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  🤖 断言[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ COMPAT-USING-RUNTIME-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=negative target=run_status eval=deterministic
     映射 kind: `status`
  🤖 断言[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMPAT-VAR-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 5 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['RUNNER_OS', '如 Linux']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['RUNNER_ARCH', '如 X64']
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['RUNNER_NAME', 'RUNNER_TEMP', 'RUNNER_TOOL_CACHE', 'RUNNER_ENVIRONMENT']
  ✅ 断言[3] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ATOMGIT_RUNNER_OS', 'ATOMGIT_RUNNER_ARCH', 'ATOMGIT_REPOSITORY_OWNER']
  ✅ 断言[4] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['历史 TC-441/442/206 不应复现']

### ✓ COMPAT-VAR-02-002 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 4 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ENV_LEVEL']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ENV_LEVEL', 'vars 不直接介入 shell 覆盖']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['历史 TC-533 不应复现']
  ✅ 断言[3] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ COMPAT-VAR-02-003 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 4 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['RUNNER_OS']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ATOMGIT_SHA']
  ✅ 断言[2] type=negative target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[3] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['RUNNER_OS']

### ✓ COMPAT-WF-CALL-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=negative target=run_status eval=deterministic
     映射 kind: `status`

### ◐ COMPAT-WF-CMD-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P2
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  🤖 断言[1] type=nonfunctional target=run_ui eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMPAT-WF-NEST-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=negative target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[2] type=negative target=run_status eval=deterministic
     映射 kind: `status`

### ✗ COMPAT-YAML-ERROR-02-001 — not_scriptable
- 维度: compatibility | 优先级: P1
- 可映射断言: 0 / 无法映射: 2 / 需 LLM: 2
- 原因: eval=llm_assisted, 需要 LLM 判定
  🤖 断言[0] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定
  🤖 断言[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ REL-ART-CACHE-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ REL-CANCEL-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['CLEANUP_EXECUTED_AFTER_CANCEL']
  ✅ 断言[2] type=negative target=run_status eval=deterministic
     映射 kind: `status`

### ✓ REL-CANCEL-02-002 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 4 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[2] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[3] type=negative target=run_status eval=deterministic
     映射 kind: `status`

### ✓ REL-CANCEL-02-003 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['Cleanup completed', "日志含 'Cleanup completed'"]
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ REL-CANCEL-02-004 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['POST_CLEANUP_MARKER']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注
  ✅ 断言[2] type=nonfunctional target=run_status eval=deterministic
     映射 kind: `status`

### ◐ REL-CANCEL-02-005 — partial_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 3 / 无法映射: 1 / 需 LLM: 0
- 原因: target=runner_schedulable 不在引擎支持范围内（需新 infra）
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=negative target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[2] type=negative target=run_status eval=deterministic
     映射 kind: `status`
  ❌ 断言[3] type=nonfunctional target=runner_schedulable eval=deterministic
     🚫 target=runner_schedulable 不在引擎支持范围内（需新 infra）

### ✓ REL-CHAOS-02-001 — full_scriptable
- 维度: reliability | 优先级: P0
- 可映射断言: 4 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[3] type=nonfunctional target=run_status eval=deterministic
     映射 kind: `status`

### ✓ REL-CHAOS-02-002 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['exit code 不等于 0']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=positive target=run_status eval=deterministic
     映射 kind: `status`

### ✓ REL-CHAOS-02-003 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 1 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`

### ✓ REL-CONCUR-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 4 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[2] type=negative target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[3] type=nonfunctional target=run_status eval=deterministic
     映射 kind: `status`

### ✓ REL-CONCUR-02-002 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 4 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[2] type=negative target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[3] type=nonfunctional target=run_status eval=deterministic
     映射 kind: `status`

### ✓ REL-CONCUR-02-003 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[2] type=negative target=run_status eval=deterministic
     映射 kind: `status`

### ✓ REL-CONCUR-02-004 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 1 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`

### ✓ REL-CONTERR-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['JOB_C_ALWAYS_EXECUTED', 'if: always(']

### ◐ REL-CONV-02-001 — partial_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 4 / 无法映射: 1 / 需 LLM: 0
- 原因: target=runner_scheduling 不在引擎支持范围内（需新 infra）
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['CLEANUP_DONE']
  ✅ 断言[3] type=negative target=run_status eval=deterministic
     映射 kind: `status`
  ❌ 断言[4] type=positive target=runner_scheduling eval=deterministic
     🚫 target=runner_scheduling 不在引擎支持范围内（需新 infra）

### ◐ REL-CRON-02-001 — partial_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 3 / 无法映射: 1 / 需 LLM: 0
- 原因: target=workflow_validation 不在引擎支持范围内（需新 infra）
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=negative target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注
  ❌ 断言[3] type=positive target=workflow_validation eval=deterministic
     🚫 target=workflow_validation 不在引擎支持范围内（需新 infra）

### ◐ REL-LARGE-REPO-02-001 — partial_scriptable
- 维度: reliability | 优先级: P2
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 0
- 原因: target=run_duration 不在引擎支持范围内（需新 infra）
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ❌ 断言[1] type=nonfunctional target=run_duration eval=deterministic
     🚫 target=run_duration 不在引擎支持范围内（需新 infra）

### ◐ REL-MANY-STEPS-02-001 — partial_scriptable
- 维度: reliability | 优先级: P2
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 0
- 原因: target=run_duration 不在引擎支持范围内（需新 infra）
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ❌ 断言[1] type=nonfunctional target=run_duration eval=deterministic
     🚫 target=run_duration 不在引擎支持范围内（需新 infra）

### ✓ REL-MATRIX-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 4 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['任务初始化错误']
  ✅ 断言[3] type=nonfunctional target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: nonfunctional 类型语义模糊，需人工判定期望

### ✓ REL-MATRIX-02-002 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['4 基础 + 3 include - 1 exclude']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ REL-MATRIX-02-003 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=negative target=run_status eval=deterministic
     映射 kind: `status`

### ✓ REL-MATRIX-02-004 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[2] type=negative target=run_status eval=deterministic
     映射 kind: `status`

### ✓ REL-NEEDS-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['JOB_D_ALWAYS_EXECUTED', 'if: always(']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ REL-NEEDS-02-002 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ALL_PARENT_INSTANCES_DONE', '等待全部 matrix 实例完成']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['任务初始化错误']

### ✓ REL-NEEDS-02-003 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['任务初始化错误']

### ✓ REL-PREEMPT-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 4 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=negative target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[2] type=negative target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[3] type=nonfunctional target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: nonfunctional 类型语义模糊，需人工判定期望

### ◐ REL-PREEMPT-02-002 — partial_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 5 / 无法映射: 1 / 需 LLM: 0
- 原因: target=runner_schedulable 不在引擎支持范围内（需新 infra）
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['TICK_30', '如 TICK_30']
  ✅ 断言[2] type=negative target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[3] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注
  ✅ 断言[4] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注
  ❌ 断言[5] type=nonfunctional target=runner_schedulable eval=deterministic
     🚫 target=runner_schedulable 不在引擎支持范围内（需新 infra）

### ✓ REL-PUSH-DEDUP-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=negative target=run_status eval=deterministic
     映射 kind: `status`

### ✓ REL-RACE-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 1 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`

### ✓ REL-RERUN-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[2] type=positive target=run_status eval=deterministic
     映射 kind: `status`

### ✓ REL-RERUN-02-002 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[2] type=negative target=run_status eval=deterministic
     映射 kind: `status`

### ✓ REL-RERUN-02-003 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ATOMGIT_RUN_ID']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ATOMGIT_RUN_NUMBER']
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ATOMGIT_SHA']

### ✓ REL-RUNNER-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[2] type=negative target=run_status eval=deterministic
     映射 kind: `status`

### ✓ REL-RUNNER-02-002 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['No space left', 'disk quota exceeded']
  ✅ 断言[2] type=negative target=run_status eval=deterministic
     映射 kind: `status`

### ✓ REL-RUNNER-02-003 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['JOB_A_ENV']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ REL-RUNNER-RESIDUE-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['NO_RESIDUE']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['RESIDUE_FOUND']

### ◐ REL-SCHED-02-001 — partial_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 3 / 无法映射: 1 / 需 LLM: 0
- 原因: target=workflow_validation 不在引擎支持范围内（需新 infra）
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=negative target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ❌ 断言[3] type=positive target=workflow_validation eval=deterministic
     🚫 target=workflow_validation 不在引擎支持范围内（需新 infra）

### ✓ REL-TIMEOUT-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=nonfunctional target=run_status eval=deterministic
     映射 kind: `status`

### ✓ REL-TIMEOUT-02-002 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[2] type=negative target=run_status eval=deterministic
     映射 kind: `status`

### ✓ REL-TIMEOUT-02-003 — full_scriptable
- 维度: reliability | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ SEC-ACTION-PERM-02-001 — full_scriptable
- 维度: security | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=negative target=run_logs eval=
     映射 kind: `mask`
     ⚠️ 缺少: secret_value: TEST_SECRET 的实际可见明文
  ✅ 断言[1] type=positive target=run_status eval=deterministic
     映射 kind: `status`

### ✓ SEC-CACHE-ISOLATE-02-001 — full_scriptable
- 维度: security | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['CACHE_HIT']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['REPO_A_SECRET_DATA']

### ✓ SEC-CONT-CRED-02-001 — full_scriptable
- 维度: security | 优先级: P1
- 可映射断言: 4 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['CONTAINER_STEP_EXECUTED']
  ✅ 断言[1] type=negative target=run_logs eval=
     映射 kind: `mask`
     ⚠️ 缺少: secret_value: REGISTRY_USERNAME 的实际可见明文
  ✅ 断言[2] type=negative target=run_logs eval=
     映射 kind: `mask`
     ⚠️ 缺少: secret_value: REGISTRY_PASSWORD 的实际可见明文
  ✅ 断言[3] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ SEC-CONT-ISOLATE-02-001 — full_scriptable
- 维度: security | 优先级: P1
- 可映射断言: 4 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['EXPLICIT_VAR_OK']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['HOST_SECRET_LEAKED']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['HOST_PATH_ACCESSIBLE']
  ✅ 断言[3] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['HOST_SECRET_ISOLATED', 'HOST_PATH_ISOLATED']

### ✓ SEC-DISK-LEAK-02-001 — full_scriptable
- 维度: security | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['DISK_NO_LEAK']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['DISK_LEAK_FOUND']

### ✓ SEC-ENV-POLLUTE-02-001 — full_scriptable
- 维度: security | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注
  ✅ 断言[1] type=positive target=run_status eval=deterministic
     映射 kind: `status`

### ✓ SEC-ENV-REVIEW-02-001 — full_scriptable
- 维度: security | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=negative target=run_logs eval=
     映射 kind: `mask`
     ⚠️ 缺少: secret_value: ENV_SECRET 的实际可见明文

### ✓ SEC-ENV-WAIT-02-001 — full_scriptable
- 维度: security | 优先级: P1
- 可映射断言: 4 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ENV_SECRET_ACCESSED']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['ENV_SECRET_ACCESSED', 'job 未提前执行']
  ✅ 断言[2] type=negative target=run_logs eval=
     映射 kind: `mask`
     ⚠️ 缺少: secret_value: DEPLOY_TOKEN 的实际可见明文
  ✅ 断言[3] type=nonfunctional target=run_status eval=deterministic
     映射 kind: `status`

### ✓ SEC-FORK-02-001 — full_scriptable
- 维度: security | 优先级: P0
- 可映射断言: 5 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['PUSH_REJECTED_AS_EXPECTED']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['SECRET_EMPTY_AS_EXPECTED']
  ✅ 断言[2] type=negative target=run_logs eval=
     映射 kind: `mask`
     ⚠️ 缺少: secret_value: DEPLOY_TOKEN 的实际可见明文
  ✅ 断言[3] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['PUSH_SUCCEEDED_UNEXPECTEDLY']
  ✅ 断言[4] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['SECRET_NOT_EMPTY_UNEXPECTED']

### ✓ SEC-FORK-02-002 — full_scriptable
- 维度: security | 优先级: P0
- 可映射断言: 5 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['PROJECT_SECRET_EMPTY_AS_EXPECTED']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ORG_SECRET_EMPTY_AS_EXPECTED']
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['API_AUTH_REJECTED_AS_EXPECTED']
  ✅ 断言[3] type=negative target=run_logs eval=
     映射 kind: `mask`
     ⚠️ 缺少: secret_value: DEPLOY_KEY 的实际可见明文
  ✅ 断言[4] type=negative target=run_logs eval=
     映射 kind: `mask`
     ⚠️ 缺少: secret_value: ORG_TOKEN 的实际可见明文

### ✓ SEC-FORK-02-003 — full_scriptable
- 维度: security | 优先级: P0
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['BASE_BRANCH_WORKFLOW_EXECUTED']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['FORK_CODE_EXECUTED']
  ✅ 断言[2] type=positive target=run_status eval=deterministic
     映射 kind: `status`

### ✓ SEC-FORK-02-004 — full_scriptable
- 维度: security | 优先级: P0
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['MAKE_BUILD_EXECUTED', '显式 checkout head.sha 后可执行 fork 侧代码']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ SEC-FORK-02-005 — full_scriptable
- 维度: security | 优先级: P0
- 可映射断言: 4 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['PUSH_SUCCEEDED_UNEXPECTEDLY']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['PUSH_REJECTED_AS_EXPECTED']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['API_NOT_REJECTED_UNEXPECTED']
  ✅ 断言[3] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['API_REJECTED_403_AS_EXPECTED']

### ✓ SEC-INJECT-02-001 — full_scriptable
- 维度: security | 优先级: P0
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['NO_INJECTION_AS_EXPECTED']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['INJECTION_SUCCEEDED_UNEXPECTEDLY']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ SEC-INJECT-02-002 — full_scriptable
- 维度: security | 优先级: P0
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['NO_INJECTION_AS_EXPECTED']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['INJECTION_SUCCEEDED_UNEXPECTEDLY']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ SEC-INJECT-02-003 — full_scriptable
- 维度: security | 优先级: P0
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['NO_INJECTION_AS_EXPECTED']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['INJECTION_SUCCEEDED_UNEXPECTEDLY']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ SEC-INJECT-02-004 — full_scriptable
- 维度: security | 优先级: P0
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['NO_INJECTION_AS_EXPECTED']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['INJECTION_SUCCEEDED_UNEXPECTEDLY']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ SEC-INJECT-02-005 — full_scriptable
- 维度: security | 优先级: P0
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['PR_TITLE']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注
  ✅ 断言[2] type=positive target=run_status eval=deterministic
     映射 kind: `status`

### ✓ SEC-INJECT-02-006 — full_scriptable
- 维度: security | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['SAFE_ENV_REFERENCE_OK']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ SEC-JOB-ISOLATE-02-001 — full_scriptable
- 维度: security | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ISOLATION_INTACT']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['ISOLATION_BROKEN']

### ✓ SEC-PERMS-02-001 — full_scriptable
- 维度: security | 优先级: P0
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['PUSH_REJECTED_AS_EXPECTED']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['PUSH_SUCCEEDED_UNEXPECTEDLY']

### ✓ SEC-PERMS-02-002 — full_scriptable
- 维度: security | 优先级: P0
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['PUSH_REJECTED_BY_DEFAULT_PERMS']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['PUSH_ALLOWED_BY_DEFAULT_PERMS']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ SEC-PERMS-02-003 — full_scriptable
- 维度: security | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['JOB_A_OVERRIDE_CLONE_OK']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['JOB_B_PR_NONE_OK']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ SEC-REFPROT-02-001 — full_scriptable
- 维度: security | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['REF_PROTECTED', 'DEPLOY_STEP_EXECUTED']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['DEPLOY_STEP_EXECUTED']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ SEC-RUNNER-LEAK-02-001 — full_scriptable
- 维度: security | 优先级: P0
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['NO_LEAK_AS_EXPECTED']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     提取候选值: ['LEAK_FOUND_UNEXPECTED']
  ✅ 断言[2] type=negative target=run_logs eval=
     映射 kind: `mask`
     ⚠️ 缺少: secret_value: LEAK_TEST_SECRET 的实际可见明文

### ✓ SEC-RUNNER-SHARE-02-001 — full_scriptable
- 维度: security | 优先级: P0
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['SECRET_EMPTY_AS_EXPECTED']
  ✅ 断言[1] type=negative target=run_logs eval=
     映射 kind: `mask`
     ⚠️ 缺少: secret_value: SECRET_A 的实际可见明文

### ✓ SEC-SECRET-MASK-02-001 — full_scriptable
- 维度: security | 优先级: P0
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=negative target=run_logs eval=
     映射 kind: `mask`
     ⚠️ 缺少: secret_value: TEST_SECRET 的实际可见明文
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['This is normal text visible in logs']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ◐ SEC-SECRET-MASK-02-002-V1 — partial_scriptable
- 维度: security | 优先级: P0
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=negative target=run_logs eval=
     映射 kind: `mask`
     ⚠️ 缺少: secret_value: SPLIT_SECRET 的实际可见明文
  🤖 断言[1] type=nonfunctional target=run_logs eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ SEC-SECRET-MASK-02-002-V2 — partial_scriptable
- 维度: security | 优先级: P1
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=negative target=run_logs eval=
     映射 kind: `mask`
     ⚠️ 缺少: secret_value: MULTILINE_SECRET 的实际可见明文
  🤖 断言[1] type=nonfunctional target=run_logs eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ SEC-SECRET-MASK-02-002 — partial_scriptable
- 维度: security | 优先级: P1
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=negative target=run_logs eval=
     映射 kind: `mask`
     ⚠️ 缺少: secret_value: TEST_SECRET 的实际可见明文
  🤖 断言[1] type=nonfunctional target=run_logs eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ SEC-SECRET-MASK-02-003 — full_scriptable
- 维度: security | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=negative target=run_logs eval=
     映射 kind: `mask`
     ⚠️ 缺少: secret_value: COMPOUND_SECRET 的实际可见明文
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ SEC-SECRET-MASK-02-004 — full_scriptable
- 维度: security | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=negative target=run_logs eval=
     映射 kind: `mask`
     ⚠️ 缺少: secret_value: MULTILINE_SECRET 的实际可见明文
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ SEC-SECRET-MASK-02-005 — full_scriptable
- 维度: security | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ADD_MASK_TEST_DONE', 'MASK_ISOLATION_TEST_DONE']
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ SEC-SHA-REF-02-001 — full_scriptable
- 维度: security | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ◐ SEC-SIDECHAN-02-001 — partial_scriptable
- 维度: security | 优先级: P1
- 可映射断言: 1 / 无法映射: 2 / 需 LLM: 0
- 原因: target=artifacts 不在引擎支持范围内（需新 infra）; target=step_summary 不在引擎支持范围内（需新 infra）
  ✅ 断言[0] type=negative target=run_logs eval=
     映射 kind: `mask`
     ⚠️ 缺少: secret_value: SIDECHAN_SECRET 的实际可见明文
  ❌ 断言[1] type=negative target=step_summary eval=deterministic
     🚫 target=step_summary 不在引擎支持范围内（需新 infra）
  ❌ 断言[2] type=negative target=artifacts eval=deterministic
     🚫 target=artifacts 不在引擎支持范围内（需新 infra）

### ◐ SEC-SUPPLY-02-001 — partial_scriptable
- 维度: security | 优先级: P1
- 可映射断言: 2 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['SHA_PINNED_ACTION_WORKS']
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注
  🤖 断言[2] type=nonfunctional target=run_logs eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ SEC-SUPPLY-02-002 — full_scriptable
- 维度: security | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✓ SEC-TOCTOU-02-001 — full_scriptable
- 维度: security | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=negative target=run_status eval=deterministic
     映射 kind: `status`

### ✓ SEC-TOKEN-02-001 — full_scriptable
- 维度: security | 优先级: P0
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=negative target=run_logs eval=
     映射 kind: `mask`
     ⚠️ 缺少: secret_value: atomgit_token 的实际可见明文
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注

### ✓ SEC-TOKEN-EXPIRE-02-001 — full_scriptable
- 维度: security | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=negative target=run_logs eval=
     映射 kind: `mask`
     ⚠️ 缺少: secret_value: TOKEN_TEST_SECRET 的实际可见明文

### ✗ USE-BADGE-02-001 — not_scriptable
- 维度: usability | 优先级: P2
- 可映射断言: 0 / 无法映射: 4 / 需 LLM: 1
- 原因: target=badge_response 不在引擎支持范围内（需新 infra）; eval=llm_assisted, 需要 LLM 判定
  ❌ 断言[0] type=positive target=badge_response eval=deterministic
     🚫 target=badge_response 不在引擎支持范围内（需新 infra）
  ❌ 断言[1] type=negative target=badge_response eval=deterministic
     🚫 target=badge_response 不在引擎支持范围内（需新 infra）
  ❌ 断言[2] type=nonfunctional target=badge_response eval=deterministic
     🚫 target=badge_response 不在引擎支持范围内（需新 infra）
  🤖 断言[3] type=nonfunctional target=documentation eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ USE-DEBUG-02-001 — full_scriptable
- 维度: usability | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注
  ✅ 断言[2] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['GROUP_FOLD_TEST_DONE']

### ✗ USE-DEBUG-02-002 — not_scriptable
- 维度: usability | 优先级: P2
- 可映射断言: 0 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  🤖 断言[0] type=nonfunctional target=run_status eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ USE-DEBUG-02-003 — full_scriptable
- 维度: usability | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ATOMGIT_']
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ATOMGIT_REPOSITORY', 'ATOMGIT_ACTOR']

### ✗ USE-DEBUG-02-004 — not_scriptable
- 维度: usability | 优先级: P2
- 可映射断言: 0 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  🤖 断言[0] type=nonfunctional target=run_status eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ USE-DOC-02-001 — full_scriptable
- 维度: usability | 优先级: P2
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=negative target=run_logs eval=deterministic
     映射 kind: `leak`
     ⚠️ 缺少: 无法从 rubric 提取具体 forbidden 值，需手工标注

### ✗ USE-DOC-02-002 — not_scriptable
- 维度: usability | 优先级: P1
- 可映射断言: 0 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  🤖 断言[0] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ USE-DOC-02-003 — full_scriptable
- 维度: usability | 优先级: P1
- 可映射断言: 2 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[1] type=negative target=run_logs eval=determistic
     映射 kind: `leak`
     提取候选值: ['FAIL']

### ◐ USE-ERR-MSG-02-001 — partial_scriptable
- 维度: usability | 优先级: P1
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['WORKFLOW_PARSED']
  🤖 断言[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ USE-ERR-MSG-02-002 — partial_scriptable
- 维度: usability | 优先级: P1
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['PR_TYPE_VALID_VALUES_WORK']
  🤖 断言[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ USE-ERR-MSG-02-003 — partial_scriptable
- 维度: usability | 优先级: P1
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['ATOMGIT_CONTEXT_WORKS']
  🤖 断言[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✗ USE-ERR-MSG-02-004 — not_scriptable
- 维度: usability | 优先级: P1
- 可映射断言: 0 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  🤖 断言[0] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✗ USE-ERR-MSG-02-005 — not_scriptable
- 维度: usability | 优先级: P1
- 可映射断言: 0 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  🤖 断言[0] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✗ USE-ERR-MSG-02-006 — not_scriptable
- 维度: usability | 优先级: P1
- 可映射断言: 0 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  🤖 断言[0] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ USE-INPUTS-DEFAULT-02-001 — partial_scriptable
- 维度: usability | 优先级: P2
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['INPUT_VAL']
  🤖 断言[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ USE-MIGR-02-001 — partial_scriptable
- 维度: usability | 优先级: P1
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['GITCODE_FORMAT_WORKS']
  🤖 断言[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ USE-MIGR-02-002 — partial_scriptable
- 维度: usability | 优先级: P1
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     提取候选值: ['GITCODE_RUNS_ON_WORKS']
  🤖 断言[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ USE-MIGR-02-003 — partial_scriptable
- 维度: usability | 优先级: P0
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  🤖 断言[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✗ USE-MIGR-02-004 — not_scriptable
- 维度: usability | 优先级: P1
- 可映射断言: 0 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  🤖 断言[0] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✗ USE-MIGR-02-005 — not_scriptable
- 维度: usability | 优先级: P1
- 可映射断言: 0 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  🤖 断言[0] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✗ USE-MIGR-02-006 — not_scriptable
- 维度: usability | 优先级: P1
- 可映射断言: 0 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  🤖 断言[0] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✗ USE-NEST-02-001 — not_scriptable
- 维度: usability | 优先级: P2
- 可映射断言: 0 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  🤖 断言[0] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✗ USE-PR-CHECKS-02-001 — not_scriptable
- 维度: usability | 优先级: P2
- 可映射断言: 0 / 无法映射: 2 / 需 LLM: 1
- 原因: target=pr_ui 不在引擎支持范围内（需新 infra）; eval=llm_assisted, 需要 LLM 判定
  ❌ 断言[0] type=positive target=pr_ui eval=deterministic
     🚫 target=pr_ui 不在引擎支持范围内（需新 infra）
  🤖 断言[1] type=nonfunctional target=pr_ui eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ USE-QUEUE-02-001 — partial_scriptable
- 维度: usability | 优先级: P2
- 可映射断言: 1 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  ✅ 断言[0] type=positive target=run_status eval=
     映射 kind: `run_status`
  🤖 断言[1] type=nonfunctional target=queue_ui eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ USE-RERUN-02-001 — full_scriptable
- 维度: usability | 优先级: P1
- 可映射断言: 3 / 无法映射: 0 / 需 LLM: 0
- 原因: 全部断言可映射
  ✅ 断言[0] type=positive target=run_status eval=deterministic
     映射 kind: `status`
  ✅ 断言[1] type=positive target=run_logs eval=deterministic
     映射 kind: `value`
     ⚠️ 缺少: 无法从 rubric 提取具体 expect 值，需手工标注
  ✅ 断言[2] type=negative target=run_status eval=deterministic
     映射 kind: `status`

### ✗ USE-RERUN-02-002 — not_scriptable
- 维度: usability | 优先级: P2
- 可映射断言: 0 / 无法映射: 1 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定
  🤖 断言[0] type=nonfunctional target=run_status eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✗ USE-SUMMARY-02-001 — not_scriptable
- 维度: usability | 优先级: P2
- 可映射断言: 0 / 无法映射: 4 / 需 LLM: 1
- 原因: eval=llm_assisted, 需要 LLM 判定; target=run_ui 不在引擎支持范围内（需新 infra）
  ❌ 断言[0] type=positive target=run_ui eval=deterministic
     🚫 target=run_ui 不在引擎支持范围内（需新 infra）
  ❌ 断言[1] type=negative target=run_ui eval=deterministic
     🚫 target=run_ui 不在引擎支持范围内（需新 infra）
  ❌ 断言[2] type=nonfunctional target=run_ui eval=deterministic
     🚫 target=run_ui 不在引擎支持范围内（需新 infra）
   🤖 断言[3] type=nonfunctional target=run_ui eval=llm_assisted
      🚫 eval=llm_assisted, 需要 LLM 判定

---

# YAML Workflow Validation Results

**数据源**: `phase02/classify-experiment/2026-07-21-02-re/cases/yaml/` (已修复)
**总 case 数**: 197
**校验时间**: 2026-07-23

## 总体统计

| 分类 | 数量 | 占比 |
|------|------|------|
| VALID (通过校验) | 149 | 75.6% |
| INVALID/ERROR (未通过) | 48 | 24.4% |

> 原始 197 case 仅有 99 VALID (50.3%)，经过 `fix_workflows_v3.py` 自动修复后提升至 149 (75.6%)。

## 48 Invalid Cases 明细

### A. YAML 解析错误 (14 cases)

这些 case 的 workflow YAML 存在结构性语法错误，无法被 API 正常解析：

| Case ID | 错误原因 |
|---------|---------|
| COMP-MATIF-02-001 | on: 反序列化失败（旧生成器 on 格式问题） |
| COMP-MATRIX-02-001 | on: 反序列化失败 |
| COMP-MATRIX-02-007 | on: 反序列化失败 |
| COMP-POST-02-001 | while parsing a block mapping（stages 内部缩进错误） |
| COMP-STAGES-02-001 | while parsing a block mapping |
| COMPAT-INJECT-02-001 | on: 反序列化失败 |
| COMPAT-POST-02-001 | Cannot construct instance（stages 反序列化失败） |
| COMPAT-STAGE-FIELDS-02-001 | mapping values are not allowed here |
| COMPAT-STAGES-02-001 | Cannot construct instance（stages 反序列化失败） |
| COMPAT-STAGES-ORCH-02-001 | mapping values are not allowed here |
| REL-CANCEL-02-002 | Cannot construct instance（stages 反序列化失败） |
| REL-CANCEL-02-003 | Cannot construct instance（stages 反序列化失败） |
| REL-MATRIX-02-001 | on: 反序列化失败 |
| REL-NEEDS-02-002 | on: 反序列化失败 |

### B. on: 格式问题 (5 cases) — 原有生成器 bug

| Case ID | 错误 |
|---------|------|
| COMP-TRIGGER-02-001 | on.pull_request_target branches 超出限制 |
| COMPAT-PR-TYPES-02-001 | on.merge_requests branches 超出限制 |
| REL-NEEDS-02-003 | on: 反序列化失败 |
| REL-PREEMPT-02-001 | on: 反序列化失败 |
| REL-PREEMPT-02-002 | on: 反序列化失败 |

### C. 兼容性测试 — 平台不支持的特性 (11 cases)

这些是有意测试平台限制的 negative test case，不应修复：

| Case ID | 错误类型 |
|---------|---------|
| COMP-EXPR-02-001 | if: success()/always 不支持（平台限制） |
| COMP-TIMEOUT-02-001 | if: cancelled() 不支持 |
| COMP-WF-CALL-02-001 | jobs[X].steps: unknown property（workflow_call 特有） |
| COMPAT-ACTION-INPUTS-02-001 | 插件 custom-action-test 不存在 |
| COMPAT-CTX-AVAIL-02-001 | if: runner.os 不支持 |
| COMPAT-EXPRSYN-02-001 | if: success()/always() 不支持 |
| COMPAT-MIGR-02-001 | if: success()/failure() 不支持 |
| COMPAT-UNKNOWN-TOP-02-001 | run-name: unknown property |
| COMPAT-USING-RUNTIME-02-001 | 插件 node20-action-test 不存在 |
| COMPAT-WF-CALL-02-001 | .secrets: unknown property（step 级 secrets 不支持） |
| REL-MATRIX-02-003 | if: matrix.os 不支持 |

### D. WAF 418 拦截 (3 cases)

| Case ID | 备注 |
|---------|------|
| SEC-ENV-WAIT-02-001 | WAF 418，需重试或白名单 |
| SEC-FORK-02-002 | WAF 418 |
| SEC-SECRET-MASK-02-002-V1 | WAF 418 |

### E. Stages 结构错误 (3 cases) — 修复后仍缺内部 name

| Case ID | 错误 |
|---------|------|
| COMP-RERUN-02-001 | jobs[fail-job].steps[0].name: 值不能为空 |
| COMPAT-OUTPUT-02-001 | jobs[producer].steps[0].name: 值不能为空 |
| REL-RERUN-02-001 | jobs[fail-job].steps[0].name: 值不能为空 |
| REL-RERUN-02-002 | jobs[always-fail].steps[0].name: 值不能为空 |
| USE-RERUN-02-001 | jobs[job-b-fail].steps[0].name: 值不能为空 |

### F. 负面测试 — 有意 INVALID (7 cases)

| Case ID | 错误类型 |
|---------|---------|
| REL-RACE-02-001 | concurrency.exceed-action/max: unknown property（job 级 concurrency） |
| REL-RUNNER-02-001 | if: success() 不支持 |
| SEC-ACTION-PERM-02-001 | uses: 格式错误（第三方 action 引用测试） |
| SEC-SHA-REF-02-001 | uses: checkout@sha 格式错误 |
| USE-DEBUG-02-004 | stages 反序列化失败（stages 格式测试） |
| USE-ERR-MSG-02-002 | on.merge_requests branches 超出限制 |
| USE-ERR-MSG-02-004 | env: 字段类型错误（string instead of map） |
| USE-ERR-MSG-02-005 | container.image: 值不能为空 + services unknown |
| USE-ERR-MSG-02-006 | if: failure() 不支持 |

---

# Cleanup Required Cases

部分 case 在单次 run 后会留下副作用（artifact、cache、fork repo 等），再次运行同名 case 会因资源冲突而失败。需提供 cleanup API 供测试框架调用。

## 需 Cleanup 的 Case 清单

### 🔧 Artifact 清理 (6 cases)

这些 case 会上传 artifact，再次运行可能因同名 artifact 冲突失败：

| Case ID | 说明 |
|---------|------|
| COMP-ARTIFACT-02-001 | artifact 上传/下载/内容校验 |
| COMPAT-ART-CACHE-02-001 | artifact 兼容性测试 |
| COMPAT-ARTIFACT-EQUIV-02-001 | artifact 等价性测试 |
| COMPAT-OUTPUT-LIMIT-02-001 | output 大小限制测试（可能产生 artifact） |
| REL-ART-CACHE-02-001 | artifact cache 可靠性测试 |
| SEC-SIDECHAN-02-001 | 侧信道泄露测试（通过 artifact 验证） |

**需要 API**: `DELETE /api/v2/projects/{owner}/{repo}/artifacts/{id}` 或批删

### 🔧 Cache 清理 (10 cases)

这些 case 依赖 cache，干净的 cache 状态是测试前提：

| Case ID | 说明 |
|---------|------|
| COMP-CACHE-02-001 | cache key 精确/前缀匹配测试 |
| COMPAT-ART-CACHE-02-001 | artifact + cache 联合测试 |
| COMPAT-CACHE-EQUIV-02-001 | cache 等价性测试 |
| COMPAT-RUN-CTX-02-001 | runner 上下文测试（使用 cache） |
| COMPAT-SETUP-STAR-02-001 | setup-* action 测试（node/setup-node 有 cache） |
| REL-ART-CACHE-02-001 | artifact cache 可靠性测试 |
| SEC-CACHE-ISOLATE-02-001 | cache 隔离性安全测试 |
| USE-MIGR-02-004 | GitHub-style uses 迁移测试（checkout 有 cache） |
| USE-MIGR-02-005 | 迁移格式测试 |
| USE-MIGR-02-006 | 迁移格式测试 |

**需要 API**: `DELETE /api/v2/projects/{owner}/{repo}/caches` 或按 key 删除

### 🔧 Fork Repo 清理 (16 cases)

这些 case 涉及 fork 仓库的 PR 测试，需要创建 fork repo 后清理：

| Case ID | 说明 |
|---------|------|
| COMP-TRIGGER-02-001 | 多触发器测试（含 pull_request） |
| COMPAT-ART-CACHE-02-001 | artifact + cache 兼容性 |
| COMPAT-CACHE-EQUIV-02-001 | cache 等价性 |
| COMPAT-PR-COMM-02-001 | PR 评论触发 |
| COMPAT-PR-TARGET-02-001 | PR target 测试 |
| COMPAT-PR-TYPES-02-001 | PR types 触发 |
| SEC-FORK-02-001 ~ 005 | fork PR 安全测试（5 个） |
| SEC-INJECT-02-001 ~ 006 | 注入攻击测试（6 个） |
| SEC-TOKEN-EXPIRE-02-001 | token 过期测试 |

**需要 API**: `DELETE /api/v2/projects/{owner}/{repo}` 或 fork repo 清理接口

### 🔧 Secret 清理 (0 case)

Secret 在测试仓库中通过 `setup.secrets` 预置，无需 run 间清理。但需确保 secret 值不因测试泄露。

---

## Summary

| 维度 | VALID | INVALID | 需 Cleanup |
|------|-------|---------|-----------|
| YAML 校验 | 149 (75.6%) | 48 (24.4%) | — |
| artifact | — | — | 6 |
| cache | — | — | 10 |
| fork repo | — | — | 16 |
| **cleanup total** | — | — | **27** (重叠) |

### Cleanup API 缺口

| 操作 | 当前状态 | 优先级 |
|------|---------|--------|
| 删除 artifact | 未找到对应 API（api-reference.md 无记录） | 高 |
| 清除 cache | 未找到对应 API | 高 |
| 删除 fork repo | 可能有 API（与普通 repo 一致），需验证 | 中 |
