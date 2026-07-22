# Case 完整可脚本化分类报告 v2（含 trigger + setup + fault + 断言）

- **数据源**: `phase01/runs/2026-07-21-02/cases/yaml/`
- **总 case 数**: 197

## 总体统计

| 分类 | 数量 | 占比 | 含义 |
|------|------|------|------|
| full_scriptable | 107 | 54.3% | trigger 支持 + 全部断言可映射，无阻断项 |
| partial_scriptable | 59 | 29.9% | trigger 支持，但存在部分断言/参数无法映射 |
| not_scriptable | 31 | 15.7% | trigger 不支持，或全部内容无法映射 |

## 按维度 × 分类交叉统计

| 维度 | full_scriptable | partial_scriptable | not_scriptable | 合计 |
|------|-----------------|--------------------|----------------|------|
| completeness | 21 | 6 | 2 | 29 |
| compatibility | 39 | 16 | 6 | 61 |
| reliability | 25 | 10 | 5 | 40 |
| security | 17 | 8 | 15 | 40 |
| usability | 5 | 19 | 3 | 27 |

## 阻断项汇总（按出现次数排序）

- **44** 条: `eval=llm_assisted, 需要 LLM 判定`
- **17** 条: `trigger.as=untrusted_contributor：需第二 GitCode 账号/token 模拟外部贡献者`
- **13** 条: `fork_pr：需第二 GitCode 账号/token 模拟 untrusted 外部贡献者`
- **6** 条: `未知 repo_fixture 'with-pr-trigger'，需确认测试仓前置资源`
- **5** 条: `manual 触发：需 workflow_dispatch API（待确认端点）`
- **5** 条: `schedule：cron 无法按需触发（基础设施限制）`
- **5** 条: `pr 触发：需建分支+开 PR（待确认 PR API）`
- **5** 条: `fault_injection 非 null：当前执行器不支持故障注入（需 kill_runner / network_partition / concurrent_flood infra）`
- **3** 条: `未知 repo_fixture 'matrix-ci'，需确认测试仓前置资源`
- **3** 条: `target=badge_response 不在引擎支持范围内`
- **3** 条: `target=run_ui 不在引擎支持范围内`
- **2** 条: `target=runner_schedulable 不在引擎支持范围内`
- **2** 条: `target=workflow_validation 不在引擎支持范围内`
- **2** 条: `target=run_duration 不在引擎支持范围内`
- **2** 条: `未知 repo_fixture 'preemption-ci'，需确认测试仓前置资源`
- **2** 条: `未知 repo_fixture 'with-permissions'，需确认测试仓前置资源`
- **1** 条: `未知 repo_fixture 'container-ci'，需确认测试仓前置资源`
- **1** 条: `pull_request：需建分支+开 PR（待确认 PR API）`
- **1** 条: `未知 repo_fixture 'matrix-compat'，需确认测试仓前置资源`
- **1** 条: `pull_request_comment：需 PR comment API（未实现）`
- **1** 条: `pull_request_target：同 PR + base 上下文语义`
- **1** 条: `target=runner_scheduling 不在引擎支持范围内`
- **1** 条: `未知 repo_fixture 'container-isolation'，需确认测试仓前置资源`
- **1** 条: `未知 repo_fixture 'with-target-workflow'，需确认测试仓前置资源`
- **1** 条: `未知 repo_fixture 'branch-protected'，需确认测试仓前置资源`
- **1** 条: `target=step_summary 不在引擎支持范围内`
- **1** 条: `target=artifacts 不在引擎支持范围内`
- **1** 条: `target=pr_ui 不在引擎支持范围内`

## Trigger 事件分布

| 事件 | 数量 | 支持 |
|------|------|------|
| push | 166 | ✅ |
| fork_pr | 13 | ❌ |
| manual | 5 | ❌ |
| schedule | 5 | ❌ |
| pr | 5 | ❌ |
| pull_request | 1 | ❌ |
| pull_request_comment | 1 | ❌ |
| pull_request_target | 1 | ❌ |

## 逐 Case 明细

### ✓ COMP-ACTION-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ALL_ACTIONS_EXECUTED']

### ◐ COMP-ACTOR-02-001 — partial_scriptable
- 维度: completeness | 优先级: P1
- 断言: 2/3 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ACTOR_EXPR', 'ACTOR_ENV']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ACTOR_CHECK_DONE', 'CONTEXTS_ENUMERATED']
  🤖 assert[2] type=nonfunctional target=run_logs eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMP-ARTIFACT-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ARTIFACT_CONTENT_VERIFIED']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['ARTIFACT_CONTENT_MISMATCH']

### ✓ COMP-CACHE-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['CACHE_HIT_', '日志含 CACHE_HIT_']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['CACHE_MISS']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✗ COMP-CONCUR-02-001 — not_scriptable
- 维度: completeness | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=manual, as=maintainer, supported=False
- Trigger params: ['simultaneous_runs']
  - 🚫 trigger: manual 触发：需 workflow_dispatch API（待确认端点）
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['2']
  ✅ assert[1] type=positive target=run_status eval=deterministic
     → kind: `status`

### ◐ COMP-CONTAINER-02-001 — partial_scriptable
- 维度: completeness | 优先级: P1
- 断言: 4/4 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=container-ci, secrets=['REGISTRY_USERNAME', 'REGISTRY_PASSWORD'], vars={}
  - ⚠️ setup: 未知 repo_fixture 'container-ci'，需确认测试仓前置资源
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['CONTAINER_PUBLIC_OK']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['CONTAINER_PRIVATE_OK']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['SHOULD_NOT_RUN']
  ✅ assert[3] type=negative target=run_status eval=deterministic
     → kind: `status`

### ✓ COMP-CONTERR-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['JOB_C_ALWAYS_EXECUTED', 'if: always(']

### ✓ COMP-CONTEXT-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['event_name/sha/ref/workspace/run_id/repository 等']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['CONTEXT_ATTRS_DUMPED']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ COMP-DAG-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['JOB_D_ALWAYS_EXECUTED', 'if: always(']
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['PARALLEL_1_DONE', 'PARALLEL_2_DONE']

### ✓ COMP-ENV-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['输出 step-value', 'step-value']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['TEST_VAR']
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ATOMGIT_WORKSPACE']

### ✓ COMP-EXPR-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['SUCCESS_CONTEXT_TRUE', 'ALWAYS_CONTEXT_TRUE']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['FAILED_CONTEXT_TRUE']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ COMP-EXPRFN-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['CONTAINS_WORKS', 'STARTSWITH_WORKS', 'ENDSWITH_WORKS']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['hello world', 'JSON']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ COMP-FILTER-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Trigger params: ['branch']
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['FILTER_MATCHED']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值

### ✓ COMP-MATIF-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ubuntu', 'MATRIX_OS', '日志含 MATRIX_OS=ubuntu']
  ✅ assert[1] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[2] type=positive target=run_status eval=deterministic
     → kind: `status`

### ✓ COMP-MATRIX-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 断言: 4/4 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['2*3']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ubuntu, 22']
  ✅ assert[3] type=positive target=run_status eval=deterministic
     → kind: `status`

### ◐ COMP-MATRIX-02-005 — partial_scriptable
- 维度: completeness | 优先级: P1
- 断言: 4/4 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=matrix-ci, secrets=[], vars={}
  - ⚠️ setup: 未知 repo_fixture 'matrix-ci'，需确认测试仓前置资源
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ubuntu-18、ubuntu-20、centos-18、centos-20 + alpine-latest']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['EXPERIMENTAL']
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['EXPERIMENTAL']
  ✅ assert[3] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['EXPERIMENTAL']

### ◐ COMP-MATRIX-02-006 — partial_scriptable
- 维度: completeness | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=matrix-ci, secrets=[], vars={}
  - ⚠️ setup: 未知 repo_fixture 'matrix-ci'，需确认测试仓前置资源
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ubuntu-18、ubuntu-20、centos-20、centos-22']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ◐ COMP-MATRIX-02-007 — partial_scriptable
- 维度: completeness | 优先级: P1
- 断言: 4/4 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=matrix-ci, secrets=[], vars={}
  - ⚠️ setup: 未知 repo_fixture 'matrix-ci'，需确认测试仓前置资源
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['DYNAMIC_RUNNER_OK']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['EXTRA']
  ✅ assert[2] type=negative target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[3] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['SHOULD_NOT_RUN']

### ✓ COMP-OUTPUT-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['OUTPUT_SET']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['NEEDS_OUTPUT']

### ◐ COMP-PARSE-02-001 — partial_scriptable
- 维度: completeness | 优先级: P1
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['YAML', 'WORKFLOW_PARSED_OK']
  🤖 assert[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMP-PERM-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['CLONE_OK']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['PUSH_REJECTED_AS_EXPECTED_READ_ONLY']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ COMP-POST-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['POST_CLEANUP_EXECUTED']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值

### ✓ COMP-RERUN-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 断言: 4/4 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['SUCCESS_JOB_DONE']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['FAIL_JOB_WILL_FAIL']
  ✅ assert[2] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[3] type=positive target=run_status eval=deterministic
     → kind: `status`

### ✓ COMP-RUNNER-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✗ COMP-SCHEDULE-02-001 — not_scriptable
- 维度: completeness | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=schedule, as=maintainer, supported=False
  - 🚫 trigger: schedule：cron 无法按需触发（基础设施限制）
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['SCHEDULE_TRIGGERED_OK']
  ✅ assert[1] type=nonfunctional target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['触发时间在 UTC 时区']
     ⚠️ 缺: nonfunctional 类型语义模糊
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ COMP-STAGES-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['prep-1/2']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['build-main 在 prep 之后']
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['PREP_1_DONE', 'PREP_2_DONE', 'BUILD_MAIN_DONE']

### ✓ COMP-TIMEOUT-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=nonfunctional target=run_status eval=deterministic
     → kind: `status`

### ✓ COMP-TRIGGER-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['TRIGGER_TEST_RUN_OK']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=positive target=run_status eval=deterministic
     → kind: `status`

### ✓ COMP-WF-CALL-02-001 — full_scriptable
- 维度: completeness | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['${{ inputs.input-a }} 为 value-from-caller', 'value-from-caller']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ COMPAT-ACTION-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['GITCODE_CHECKOUT_OK', 'GITCODE_SETUP_NODE_OK']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ◐ COMPAT-ACTION-INPUTS-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P2
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['INPUT_TEST_PARAM']
  🤖 assert[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMPAT-ART-CACHE-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ARTIFACT_COMPAT_VERIFIED']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ COMPAT-ARTIFACT-EQUIV-02-001 — full_scriptable
- 维度: compatibility | 优先级: P2
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=positive target=run_status eval=deterministic
     → kind: `status`

### ✓ COMPAT-CACHE-EQUIV-02-001 — full_scriptable
- 维度: compatibility | 优先级: P2
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['CACHE_HIT', 'CACHE_MISS']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['CACHE_HIT']

### ✓ COMPAT-CHECKOUT-EQUIV-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=positive target=run_status eval=deterministic
     → kind: `status`

### ✗ COMPAT-CONCUR-02-001 — not_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=manual, as=maintainer, supported=False
  - 🚫 trigger: manual 触发：需 workflow_dispatch API（待确认端点）
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['所有触发均产生可追踪的 run']

### ◐ COMPAT-CONCUR-MODEL-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=negative target=run_status eval=deterministic
     → kind: `status`
  🤖 assert[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMPAT-CONTEXT-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ATOMGIT_CONTEXT_DUMP_COMPLETE']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['包括 repository_owner 应可访问']

### ✓ COMPAT-CTX-AVAIL-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 4/4 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=['TEST_TOKEN'], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[3] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ COMPAT-DEF-SHELL-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 4/4 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['SHELL', 'SHELL 输出含 bash']
  ✅ assert[1] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[3] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['如 sh/dash']

### ◐ COMPAT-DEPRECATED-CMD-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P2
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  🤖 assert[1] type=nonfunctional target=run_logs eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMPAT-EXPRCO-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ COMPAT-EXPRCS-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['STARTSWITH_SENSITIVE_MATCH_UPPER']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['STARTSWITH_SENSITIVE_MISMATCH_LOWER', '小写不匹配，与 GitHub 有意不同']
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['CONTAINS_WORKS', 'contains 行为明确']

### ✓ COMPAT-EXPRFN-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['输出 Hello', 'Hello']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['输出 HelloGitCode', 'HelloGitCode']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ COMPAT-EXPRFN-02-002 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 5/5 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['RESULT']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['RESULT']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['RESULT']
  ✅ assert[3] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['RESULT']
  ✅ assert[4] type=nonfunctional target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['RESULT']
     ⚠️ 缺: nonfunctional 类型语义模糊

### ✓ COMPAT-EXPRFN-02-003 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 5/5 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['hello', 'RESULT', "'hello', 0, 7"]
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['aaa', 'a', 'b', 'RESULT', "'aaa', 'a', 'b'"]
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['JSON_NULL', 'JSON_TRUE', 'null', 'true']
  ✅ assert[3] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值
  ✅ assert[4] type=nonfunctional target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['JSON', 'atomgit.event']
     ⚠️ 缺: nonfunctional 类型语义模糊

### ✓ COMPAT-EXPRSYN-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['SUCCESS_CONDITION_TRUE', '${{ success }} 语义等价于 GitHub ${{ success(']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ALWAYS_CONDITION_TRUE', '${{ always }} 正确求值']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ◐ COMPAT-FLAVOR-LABEL-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P2
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  🤖 assert[1] type=nonfunctional target=run_logs eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMPAT-IN-TYPE-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=negative target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✗ COMPAT-INJECT-02-001 — not_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 4/4 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=pull_request, as=untrusted_contributor, supported=False
  - 🚫 trigger: pull_request：需建分支+开 PR（待确认 PR API）
  - 🚫 trigger: trigger.as=untrusted_contributor：需第二 GitCode 账号/token 模拟外部贡献者
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['; curl evil.com']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['whoami']
  ✅ assert[3] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ COMPAT-MATFF-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值

### ◐ COMPAT-MATRIX-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 6/6 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=matrix-compat, secrets=[], vars={}
  - ⚠️ setup: 未知 repo_fixture 'matrix-compat'，需确认测试仓前置资源
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ubuntu-18、ubuntu-20、centos-20 + alpine-edge']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['EXPERIMENTAL']
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[3] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值
  ✅ assert[4] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值
  ✅ assert[5] type=negative target=run_status eval=deterministic
     → kind: `status`

### ✓ COMPAT-MIGR-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['非 500/内部错误']

### ✓ COMPAT-MULTILINE-DELIM-02-001 — full_scriptable
- 维度: compatibility | 优先级: P2
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['MY_VAR', 'line1']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['PATH']

### ◐ COMPAT-NO-WIN-MAC-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=negative target=run_status eval=deterministic
     → kind: `status`
  🤖 assert[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMPAT-OUTPUT-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ATOMGIT_OUTPUT']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['version=1.2.3, status=stable']

### ◐ COMPAT-OUTPUT-LIMIT-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P2
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  🤖 assert[1] type=nonfunctional target=run_logs eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMPAT-PATHS-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Trigger params: ['changed_files_count']
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['PATHS_MATCHED_AND_TRIGGERED']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=positive target=run_status eval=deterministic
     → kind: `status`

### ✓ COMPAT-PERMS-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['CLONE_WITH_GC_PERMS_OK', 'PUSH_REJECTED_AS_EXPECTED']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ COMPAT-POST-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=negative target=run_status eval=deterministic
     → kind: `status`

### ✗ COMPAT-PR-COMM-02-001 — not_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=pull_request_comment, as=untrusted_contributor, supported=False
  - 🚫 trigger: pull_request_comment：需 PR comment API（未实现）
  - 🚫 trigger: trigger.as=untrusted_contributor：需第二 GitCode 账号/token 模拟外部贡献者
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✗ COMPAT-PR-TARGET-02-001 — not_scriptable
- 维度: compatibility | 优先级: P0
- 断言: 4/4 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=pull_request_target, as=untrusted_contributor, supported=False
  - 🚫 trigger: pull_request_target：同 PR + base 上下文语义
  - 🚫 trigger: trigger.as=untrusted_contributor：需第二 GitCode 账号/token 模拟外部贡献者
- Setup: fixture=with-secrets, secrets=['API_TOKEN'], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ATOMGIT_TOKEN']
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[3] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['YAML']

### ✗ COMPAT-PR-TYPES-02-001 — not_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=pr, as=maintainer, supported=False
- Trigger params: ['pr_action']
  - 🚫 trigger: pr 触发：需建分支+开 PR（待确认 PR API）
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['PR_TYPE_TRIGGERED_OK', 'open/update/reopen/merge']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['opened/synchronize/reopened']

### ✓ COMPAT-RECURSIVE-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=['TRIGGER_TOKEN'], vars={}
  ✅ assert[0] type=negative target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['TRIGGER_BLOCKED']

### ✓ COMPAT-RUN-CTX-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['RUNNER_CONTEXT_DUMPED']

### ✓ COMPAT-RUN-LBL-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['THREE_PART_LABEL_MATCHED']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ COMPAT-RUNNER-NAME-02-001 — full_scriptable
- 维度: compatibility | 优先级: P2
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ARCH']

### ✓ COMPAT-RUNSON-EQUIV-02-001 — full_scriptable
- 维度: compatibility | 优先级: P2
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ARRAY_FORM_OK']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['DEFAULT_FORM_OK']

### ◐ COMPAT-RUNSON-MIGR-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P0
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=negative target=run_status eval=deterministic
     → kind: `status`
  🤖 assert[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✗ COMPAT-SCHEDULE-02-001 — not_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=schedule, as=maintainer, supported=False
  - 🚫 trigger: schedule：cron 无法按需触发（基础设施限制）
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ATOMGIT_EVENT_NAME', 'schedule']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=negative target=run_status eval=deterministic
     → kind: `status`

### ✓ COMPAT-SECRET-M-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 4/4 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=with-secrets, secrets=['TEST_SECRET'], vars={}
  ✅ assert[0] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值
  ✅ assert[3] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ COMPAT-SETUP-STAR-02-001 — full_scriptable
- 维度: compatibility | 优先级: P2
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['v20']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值

### ✓ COMPAT-STAGE-FIELDS-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['PRE_BUILD', 'BUILD_DONE']
  ✅ assert[1] type=positive target=run_status eval=deterministic
     → kind: `status`

### ✓ COMPAT-STAGES-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=positive target=run_status eval=deterministic
     → kind: `status`

### ✓ COMPAT-STAGES-ORCH-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['BUILD_DONE', 'TEST_DONE']
  ✅ assert[1] type=positive target=run_status eval=deterministic
     → kind: `status`

### ◐ COMPAT-STAGES-SYNTAX-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P2
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  🤖 assert[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMPAT-SYSENV-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ATOMGIT_', 'ATOMGIT_SYSENV_DUMP_COMPLETE']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ATOMGIT_REPOSITORY_OWNER']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['GITHUB_TOKEN']

### ◐ COMPAT-SYSENV-MAP-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ATOMGIT_ENV']
  🤖 assert[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ COMPAT-TOOLCHAIN-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P2
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  🤖 assert[1] type=nonfunctional target=run_logs eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ COMPAT-UNKNOWN-TOP-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=negative target=run_status eval=deterministic
     → kind: `status`
  🤖 assert[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMPAT-UNSUPP-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['container.image / environment / services']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['BASIC_EXECUTION_OK']

### ◐ COMPAT-USES-REF-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  🤖 assert[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ COMPAT-USING-RUNTIME-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=negative target=run_status eval=deterministic
     → kind: `status`
  🤖 assert[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMPAT-VAR-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 5/5 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['RUNNER_OS', '如 Linux']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['RUNNER_ARCH', '如 X64']
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['RUNNER_NAME', 'RUNNER_TEMP', 'RUNNER_TOOL_CACHE', 'RUNNER_ENVIRONMENT']
  ✅ assert[3] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ATOMGIT_RUNNER_OS', 'ATOMGIT_RUNNER_ARCH', 'ATOMGIT_REPOSITORY_OWNER']
  ✅ assert[4] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['历史 TC-441/442/206 不应复现']

### ✓ COMPAT-VAR-02-002 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 4/4 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={'ENV_LEVEL': 'vars'}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ENV_LEVEL']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ENV_LEVEL', 'vars 不直接介入 shell 覆盖']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['历史 TC-533 不应复现']
  ✅ assert[3] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ COMPAT-VAR-02-003 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 4/4 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['RUNNER_OS']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ATOMGIT_SHA']
  ✅ assert[2] type=negative target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[3] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['RUNNER_OS']

### ✓ COMPAT-WF-CALL-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=['CALLEE_SECRET'], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=negative target=run_status eval=deterministic
     → kind: `status`

### ◐ COMPAT-WF-CMD-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P2
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  🤖 assert[1] type=nonfunctional target=run_ui eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ COMPAT-WF-NEST-02-001 — full_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=negative target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[2] type=negative target=run_status eval=deterministic
     → kind: `status`

### ◐ COMPAT-YAML-ERROR-02-001 — partial_scriptable
- 维度: compatibility | 优先级: P1
- 断言: 0/2 可映射, 2 无法映射, 2 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  🤖 assert[0] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定
  🤖 assert[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ REL-ART-CACHE-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ REL-CANCEL-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Trigger params: ['cancel_after_seconds']
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['CLEANUP_EXECUTED_AFTER_CANCEL']
  ✅ assert[2] type=negative target=run_status eval=deterministic
     → kind: `status`

### ✓ REL-CANCEL-02-002 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 4/4 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[2] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[3] type=negative target=run_status eval=deterministic
     → kind: `status`

### ✓ REL-CANCEL-02-003 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['Cleanup completed', "日志含 'Cleanup completed'"]
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ REL-CANCEL-02-004 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Trigger params: ['cancel_after_seconds']
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['POST_CLEANUP_MARKER']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值
  ✅ assert[2] type=nonfunctional target=run_status eval=deterministic
     → kind: `status`

### ◐ REL-CANCEL-02-005 — partial_scriptable
- 维度: reliability | 优先级: P1
- 断言: 3/4 可映射, 1 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Trigger params: ['cancel_after_seconds', 'poll_status_interval', 'poll_status_count', 'probe_runner_interval']
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=negative target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[2] type=negative target=run_status eval=deterministic
     → kind: `status`
  ❌ assert[3] type=nonfunctional target=runner_schedulable eval=deterministic
     🚫 target=runner_schedulable 不在引擎支持范围内

### ◐ REL-CHAOS-02-001 — partial_scriptable
- 维度: reliability | 优先级: P0
- 断言: 4/4 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  - 💥 fault_injection: fault_injection 非 null：当前执行器不支持故障注入（需 kill_runner / network_partition / concurrent_flood infra）
    detail: {'at': 'mid_job', 'action': 'kill_runner', 'params': {'delay_seconds': 10}, 'recovery_expectation': 'retry_and_succeed'}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[3] type=nonfunctional target=run_status eval=deterministic
     → kind: `status`

### ◐ REL-CHAOS-02-002 — partial_scriptable
- 维度: reliability | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  - 💥 fault_injection: fault_injection 非 null：当前执行器不支持故障注入（需 kill_runner / network_partition / concurrent_flood infra）
    detail: {'at': 'mid_job', 'action': 'network_partition', 'params': {'direction': 'outbound', 'duration_seconds': 60}, 'recovery_expectation': 'step_fails_then_recovers'}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['exit code 不等于 0']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=positive target=run_status eval=deterministic
     → kind: `status`

### ◐ REL-CHAOS-02-003 — partial_scriptable
- 维度: reliability | 优先级: P1
- 断言: 1/1 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  - 💥 fault_injection: fault_injection 非 null：当前执行器不支持故障注入（需 kill_runner / network_partition / concurrent_flood infra）
    detail: {'at': 'pre_job', 'action': 'kill_runner', 'params': {'delay_seconds': 5}, 'recovery_expectation': 'rerun_and_succeed'}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`

### ✓ REL-CONCUR-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 4/4 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Trigger params: ['simultaneous_pushes', 'window_seconds']
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[2] type=negative target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[3] type=nonfunctional target=run_status eval=deterministic
     → kind: `status`

### ✗ REL-CONCUR-02-002 — not_scriptable
- 维度: reliability | 优先级: P1
- 断言: 4/4 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=manual, as=maintainer, supported=False
- Trigger params: ['simultaneous_runs']
  - 🚫 trigger: manual 触发：需 workflow_dispatch API（待确认端点）
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[2] type=negative target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[3] type=nonfunctional target=run_status eval=deterministic
     → kind: `status`

### ✗ REL-CONCUR-02-003 — not_scriptable
- 维度: reliability | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=manual, as=maintainer, supported=False
- Trigger params: ['stagger_seconds']
  - 🚫 trigger: manual 触发：需 workflow_dispatch API（待确认端点）
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[2] type=negative target=run_status eval=deterministic
     → kind: `status`

### ◐ REL-CONCUR-02-004 — partial_scriptable
- 维度: reliability | 优先级: P1
- 断言: 1/1 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  - 💥 fault_injection: fault_injection 非 null：当前执行器不支持故障注入（需 kill_runner / network_partition / concurrent_flood infra）
    detail: {'at': 'pre_job', 'action': 'concurrent_flood', 'params': {'concurrency': 2}, 'recovery_expectation': 'second_run_ignored'}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`

### ✓ REL-CONTERR-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['JOB_C_ALWAYS_EXECUTED', 'if: always(']

### ✗ REL-CONV-02-001 — not_scriptable
- 维度: reliability | 优先级: P1
- 断言: 4/5 可映射, 1 无法映射, 0 需 LLM
- Trigger: event=schedule, as=maintainer, supported=False
- Trigger params: ['observation_window_minutes', 'cancel_after_seconds', 'runner_release_probe']
  - 🚫 trigger: schedule：cron 无法按需触发（基础设施限制）
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['CLEANUP_DONE']
  ✅ assert[3] type=negative target=run_status eval=deterministic
     → kind: `status`
  ❌ assert[4] type=positive target=runner_scheduling eval=deterministic
     🚫 target=runner_scheduling 不在引擎支持范围内

### ✗ REL-CRON-02-001 — not_scriptable
- 维度: reliability | 优先级: P1
- 断言: 3/4 可映射, 1 无法映射, 0 需 LLM
- Trigger: event=schedule, as=maintainer, supported=False
- Trigger params: ['observation_window_minutes', 'cron_operators_under_test']
  - 🚫 trigger: schedule：cron 无法按需触发（基础设施限制）
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=negative target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值
  ❌ assert[3] type=positive target=workflow_validation eval=deterministic
     🚫 target=workflow_validation 不在引擎支持范围内

### ◐ REL-LARGE-REPO-02-001 — partial_scriptable
- 维度: reliability | 优先级: P2
- 断言: 1/2 可映射, 1 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=large-repo, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ❌ assert[1] type=nonfunctional target=run_duration eval=deterministic
     🚫 target=run_duration 不在引擎支持范围内

### ◐ REL-MANY-STEPS-02-001 — partial_scriptable
- 维度: reliability | 优先级: P2
- 断言: 1/2 可映射, 1 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ❌ assert[1] type=nonfunctional target=run_duration eval=deterministic
     🚫 target=run_duration 不在引擎支持范围内

### ✓ REL-MATRIX-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 4/4 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['任务初始化错误']
  ✅ assert[3] type=nonfunctional target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: nonfunctional 类型语义模糊

### ✓ REL-MATRIX-02-002 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['4 基础 + 3 include - 1 exclude']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ REL-MATRIX-02-003 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=negative target=run_status eval=deterministic
     → kind: `status`

### ✓ REL-MATRIX-02-004 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[2] type=negative target=run_status eval=deterministic
     → kind: `status`

### ✓ REL-NEEDS-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['JOB_D_ALWAYS_EXECUTED', 'if: always(']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ REL-NEEDS-02-002 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ALL_PARENT_INSTANCES_DONE', '等待全部 matrix 实例完成']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['任务初始化错误']

### ✓ REL-NEEDS-02-003 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['任务初始化错误']

### ◐ REL-PREEMPT-02-001 — partial_scriptable
- 维度: reliability | 优先级: P1
- 断言: 4/4 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Trigger params: ['preemption_scenarios', 'stagger_seconds']
- Setup: fixture=preemption-ci, secrets=[], vars={}
  - ⚠️ setup: 未知 repo_fixture 'preemption-ci'，需确认测试仓前置资源
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=negative target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[2] type=negative target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[3] type=nonfunctional target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: nonfunctional 类型语义模糊

### ◐ REL-PREEMPT-02-002 — partial_scriptable
- 维度: reliability | 优先级: P1
- 断言: 5/6 可映射, 1 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Trigger params: ['preempt_after_seconds', 'probe_runner_interval']
- Setup: fixture=preemption-ci, secrets=[], vars={}
  - ⚠️ setup: 未知 repo_fixture 'preemption-ci'，需确认测试仓前置资源
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['TICK_30', '如 TICK_30']
  ✅ assert[2] type=negative target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[3] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值
  ✅ assert[4] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值
  ❌ assert[5] type=nonfunctional target=runner_schedulable eval=deterministic
     🚫 target=runner_schedulable 不在引擎支持范围内

### ✓ REL-PUSH-DEDUP-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Trigger params: ['simultaneous_pushes', 'window_seconds']
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=negative target=run_status eval=deterministic
     → kind: `status`

### ◐ REL-RACE-02-001 — partial_scriptable
- 维度: reliability | 优先级: P1
- 断言: 1/1 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  - 💥 fault_injection: fault_injection 非 null：当前执行器不支持故障注入（需 kill_runner / network_partition / concurrent_flood infra）
    detail: {'at': 'pre_job', 'action': 'concurrent_flood', 'params': {'concurrency': 2}, 'recovery_expectation': 'no_deadlock'}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`

### ✓ REL-RERUN-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[2] type=positive target=run_status eval=deterministic
     → kind: `status`

### ✓ REL-RERUN-02-002 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[2] type=negative target=run_status eval=deterministic
     → kind: `status`

### ✓ REL-RERUN-02-003 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ATOMGIT_RUN_ID']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ATOMGIT_RUN_NUMBER']
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ATOMGIT_SHA']

### ✓ REL-RUNNER-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[2] type=negative target=run_status eval=deterministic
     → kind: `status`

### ✓ REL-RUNNER-02-002 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['No space left', 'disk quota exceeded']
  ✅ assert[2] type=negative target=run_status eval=deterministic
     → kind: `status`

### ✓ REL-RUNNER-02-003 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['JOB_A_ENV']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ REL-RUNNER-RESIDUE-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['NO_RESIDUE']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['RESIDUE_FOUND']

### ✗ REL-SCHED-02-001 — not_scriptable
- 维度: reliability | 优先级: P1
- 断言: 3/4 可映射, 1 无法映射, 0 需 LLM
- Trigger: event=schedule, as=maintainer, supported=False
- Trigger params: ['observation_window_minutes', 'baseline_cron', 'high_frequency_crons']
  - 🚫 trigger: schedule：cron 无法按需触发（基础设施限制）
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=negative target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ❌ assert[3] type=positive target=workflow_validation eval=deterministic
     🚫 target=workflow_validation 不在引擎支持范围内

### ✓ REL-TIMEOUT-02-001 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=nonfunctional target=run_status eval=deterministic
     → kind: `status`

### ✓ REL-TIMEOUT-02-002 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[2] type=negative target=run_status eval=deterministic
     → kind: `status`

### ✓ REL-TIMEOUT-02-003 — full_scriptable
- 维度: reliability | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ SEC-ACTION-PERM-02-001 — full_scriptable
- 维度: security | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=with-secrets, secrets=['TEST_SECRET'], vars={}
  ✅ assert[0] type=negative target=run_logs eval=
     → kind: `mask`
     ⚠️ 缺: secret_value: TEST_SECRET 的实际可见明文
  ✅ assert[1] type=positive target=run_status eval=deterministic
     → kind: `status`

### ✓ SEC-CACHE-ISOLATE-02-001 — full_scriptable
- 维度: security | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Trigger params: ['cross_repo_check']
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['CACHE_HIT']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['REPO_A_SECRET_DATA']

### ✓ SEC-CONT-CRED-02-001 — full_scriptable
- 维度: security | 优先级: P1
- 断言: 4/4 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=private-registry, secrets=['REGISTRY_USERNAME', 'REGISTRY_PASSWORD'], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['CONTAINER_STEP_EXECUTED']
  ✅ assert[1] type=negative target=run_logs eval=
     → kind: `mask`
     ⚠️ 缺: secret_value: REGISTRY_USERNAME 的实际可见明文
  ✅ assert[2] type=negative target=run_logs eval=
     → kind: `mask`
     ⚠️ 缺: secret_value: REGISTRY_PASSWORD 的实际可见明文
  ✅ assert[3] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ◐ SEC-CONT-ISOLATE-02-001 — partial_scriptable
- 维度: security | 优先级: P1
- 断言: 4/4 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=container-isolation, secrets=['HOST_SECRET_MARKER'], vars={}
  - ⚠️ setup: 未知 repo_fixture 'container-isolation'，需确认测试仓前置资源
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['EXPLICIT_VAR_OK']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['HOST_SECRET_LEAKED']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['HOST_PATH_ACCESSIBLE']
  ✅ assert[3] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['HOST_SECRET_ISOLATED', 'HOST_PATH_ISOLATED']

### ✓ SEC-DISK-LEAK-02-001 — full_scriptable
- 维度: security | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=with-secrets, secrets=['DISK_TEST_SECRET'], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['DISK_NO_LEAK']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['DISK_LEAK_FOUND']

### ✗ SEC-ENV-POLLUTE-02-001 — not_scriptable
- 维度: security | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=pr, as=untrusted_contributor, supported=False
- Trigger params: ['pr_title_injection']
  - 🚫 trigger: pr 触发：需建分支+开 PR（待确认 PR API）
  - 🚫 trigger: trigger.as=untrusted_contributor：需第二 GitCode 账号/token 模拟外部贡献者
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值
  ✅ assert[1] type=positive target=run_status eval=deterministic
     → kind: `status`

### ✓ SEC-ENV-REVIEW-02-001 — full_scriptable
- 维度: security | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=with-secrets, secrets=['ENV_SECRET'], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=negative target=run_logs eval=
     → kind: `mask`
     ⚠️ 缺: secret_value: ENV_SECRET 的实际可见明文

### ✓ SEC-ENV-WAIT-02-001 — full_scriptable
- 维度: security | 优先级: P1
- 断言: 4/4 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Trigger params: ['observe_wait_timer']
- Setup: fixture=environment-protected, secrets=['DEPLOY_TOKEN'], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ENV_SECRET_ACCESSED']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['ENV_SECRET_ACCESSED', 'job 未提前执行']
  ✅ assert[2] type=negative target=run_logs eval=
     → kind: `mask`
     ⚠️ 缺: secret_value: DEPLOY_TOKEN 的实际可见明文
  ✅ assert[3] type=nonfunctional target=run_status eval=deterministic
     → kind: `status`

### ✗ SEC-FORK-02-001 — not_scriptable
- 维度: security | 优先级: P0
- 断言: 5/5 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=fork_pr, as=untrusted_contributor, supported=False
- Trigger params: ['event_type']
  - 🚫 trigger: fork_pr：需第二 GitCode 账号/token 模拟 untrusted 外部贡献者
  - 🚫 trigger: trigger.as=untrusted_contributor：需第二 GitCode 账号/token 模拟外部贡献者
- Setup: fixture=with-secrets, secrets=['DEPLOY_TOKEN'], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['PUSH_REJECTED_AS_EXPECTED']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['SECRET_EMPTY_AS_EXPECTED']
  ✅ assert[2] type=negative target=run_logs eval=
     → kind: `mask`
     ⚠️ 缺: secret_value: DEPLOY_TOKEN 的实际可见明文
  ✅ assert[3] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['PUSH_SUCCEEDED_UNEXPECTEDLY']
  ✅ assert[4] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['SECRET_NOT_EMPTY_UNEXPECTED']

### ✗ SEC-FORK-02-002 — not_scriptable
- 维度: security | 优先级: P0
- 断言: 5/5 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=fork_pr, as=untrusted_contributor, supported=False
  - 🚫 trigger: fork_pr：需第二 GitCode 账号/token 模拟 untrusted 外部贡献者
  - 🚫 trigger: trigger.as=untrusted_contributor：需第二 GitCode 账号/token 模拟外部贡献者
- Setup: fixture=with-secrets, secrets=['DEPLOY_KEY', 'ORG_TOKEN'], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['PROJECT_SECRET_EMPTY_AS_EXPECTED']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ORG_SECRET_EMPTY_AS_EXPECTED']
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['API_AUTH_REJECTED_AS_EXPECTED']
  ✅ assert[3] type=negative target=run_logs eval=
     → kind: `mask`
     ⚠️ 缺: secret_value: DEPLOY_KEY 的实际可见明文
  ✅ assert[4] type=negative target=run_logs eval=
     → kind: `mask`
     ⚠️ 缺: secret_value: ORG_TOKEN 的实际可见明文

### ✗ SEC-FORK-02-003 — not_scriptable
- 维度: security | 优先级: P0
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=fork_pr, as=untrusted_contributor, supported=False
- Trigger params: ['fork_has_modified_yaml']
  - 🚫 trigger: fork_pr：需第二 GitCode 账号/token 模拟 untrusted 外部贡献者
  - 🚫 trigger: trigger.as=untrusted_contributor：需第二 GitCode 账号/token 模拟外部贡献者
- Setup: fixture=with-target-workflow, secrets=[], vars={}
  - ⚠️ setup: 未知 repo_fixture 'with-target-workflow'，需确认测试仓前置资源
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['BASE_BRANCH_WORKFLOW_EXECUTED']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['FORK_CODE_EXECUTED']
  ✅ assert[2] type=positive target=run_status eval=deterministic
     → kind: `status`

### ✗ SEC-FORK-02-004 — not_scriptable
- 维度: security | 优先级: P0
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=fork_pr, as=untrusted_contributor, supported=False
- Trigger params: ['event_type']
  - 🚫 trigger: fork_pr：需第二 GitCode 账号/token 模拟 untrusted 外部贡献者
  - 🚫 trigger: trigger.as=untrusted_contributor：需第二 GitCode 账号/token 模拟外部贡献者
- Setup: fixture=with-secrets, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['MAKE_BUILD_EXECUTED', '显式 checkout head.sha 后可执行 fork 侧代码']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✗ SEC-FORK-02-005 — not_scriptable
- 维度: security | 优先级: P0
- 断言: 4/4 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=fork_pr, as=untrusted_contributor, supported=False
- Trigger params: ['event_type']
  - 🚫 trigger: fork_pr：需第二 GitCode 账号/token 模拟 untrusted 外部贡献者
  - 🚫 trigger: trigger.as=untrusted_contributor：需第二 GitCode 账号/token 模拟外部贡献者
- Setup: fixture=with-secrets, secrets=[], vars={}
  ✅ assert[0] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['PUSH_SUCCEEDED_UNEXPECTEDLY']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['PUSH_REJECTED_AS_EXPECTED']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['API_NOT_REJECTED_UNEXPECTED']
  ✅ assert[3] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['API_REJECTED_403_AS_EXPECTED']

### ✗ SEC-INJECT-02-001 — not_scriptable
- 维度: security | 优先级: P0
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=fork_pr, as=untrusted_contributor, supported=False
- Trigger params: ['pr_title_contains_injection']
  - 🚫 trigger: fork_pr：需第二 GitCode 账号/token 模拟 untrusted 外部贡献者
  - 🚫 trigger: trigger.as=untrusted_contributor：需第二 GitCode 账号/token 模拟外部贡献者
- Setup: fixture=with-pr-trigger, secrets=[], vars={}
  - ⚠️ setup: 未知 repo_fixture 'with-pr-trigger'，需确认测试仓前置资源
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['NO_INJECTION_AS_EXPECTED']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['INJECTION_SUCCEEDED_UNEXPECTEDLY']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✗ SEC-INJECT-02-002 — not_scriptable
- 维度: security | 优先级: P0
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=fork_pr, as=untrusted_contributor, supported=False
- Trigger params: ['pr_body_contains_injection']
  - 🚫 trigger: fork_pr：需第二 GitCode 账号/token 模拟 untrusted 外部贡献者
  - 🚫 trigger: trigger.as=untrusted_contributor：需第二 GitCode 账号/token 模拟外部贡献者
- Setup: fixture=with-pr-trigger, secrets=[], vars={}
  - ⚠️ setup: 未知 repo_fixture 'with-pr-trigger'，需确认测试仓前置资源
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['NO_INJECTION_AS_EXPECTED']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['INJECTION_SUCCEEDED_UNEXPECTEDLY']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✗ SEC-INJECT-02-003 — not_scriptable
- 维度: security | 优先级: P0
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=fork_pr, as=untrusted_contributor, supported=False
- Trigger params: ['branch_name_contains_injection']
  - 🚫 trigger: fork_pr：需第二 GitCode 账号/token 模拟 untrusted 外部贡献者
  - 🚫 trigger: trigger.as=untrusted_contributor：需第二 GitCode 账号/token 模拟外部贡献者
- Setup: fixture=with-pr-trigger, secrets=[], vars={}
  - ⚠️ setup: 未知 repo_fixture 'with-pr-trigger'，需确认测试仓前置资源
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['NO_INJECTION_AS_EXPECTED']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['INJECTION_SUCCEEDED_UNEXPECTEDLY']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✗ SEC-INJECT-02-004 — not_scriptable
- 维度: security | 优先级: P0
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=fork_pr, as=untrusted_contributor, supported=False
- Trigger params: ['commit_message_contains_injection']
  - 🚫 trigger: fork_pr：需第二 GitCode 账号/token 模拟 untrusted 外部贡献者
  - 🚫 trigger: trigger.as=untrusted_contributor：需第二 GitCode 账号/token 模拟外部贡献者
- Setup: fixture=with-pr-trigger, secrets=[], vars={}
  - ⚠️ setup: 未知 repo_fixture 'with-pr-trigger'，需确认测试仓前置资源
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['NO_INJECTION_AS_EXPECTED']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['INJECTION_SUCCEEDED_UNEXPECTEDLY']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✗ SEC-INJECT-02-005 — not_scriptable
- 维度: security | 优先级: P0
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=fork_pr, as=untrusted_contributor, supported=False
- Trigger params: ['pr_title_is_malicious']
  - 🚫 trigger: fork_pr：需第二 GitCode 账号/token 模拟 untrusted 外部贡献者
  - 🚫 trigger: trigger.as=untrusted_contributor：需第二 GitCode 账号/token 模拟外部贡献者
- Setup: fixture=with-pr-trigger, secrets=[], vars={}
  - ⚠️ setup: 未知 repo_fixture 'with-pr-trigger'，需确认测试仓前置资源
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['PR_TITLE']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值
  ✅ assert[2] type=positive target=run_status eval=deterministic
     → kind: `status`

### ✗ SEC-INJECT-02-006 — not_scriptable
- 维度: security | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=fork_pr, as=untrusted_contributor, supported=False
- Trigger params: ['pr_title_contains_metacharacters']
  - 🚫 trigger: fork_pr：需第二 GitCode 账号/token 模拟 untrusted 外部贡献者
  - 🚫 trigger: trigger.as=untrusted_contributor：需第二 GitCode 账号/token 模拟外部贡献者
- Setup: fixture=with-pr-trigger, secrets=[], vars={}
  - ⚠️ setup: 未知 repo_fixture 'with-pr-trigger'，需确认测试仓前置资源
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['SAFE_ENV_REFERENCE_OK']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ SEC-JOB-ISOLATE-02-001 — full_scriptable
- 维度: security | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ISOLATION_INTACT']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['ISOLATION_BROKEN']

### ◐ SEC-PERMS-02-001 — partial_scriptable
- 维度: security | 优先级: P0
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=with-permissions, secrets=[], vars={}
  - ⚠️ setup: 未知 repo_fixture 'with-permissions'，需确认测试仓前置资源
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['PUSH_REJECTED_AS_EXPECTED']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['PUSH_SUCCEEDED_UNEXPECTEDLY']

### ✓ SEC-PERMS-02-002 — full_scriptable
- 维度: security | 优先级: P0
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Trigger params: ['repo_default_permission']
- Setup: fixture=with-secrets, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['PUSH_REJECTED_BY_DEFAULT_PERMS']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['PUSH_ALLOWED_BY_DEFAULT_PERMS']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ SEC-PERMS-02-003 — full_scriptable
- 维度: security | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['JOB_A_OVERRIDE_CLONE_OK']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['JOB_B_PR_NONE_OK']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ◐ SEC-REFPROT-02-001 — partial_scriptable
- 维度: security | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Trigger params: ['branches']
- Setup: fixture=branch-protected, secrets=[], vars={}
  - ⚠️ setup: 未知 repo_fixture 'branch-protected'，需确认测试仓前置资源
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['REF_PROTECTED', 'DEPLOY_STEP_EXECUTED']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['DEPLOY_STEP_EXECUTED']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ SEC-RUNNER-LEAK-02-001 — full_scriptable
- 维度: security | 优先级: P0
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=with-secrets, secrets=['LEAK_TEST_SECRET'], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['NO_LEAK_AS_EXPECTED']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     → 候选值: ['LEAK_FOUND_UNEXPECTED']
  ✅ assert[2] type=negative target=run_logs eval=
     → kind: `mask`
     ⚠️ 缺: secret_value: LEAK_TEST_SECRET 的实际可见明文

### ✓ SEC-RUNNER-SHARE-02-001 — full_scriptable
- 维度: security | 优先级: P0
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Trigger params: ['cross_project']
- Setup: fixture=with-secrets, secrets=['SECRET_A'], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['SECRET_EMPTY_AS_EXPECTED']
  ✅ assert[1] type=negative target=run_logs eval=
     → kind: `mask`
     ⚠️ 缺: secret_value: SECRET_A 的实际可见明文

### ✓ SEC-SECRET-MASK-02-001 — full_scriptable
- 维度: security | 优先级: P0
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=with-secrets, secrets=['TEST_SECRET'], vars={}
  ✅ assert[0] type=negative target=run_logs eval=
     → kind: `mask`
     ⚠️ 缺: secret_value: TEST_SECRET 的实际可见明文
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['This is normal text visible in logs']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ◐ SEC-SECRET-MASK-02-002-V1 — partial_scriptable
- 维度: security | 优先级: P0
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=with-secrets, secrets=['SPLIT_SECRET'], vars={}
  ✅ assert[0] type=negative target=run_logs eval=
     → kind: `mask`
     ⚠️ 缺: secret_value: SPLIT_SECRET 的实际可见明文
  🤖 assert[1] type=nonfunctional target=run_logs eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ SEC-SECRET-MASK-02-002-V2 — partial_scriptable
- 维度: security | 优先级: P1
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=with-secrets, secrets=['MULTILINE_SECRET'], vars={}
  ✅ assert[0] type=negative target=run_logs eval=
     → kind: `mask`
     ⚠️ 缺: secret_value: MULTILINE_SECRET 的实际可见明文
  🤖 assert[1] type=nonfunctional target=run_logs eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ SEC-SECRET-MASK-02-002 — partial_scriptable
- 维度: security | 优先级: P1
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=with-secrets, secrets=['TEST_SECRET'], vars={}
  ✅ assert[0] type=negative target=run_logs eval=
     → kind: `mask`
     ⚠️ 缺: secret_value: TEST_SECRET 的实际可见明文
  🤖 assert[1] type=nonfunctional target=run_logs eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ SEC-SECRET-MASK-02-003 — full_scriptable
- 维度: security | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=with-secrets, secrets=['COMPOUND_SECRET'], vars={}
  ✅ assert[0] type=negative target=run_logs eval=
     → kind: `mask`
     ⚠️ 缺: secret_value: COMPOUND_SECRET 的实际可见明文
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ SEC-SECRET-MASK-02-004 — full_scriptable
- 维度: security | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=with-secrets, secrets=['MULTILINE_SECRET'], vars={}
  ✅ assert[0] type=negative target=run_logs eval=
     → kind: `mask`
     ⚠️ 缺: secret_value: MULTILINE_SECRET 的实际可见明文
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ SEC-SECRET-MASK-02-005 — full_scriptable
- 维度: security | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ADD_MASK_TEST_DONE', 'MASK_ISOLATION_TEST_DONE']
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✓ SEC-SHA-REF-02-001 — full_scriptable
- 维度: security | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ◐ SEC-SIDECHAN-02-001 — partial_scriptable
- 维度: security | 优先级: P1
- 断言: 1/3 可映射, 2 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=with-secrets, secrets=['SIDECHAN_SECRET'], vars={}
  ✅ assert[0] type=negative target=run_logs eval=
     → kind: `mask`
     ⚠️ 缺: secret_value: SIDECHAN_SECRET 的实际可见明文
  ❌ assert[1] type=negative target=step_summary eval=deterministic
     🚫 target=step_summary 不在引擎支持范围内
  ❌ assert[2] type=negative target=artifacts eval=deterministic
     🚫 target=artifacts 不在引擎支持范围内

### ◐ SEC-SUPPLY-02-001 — partial_scriptable
- 维度: security | 优先级: P1
- 断言: 2/3 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['SHA_PINNED_ACTION_WORKS']
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值
  🤖 assert[2] type=nonfunctional target=run_logs eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✗ SEC-SUPPLY-02-002 — not_scriptable
- 维度: security | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=fork_pr, as=untrusted_contributor, supported=False
  - 🚫 trigger: fork_pr：需第二 GitCode 账号/token 模拟 untrusted 外部贡献者
  - 🚫 trigger: trigger.as=untrusted_contributor：需第二 GitCode 账号/token 模拟外部贡献者
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ✗ SEC-TOCTOU-02-001 — not_scriptable
- 维度: security | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=pr, as=maintainer, supported=False
  - 🚫 trigger: pr 触发：需建分支+开 PR（待确认 PR API）
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=negative target=run_status eval=deterministic
     → kind: `status`

### ✗ SEC-TOKEN-02-001 — not_scriptable
- 维度: security | 优先级: P0
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=fork_pr, as=untrusted_contributor, supported=False
- Trigger params: ['event_type']
  - 🚫 trigger: fork_pr：需第二 GitCode 账号/token 模拟 untrusted 外部贡献者
  - 🚫 trigger: trigger.as=untrusted_contributor：需第二 GitCode 账号/token 模拟外部贡献者
- Setup: fixture=with-secrets, secrets=[], vars={}
  ✅ assert[0] type=negative target=run_logs eval=
     → kind: `mask`
     ⚠️ 缺: secret_value: atomgit_token 的实际可见明文
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值

### ✓ SEC-TOKEN-EXPIRE-02-001 — full_scriptable
- 维度: security | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=['TOKEN_TEST_SECRET'], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=negative target=run_logs eval=
     → kind: `mask`
     ⚠️ 缺: secret_value: TOKEN_TEST_SECRET 的实际可见明文

### ◐ USE-BADGE-02-001 — partial_scriptable
- 维度: usability | 优先级: P2
- 断言: 0/4 可映射, 4 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Trigger params: ['badge_url_template', 'observe_refresh']
- Setup: fixture=basic-ci, secrets=[], vars={}
  ❌ assert[0] type=positive target=badge_response eval=deterministic
     🚫 target=badge_response 不在引擎支持范围内
  ❌ assert[1] type=negative target=badge_response eval=deterministic
     🚫 target=badge_response 不在引擎支持范围内
  ❌ assert[2] type=nonfunctional target=badge_response eval=deterministic
     🚫 target=badge_response 不在引擎支持范围内
  🤖 assert[3] type=nonfunctional target=documentation eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ USE-DEBUG-02-001 — full_scriptable
- 维度: usability | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值
  ✅ assert[2] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['GROUP_FOLD_TEST_DONE']

### ◐ USE-DEBUG-02-002 — partial_scriptable
- 维度: usability | 优先级: P2
- 断言: 0/1 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  🤖 assert[0] type=nonfunctional target=run_status eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ USE-DEBUG-02-003 — full_scriptable
- 维度: usability | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ATOMGIT_']
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ATOMGIT_REPOSITORY', 'ATOMGIT_ACTOR']

### ◐ USE-DEBUG-02-004 — partial_scriptable
- 维度: usability | 优先级: P2
- 断言: 0/1 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  🤖 assert[0] type=nonfunctional target=run_status eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ USE-DOC-02-001 — full_scriptable
- 维度: usability | 优先级: P2
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=negative target=run_logs eval=deterministic
     → kind: `leak`
     ⚠️ 缺: 无法从 rubric 提取具体 forbidden 值

### ◐ USE-DOC-02-002 — partial_scriptable
- 维度: usability | 优先级: P1
- 断言: 0/1 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  🤖 assert[0] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ USE-DOC-02-003 — full_scriptable
- 维度: usability | 优先级: P1
- 断言: 2/2 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[1] type=negative target=run_logs eval=determistic
     → kind: `leak`
     → 候选值: ['FAIL']

### ◐ USE-ERR-MSG-02-001 — partial_scriptable
- 维度: usability | 优先级: P1
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['WORKFLOW_PARSED']
  🤖 assert[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✗ USE-ERR-MSG-02-002 — not_scriptable
- 维度: usability | 优先级: P1
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=pr, as=maintainer, supported=False
- Trigger params: ['pr_action']
  - 🚫 trigger: pr 触发：需建分支+开 PR（待确认 PR API）
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['PR_TYPE_VALID_VALUES_WORK']
  🤖 assert[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ USE-ERR-MSG-02-003 — partial_scriptable
- 维度: usability | 优先级: P1
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['ATOMGIT_CONTEXT_WORKS']
  🤖 assert[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ USE-ERR-MSG-02-004 — partial_scriptable
- 维度: usability | 优先级: P1
- 断言: 0/1 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  🤖 assert[0] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ USE-ERR-MSG-02-005 — partial_scriptable
- 维度: usability | 优先级: P1
- 断言: 0/1 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  🤖 assert[0] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ USE-ERR-MSG-02-006 — partial_scriptable
- 维度: usability | 优先级: P1
- 断言: 0/1 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  🤖 assert[0] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✗ USE-INPUTS-DEFAULT-02-001 — not_scriptable
- 维度: usability | 优先级: P2
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=manual, as=maintainer, supported=False
- Trigger params: ['skip_inputs']
  - 🚫 trigger: manual 触发：需 workflow_dispatch API（待确认端点）
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['INPUT_VAL']
  🤖 assert[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ USE-MIGR-02-001 — partial_scriptable
- 维度: usability | 优先级: P1
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['GITCODE_FORMAT_WORKS']
  🤖 assert[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ USE-MIGR-02-002 — partial_scriptable
- 维度: usability | 优先级: P1
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_logs eval=deterministic
     → kind: `value`
     → 候选值: ['GITCODE_RUNS_ON_WORKS']
  🤖 assert[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ USE-MIGR-02-003 — partial_scriptable
- 维度: usability | 优先级: P0
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=with-permissions, secrets=[], vars={}
  - ⚠️ setup: 未知 repo_fixture 'with-permissions'，需确认测试仓前置资源
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  🤖 assert[1] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ USE-MIGR-02-004 — partial_scriptable
- 维度: usability | 优先级: P1
- 断言: 0/1 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  🤖 assert[0] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ USE-MIGR-02-005 — partial_scriptable
- 维度: usability | 优先级: P1
- 断言: 0/1 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  🤖 assert[0] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ USE-MIGR-02-006 — partial_scriptable
- 维度: usability | 优先级: P1
- 断言: 0/1 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  🤖 assert[0] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ USE-NEST-02-001 — partial_scriptable
- 维度: usability | 优先级: P2
- 断言: 0/1 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  🤖 assert[0] type=nonfunctional target=error_message eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✗ USE-PR-CHECKS-02-001 — not_scriptable
- 维度: usability | 优先级: P2
- 断言: 0/2 可映射, 2 无法映射, 1 需 LLM
- Trigger: event=pr, as=maintainer, supported=False
  - 🚫 trigger: pr 触发：需建分支+开 PR（待确认 PR API）
- Setup: fixture=basic-ci, secrets=[], vars={}
  ❌ assert[0] type=positive target=pr_ui eval=deterministic
     🚫 target=pr_ui 不在引擎支持范围内
  🤖 assert[1] type=nonfunctional target=pr_ui eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ USE-QUEUE-02-001 — partial_scriptable
- 维度: usability | 优先级: P2
- 断言: 1/2 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Trigger params: ['consecutive']
- Setup: fixture=clean, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=
     → kind: `run_status`
  🤖 assert[1] type=nonfunctional target=queue_ui eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ✓ USE-RERUN-02-001 — full_scriptable
- 维度: usability | 优先级: P1
- 断言: 3/3 可映射, 0 无法映射, 0 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ✅ assert[0] type=positive target=run_status eval=deterministic
     → kind: `status`
  ✅ assert[1] type=positive target=run_logs eval=deterministic
     → kind: `value`
     ⚠️ 缺: 无法从 rubric 提取具体 expect 值
  ✅ assert[2] type=negative target=run_status eval=deterministic
     → kind: `status`

### ◐ USE-RERUN-02-002 — partial_scriptable
- 维度: usability | 优先级: P2
- 断言: 0/1 可映射, 1 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  🤖 assert[0] type=nonfunctional target=run_status eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定

### ◐ USE-SUMMARY-02-001 — partial_scriptable
- 维度: usability | 优先级: P2
- 断言: 0/4 可映射, 4 无法映射, 1 需 LLM
- Trigger: event=push, as=maintainer, supported=True
- Setup: fixture=basic-ci, secrets=[], vars={}
  ❌ assert[0] type=positive target=run_ui eval=deterministic
     🚫 target=run_ui 不在引擎支持范围内
  ❌ assert[1] type=negative target=run_ui eval=deterministic
     🚫 target=run_ui 不在引擎支持范围内
  ❌ assert[2] type=nonfunctional target=run_ui eval=deterministic
     🚫 target=run_ui 不在引擎支持范围内
  🤖 assert[3] type=nonfunctional target=run_ui eval=llm_assisted
     🚫 eval=llm_assisted, 需要 LLM 判定
