# 74 条校验失败/错误 · 分类归因 + 汇总分析

> 数据源: `phase01/runs/2026-07-23-01/cases/yaml/` (369 cases)
> 校验结果: 289 VALID, 66 INVALID, 6 SKIP, 8 ERROR
> 逐例详情: `failure/2026-07-24/case/*.md`
> 分析日期: 2026-07-24

## 一、概览

| 分类 | 数量 | 占比 |
|------|------|------|
| VALID | 289 | 78.3% |
| INVALID | 66 | 17.9% |
| SKIP | 6 | 1.6% |
| ERROR | 8 | 2.2% |

## 二、INVALID 错误分类

| 类别 | 涉及 Cases | 数量 |
|------|----------|------|
| 未知字段 | COMP-STAGES-01-003, COMP-STAGES-01-003, COMP-UNKNOWN-01-001, COMP-WFLOW-01-065, COMP-WFLOW-01-065 ... (+16) | 21 |
| concurrency 配置 | COMPAT-CONCUR-01-001, COMPAT-CONCUR-01-001, COMPAT-CONCUR-01-002, COMPAT-CONCUR-01-003, COMPAT-CONCUR-01-003 ... (+7) | 12 |
| cron 表达式 | COMP-BOUND-01-085, COMP-BOUND-01-085, COMP-BOUND-01-085, COMP-SCHEDULE-01-001, COMP-SCHEDULE-01-002 ... (+3) | 8 |
| if 表达式 | COMP-EXPR-01-058, COMPAT-EXPR-01-013, COMPAT-EXPR-01-013, COMPAT-EXPR-01-014, COMPAT-VARS-01-005 ... (+3) | 8 |
| runs-on 格式 | COMP-RUNNER-01-003, COMPAT-RUNNER-01-004, COMPAT-RUNNER-01-005, COMPAT-SHELL-01-003, USE-LBL-01-001 ... (+1) | 6 |
| 列表长度限制 | COMPAT-PATHS-01-001, COMPAT-PATHS-01-002, COMPAT-PR-01-003, COMPAT-PR-01-004, COMPAT-PR-01-005 ... (+1) | 6 |
| 类型反序列化失败 | COMP-STAGES-01-001, COMP-STAGES-01-002, COMPAT-SCHEDULE-01-001, COMPAT-SCHEDULE-01-002, REL-STAGES-01-029 | 5 |
| 插件名格式错误 | COMPAT-ACTIONDEV-01-001, SEC-SUPPLY-01-003, USE-NEST-01-001, USE-NEST-01-002 | 4 |
| 依赖插件不存在 | COMPAT-ACTIONDEV-01-001, SEC-SUPPLY-01-003, USE-NEST-01-001, USE-NEST-01-002 | 4 |
| unknown | SEC-WCMD-01-003, SEC-WCMD-01-004, USE-YAML-01-001, USE-YAML-01-002 | 4 |
| 枚举值非法 | COMPAT-PR-01-002, USE-TYPE-01-002 | 2 |

## 三、ERROR 案例 (8 条)

以下 cases 在校验 API 调用时返回 HTTP 418 (WAF 拦截)，无法获取校验结果：

- **COMP-ATOMGIT-01-049**: atomgit 边界格式校验 (dim=completeness, trigger=workflow_dispatch)
- **COMP-SCRIPT-01-082**: 脚本权限设置与直接执行验证 (dim=completeness, trigger=workflow_dispatch)
- **COMPAT-TOKEN-01-001**: ATOMGIT_TOKEN 应正确返回有效令牌 (dim=compatibility, trigger=workflow_dispatch)
- **COMPAT-TOKEN-01-002**: GITHUB_TOKEN 在 GitCode 中应为空且不应被静默映射 (dim=compatibility, trigger=workflow_dispatch)
- **REL-LOG-01-040**: 超长日志——单 job 输出 100 MB 日志应完整保留且可下载查看 (dim=reliability, trigger=workflow_dispatch)
- **REL-OUTPUT-01-017**: step output 越界值——ATOMGIT_OUTPUT 写入 1 MB+1 byte 应被拒绝或报错 (dim=reliability, trigger=workflow_dispatch)
- **SEC-NAME-01-002**: 通过 printenv 或进程枚举获取 ATOMGIT_TOKEN/secrets 时日志中必须保持脱敏 (dim=security, trigger=workflow_dispatch)
- **USE-MASK-01-001**: secret 脱敏文档描述与实际行为一致并给出缓解建议 (dim=usability, trigger=workflow_dispatch)

## 四、按维度统计

| 维度 | 数量 |
|------|------|
| compatibility | 31 |
| completeness | 14 |
| usability | 13 |
| security | 9 |
| reliability | 7 |

## 五、逐条归因表

| # | case_id | status | dimension | trigger | 根因 | 诊断摘要 |
|---|---------|--------|-----------|---------|------|---------|
| 1 | COMP-BOUND-01-085 | INVALID | completeness | schedule | cron_expression | on.schedule[0].cron: 不是可识别的cron表达式 |
| 2 | COMP-EXPR-01-058 | INVALID | completeness | workflow_dispatch | schema_violation | jobs[verify].steps[2].if: if表达式无法解析 {0} |
| 3 | COMP-RUNNER-01-003 | INVALID | completeness | workflow_dispatch | schema_violation | jobs[verify].runs-on: runs-on以数组形式定义时，若为默认资源池则定义为['codearts-hosted',{o |
| 4 | COMP-SCHEDULE-01-001 | INVALID | completeness | schedule | cron_expression | on.schedule[0].cron: 不是可识别的cron表达式 |
| 5 | COMP-SCHEDULE-01-002 | INVALID | completeness | schedule | cron_expression | on.schedule[0].cron: 不是可识别的cron表达式 |
| 6 | COMP-SCHEDULE-01-003 | INVALID | completeness | schedule | cron_expression | on.schedule[0].cron: 不是可识别的cron表达式 |
| 7 | COMP-STAGES-01-001 | INVALID | completeness | workflow_dispatch | deserialization | Cannot deserialize value of type `java.util.LinkedHashMap<java.lang.St |
| 8 | COMP-STAGES-01-002 | INVALID | completeness | workflow_dispatch | deserialization | Cannot deserialize value of type `java.util.LinkedHashMap<java.lang.St |
| 9 | COMP-STAGES-01-003 | INVALID | completeness | workflow_dispatch | unknown_property | post.steps: unknown property |
| 10 | COMP-TRIG-01-075 | INVALID | completeness | schedule | cron_expression | on.schedule[0].cron: 不是可识别的cron表达式 |
| 11 | COMP-UNKNOWN-01-001 | INVALID | completeness | workflow_dispatch | unknown_property | unknown_field: unknown property |
| 12 | COMP-WFLOW-01-065 | INVALID | completeness | workflow_dispatch | unknown_property | post.steps: unknown property |
| 13 | COMPAT-ACTIONDEV-01-001 | INVALID | compatibility | workflow_dispatch | schema_violation | jobs[test-action-meta].steps[1].uses: 格式错误：pluginname@version，其中 plugi |
| 14 | COMPAT-CONCUR-01-001 | INVALID | compatibility | workflow_dispatch | concurrency | concurrency.exceed-action: 值不能为空 |
| 15 | COMPAT-CONCUR-01-002 | INVALID | compatibility | workflow_dispatch | concurrency | Cannot deserialize value of type `java.lang.String` from Array value ( |
| 16 | COMPAT-CONCUR-01-003 | INVALID | compatibility | workflow_dispatch | concurrency | concurrency.exceed-action: 值不能为空 |
| 17 | COMPAT-CONCUR-01-004 | INVALID | compatibility | workflow_dispatch | concurrency | concurrency.exceed-action: 值不能为空 |
| 18 | COMPAT-ENVIRON-01-001 | INVALID | compatibility | workflow_dispatch | unknown_property | jobs[test].environment: unknown property |
| 19 | COMPAT-ENVIRON-01-002 | INVALID | compatibility | workflow_dispatch | unknown_property | jobs[test-environment].environment: unknown property |
| 20 | COMPAT-EXPR-01-013 | INVALID | compatibility | workflow_dispatch | schema_violation | jobs[test-success-paren].steps[0].if: if表达式无法解析 表达式：success()第1位出现不支持的 |
| 21 | COMPAT-EXPR-01-014 | INVALID | compatibility | workflow_dispatch | schema_violation | jobs[test-always-paren].steps[1].if: if表达式无法解析 表达式：always第1位出现不支持的关键字 |
| 22 | COMPAT-FIELD-01-001 | INVALID | compatibility | workflow_dispatch | unknown_property | run-name: unknown property |
| 23 | COMPAT-FIELD-01-002 | INVALID | compatibility | workflow_dispatch | unknown_property | jobs[test].services: unknown property |
| 24 | COMPAT-FIELD-01-003 | INVALID | compatibility | workflow_dispatch | unknown_property | custom_field: unknown property |
| 25 | COMPAT-MIGRATE-01-001 | INVALID | compatibility | workflow_dispatch | unknown_property | jobs[migrate-permissions].permissions: unknown property |
| 26 | COMPAT-MIGRATE-01-002 | INVALID | compatibility | workflow_dispatch | unknown_property | run-name: unknown property |
| 27 | COMPAT-PATHS-01-001 | INVALID | compatibility | push | schema_violation | on.push: 列表长度超出限制，paths paths-ignore之和不能小于1或超过32 |
| 28 | COMPAT-PATHS-01-002 | INVALID | compatibility | push | schema_violation | on.push: 列表长度超出限制，paths paths-ignore之和不能小于1或超过32 |
| 29 | COMPAT-PERM-01-003 | INVALID | compatibility | workflow_dispatch | unknown_property | permissions.contents: unknown property |
| 30 | COMPAT-PR-01-002 | INVALID | compatibility | pull_request | schema_violation | on.merge_requests.types: 列表中存在非法值:[opened] 允许值:[close, merge, open, re |
| 31 | COMPAT-PR-01-003 | INVALID | compatibility | pull_request | schema_violation | on.merge_requests: 列表长度超出限制，branches branches-ignore之和不能小于1或超过32 |
| 32 | COMPAT-PR-01-004 | INVALID | compatibility | pull_request | schema_violation | on.merge_requests: 列表长度超出限制，branches branches-ignore之和不能小于1或超过32 |
| 33 | COMPAT-PR-01-005 | INVALID | compatibility | pull_request | schema_violation | on.merge_requests: 列表长度超出限制，branches branches-ignore之和不能小于1或超过32 |
| 34 | COMPAT-RUNNER-01-004 | INVALID | compatibility | workflow_dispatch | schema_violation | jobs[test-custom-label].runs-on: runs-on以数组形式定义时，若为默认资源池则定义为['codearts |
| 35 | COMPAT-RUNNER-01-005 | INVALID | compatibility | workflow_dispatch | schema_violation | jobs[test-intranet].runs-on: runs-on以数组形式定义时，若为默认资源池则定义为['codearts-hos |
| 36 | COMPAT-SCHEDULE-01-001 | INVALID | compatibility | schedule | deserialization | Cannot deserialize value of type `java.util.ArrayList<com.huawei.devcl |
| 37 | COMPAT-SCHEDULE-01-002 | INVALID | compatibility | schedule | deserialization | Cannot deserialize value of type `java.util.ArrayList<com.huawei.devcl |
| 38 | COMPAT-SCHEDULE-01-003 | INVALID | compatibility | schedule | cron_expression | on.schedule[0].cron: 不是可识别的cron表达式 |
| 39 | COMPAT-SECRET-01-005 | INVALID | compatibility | workflow_dispatch | unknown_property | jobs[test-env-secret].environment: unknown property |
| 40 | COMPAT-SHELL-01-003 | INVALID | compatibility | workflow_dispatch | schema_violation | jobs[test-windows-shell].runs-on: runs-on以数组形式定义时，若为默认资源池则定义为['codeart |
| 41 | COMPAT-VARS-01-005 | INVALID | compatibility | workflow_dispatch | schema_violation | jobs[test-vars-if].steps[1].if: if表达式无法解析 表达式：vars.ENABLE_FEATURE == ' |
| 42 | REL-PREEMPT-01-005 | INVALID | reliability | workflow_dispatch | concurrency | concurrency.preemption.events: 列表中存在非法值:[push] 允许值:[mr_id] |
| 43 | REL-PREEMPT-01-006 | INVALID | reliability | workflow_dispatch | concurrency | concurrency.preemption.events: 列表中存在非法值:[push] 允许值:[mr_id] |
| 44 | REL-RACE-01-048 | INVALID | reliability | workflow_dispatch | schema_violation | jobs[job_b].if: if表达式无法解析 表达式：failure()第1位出现不支持的函数 |
| 45 | REL-STAGES-01-029 | INVALID | reliability | workflow_dispatch | deserialization | Cannot deserialize value of type `java.util.LinkedHashMap<java.lang.St |
| 46 | REL-STEPS-01-042 | INVALID | reliability | workflow_dispatch | schema_violation | jobs[test].steps: 列表长度必须在0到16之间 |
| 47 | SEC-DEFPERM-01-002 | INVALID | security | workflow_dispatch | unknown_property | jobs[override-test].permissions: unknown property |
| 48 | SEC-ENV-01-001 | INVALID | security | workflow_dispatch | unknown_property | jobs[env-secret-approved].environment: unknown property |
| 49 | SEC-ENV-01-002 | INVALID | security | workflow_dispatch | unknown_property | jobs[env-secret-denied].environment: unknown property |
| 50 | SEC-PERM-01-001 | INVALID | security | workflow_dispatch | unknown_property | jobs[perm-read].permissions: unknown property |
| 51 | SEC-PERM-01-002 | INVALID | security | workflow_dispatch | unknown_property | jobs[perm-write-denied].permissions: unknown property |
| 52 | SEC-SUPPLY-01-003 | INVALID | security | workflow_dispatch | schema_violation | jobs[typo-test].steps[0].uses: 格式错误：pluginname@version，其中 pluginname 为 |
| 53 | SEC-WCMD-01-003 | INVALID | security | workflow_dispatch | schema_violation | while scanning a simple key
 in 'string', line 11, column 1:
    INJEC |
| 54 | SEC-WCMD-01-004 | INVALID | security | workflow_dispatch | schema_violation | while scanning a simple key
 in 'string', line 12, column 1:
    hijac |
| 55 | USE-CONC-01-002 | INVALID | usability | workflow_dispatch | concurrency | concurrency.max: 值不能小于1 |
| 56 | USE-EXPR-01-002 | INVALID | usability | workflow_dispatch | schema_violation | jobs[bad].steps[0].if: if表达式无法解析 表达式：unknownFunc()第1位出现不支持的函数 |
| 57 | USE-LBL-01-001 | INVALID | usability | workflow_dispatch | schema_violation | jobs[bad].runs-on: runs-on以数组形式定义时，若为默认资源池则定义为['codearts-hosted',{os}, |
| 58 | USE-NEST-01-001 | INVALID | usability | workflow_dispatch | schema_violation | jobs[caller].steps[0].uses: 格式错误：pluginname@version，其中 pluginname 为 1~ |
| 59 | USE-NEST-01-002 | INVALID | usability | workflow_dispatch | schema_violation | jobs[caller].steps[0].uses: 格式错误：pluginname@version，其中 pluginname 为 1~ |
| 60 | USE-PERM-01-002 | INVALID | usability | workflow_dispatch | unknown_property | permissions.contents: unknown property |
| 61 | USE-RUN-01-002 | INVALID | usability | workflow_dispatch | schema_violation | jobs[bad-runner].runs-on: runs-on以数组形式定义时，若为默认资源池则定义为['codearts-hosted |
| 62 | USE-STAT-01-002 | INVALID | usability | workflow_dispatch | schema_violation | jobs[bad-stat].steps[0].if: if表达式无法解析 表达式：success()第1位出现不支持的函数 |
| 63 | USE-TYPE-01-002 | INVALID | usability | pull_request | schema_violation | on.merge_requests.types: 列表中存在非法值:[opened] 允许值:[close, merge, open, re |
| 64 | USE-UNKN-01-001 | INVALID | usability | workflow_dispatch | unknown_property | run-name: unknown property |
| 65 | USE-YAML-01-001 | INVALID | usability | workflow_dispatch | schema_violation | on: 值不能为空 |
| 66 | USE-YAML-01-002 | INVALID | usability | workflow_dispatch | schema_violation | while parsing a block mapping
 in 'string', line 5, column 5:
         |
| 67 | COMP-ATOMGIT-01-049 | ERROR | completeness | workflow_dispatch | WAF_blocked | HTTP 418 |
| 68 | COMP-SCRIPT-01-082 | ERROR | completeness | workflow_dispatch | WAF_blocked | HTTP 418 |
| 69 | COMPAT-TOKEN-01-001 | ERROR | compatibility | workflow_dispatch | WAF_blocked | HTTP 418 |
| 70 | COMPAT-TOKEN-01-002 | ERROR | compatibility | workflow_dispatch | WAF_blocked | HTTP 418 |
| 71 | REL-LOG-01-040 | ERROR | reliability | workflow_dispatch | WAF_blocked | HTTP 418 |
| 72 | REL-OUTPUT-01-017 | ERROR | reliability | workflow_dispatch | WAF_blocked | HTTP 418 |
| 73 | SEC-NAME-01-002 | ERROR | security | workflow_dispatch | WAF_blocked | HTTP 418 |
| 74 | USE-MASK-01-001 | ERROR | usability | workflow_dispatch | WAF_blocked | HTTP 418 |

## 六、建议

1. **WAF 拦截 (8 cases)**: HTTP 418 说明部分 YAML 被阿里云 WAF 拦截，可能触发 SQL/XSS 检测规则。建议：排查 YAML 内容中的特殊字符（如 `${}`、反引号、URI 编码样式字符串）
2. **concurrency 配置 (6+ cases)**: 多个 case 因 concurrency.max < 1、exceed-action 为空、preemption events 非法值被拒。检查 docs 与平台实现的差异
3. **cron 表达式 (7 cases)**: schedule cron 校验失败，可能是平台 cron 语法与标准有差异（如不允许缩减的星期/月份字段）
4. **unknown property 类 (7+ cases)**: `post.steps`、`post.run_always`、`run-name`、`permissions.contents` 这些字段是否确为平台不支持，还是校验器滞后于平台实际能力
5. **merge_requests (3 cases)**: branches+branches-ignore 长度限制 + types 枚举值差异（opened vs open），GitCode MR 事件与 GitHub PR 事件的字段映射不完整
