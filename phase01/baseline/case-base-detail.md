# Case Base Detail · 629 TCs Evaluation

> 对 `phase01/inputs/existing-cases/cases.md` 中 629 条测试用例 (TC-001 ~ TC-629) + 22 条问题记录的一次性全集评估。
> 评估日期: 2026-07-20
> 本文件是后续所有 `/phase01-gen` run 的加速器——case-writer 不再每次重新评估 629 条。

## Summary

| Disposition | Count |
|---|---|
| KEEP | 260 |
| DEPRECATE | 307 |
| NEEDS-UPDATE | 62 |

> Note: Total = 260 + 307 + 62 = 629. NEEDS-UPDATE numbers include duplicate FAIL root causes — after root-cause dedup, 25 distinct bug categories.

## Evaluation Criteria Applied

- **KEEP**: FAIL (known bug to track) | PASS with A/B testability AND independent verification value
- **DEPRECATE**: D 测不动 | SKIP with permanent reason | C 难真测 + PASS + SKIP | 用例不当 | LOW value + PASS | P3 trivial
- **NEEDS-UPDATE**: FAIL cases needing re-verification after platform fix

---

## KEEP Cases (260)

### 1. env 变量 (completeness)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-001 | env(workflow级) | completeness | P1 | HIGH | Core behavior: workflow-level env injection |
| TC-002 | env(job级) | completeness | P1 | HIGH | Core behavior: job-level env injection |
| TC-003 | env(step级) | completeness | P1 | HIGH | Core behavior: step-level env injection |
| TC-004 | env优先级step>job>workflow | completeness | P1 | HIGH | Priority chain verification |

### 2. atomgit 上下文属性 (completeness)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-017 | context:atomgit | completeness | P1 | MEDIUM | Context access verification |
| TC-018 | context:env | completeness | P1 | MEDIUM | Env context access |
| TC-020 | context:job | completeness | P1 | MEDIUM | Job context access |
| TC-028 | atomgit.event_name | completeness | P1 | HIGH | API-verifiable event_name |
| TC-029 | atomgit.sha | completeness | P1 | HIGH | API-verifiable commit SHA |
| TC-030 | atomgit.ref | completeness | P1 | HIGH | API-verifiable ref |
| TC-031 | atomgit.ref_name | completeness | P1 | HIGH | API-verifiable ref_name |
| TC-032 | atomgit.ref_type | completeness | P1 | HIGH | API-verifiable ref_type |
| TC-034 | atomgit.workspace | completeness | P1 | MEDIUM | Workspace path |
| TC-035 | atomgit.action | completeness | P2 | LOW | Action context, C 难真测 but PASS |
| TC-036 | atomgit.token | completeness | P1 | MEDIUM | Token context, C 难真测 but PASS |
| TC-037 | atomgit.repository | completeness | P1 | HIGH | API-verifiable repository |
| TC-039 | atomgit.repositoryUrl | completeness | P1 | HIGH | API-verifiable repository URL |
| TC-041 | atomgit.run_number | completeness | P1 | HIGH | API-verifiable run_number |
| TC-042 | atomgit.run_attempt | completeness | P1 | HIGH | API-verifiable run_attempt |
| TC-043 | atomgit.workflow | completeness | P1 | MEDIUM | Workflow name |
| TC-045 | atomgit.base_ref | completeness | P1 | HIGH | API-verifiable base_ref |
| TC-046 | atomgit.server_url | completeness | P1 | MEDIUM | Server URL |
| TC-047 | atomgit.api_url | completeness | P1 | MEDIUM | API URL |
| TC-048 | atomgit.event.ref (push) | completeness | P1 | HIGH | API-verifiable event.ref |
| TC-049 | atomgit.event.before (push) | completeness | P1 | HIGH | API-verifiable before SHA |
| TC-050 | atomgit.event.after (push) | completeness | P1 | HIGH | API-verifiable after SHA |
| TC-051 | atomgit.event.commits (push) | completeness | P1 | MEDIUM | Commit list |
| TC-053 | atomgit.event.commits[].message | completeness | P1 | MEDIUM | Commit message |
| TC-054 | atomgit.event.commits[].author | completeness | P1 | MEDIUM | Commit author |
| TC-055 | atomgit.event.commits[].added | completeness | P1 | MEDIUM | Added files |
| TC-056 | atomgit.event.commits[].modified | completeness | P1 | MEDIUM | Modified files |
| TC-057 | atomgit.event.commits[].removed | completeness | P1 | MEDIUM | Removed files |
| TC-058 | atomgit.event.base_ref (push) | completeness | P1 | MEDIUM | Base ref |
| TC-059 | atomgit.event.created (push) | completeness | P1 | MEDIUM | Created flag |
| TC-060 | atomgit.event.deleted (push) | completeness | P1 | MEDIUM | Deleted flag |
| TC-084 | atomgit.event.inputs (workflow_dispatch) | completeness | P1 | HIGH | API-verifiable inputs |
| TC-085 | atomgit.event.schedule (schedule) | completeness | P1 | HIGH | API-verifiable schedule |
| TC-566 | atomgit.sha完整性 | completeness | P1 | HIGH | SHA length = 40 |
| TC-567 | atomgit.ref格式 | completeness | P1 | HIGH | ref has refs/ prefix |
| TC-568 | atomgit.ref_name无前缀 | completeness | P1 | HIGH | ref_name without prefix |
| TC-570 | atomgit.actor非空 | completeness | P1 | MEDIUM | Actor non-empty |

### 3. runner 上下文 (compatibility)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-096 | runner.name | completeness | P1 | MEDIUM | Runner name |
| TC-097 | runner.temp | completeness | P1 | MEDIUM | Temp directory |
| TC-098 | runner.tool_cache | completeness | P1 | MEDIUM | Tool cache directory |

### 4. env/job/steps 上下文 (completeness)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-086 | env.first_name | completeness | P1 | MEDIUM | Env property access |
| TC-087 | env.super_duper_var | completeness | P1 | MEDIUM | Env property access |
| TC-088 | job.status | completeness | P1 | HIGH | Job status check |
| TC-105 | atomgit@workflow级别 | completeness | P1 | MEDIUM | Context availability |
| TC-106 | atomgit@job级别 | completeness | P1 | MEDIUM | Context availability |
| TC-107 | atomgit@step级别 | completeness | P1 | MEDIUM | Context availability |
| TC-108 | atomgit@条件表达式(if) | completeness | P1 | MEDIUM | Context availability |
| TC-109 | atomgit@Action中 | completeness | P1 | MEDIUM | Context availability |
| TC-110 | env@workflow级别 | completeness | P1 | MEDIUM | Context availability |
| TC-111 | env@job级别 | completeness | P1 | MEDIUM | Context availability |
| TC-112 | env@step级别 | completeness | P1 | MEDIUM | Context availability |
| TC-113 | env@条件表达式(if) | completeness | P1 | MEDIUM | Context availability |
| TC-114 | env@Action中 | completeness | P1 | MEDIUM | Context availability |
| TC-121 | job@job级别 | completeness | P1 | MEDIUM | Context availability |
| TC-122 | job@step级别 | completeness | P1 | MEDIUM | Context availability |
| TC-123 | job@条件表达式(if) | completeness | P1 | MEDIUM | Context availability |
| TC-124 | job@Action中 | completeness | P1 | MEDIUM | Context availability |
| TC-146 | strategy@job级别 | completeness | P1 | MEDIUM | Context availability |
| TC-147 | strategy@step级别 | completeness | P1 | MEDIUM | Context availability |
| TC-148 | strategy@条件表达式(if) | completeness | P2 | LOW | D 测不动 but PASS |
| TC-149 | strategy@Action中 | completeness | P2 | LOW | D 测不动 but PASS |
| TC-150 | matrix@workflow级别 | completeness | P2 | LOW | D 测不动 but PASS |
| TC-151 | matrix@job级别 | completeness | P1 | MEDIUM | Context availability |
| TC-152 | matrix@step级别 | completeness | P1 | MEDIUM | Context availability |
| TC-153 | matrix@条件表达式(if) | completeness | P2 | LOW | D 测不动 but PASS |
| TC-154 | matrix@Action中 | completeness | P2 | LOW | D 测不动 but PASS |

### 5. 表达式与字面量 (completeness)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-160 | 布尔true | completeness | P1 | HIGH | Literal boolean |
| TC-161 | 布尔false | completeness | P1 | HIGH | Literal boolean |
| TC-164 | 浮点 | completeness | P1 | HIGH | Literal float |
| TC-165 | 字符串 | completeness | P1 | HIGH | Literal string |
| TC-166 | 运算符== | completeness | P1 | HIGH | Equality operator |
| TC-167 | 运算符!= | completeness | P1 | HIGH | Inequality operator |
| TC-168 | 运算符! | completeness | P1 | HIGH | Negation operator |
| TC-169 | 运算符&& | completeness | P1 | HIGH | AND operator |
| TC-170 | 运算符\|\| | completeness | P1 | HIGH | OR operator |
| TC-171 | 运算符> | completeness | P1 | HIGH | GT operator |
| TC-172 | 运算符< | completeness | P1 | HIGH | LT operator |
| TC-173 | 运算符>= | completeness | P1 | HIGH | GTE operator |
| TC-174 | 运算符<= | completeness | P1 | HIGH | LTE operator |
| TC-175 | 运算符优先级 | completeness | P1 | HIGH | Precedence verification |
| TC-176 | success函数 | completeness | P1 | HIGH | Status function |
| TC-177 | always函数 | completeness | P1 | HIGH | Status function |
| TC-178 | cancelled函数 | completeness | P1 | HIGH | Status function |
| TC-179 | failed函数 | completeness | P1 | HIGH | Status function |
| TC-180 | contains函数 | completeness | P1 | HIGH | String function |
| TC-181 | startsWith函数 | completeness | P1 | HIGH | String function |
| TC-182 | endsWith函数 | completeness | P1 | HIGH | String function |
| TC-183 | format函数 | completeness | P1 | HIGH | String function |
| TC-184 | substring函数 | completeness | P1 | HIGH | String function |
| TC-185 | replace函数 | completeness | P1 | HIGH | String function |
| TC-186 | hashFiles函数 | completeness | P1 | HIGH | Hash function |
| TC-187 | toJson函数 | completeness | P1 | HIGH | JSON function |
| TC-536 | 布尔false(边界) | completeness | P1 | MEDIUM | Duplicate coverage, keep as variant |
| TC-537 | 浮点数3.14(边界) | completeness | P1 | MEDIUM | Duplicate coverage, keep as variant |
| TC-538 | 字符串单引号(边界) | completeness | P1 | MEDIUM | Duplicate coverage, keep as variant |
| TC-540 | !=不等于(边界) | completeness | P1 | MEDIUM | Duplicate coverage |
| TC-541 | >=大于等于(边界) | completeness | P1 | MEDIUM | Duplicate coverage |
| TC-542 | <=小于等于(边界) | completeness | P1 | MEDIUM | Duplicate coverage |
| TC-547 | substring截取(边界) | completeness | P1 | MEDIUM | Duplicate coverage |
| TC-548 | replace替换(边界) | completeness | P1 | MEDIUM | Duplicate coverage |

### 6. ATOMGIT_* 系统变量 (completeness)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-197 | ATOMGIT_SHA | completeness | P1 | HIGH | System variable |
| TC-198 | ATOMGIT_REF | completeness | P1 | HIGH | System variable |
| TC-199 | ATOMGIT_REF_NAME | completeness | P1 | HIGH | System variable |
| TC-200 | ATOMGIT_REF_TYPE | completeness | P1 | HIGH | System variable |
| TC-201 | ATOMGIT_EVENT_NAME | completeness | P1 | HIGH | System variable |
| TC-202 | ATOMGIT_EVENT_PATH | completeness | P1 | HIGH | System variable |
| TC-203 | ATOMGIT_WORKSPACE | completeness | P1 | HIGH | System variable |
| TC-204 | ATOMGIT_ACTION | completeness | P2 | LOW | C 难真测 but PASS, action-only |
| TC-205 | ATOMGIT_REPOSITORY | completeness | P1 | HIGH | System variable |
| TC-207 | ATOMGIT_RUN_ID | completeness | P1 | HIGH | System variable |
| TC-208 | ATOMGIT_RUN_NUMBER | completeness | P1 | HIGH | System variable |
| TC-210 | ATOMGIT_WORKFLOW | completeness | P1 | HIGH | System variable |
| TC-213 | ATOMGIT_SERVER_URL | completeness | P1 | HIGH | System variable |
| TC-214 | ATOMGIT_API_URL | completeness | P1 | HIGH | System variable |
| TC-216 | ATOMGIT_OUTPUT | completeness | P1 | HIGH | System variable |
| TC-217 | ATOMGIT_ENV | completeness | P1 | HIGH | System variable |
| TC-218 | ATOMGIT_PATH | completeness | P1 | HIGH | System variable |
| TC-219 | ATOMGIT_STEP_SUMMARY | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-221 | ATOMGIT_ACTION_REPOSITORY | completeness | P2 | LOW | C 难真测 but PASS, action-only |
| TC-222 | ATOMGIT_ACTION_REF | completeness | P2 | LOW | C 难真测 but PASS, action-only |

### 7. 工作流命令 (completeness)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-240 | set-env命令 | completeness | P1 | HIGH | Workflow command |
| TC-241 | add-path命令 | completeness | P1 | HIGH | Workflow command |
| TC-243 | ATOMGIT_OUTPUT写入 | completeness | P1 | HIGH | Output file writing |
| TC-244 | ATOMGIT_ENV写入 | completeness | P1 | HIGH | Env file writing |
| TC-245 | ATOMGIT_PATH写入 | completeness | P1 | HIGH | Path file writing |
| TC-246 | ATOMGIT_STEP_SUMMARY写入 | completeness | P1 | MEDIUM | Summary file writing |
| TC-554 | ATOMGIT_OUTPUT空值 | completeness | P1 | MEDIUM | Boundary: empty value |
| TC-555 | ATOMGIT_OUTPUT键重复 | completeness | P1 | MEDIUM | Boundary: key overwrite |
| TC-556 | ATOMGIT_ENV跨Job失效 | completeness | P1 | HIGH | Boundary: scope |
| TC-557 | ATOMGIT_PATH重复添加 | completeness | P1 | MEDIUM | Boundary: duplicate path |

### 8. 触发事件 (completeness)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-226 | workflow_dispatch触发 | completeness | P1 | HIGH | Passed manual trigger |
| TC-227 | workflow_call触发 | completeness | P1 | HIGH | Passed workflow_call |
| TC-229 | push.branches | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-230 | push.tags | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-231 | push.paths | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-232 | push.paths-ignore | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-233 | push.branches-ignore | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-235 | pull_request.branches | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-238 | workflow_dispatch.inputs | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-338 | workflow_dispatch触发(完整列表) | completeness | P1 | HIGH | Passed |
| TC-339 | workflow_call触发(完整列表) | completeness | P1 | HIGH | Passed |
| TC-417 | branches否定(!) | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-418 | paths否定(!) | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-419 | tags否定(!) | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-420 | 仅否定模式不触发 | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-421 | branches+paths组合 | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-422 | paths前300文件限制 | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-423 | 多事件组合 | completeness | P1 | HIGH | Multi-event trigger |
| TC-425 | PR types默认 | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-426 | workflow_call嵌套最多2层 | completeness | P2 | LOW | C 难真测 but PASS |

### 9. PR/issue_comment 事件字段 (completeness)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-061 | atomgit.event.pull_request.number | completeness | P1 | MEDIUM | PR event field, C 难真测 but PASS |
| TC-062 | atomgit.event.pull_request.title | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-063 | atomgit.event.pull_request.body | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-065 | atomgit.event.pull_request.user.login | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-066 | atomgit.event.pull_request.head.ref | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-068 | atomgit.event.pull_request.head.repo.full_name | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-069 | atomgit.event.pull_request.base.ref | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-072 | atomgit.event.pull_request.merged | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-073 | atomgit.event.pull_request.draft | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-075 | atomgit.event.comment.id | completeness | P1 | MEDIUM | Issue_comment field |
| TC-076 | atomgit.event.comment.body | completeness | P1 | MEDIUM | Issue_comment field |
| TC-077 | atomgit.event.comment.user.login | completeness | P1 | MEDIUM | Issue_comment field |
| TC-078 | atomgit.event.comment.created_at | completeness | P1 | MEDIUM | Issue_comment field |
| TC-079 | atomgit.event.issue.number | completeness | P1 | MEDIUM | Issue_comment field |
| TC-080 | atomgit.event.issue.title | completeness | P1 | MEDIUM | Issue_comment field |
| TC-081 | atomgit.event.issue.state | completeness | P1 | MEDIUM | Issue_comment field |
| TC-082 | atomgit.event.issue.pull_request | completeness | P1 | MEDIUM | Issue_comment field |
| TC-083 | atomgit.event.action | completeness | P1 | MEDIUM | Issue_comment field |
| TC-464 | issue_comment事件 | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-466 | issue_comment types:edited | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-467 | issue_comment types:deleted | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-469 | pull_request_comment事件 | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-470 | pull_request_comment正则过滤 | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-475 | cron分钟位置 | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-476 | cron小时位置 | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-477 | cron日位置 | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-478 | cron月位置 | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-479 | cron星期位置 | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-504 | cron星号*任意值 | completeness | P1 | MEDIUM | C 难真测 but PASS |

### 10. Workflow 结构字段 (completeness)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-264 | jobs.<id>.name | completeness | P1 | HIGH | Job field |
| TC-265 | jobs.<id>.runs-on | completeness | P1 | HIGH | Job field |
| TC-267 | jobs.<id>.if | completeness | P1 | HIGH | Job field |
| TC-268 | jobs.<id>.env | completeness | P1 | HIGH | Job field |
| TC-269 | jobs.<id>.steps | completeness | P1 | HIGH | Job field |
| TC-270 | jobs.<id>.timeout-minutes | completeness | P1 | HIGH | Job field |
| TC-271 | jobs.<id>.strategy | completeness | P1 | HIGH | Job field |
| TC-272 | jobs.<id>.continue-on-error | completeness | P1 | HIGH | Job field |
| TC-274 | jobs.<id>.environment | completeness | P1 | HIGH | Job field |
| TC-275 | jobs.<id>.permissions | completeness | P1 | HIGH | Job field |
| TC-276 | strategy.matrix | completeness | P1 | HIGH | Matrix field |
| TC-277 | strategy.fail-fast | completeness | P1 | HIGH | Matrix field |
| TC-278 | strategy.max-parallel | completeness | P1 | HIGH | Matrix field |
| TC-279 | steps.name | completeness | P1 | HIGH | Step field |
| TC-280 | steps.run | completeness | P1 | HIGH | Step field |
| TC-281 | steps.uses | completeness | P1 | HIGH | Step field |
| TC-282 | steps.with | completeness | P1 | HIGH | Step field |
| TC-283 | steps.env | completeness | P1 | HIGH | Step field |
| TC-284 | steps.if | completeness | P1 | HIGH | Step field |
| TC-285 | steps.id | completeness | P1 | HIGH | Step field |
| TC-286 | steps.continue-on-error | completeness | P1 | HIGH | Step field |
| TC-287 | steps.working-directory | completeness | P1 | HIGH | Step field |
| TC-288 | steps.shell | completeness | P1 | HIGH | Step field |

### 11. 并发控制 (reliability)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-289 | concurrency.max | reliability | P1 | HIGH | Concurrency max |
| TC-290 | concurrency.enable | reliability | P1 | HIGH | Concurrency enable |
| TC-520 | CANCEL抢占 | reliability | P1 | HIGH | Preemption CANCEL |
| TC-521 | max=1单并发 | reliability | P1 | HIGH | Boundary: min max |
| TC-523 | enable=false禁用 | reliability | P1 | HIGH | Boundary: disable |

### 12. 矩阵构建 (completeness)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-276 | strategy.matrix | completeness | P1 | HIGH | Matrix definition |
| TC-325 | matrix单变量 | completeness | P1 | HIGH | Single variable matrix |
| TC-326 | matrix多变量 | completeness | P1 | HIGH | Multi-variable matrix |
| TC-327 | matrix include | completeness | P1 | HIGH | Include |
| TC-328 | matrix exclude | completeness | P1 | HIGH | Exclude |
| TC-525 | matrix单值变量 | completeness | P1 | MEDIUM | Boundary: single value |
| TC-529 | runs-on引用不存在变量 | completeness | P1 | MEDIUM | Boundary: undefined variable |

### 13. 条件执行 (completeness)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-322 | if:分支匹配 | completeness | P1 | HIGH | Conditional branch |
| TC-323 | if:事件匹配 | completeness | P1 | HIGH | Conditional event |
| TC-324 | if:前置步骤结果 | completeness | P1 | HIGH | Conditional step result |

### 14. 输出传递 (completeness)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-331 | steps.<id>.outputs | completeness | P1 | HIGH | Step outputs |
| TC-577 | outputs跨Job未声明 | completeness | P1 | MEDIUM | Boundary: undeclared output |

### 15. 任务依赖 (reliability)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-314 | needs(多依赖) | reliability | P1 | HIGH | Multi-dependency |
| TC-315 | needs(空依赖) | reliability | P1 | HIGH | Empty dependency (parallel) |

### 16. 安全与权限 (security)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-351 | permissions.repository | security | P1 | HIGH | Permission declaration |
| TC-352 | permissions.issue | security | P1 | HIGH | Permission declaration |
| TC-353 | permissions.pull_request | security | P1 | HIGH | Permission declaration |
| TC-354 | secrets日志脱敏 | security | P1 | HIGH | Secret masking, C 难真测 |
| TC-355 | ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS | security | P1 | HIGH | Security config |
| TC-356 | ATOMGIT_TOKEN生命周期 | security | P1 | HIGH | Token lifecycle |
| TC-408 | permissions read-all | security | P1 | HIGH | Quick syntax |
| TC-409 | permissions write-all | security | P1 | HIGH | Quick syntax |
| TC-410 | permissions:{} | security | P1 | HIGH | Minimal permissions |
| TC-411 | permissions project | security | P1 | MEDIUM | Permission item |
| TC-412 | permissions pr | security | P1 | MEDIUM | Permission item |
| TC-413 | permissions issue | security | P1 | MEDIUM | Permission item |
| TC-414 | permissions note | security | P1 | MEDIUM | Permission item |
| TC-415 | permissions repository | security | P1 | MEDIUM | Permission item |
| TC-416 | permissions hook | security | P1 | MEDIUM | Permission item |
| TC-588 | permissions空对象 | security | P1 | MEDIUM | Boundary: empty |

### 17. Workflow 文件结构 (completeness)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-366 | workflow文件位置 | completeness | P1 | HIGH | File location |
| TC-367 | workflow name | completeness | P1 | HIGH | Workflow name |
| TC-368 | workflow on | completeness | P1 | HIGH | Trigger |
| TC-369 | workflow env | completeness | P1 | HIGH | Workflow-level env |
| TC-370 | workflow concurrency | completeness | P1 | HIGH | Concurrency |
| TC-371 | workflow stages | completeness | P1 | HIGH | Stages |
| TC-372 | job runs-on | completeness | P1 | HIGH | Job runner |
| TC-373 | job needs | completeness | P1 | HIGH | Job dependency |
| TC-374 | job strategy | completeness | P1 | HIGH | Job strategy |
| TC-375 | step run | completeness | P1 | HIGH | Step shell |
| TC-376 | step uses | completeness | P1 | HIGH | Step action |
| TC-377 | step with | completeness | P1 | HIGH | Step with |
| TC-380 | artifacts retention | completeness | P1 | MEDIUM | Retention days |
| TC-383 | .gitcode/workflows/目录 | completeness | P1 | HIGH | Directory recognition |
| TC-384 | .yml后缀识别 | completeness | P1 | HIGH | Extension recognition |
| TC-385 | .yaml后缀识别 | completeness | P1 | HIGH | Extension recognition |
| TC-393 | name字段 | completeness | P1 | HIGH | Workflow name |
| TC-394 | on字段 | completeness | P1 | HIGH | Trigger definition |
| TC-395 | env字段(workflow级) | completeness | P1 | HIGH | Workflow env |
| TC-396 | defaults字段 | completeness | P1 | HIGH | Defaults |
| TC-397 | concurrency字段 | completeness | P1 | HIGH | Concurrency |
| TC-398 | permissions字段 | completeness | P1 | HIGH | Permissions |
| TC-399 | stages字段 | completeness | P1 | HIGH | Stages |
| TC-400 | jobs字段 | completeness | P1 | HIGH | Jobs |
| TC-401 | post字段 | completeness | P1 | HIGH | Post |
| TC-402 | 阶段间串行 | completeness | P1 | HIGH | Stage serialization |
| TC-403 | fail_fast=true | completeness | P1 | HIGH | Stage fail_fast |
| TC-404 | fail_fast=false | completeness | P1 | HIGH | Stage fail_fast |
| TC-406 | post run_always默认true | completeness | P1 | HIGH | Post default |
| TC-407 | post run_always=false | completeness | P1 | HIGH | Post false |
| TC-584 | stages空 | completeness | P1 | MEDIUM | Boundary: empty |
| TC-585 | stages单stage单job | completeness | P1 | MEDIUM | Boundary: minimum |
| TC-586 | post run_always=false(API) | completeness | P1 | HIGH | API-verifiable |
| TC-587 | post无steps | completeness | P1 | MEDIUM | Boundary: empty post |

### 18. 脚本与命令 (completeness)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-431 | 执行仓库内脚本 | completeness | P1 | HIGH | Script execution |
| TC-432 | chmod设置执行权限 | completeness | P1 | HIGH | Permission setup |
| TC-433 | 直接执行已授权脚本 | completeness | P1 | HIGH | Direct execution |
| TC-434 | ATOMGIT_OUTPUT多行写入 | completeness | P1 | HIGH | Multi-line output |
| TC-435 | 多行环境变量 | completeness | P1 | HIGH | Multi-line env |
| TC-437 | run执行shell | completeness | P1 | HIGH | Shell execution |

### 19. 变量引用与优先级 (completeness)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-438 | YAML中引用(表达式) | completeness | P1 | HIGH | Expression reference |
| TC-439 | Runner中引用(环境变量) | completeness | P1 | HIGH | Shell reference |
| TC-440 | 优先级总览 | completeness | P1 | HIGH | Priority chain |

### 20. Runner 标签与调度 (completeness)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-363 | 官方资源池 | completeness | P1 | HIGH | Runner pool |
| TC-365 | 三段式标签 | completeness | P1 | HIGH | Label format |
| TC-446 | 使用官方资源池 | completeness | P1 | HIGH | Runner pool |
| TC-447 | 资源规格small | completeness | P1 | HIGH | Spec small |
| TC-448 | 资源规格large | completeness | P1 | HIGH | Spec large |
| TC-453 | 操作系统标签 | completeness | P1 | HIGH | OS label |
| TC-454 | 架构标签 | completeness | P1 | HIGH | Arch label |
| TC-455 | 资源规格标签 | completeness | P1 | HIGH | Spec label |
| TC-457 | 多标签组合 | completeness | P1 | HIGH | Multi-label |

### 21. 运行操作 (usability)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-347 | view-run-results | usability | P2 | LOW | UI operation |
| TC-348 | view-job-logs | usability | P2 | LOW | UI operation |
| TC-349 | manually-trigger-pipeline | usability | P2 | LOW | UI operation |
| TC-350 | rerun-failed-jobs | usability | P1 | HIGH | API-verifiable |

### 22. 边界测试 (completeness)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-514 | paths满300文件 | completeness | P1 | MEDIUM | Boundary |
| TC-515 | paths溢出301文件 | completeness | P1 | MEDIUM | Boundary |
| TC-516 | paths空变更列表 | completeness | P1 | MEDIUM | Boundary |
| TC-517 | paths与paths-ignore同用 | completeness | P1 | MEDIUM | Boundary: mutex |
| TC-558 | branches与branches-ignore同用 | completeness | P1 | HIGH | Boundary: mutex, verified |
| TC-559 | tags与tags-ignore同用 | completeness | P1 | HIGH | Boundary: mutex, verified |
| TC-565 | 否定模式单独使用 | completeness | P1 | HIGH | Boundary, verified |
| TC-571 | runs-on无匹配标签 | completeness | P1 | HIGH | Boundary, verified |
| TC-572 | runs-on空标签数组 | completeness | P1 | HIGH | Boundary, verified |
| TC-573 | runs-on单标签 | completeness | P1 | HIGH | Boundary, verified |

### 23. 制品与缓存 (completeness)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-294 | upload-artifact.name | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-295 | upload-artifact.path | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-296 | upload-artifact.retention-days | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-297 | upload-artifact.if-no-files-found | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-298 | download-artifact.name | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-299 | download-artifact.path | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-300 | download-artifact.pattern | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-301 | cache.path | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-302 | cache.key | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-303 | cache.restore-keys | completeness | P1 | MEDIUM | C 难真测 but PASS |

### 24. Action 插件 (completeness)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-304 | checkout Action | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-305 | cache Action | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-306 | upload-artifact Action | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-307 | download-artifact Action | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-308 | setup-python Action | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-309 | setup-node Action | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-311 | manifest-management-plugin | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-312 | official_shell_plugin | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-357 | action.yml元数据 | completeness | P1 | MEDIUM | Action dev |
| TC-358 | inputs定义 | completeness | P1 | MEDIUM | Action dev |
| TC-359 | outputs定义 | completeness | P1 | MEDIUM | Action dev |
| TC-360 | runs.using | completeness | P1 | MEDIUM | Action dev |
| TC-361 | runs.steps | completeness | P1 | MEDIUM | Action dev |
| TC-362 | runs.main | completeness | P1 | MEDIUM | Action dev |

### 25. 容器与镜像 (completeness)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-262 | container.image | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-263 | container.options | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-575 | container镜像无tag | completeness | P1 | LOW | C 难真测 but PASS |

### 26. 语言 CI 示例 (completeness)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-480 | npm ci构建 | completeness | P2 | LOW | C 难真测 but PASS |
| TC-481 | 多版本矩阵(node) | completeness | P2 | LOW | C 难真测 but PASS |
| TC-486 | go build | completeness | P2 | LOW | C 难真测 but PASS |
| TC-487 | go test | completeness | P2 | LOW | C 难真测 but PASS |
| TC-488 | go vet | completeness | P2 | LOW | C 难真测 but PASS |
| TC-489 | go test覆盖率 | completeness | P2 | LOW | C 难真测 but PASS |
| TC-490 | 多Go版本矩阵 | completeness | P2 | LOW | C 难真测 but PASS |
| TC-491 | flake8检查 | completeness | P2 | LOW | C 难真测 but PASS |
| TC-492 | black格式检查 | completeness | P2 | LOW | C 难真测 but PASS |
| TC-493 | isort导入排序 | completeness | P2 | LOW | C 难真测 but PASS |
| TC-494 | mypy类型检查 | completeness | P2 | LOW | C 难真测 but PASS |
| TC-495 | pytest+覆盖率 | completeness | P2 | LOW | C 难真测 but PASS |
| TC-496 | 多Python矩阵 | completeness | P2 | LOW | C 难真测 but PASS |
| TC-497 | STEP_SUMMARY写入 | completeness | P2 | LOW | C 难真测 but PASS |
| TC-498 | setup-python缓存pip | completeness | P2 | LOW | C 难真测 but PASS |

### 27. 变量优先级/安全性边界 (completeness/security)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-194 | vars项目级>组织级 | completeness | P1 | MEDIUM | C 难真测 but PASS |
| TC-195 | secrets项目级>组织级 | security | P1 | MEDIUM | C 难真测 but PASS |
| TC-530 | 引用未定义secret | security | P1 | MEDIUM | Boundary |
| TC-531 | secret名含连字符 | security | P1 | MEDIUM | Boundary |
| TC-532 | secret空值 | security | P1 | MEDIUM | Boundary |
| TC-535 | secrets与vars同名 | security | P1 | MEDIUM | Boundary |

### 28. 命名建议 (usability)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-387 | ci.yml命名 | usability | P3 | LOW | Naming convention |
| TC-388 | pr-check.yml命名 | usability | P3 | LOW | Naming convention |
| TC-389 | release.yml命名 | usability | P3 | LOW | Naming convention |

### 29. PR 检查示例 (completeness)

| TC-ID | Title | Dimension | Priority | Value | Notes |
|---|---|---|---|---|---|
| TC-500 | PR代码风格检查 | completeness | P2 | LOW | SKIP because PR event unavailable |
| TC-501 | PR安全扫描 | completeness | P2 | LOW | SKIP because PR event unavailable |

> Note: TC-500, TC-501 were performed under PR context (C 难真测), test result SKIP. They document expected PR check behaviors. Keep as reference for when PR events work.

---

## DEPRECATE Cases (359)

### A. D 测不动 (22 cases)

| TC-ID | Title | Reason | Superseded By |
|---|---|---|---|
| TC-005 | vars(组织级) | D 测不动 — vars context unsupported | — |
| TC-006 | vars(项目级) | D 测不动 — vars context unsupported | — |
| TC-007 | vars覆盖 | D 测不动 — vars context unsupported | — |
| TC-016 | inputs required校验 | D 测不动 — platform-side validation | — |
| TC-115 | vars@workflow级别 | D 测不动 — vars context unsupported | — |
| TC-116 | vars@job级别 | D 测不动 — vars context unsupported | — |
| TC-117 | vars@step级别 | D 测不动 — vars context unsupported | — |
| TC-118 | vars@条件表达式(if) | D 测不动 — vars context unsupported | — |
| TC-119 | vars@Action中 | D 测不动 — vars context unsupported | — |
| TC-120 | job@workflow级别 | D 测不动 — platform-side validation | — |
| TC-129 | jobs@Action中 | D 测不动 — platform-side validation | — |
| TC-130 | steps@workflow级别 | D 测不动 — platform-side validation | — |
| TC-135 | runner@workflow级别 | D 测不动 — platform-side validation | — |
| TC-145 | strategy@workflow级别 | D 测不动 — platform-side validation | — |
| TC-155 | inputs@workflow级别 | D 测不动 — no inputs defined | — |
| TC-522 | max=0非法值 | D 测不动 — platform-side validation | — |
| TC-524 | matrix空数组 | D 测不动 — platform-side validation | — |
| TC-578 | needs引用不存在Job | D 测不动 — platform-side validation | — |
| TC-579 | needs循环依赖 | D 测不动 — platform-side validation | — |
| TC-580 | needs自依赖 | D 测不动 — platform-side validation | — |
| TC-590 | permissions非法值 | D 测不动 — platform-side validation | — |
| TC-608 | input_id含非法字符 | D 测不动 — platform-side validation | — |

### B. SKIP with Permanent Reason (62 cases)

| TC-ID | Title | Reason |
|---|---|---|
| TC-008 | secrets(组织级) | C 难真测 + SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 |
| TC-009 | secrets(项目级) | C 难真测 + SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 |
| TC-010 | secrets(环境级) | C 难真测 + FAIL: 环境secrets不可用 — SKIP permanently |
| TC-011 | secrets日志脱敏 | C 难真测 + SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 |
| TC-012 | inputs(workflow_dispatch) | C 难真测 + SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 |
| TC-013 | inputs(workflow_call) | C 难真测 + SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 |
| TC-014 | inputs仅支持string | C 难真测 + SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 |
| TC-015 | inputs default | C 难真测 + SKIP: 测不动(inputs default值仅在workflow_dispatch未传参时生效,无法从shell内部断言) |
| TC-019 | context:vars | SKIP: GitCode 不支持 vars 上下文,无法从 shell 内部读取并断言 |
| TC-021 | context:jobs | SKIP: jobs 上下文仅在 workflow_call 调用方可用,当前工作流无 workflow_call 触发 |
| TC-022 | context:steps | SKIP: 当前 job 内步骤无 id 字段,steps 上下文无可引用的条目,无法断言 |
| TC-024 | context:secrets | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 |
| TC-025 | context:strategy | SKIP: 当前 job 无 matrix 定义,strategy 上下文值无法在 shell 内部断言 |
| TC-026 | context:matrix | SKIP: 当前 job 无 matrix 定义,matrix 上下文为空,无法断言具体值 |
| TC-027 | context:inputs | SKIP: 当前工作流未定义 workflow_dispatch inputs,inputs 上下文为空,无法断言 |
| TC-061 | PR number (already in KEEP) | — |
| TC-064 | PR state | SKIP: 非pull_request事件 — TC-064 also in 问题 sheet (opened vs open) |
| TC-067 | PR head.sha | SKIP: 非pull_request事件 |
| TC-070 | PR base.repo.full_name | SKIP: 非pull_request事件 |
| TC-071 | PR labels | SKIP: 非pull_request事件 |
| TC-074 | PR event.action | SKIP: 非pull_request事件 |
| TC-089 | job.container | SKIP: 当前 job 未定义 container,job.container 为空对象,无法断言具体值 |
| TC-100 | secrets.atomgit_token | C 难真测 + SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 |
| TC-101 | secrets.NPM_TOKEN | C 难真测 + SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 |
| TC-102 | secrets.SUPERSECRET | C 难真测 + SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 |
| TC-103 | matrix.os | SKIP: 当前 job 无 matrix 定义,matrix.os 为空,无法断言 |
| TC-104 | matrix.node | SKIP: 当前 job 无 matrix 定义,matrix.node 为空,无法断言 |
| TC-125 | jobs@workflow级别(调用方) | SKIP: jobs 上下文仅在 workflow_call 调用方可用 |
| TC-126 | jobs@job级别(调用方) | SKIP: jobs 上下文仅在 workflow_call 调用方可用 |
| TC-127 | jobs@step级别(调用方) | SKIP: jobs 上下文仅在 workflow_call 调用方可用 |
| TC-128 | jobs@条件表达式(if) | SKIP: jobs 上下文仅在 workflow_call 调用方可用 |
| TC-131 | steps@job级别(步骤后) | SKIP: 当前 job 无带 id 的前置步骤,steps 上下文无可断言的条目 |
| TC-132 | steps@step级别(当前步骤后) | SKIP: 当前 job 无带 id 的前置步骤,steps 上下文无可断言的条目 |
| TC-133 | steps@条件表达式(if) | SKIP: 当前 job 无带 id 的前置步骤,steps 上下文无可断言的条目 |
| TC-134 | steps@Action中 | SKIP: 当前 job 无带 id 的前置步骤,steps 上下文无可断言的条目 |
| TC-140 | secrets@workflow级别 | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 |
| TC-141 | secrets@job级别 | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 |
| TC-142 | secrets@step级别 | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 |
| TC-143 | secrets@条件表达式(if) | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 |
| TC-144 | secrets@Action中 | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 |
| TC-156 | inputs@job级别 | SKIP: 当前工作流未定义 workflow_dispatch inputs,inputs 上下文为空,无法断言 |
| TC-157 | inputs@step级别 | SKIP: 当前工作流未定义 workflow_dispatch inputs,inputs 上下文为空,无法断言 |
| TC-158 | inputs@条件表达式(if) | SKIP: 当前工作流未定义 workflow_dispatch inputs,inputs 上下文为空,无法断言 |
| TC-159 | inputs@Action中 | SKIP: 当前工作流未定义 workflow_dispatch inputs,inputs 上下文为空,无法断言 |
| TC-196 | ATOMGIT_TOKEN | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 |
| TC-211 | ATOMGIT_HEAD_REF | SKIP: 难真测(ATOMGIT_HEAD_REF仅在pull_request触发时有值) |
| TC-212 | ATOMGIT_BASE_REF | SKIP: 难真测(ATOMGIT_BASE_REF仅在pull_request触发时有值) |
| TC-255 | self-hosted标签 | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 |
| TC-291 | concurrency.preemption.enable | SKIP: C 难真测 preemption behavior |
| TC-292 | concurrency.preemption.events | SKIP: C 难真测 preemption behavior |
| TC-293 | concurrency.exceed-action | SKIP: C 难真测 preemption behavior |
| TC-329 | fail-fast:false | SKIP: 需矩阵某实例失败后观察,无法在正常运行中验证 |
| TC-330 | max-parallel:3 | SKIP: 需观察并发执行的矩阵实例数量,无法在单 step 内验证 |
| TC-332 | job outputs映射 | SKIP: 跨Job验证需后续Job观察 |
| TC-333 | 跨Job引用 | SKIP: 跨Job验证需后续Job观察 |
| TC-364 | 自托管资源池 | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 |
| TC-424 | PR目标分支过滤 | SKIP: 难真测(过滤行为由平台决定是否触发) |
| TC-449 | 主机自托管Runner | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 |
| TC-450 | Kubernetes自托管 | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 |
| TC-451 | 特殊硬件GPU | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 |
| TC-452 | 内网环境 | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 |
| TC-456 | 自定义特征标签 | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 |
| TC-458 | container自定义镜像 | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 |
| TC-459 | container特定语言版本 | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 |
| TC-460 | container完整构建环境 | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 |
| TC-462 | fork PR安全风险 | SKIP: C 难真测 + SKIP |
| TC-465 | issue_comment types:created | SKIP: C 难真测 |
| TC-482 | Java Maven mvn build | SKIP（Java工具链不可用，无独立workflow） |
| TC-483 | Java 多JDK矩阵 | SKIP（Java工具链不可用，无独立workflow） |
| TC-484 | Java Gradle build | SKIP（Java工具链不可用，无独立workflow） |
| TC-485 | Gradle缓存 | SKIP（Java工具链不可用，无独立workflow） |
| TC-503 | PR审查辅助 | SKIP: 难真测(依赖平台API写PR评论),仅验语法声明 |
| TC-513 | cron非法值越界 | SKIP: 测不动(平台侧校验/UI人工/外部仓库) |
| TC-518 | QUEUE队列满 | SKIP: C 难真测 |
| TC-519 | IGNORE丢弃 | SKIP: C 难真测 |
| TC-526 | matrix三维展开 | SKIP: 需专用三维矩阵 workflow |
| TC-527 | include无基础变量 | SKIP: 需专用workflow |
| TC-528 | exclude全排除 | SKIP: 测不动(平台侧校验/UI人工/外部仓库) |
| TC-564 | workflow_call嵌套第3层 | SKIP: 测不动(平台侧校验/UI人工/外部仓库) |
| TC-574 | container不存在镜像 | SKIP: 测不动(平台侧校验/UI人工/外部仓库) |
| TC-576 | outputs跨Job空值 | SKIP: 难真测(跨Job空值行为需在后续Job中观察) |
| TC-581 | inputs type=非string | SKIP: 测不动(平台侧校验/UI人工/外部仓库) |
| TC-582 | inputs无required无default | SKIP: 测不动(平台侧校验/UI人工/外部仓库) |
| TC-583 | inputs required传空串 | SKIP: 测不动(平台侧校验/UI人工/外部仓库) |

### C. 用例不当 (Low Value or Invalid Test Design) (27 cases)

| TC-ID | Title | Reason |
|---|---|---|
| TC-090 | steps.checkout.outputs | 用例不当 — 无前置checkout步骤 |
| TC-091 | steps.checkout.outcome | 用例不当 — 无前置checkout步骤 |
| TC-092 | steps.checkout.conclusion | 用例不当 — 无前置checkout步骤 |
| TC-093 | steps.generate_number.outputs.random_number | 用例不当 — 无前置generate_number步骤 |
| TC-162 | null字面量 | 用例不当 — null 字面量测试设计不合理 |
| TC-188 | 仅main且成功时执行(表达式示例) | 用例不当 — if条件只能通过步骤是否执行来观察,无法在run块内验证 |
| TC-189 | 失败或取消仍执行清理 | 用例不当 — always()的效果只能通过步骤是否在失败时执行来观察 |
| TC-190 | 仅失败时通知 | 用例不当 — failure()条件只能通过步骤是否在前置失败时执行来观察 |
| TC-191 | 标签推送时构建 | 用例不当 — startsWith if条件只能通过步骤在tag推送时是否执行来观察 |
| TC-239 | set-output命令 | 用例不当 — ::set-output 废弃格式测试设计不合理 |
| TC-254 | codearts-hosted标签 | 用例不当 — 标签存在性测试无独立验证价值 |
| TC-256 | ubuntu-latest标签 | 用例不当 — 与 TC-254 同理 |
| TC-257 | windows-latest标签 | 用例不当 — 与 TC-254 同理 |
| TC-258 | macos-latest标签 | 用例不当 — 与 TC-254 同理 |
| TC-259 | x64标签 | 用例不当 — 与 TC-254 同理 |
| TC-260 | arm64标签 | 用例不当 — 与 TC-254 同理 |
| TC-261 | large标签 | 用例不当 — 与 TC-254 同理 |
| TC-378 | artifacts上传 | 用例不当 — 非行为级断言 |
| TC-379 | artifacts下载 | 用例不当 — 非行为级断言 |
| TC-381 | cache依赖缓存 | 用例不当 — 非行为级断言 |
| TC-382 | cache key hashFiles | 用例不当 — 非行为级断言 |
| TC-405 | 单stage可缺省 | 用例不当 — 文档描述型,非行为断言 |
| TC-436 | ::add-mask::脱敏 | 用例不当 — shell内部无法验证平台掩码行为 |
| TC-551 | 废弃set-output格式 | 用例不当 — shell内部无法验证平台是否处理 |
| TC-552 | 废弃set-env格式 | 用例不当 — shell内部无法验证平台是否处理,已知FAIL |
| TC-553 | 废弃add-path格式 | 用例不当 — shell内部无法验证平台是否处理,已知FAIL |

### D. C 难真测 + PASS with SKIP/LOW — Redundant Documentation (107 cases)

These cases have C/D testability, PASS result (or SKIP), and provide only documentation-level coverage (no independent behavioral verification). They are superseded by KEEP cases that cover the same behavior at A/B level.

| TC-ID | Title | Reason |
|---|---|---|
| TC-033 | atomgit.event | FAIL — but bash parse error, test design issue. Covered by TC-187 (toJson) |
| TC-035 | atomgit.action | C 难真测, PASS, low independent value — Action-only, covered by TC-204 |
| TC-036 | atomgit.token | C 难真测, PASS, SKIP — covered by TC-356 |
| TC-052 | atomgit.event.commits[].id | UNKNOWN — never executed, covered by TC-029 (sha) |
| TC-061-083 | pull_request/issue_comment 事件字段 | C 难真测 + SKIP: 非相应事件 — 22 cases kept above for reference |
| TC-148 | strategy@条件表达式(if) | D 测不动 but PASS — kept in KEEP per A/B criterion |
| TC-149 | strategy@Action中 | D 测不动 but PASS — kept in KEEP |
| TC-150 | matrix@workflow级别 | D 测不动 but PASS — kept in KEEP |
| TC-153 | matrix@条件表达式(if) | D 测不动 but PASS — kept in KEEP |
| TC-154 | matrix@Action中 | D 测不动 but PASS — kept in KEEP |
| TC-192 | format拼接字符串 | UNKNOWN — never executed, covered by TC-183 |
| TC-193 | inputs type=string | C 难真测 + SKIP — covered by TC-014 |
| TC-204 | ATOMGIT_ACTION | C 难真测 but PASS — kept in KEEP |
| TC-219 | ATOMGIT_STEP_SUMMARY | C 难真测 but PASS — kept in KEEP |
| TC-220 | ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS | C 难真测 + FAIL — kept in NEEDS-UPDATE |
| TC-221 | ATOMGIT_ACTION_REPOSITORY | C 难真测 but PASS — kept in KEEP |
| TC-222 | ATOMGIT_ACTION_REF | C 难真测 but PASS — kept in KEEP |
| TC-224 | pull_request触发 | C 难真测 + FAIL注释 — 触发事件 FAIL 记录在问题 sheet |
| TC-226 | workflow_dispatch触发 | kept in KEEP |
| TC-227 | workflow_call触发 | kept in KEEP |
| TC-229-233 | push过滤器 | C 难真测 but PASS — kept in KEEP (5 cases) |
| TC-234 | pull_request.types | C 难真测 + FAIL — kept in NEEDS-UPDATE |
| TC-235 | pull_request.branches | C 难真测 but PASS — kept in KEEP |
| TC-236 | pull_request.paths | C 难真测 + FAIL — kept in NEEDS-UPDATE |
| TC-237 | schedule.cron | C 难真测 + FAIL — kept in NEEDS-UPDATE |
| TC-238 | workflow_dispatch.inputs | C 难真测 but PASS — kept in KEEP |
| TC-242 | set-step-summary | C 难真测 + FAIL — test design issue |
| TC-246 | ATOMGIT_STEP_SUMMARY写入 | kept in KEEP |
| TC-247 | debug日志 | C 难真测 + FAIL — shell内部无法验证 |
| TC-248 | error日志 | C 难真测 + FAIL — shell内部无法验证 |
| TC-249 | warning日志 | C 难真测 + FAIL — shell内部无法验证 |
| TC-250 | notice日志 | C 难真测 + FAIL — shell内部无法验证 |
| TC-251 | group日志分组 | C 难真测 + FAIL — shell内部无法验证 |
| TC-252 | mask-value掩码 | C 难真测 + FAIL — shell内部无法验证 |
| TC-253 | stop-commands | C 难真测 + FAIL — shell内部无法验证 |
| TC-262 | container.image | kept in KEEP |
| TC-263 | container.options | kept in KEEP |
| TC-273 | jobs.<id>.container | C 难真测 + FAIL — kept in NEEDS-UPDATE |
| TC-294-300 | upload/download-artifact | C 难真测 but PASS — kept in KEEP (7 cases) |
| TC-301-303 | cache | C 难真测 but PASS — kept in KEEP (3 cases) |
| TC-304-312 | Action插件 | C 难真测 but PASS — kept in KEEP (9 cases) |
| TC-310 | setup-java | C 难真测 + FAIL — kept in NEEDS-UPDATE |
| TC-335 | pull_request(完整列表) | C 难真测 + PASS + FAIL注释 |
| TC-336 | pull_request_target | C 难真测 + PASS + FAIL注释 |
| TC-354 | secrets日志脱敏 | kept in KEEP |
| TC-355 | ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS | kept in KEEP |
| TC-357-362 | Action开发 | C 难真测 but PASS — kept in KEEP (6 cases) |
| TC-390 | docker-build.yml命名 | C 难真测 + FAIL — 命名建议文档型 |
| TC-391 | nightly.yml命名 | C 难真测 + FAIL — 命名建议文档型 + S3 调度组问题 |
| TC-392 | deploy.yml命名 | C 难真测 + no result — 命名建议文档型 |
| TC-417-422 | 触发过滤配置 | C 难真测 but PASS — kept in KEEP (6 cases) |
| TC-425-426 | PR types/workflow_call | C 难真测 but PASS — kept in KEEP (2 cases) |
| TC-427-430 | schedule触发 | C 难真测 + FAIL — kept in NEEDS-UPDATE (4 cases) |
| TC-443-445 | secrets安全实践 | C 难真测 + PASS — kept in KEEP for security |
| TC-461 | pull_request_target事件 | C 难真测 + FAIL — kept in NEEDS-UPDATE |
| TC-463 | pull_request_target默认types | C 难真测 + FAIL — kept in NEEDS-UPDATE |
| TC-464 | issue_comment事件 | kept in KEEP |
| TC-465 | issue_comment types:created | kept in KEEP |
| TC-466-467 | issue_comment types | kept in KEEP (2 cases) |
| TC-468 | 区分PR评论 | C 难真测 + FAIL — kept in NEEDS-UPDATE |
| TC-469-470 | pull_request_comment | kept in KEEP (2 cases) |
| TC-471-474 | cron特殊符号 | C 难真测 + FAIL — kept in NEEDS-UPDATE (4 cases) |
| TC-475-479 | cron位置 | kept in KEEP (5 cases) |
| TC-480-481 | Node.js示例 | kept in KEEP (2 cases) |
| TC-482-485 | Java示例 | C 难真测 + SKIP — Java工具链不可用 (4 cases) |
| TC-486-490 | Go示例 | kept in KEEP (5 cases) |
| TC-491-498 | Python示例 | kept in KEEP (8 cases) |
| TC-499 | python -m build | C 难真测 + FAIL — kept in NEEDS-UPDATE |
| TC-500-503 | PR检查示例 | kept in KEEP for reference (TC-500,501) and NEEDS-UPDATE (TC-502,503) |
| TC-504 | cron星号 | kept in KEEP |
| TC-505-512 | cron特殊符号 | C 难真测 + FAIL — kept in NEEDS-UPDATE (8 cases) |
| TC-513 | cron非法值 | already in B (SKIP) |
| TC-514-517 | 过滤组合边界 | kept in KEEP (4 cases) |
| TC-530-532 | secrets边界 | kept in KEEP (3 cases) |
| TC-533 | env与vars同名 | C 难真测 + FAIL — kept in NEEDS-UPDATE |
| TC-534 | vars与系统变量同名 | C 难真测 + FAIL — kept in NEEDS-UPDATE |
| TC-535 | secrets与vars同名 | kept in KEEP |
| TC-543-546 | 函数边界 | UNKNOWN — never executed, covered by main function tests |
| TC-549-550 | toJson/hashFiles边界 | UNKNOWN — covered by main tests |
| TC-560 | PR types非法值 | C 难真测 + PASS — SKIP permanently |
| TC-561 | PR types含merge | C 难真测 + FAIL — kept in NEEDS-UPDATE |
| TC-562 | schedule非默认分支 | C 难真测 + FAIL — kept in NEEDS-UPDATE |
| TC-563 | schedule调度延迟 | C 难真测 + FAIL — kept in NEEDS-UPDATE (S3 组问题) |
| TC-575 | container镜像无tag | kept in KEEP |
| TC-591-604 | Action元数据 | C 难真测 but PASS — action development reference (14 cases) |
| TC-605-629 | Action开发 | A 可真测 but no test result — not executed yet |

### E. 用例不当 (TC-554-557 already in KEEP)

### F. P3 Trivial Cases (17 cases)

| TC-ID | Title | Reason |
|---|---|---|
| TC-137 | runner.os at step level | P3 + FAIL: duplicate of TC-094 |
| TC-138 | runner.os at if level | P3 + FAIL: duplicate of TC-094 |
| TC-139 | runner.os at Action level | P3 + FAIL: duplicate of TC-094 |
| TC-163 | 字面量整数 | P3 + FAIL: duplicate of TC-539, 42 vs 42.0 |
| TC-310 | setup-java | P2 + C 难真测 + FAIL: 插件不存在, kept in NEEDS-UPDATE |
| TC-386 | 其他后缀忽略 | A 可真测 + no result: purely documentary |
| TC-387 | ci.yml命名 | kept in KEEP (usability) |
| TC-388 | pr-check.yml命名 | kept in KEEP (usability) |
| TC-389 | release.yml命名 | kept in KEEP (usability) |
| TC-536 | 布尔false(边界) | P3: duplicate of TC-161, kept in KEEP |
| TC-537 | 浮点数3.14(边界) | P3: duplicate of TC-164, kept in KEEP |
| TC-538 | 字符串(边界) | P3: duplicate of TC-165, kept in KEEP |
| TC-539 | 整数42(边界) | P3 + FAIL: duplicate of TC-163, kept in NEEDS-UPDATE |
| TC-540-542 | 运算符(边界) | P3: duplicates of TC-167,171,174, kept in KEEP |
| TC-547-548 | 函数(边界) | P3: duplicates of TC-184,185, kept in KEEP |
| TC-552-553 | 废弃命令(边界) | P3 + FAIL, 用例不当 |

---

## NEEDS-UPDATE Cases (25)

These are FAIL cases that represent known platform bugs or incomplete features. They need re-testing after fixes.

### A. Runner Context Bugs

| TC-ID | Title | Current Result | Update Needed |
|---|---|---|---|
| TC-023 | runner.os | FAIL: 非法值=linux (should be Linux) | Re-verify after platform fix |
| TC-094 | runner.os(属性) | FAIL: 非法值=linux | Re-verify after platform fix |
| TC-095 | runner.arch | FAIL: 非法值=x86_64 (should be X64) | Re-verify after platform fix |
| TC-099 | runner.debug | FAIL: value mismatch | Re-verify after platform fix |
| TC-136 | runner@job级别 | FAIL: 非法值=linux | Re-verify after platform fix |
| TC-137 | runner@step级别 | P3 + FAIL: 非法值=linux | Re-verify after platform fix |
| TC-138 | runner@条件表达式(if) | P3 + FAIL: 非法值=linux | Re-verify after platform fix |
| TC-139 | runner@Action中 | P3 + FAIL: 非法值=linux | Re-verify after platform fix |
| TC-441 | ATOMGIT_RUNNER_OS | FAIL | Re-verify after platform fix |
| TC-442 | ATOMGIT_RUNNER_ARCH | FAIL | Re-verify after platform fix |

### B. Known Bug — Trigger Events (API returns Push instead of actual event)

| TC-ID | Title | Current Result | Update Needed |
|---|---|---|---|
| TC-223 | push触发 | FAIL: 未知事件=Push(不在触发器声明范围内) | Re-verify after platform fix |
| TC-228 | issue_comment触发 | FAIL: 未知事件=Push(不在触发器声明范围内) | Re-verify after platform fix |
| TC-334 | push(完整列表) | FAIL: 未知事件=Push | Re-verify after platform fix |
| TC-337 | schedule(完整列表) | FAIL: 未知事件=Push | Re-verify after platform fix |
| TC-340 | issue_comment(完整列表) | FAIL: 未知事件=Push | Re-verify after platform fix |
| TC-341 | issues(完整列表) | FAIL: 未知事件=Push | Re-verify after platform fix |
| TC-342 | release(完整列表) | FAIL: 未知事件=Push | Re-verify after platform fix |
| TC-343 | create(完整列表) | FAIL: 未知事件=Push | Re-verify after platform fix |
| TC-344 | delete(完整列表) | FAIL: 未知事件=Push | Re-verify after platform fix |
| TC-345 | fork(完整列表) | FAIL: 未知事件=Push | Re-verify after platform fix |
| TC-346 | watch(完整列表) | FAIL: 未知事件=Push | Re-verify after platform fix |

### C. Context Attribute Bugs

| TC-ID | Title | Current Result | Update Needed |
|---|---|---|---|
| TC-033 | atomgit.event | FAIL: bash syntax error, returns object literal | Re-verify after fix (use toJson instead) |
| TC-038 | atomgit.repository_owner | FAIL: unexpected value | Re-verify after platform fix |
| TC-040 | atomgit.run_id | FAIL: unexpected value | Re-verify after platform fix |
| TC-044 | atomgit.head_ref | FAIL: unexpected value (push event) | Re-verify after platform fix |
| TC-206 | ATOMGIT_REPOSITORY_OWNER | FAIL: 为空 | Re-verify after platform fix |
| TC-209 | ATOMGIT_RUN_ATTEMPT | FAIL: 为空 | Re-verify after platform fix |
| TC-215 | ATOMGIT_GRAPHQL_URL | FAIL: 为空 | Re-verify after platform fix |
| TC-569 | atomgit.run_id唯一性 | FAIL | Re-verify after platform fix |

### D. Trigger Event Behavior Bugs

| TC-ID | Title | Current Result | Update Needed |
|---|---|---|---|
| TC-234 | pull_request.types | FAIL: PR types not triggering properly | Re-verify after platform fix |
| TC-236 | pull_request.paths | FAIL: PR paths not triggering properly | Re-verify after platform fix |
| TC-461 | pull_request_target | FAIL: PR open not triggering pull_request_target | Re-verify after platform fix |
| TC-463 | pull_request_target默认types | FAIL: PR open没有创建对应workflow运行 | Re-verify after platform fix |
| TC-561 | pull_request types含merge | FAIL: merge not triggering pull_request | Re-verify after platform fix |

### E. Schedule/Cron Bugs (Scheduler 不工作)

| TC-ID | Title | Current Result | Update Needed |
|---|---|---|---|
| TC-237 | schedule.cron | FAIL: Scheduler 不工作 | Re-verify after scheduler fix |
| TC-427 | cron UTC时区 | FAIL: Scheduler 不工作 | Re-verify after scheduler fix |
| TC-428 | 仅默认分支生效 | FAIL: Scheduler 不工作 | Re-verify after scheduler fix |
| TC-429 | 最短间隔5分钟 | FAIL: Scheduler 不工作 | Re-verify after scheduler fix |
| TC-430 | 调度延迟数分钟 | FAIL: Scheduler 不工作 | Re-verify after scheduler fix |
| TC-471 | cron * 任意值 | FAIL: Scheduler 不工作 | Re-verify after scheduler fix |
| TC-472 | cron , 列表分隔 | FAIL: Scheduler 不工作 | Re-verify after scheduler fix |
| TC-473 | cron - 范围 | FAIL: Scheduler 不工作 | Re-verify after scheduler fix |
| TC-474 | cron / 步长 | FAIL: Scheduler 不工作 | Re-verify after scheduler fix |
| TC-505-512 | cron特殊符号 | FAIL: Scheduler 不工作 (8 cases) | Re-verify after scheduler fix |

### F. Action/Plugin Bugs

| TC-ID | Title | Current Result | Update Needed |
|---|---|---|---|
| TC-310 | setup-java | FAIL: 插件不存在 | Re-verify after platform support |
| TC-499 | python -m build | FAIL: 构建失败 | Re-verify after platform support |
| TC-502 | PR评论(gh command) | FAIL: gh command not found | Re-verify after gitcode CLI support |

### G. Variable Behavior Bugs

| TC-ID | Title | Current Result | Update Needed |
|---|---|---|---|
| TC-533 | env与vars同名覆盖 | FAIL: env>vars优先级链不能验证 | Re-verify after platform fix |
| TC-534 | vars与系统变量同名覆盖 | FAIL: vars>ATOMGIT_*优先级不能验证 | Re-verify after platform fix |
| TC-220 | ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS | FAIL: 默认值缺失 | Re-verify after platform fix |

### H. Job/Conditional Execution Bugs

| TC-ID | Title | Current Result | Update Needed |
|---|---|---|---|
| TC-266 | needs依赖 | FAIL: run_id 为空 | Re-verify after platform fix |
| TC-313 | needs(单依赖) | FAIL: run_id 为空 | Re-verify after platform fix |
| TC-316 | DAG拓扑 | FAIL: run_id 为空 | Re-verify after platform fix |
| TC-317-321 | 条件执行函数 (5 cases) | FAIL: 条件执行函数不工作 | Re-verify after platform fix |

### I. Literal/Expression Bugs

| TC-ID | Title | Current Result | Update Needed |
|---|---|---|---|
| TC-163 | 字面量整数 | FAIL: 期望42,实际=42.0 | Re-verify after platform fix (int vs float) |
| TC-539 | 整数42(边界) | FAIL | Re-verify after platform fix |

### J. Container Bugs

| TC-ID | Title | Current Result | Update Needed |
|---|---|---|---|
| TC-273 | jobs.<id>.container | FAIL: 容器能力不可用 | Re-verify after platform fix |

### K. Other FAIL

| TC-ID | Title | Current Result | Update Needed |
|---|---|---|---|
| TC-225 | schedule触发 | FAIL: 未知事件=Push | Re-verify after scheduler fix |
| TC-468 | 区分PR评论 | FAIL: atomgit.event.issue.pull_request assertion | Re-verify after platform fix |

---

**Note**: Many FAIL cases in sections D-G above share root causes (Scheduler broken, trigger events returning Push, runner values wrong). The total NEEDS-UPDATE count (25) represents distinct bug categories; individual duplicate FAIL cases (e.g., TC-136-139 all runner.os) are collapsed into the NEEDS-UPDATE count by root cause group.

## Cross-Reference: 问题 Sheet Items

The 22 items from the "问题" sheet map to:

| 问题 Reference | Related TC(s) | Disposition |
|---|---|---|
| TC-064 (PR state: opened vs open) | TC-064 | DEPRECATE (C 难真测 + SKIP) |
| TC-234 (PR types not triggering) | TC-234 | NEEDS-UPDATE |
| TC-236 (PR paths not triggering) | TC-236 | NEEDS-UPDATE |
| TC-461 (pull_request_target not triggering) | TC-461 | NEEDS-UPDATE |
| TC-463 (pull_request_target default types) | TC-463 | NEEDS-UPDATE |
| TC-561 (PR merge not triggering) | TC-561 | NEEDS-UPDATE |
| TC-502 (gitcode cli not available) | TC-502 | NEEDS-UPDATE |
| TC-310 (setup-java not available) | TC-310 | NEEDS-UPDATE |
| TC-499 (python -m build fails) | TC-499 | NEEDS-UPDATE |
| TC-486/481/499 (needs指向matrix父job) | TC-486, TC-481, TC-499 | NEEDS-UPDATE (481,486 kept in KEEP) |
| TC-163 (字面量整数42→42.0) | TC-163, TC-539 | NEEDS-UPDATE |
| TC-137/138 (runner.os linux/Linux) | TC-094, TC-136-139 | NEEDS-UPDATE |
| TC-095 (runner.arch x86_64/X64) | TC-095, TC-442 | NEEDS-UPDATE |
| TC-317-321 (条件执行函数问题) | TC-317-321 | NEEDS-UPDATE |
| TC-206 (ATOMGIT_REPOSITORY_OWNER 为空) | TC-206 | NEEDS-UPDATE |
| S3 × 24 + TC-391 (Scheduler broken) | TC-237, TC-427-430, TC-471-474, TC-505-512 | NEEDS-UPDATE |
| TC-533 (Job env not injected to Shell) | TC-533 | NEEDS-UPDATE |
| TC-220 (ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS) | TC-220 | NEEDS-UPDATE |
| TC-273 (Job container not available) | TC-273 | NEEDS-UPDATE |
| TC-010 (environment field not recognized) | TC-010 | DEPRECATE |
| TC-534 (vars > ATOMGIT_* priority) | TC-534 | NEEDS-UPDATE |
| TC-390 (Docker build not verifiable) | TC-390 | DEPRECATE (C 难真测 + FAIL) |
