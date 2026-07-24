# 66 INVALID Cases — 预期非法 (24) vs 非预期非法 (42)

> Run: 2026-07-23-01 | 数据源: 369 cases → 289 通过 API 校验
> 逐例详情: `failure/2026-07-24/case/*.md` | 分析日期: 2026-07-24
> 分析方法: 遵循 `phase02/agents/failure-analyst/CLAUDE.md` 原则

## 一、总体结论

| 类别 | 数量 | 说明 |
|------|------|------|
| **预期非法** (negative test) | **24** | case 有意测试平台对非法输入的报错 — INVALID 是期望结果 |
| **非预期非法** → 需要修复 | **42** | case 描述正常功能但被平台校验驳回 — 属于平台缺陷或 case bug |
| **总计** | **66** | |

## 二、非预期非法 (42 cases) — 根因分类

按 `failure-analyst/CLAUDE.md` 原则分类: 文档承诺了 X 但平台做不到 X → 产品缺陷；case 用错语法 → case bug。

| 根因 | 数量 | 说明 | 涉及 Cases |
|------|------|------|----------|
| 列表长度限制未在文档声明 | 5 | | COMPAT-PATHS-01-001, COMPAT-PATHS-01-002, COMPAT-PR-01-003, COMPAT-PR-01-004 ... (+1) |
| cron 表达式被拒 (合法语法) | 4 | | COMP-BOUND-01-085, COMP-SCHEDULE-01-001, COMP-TRIG-01-075, COMPAT-SCHEDULE-01-003 |
| 其他 | 4 | | COMP-EXPR-01-058, COMPAT-CONCUR-01-001, COMPAT-CONCUR-01-003, COMPAT-EXPR-01-014 |
| environment 字段不支持 | 4 | | COMPAT-ENVIRON-01-002, COMPAT-SECRET-01-005, SEC-ENV-01-001, SEC-ENV-01-002 |
| runs-on 数组校验过严 | 3 | | COMP-RUNNER-01-003, COMPAT-RUNNER-01-005, COMPAT-SHELL-01-003 |
| stages 反序列化错误 (array vs map) | 3 | | COMP-STAGES-01-001, COMP-STAGES-01-002, REL-STAGES-01-029 |
| uses 格式错误 | 3 | | COMPAT-ACTIONDEV-01-001, SEC-SUPPLY-01-003, USE-NEST-01-002 |
| GitHub 表达式函数 vs GitCode 关键字 | 3 | | COMPAT-EXPR-01-013, COMPAT-VARS-01-005, REL-RACE-01-048 |
| job 级 permissions 不支持 | 3 | | SEC-DEFPERM-01-002, SEC-PERM-01-001, SEC-PERM-01-002 |
| post.steps/run_always 文档描述但平台拒 | 2 | | COMP-STAGES-01-003, COMP-WFLOW-01-065 |
| preemption events 取值限制 | 2 | | COMPAT-CONCUR-01-004, REL-PREEMPT-01-005 |
| schedule 反序列化错误 | 2 | | COMPAT-SCHEDULE-01-001, COMPAT-SCHEDULE-01-002 |
| YAML 语法错误 | 2 | | SEC-WCMD-01-003, SEC-WCMD-01-004 |
| 未知字段静默拒绝 (应警告) | 1 | | COMP-UNKNOWN-01-001 |
| steps <=16 限制未在文档声明 | 1 | | REL-STEPS-01-042 |

---

## 三、预期非法 — 24 Negative Tests

以下 cases 有意提交非法 YAML 以测试平台的报错能力，INVALID 是期望结果。

| # | case_id | dimension | trigger | 标题 | neg/pos | 诊断摘要 |
|---|---------|-----------|---------|------|---------|---------|
| 1 | COMP-SCHEDULE-01-002 | completeness | schedule | 非默认分支的 schedule workflow 不应触发 | 1/0 | on.schedule[0].cron: 不是可识别的cron表达式 |
| 2 | COMP-SCHEDULE-01-003 | completeness | schedule | cron 间隔短于 5 分钟时被拒绝或降级 | 1/0 | on.schedule[0].cron: 不是可识别的cron表达式 |
| 3 | COMPAT-CONCUR-01-002 | compatibility | workflow_dispatch | concurrency 配置越界或不支持时应给出清晰报错 | 1/1 | Cannot deserialize value of type `java.lang.String` fro |
| 4 | COMPAT-ENVIRON-01-001 | compatibility | workflow_dispatch | 含 environment 字段的 job 应被报错或警告 | 0/0 | jobs[test].environment: unknown property |
| 5 | COMPAT-FIELD-01-001 | compatibility | workflow_dispatch | 含 run-name 字段的 workflow 应被报错或警告 | 0/0 | run-name: unknown property |
| 6 | COMPAT-FIELD-01-002 | compatibility | workflow_dispatch | 含 services 字段的 job 应被报错或警告 | 0/0 | jobs[test].services: unknown property |
| 7 | COMPAT-FIELD-01-003 | compatibility | workflow_dispatch | 未知顶层字段不应被静默忽略而应给出警告 | 1/1 | custom_field: unknown property |
| 8 | COMPAT-MIGRATE-01-001 | compatibility | workflow_dispatch | GitHub 风格 permissions 块迁移报错应给出可操作指引 | 1/1 | jobs[migrate-permissions].permissions: unknown property |
| 9 | COMPAT-MIGRATE-01-002 | compatibility | workflow_dispatch | GitHub 风格 run-name 语法迁移报错应给出可操作指引 | 1/1 | run-name: unknown property |
| 10 | COMPAT-PERM-01-003 | compatibility | workflow_dispatch | permissions 命名差异——GitHub contents 权限项应报错 | 2/1 | permissions.contents: unknown property |
| 11 | COMPAT-PR-01-002 | compatibility | pull_request | pull_request types 命名差异 - GitHub 风格 type | 1/0 | on.merge_requests.types: 列表中存在非法值:[opened] 允许值:[close,  |
| 12 | COMPAT-RUNNER-01-004 | compatibility | workflow_dispatch | 自定义特征标签不被支持时应给出可用标签列表 | 0/2 | jobs[test-custom-label].runs-on: runs-on以数组形式定义时，若为默认资源 |
| 13 | REL-PREEMPT-01-006 | reliability | workflow_dispatch | preemption events 越界值——配置 11 个应被拒绝 | 0/1 | concurrency.preemption.events: 列表中存在非法值:[push] 允许值:[mr_ |
| 14 | USE-CONC-01-002 | usability | workflow_dispatch | concurrency.max 配置 -1 时报错应提示有效范围 | 1/0 | concurrency.max: 值不能小于1 |
| 15 | USE-EXPR-01-002 | usability | workflow_dispatch | 调用未知函数时报错应提示函数名错误与修正方向 | 1/0 | jobs[bad].steps[0].if: if表达式无法解析 表达式：unknownFunc()第1位出现 |
| 16 | USE-LBL-01-001 | usability | workflow_dispatch | runs-on 标签完全不匹配时应给出明确失败原因与可用标签列表 | 1/0 | jobs[bad].runs-on: runs-on以数组形式定义时，若为默认资源池则定义为['codeart |
| 17 | USE-NEST-01-001 | usability | workflow_dispatch | workflow_call 嵌套 3 层时报错应明确提示上限为 2 层 | 1/0 | jobs[caller].steps[0].uses: 格式错误：pluginname@version，其中  |
| 18 | USE-PERM-01-002 | usability | workflow_dispatch | 使用 GitHub 权限域命名时报错应给出 GitCode 对照表 | 1/0 | permissions.contents: unknown property |
| 19 | USE-RUN-01-002 | usability | workflow_dispatch | 使用单标签 ubuntu-latest 时报错应给出三段式格式指引 | 1/0 | jobs[bad-runner].runs-on: runs-on以数组形式定义时，若为默认资源池则定义为[' |
| 20 | USE-STAT-01-002 | usability | workflow_dispatch | 使用 success() 带括号时报错应提示 GitCode 括号差异 | 1/0 | jobs[bad-stat].steps[0].if: if表达式无法解析 表达式：success()第1位出 |
| 21 | USE-TYPE-01-002 | usability | pull_request | 使用 GitHub types 命名 opened/synchronize 时应 | 1/0 | on.merge_requests.types: 列表中存在非法值:[opened] 允许值:[close,  |
| 22 | USE-UNKN-01-001 | usability | workflow_dispatch | 未知字段如 run-name 不应被静默忽略而应给出警告或错误 | 0/0 | run-name: unknown property |
| 23 | USE-YAML-01-001 | usability | workflow_dispatch | 缺少必填字段 on 时报错应指出具体字段名与位置 | 1/0 | on: 值不能为空 |
| 24 | USE-YAML-01-002 | usability | workflow_dispatch | YAML 缩进错误时报错应指出具体行号与列号 | 1/0 | while parsing a block mapping
 in 'string', line 5, col |

---

## 四、非预期非法 — 逐根因详细分析

每条都标明了是平台缺陷还是 case bug，附 GitCode docs 对照。

### 列表长度限制未在文档声明 (5 cases)

**COMPAT-PATHS-01-001** — paths 过滤器 300 条边界测试
- 维度: compatibility | 优先级: P1 | trigger: push
- intent_ref: INTENT-COMPAT-012
- [Error] L3:C5: on.push: 列表长度超出限制，paths paths-ignore之和不能小于1或超过32

**COMPAT-PATHS-01-002** — paths 过滤器 301 条越界测试
- 维度: compatibility | 优先级: P1 | trigger: push
- intent_ref: INTENT-COMPAT-012
- [Error] L3:C5: on.push: 列表长度超出限制，paths paths-ignore之和不能小于1或超过32

**COMPAT-PR-01-003** — PR types 配置后匹配类型不触发与 GitHub 行为差异
- 维度: compatibility | 优先级: P1 | trigger: pull_request
- intent_ref: INTENT-COMPAT-NEW-003
- [Error] L0:C0: on.merge_requests: 列表长度超出限制，branches branches-ignore之和不能小于1或超过32

**COMPAT-PR-01-004** — PR types 含 merge 时不触发与 GitHub 行为差异
- 维度: compatibility | 优先级: P1 | trigger: pull_request
- intent_ref: INTENT-COMPAT-NEW-003
- [Error] L0:C0: on.merge_requests: 列表长度超出限制，branches branches-ignore之和不能小于1或超过32

**COMPAT-PR-01-005** — PR paths 过滤不工作时的兼容性差异
- 维度: compatibility | 优先级: P1 | trigger: pull_request
- intent_ref: INTENT-COMPAT-NEW-003
- [Error] L0:C0: on.merge_requests: 列表长度超出限制，branches branches-ignore之和不能小于1或超过32

**分析**: 文档 `configure-triggers.md` 只说明 paths 匹配前 300 个变更文件，未说明 paths/branches 条目数上限为 32。属于**文档缺失**。

### cron 表达式被拒 (合法语法) (4 cases)

**COMP-BOUND-01-085** — cron 表达式格式与位置边界验证
- 维度: completeness | 优先级: P1 | trigger: schedule
- intent_ref: KEEP-TC-475~512
- [Error] L3:C13: on.schedule[0].cron: 不是可识别的cron表达式
- [Error] L4:C13: on.schedule[1].cron: 不是可识别的cron表达式
- [Error] L5:C13: on.schedule[2].cron: 不是可识别的cron表达式

**COMP-SCHEDULE-01-001** — 合法 cron 在默认分支按时触发
- 维度: completeness | 优先级: P1 | trigger: schedule
- intent_ref: INTENT-COMP-005
- [Error] L3:C13: on.schedule[0].cron: 不是可识别的cron表达式

**COMP-TRIG-01-075** — schedule 事件关键字段与 cron 格式验证
- 维度: completeness | 优先级: P1 | trigger: schedule
- intent_ref: KEEP-TC-237~430
- [Error] L3:C13: on.schedule[0].cron: 不是可识别的cron表达式

**COMPAT-SCHEDULE-01-003** — schedule 在非默认分支不触发与 GitHub 差异
- 维度: compatibility | 优先级: P1 | trigger: schedule
- intent_ref: INTENT-COMPAT-013
- [Error] L3:C13: on.schedule[0].cron: 不是可识别的cron表达式

**分析**: GitCode 文档 `configure-triggers.md` 描述了 schedule cron 触发方式。但平台 cron 解析器与标准 cron 语法不兼容——合法的 cron 表达式被拒绝。属于**平台缺陷**（cron 语法兼容性）。

### 其他 (4 cases)

**COMP-EXPR-01-058** — 表达式运算符与优先级边界行为
- 维度: completeness | 优先级: P1 | trigger: workflow_dispatch
- intent_ref: KEEP-TC-160~175
- [Error] L0:C0: jobs[verify].steps[2].if: if表达式无法解析 {0}

**COMPAT-CONCUR-01-001** — concurrency cancel-in-progress false 时应排队而非报错
- 维度: compatibility | 优先级: P1 | trigger: workflow_dispatch
- intent_ref: INTENT-COMPAT-034
- [Error] L0:C0: concurrency.exceed-action: 值不能为空
- [Error] L0:C0: concurrency.max: 值不能小于1

**COMPAT-CONCUR-01-003** — concurrency preemption enable 行为差异
- 维度: compatibility | 优先级: P1 | trigger: workflow_dispatch
- intent_ref: INTENT-COMPAT-NEW-005
- [Error] L0:C0: concurrency.exceed-action: 值不能为空
- [Error] L0:C0: concurrency.max: 值不能小于1

**COMPAT-EXPR-01-014** — always() 带括号与不带括号的兼容性差异
- 维度: compatibility | 优先级: P1 | trigger: workflow_dispatch
- intent_ref: INTENT-COMPAT-004
- [Error] L0:C0: jobs[test-always-paren].steps[1].if: if表达式无法解析 表达式：always第1位出现不支持的关键字


### environment 字段不支持 (4 cases)

**COMPAT-ENVIRON-01-002** — environment 字段绑定 secrets 的行为差异
- 维度: compatibility | 优先级: P1 | trigger: workflow_dispatch
- intent_ref: INTENT-COMPAT-023
- [Error] L0:C0: jobs[test-environment].environment: unknown property

**COMPAT-SECRET-01-005** — 环境级 secrets 不支持时应明确报错而非降级为项目级
- 维度: compatibility | 优先级: P1 | trigger: workflow_dispatch
- intent_ref: INTENT-COMPAT-NEW-002
- [Error] L0:C0: jobs[test-env-secret].environment: unknown property

**SEC-ENV-01-001** — 环境级 secret 必须经审批后才能被 workflow 访问
- 维度: security | 优先级: P0 | trigger: workflow_dispatch
- intent_ref: INTENT-SEC-027
- [Error] L0:C0: jobs[env-secret-approved].environment: unknown property

**SEC-ENV-01-002** — 环境级 secret 审批前 workflow 不可读取
- 维度: security | 优先级: P0 | trigger: workflow_dispatch
- intent_ref: INTENT-SEC-027
- [Error] L0:C0: jobs[env-secret-denied].environment: unknown property

**分析**: 文档描述了 `environment` 字段绑定环境级 secrets，但平台校验器拒绝此字段。属于**平台缺陷**（环境级 secrets 功能未实现）。

### runs-on 数组校验过严 (3 cases)

**COMP-RUNNER-01-003** — 不存在的标签组合导致 job 排队或失败
- 维度: completeness | 优先级: P1 | trigger: workflow_dispatch
- intent_ref: INTENT-COMP-010
- [Error] L0:C0: jobs[verify].runs-on: runs-on以数组形式定义时，若为默认资源池则定义为['codearts-hosted',{os},{arch},{flavor}]，如['codearts-hosted','ubuntu-latest','x64','large']，其中'codearts-hosted'可省略；若为自定义资源池则定义为['self-hosted',{name},{label_1},{label_2},...,{label_n}]，如['self-hosted','my-private-pool','x64','region=cn-north-4']

**COMPAT-RUNNER-01-005** — 内网环境 Runner 不支持时的差异
- 维度: compatibility | 优先级: P2 | trigger: workflow_dispatch
- intent_ref: INTENT-COMPAT-NEW-008
- [Error] L0:C0: jobs[test-intranet].runs-on: runs-on以数组形式定义时，若为默认资源池则定义为['codearts-hosted',{os},{arch},{flavor}]，如['codearts-hosted','ubuntu-latest','x64','large']，其中'codearts-hosted'可省略；若为自定义资源池则定义为['self-hosted',{name},{label_1},{label_2},...,{label_n}]，如['self-hosted','my-private-pool','x64','region=cn-north-4']

**COMPAT-SHELL-01-003** — Windows runner 默认 shell 差异
- 维度: compatibility | 优先级: P2 | trigger: workflow_dispatch
- intent_ref: INTENT-COMPAT-001
- [Error] L0:C0: jobs[test-windows-shell].runs-on: runs-on以数组形式定义时，若为默认资源池则定义为['codearts-hosted',{os},{arch},{flavor}]，如['codearts-hosted','ubuntu-latest','x64','large']，其中'codearts-hosted'可省略；若为自定义资源池则定义为['self-hosted',{name},{label_1},{label_2},...,{label_n}]，如['self-hosted','my-private-pool','x64','region=cn-north-4']

**分析**: 平台的 runs-on 数组格式校验过严。合法 label 组合（如自定义标签）被判定为非法，且错误消息未给出可用标签列表。属于**平台缺陷**。

### stages 反序列化错误 (array vs map) (3 cases)

**COMP-STAGES-01-001** — stages 阶段间串行、阶段内 job 并行执行
- 维度: completeness | 优先级: P1 | trigger: workflow_dispatch
- intent_ref: INTENT-COMP-007
- [Error] L0:C0: Cannot deserialize value of type `java.util.LinkedHashMap<java.lang.String,com.huawei.devcloud.cloudpipeline.v2.domain.entity.pac2.gitcode.structs.GitcodeStage>` from Array value (token `JsonToken.START_ARRAY`)
 at [Source: UNKNOWN; byte offset: #UNKNOWN] (through reference chain: com.huawei.devcloud.cloudpipeline.v2.domain.entity.pac2.gitcode.GitcodePipelineDefinition["stages"])

**COMP-STAGES-01-002** — fail_fast true 时 stage 内任一 job 失败终止同阶段其余 job
- 维度: completeness | 优先级: P1 | trigger: workflow_dispatch
- intent_ref: INTENT-COMP-007
- [Error] L0:C0: Cannot deserialize value of type `java.util.LinkedHashMap<java.lang.String,com.huawei.devcloud.cloudpipeline.v2.domain.entity.pac2.gitcode.structs.GitcodeStage>` from Array value (token `JsonToken.START_ARRAY`)
 at [Source: UNKNOWN; byte offset: #UNKNOWN] (through reference chain: com.huawei.devcloud.cloudpipeline.v2.domain.entity.pac2.gitcode.GitcodePipelineDefinition["stages"])

**REL-STAGES-01-029** — stages fail_fast 机制——阶段内任一 job 失败应立即终止同阶段其他 jobs
- 维度: reliability | 优先级: P1 | trigger: workflow_dispatch
- intent_ref: INTENT-REL-029
- [Error] L0:C0: Cannot deserialize value of type `java.util.LinkedHashMap<java.lang.String,com.huawei.devcloud.cloudpipeline.v2.domain.entity.pac2.gitcode.structs.GitcodeStage>` from Array value (token `JsonToken.START_ARRAY`)
 at [Source: UNKNOWN; byte offset: #UNKNOWN] (through reference chain: com.huawei.devcloud.cloudpipeline.v2.domain.entity.pac2.gitcode.GitcodePipelineDefinition["stages"])

**分析**: 文档 `configure-dependencies-order.md` 展示了 stages array 和 map 两种格式，但平台只接受 map 格式。属于**文档冲突**（两种格式都给了示例但只支持一种）。

### uses 格式错误 (3 cases)

**COMPAT-ACTIONDEV-01-001** — action.yml 元数据校验与 GitHub 差异
- 维度: compatibility | 优先级: P2 | trigger: workflow_dispatch
- intent_ref: INTENT-COMPAT-NEW-010
- [Error] L0:C0: jobs[test-action-meta].steps[1].uses: 格式错误：pluginname@version，其中 pluginname 为 1~50 位字母、数字、"-"、"_"，version（官方插件不填）为 00-99.00-99.00-99 三段两位数字
- [Error] L0:C0: stages[default].jobs[test-action-meta]: 插件./.github/actions/my-action不存在

**SEC-SUPPLY-01-003** — 第三方 Action 来源应具备信任边界（typosquatting 限制）
- 维度: security | 优先级: P0 | trigger: workflow_dispatch
- intent_ref: INTENT-SEC-015
- [Error] L0:C0: jobs[typo-test].steps[0].uses: 格式错误：pluginname@version，其中 pluginname 为 1~50 位字母、数字、"-"、"_"，version（官方插件不填）为 00-99.00-99.00-99 三段两位数字
- [Error] L0:C0: stages[default].jobs[typo-test]: 插件checkout-action@v1不存在

**USE-NEST-01-002** — workflow_call 嵌套 2 层时应正常执行
- 维度: usability | 优先级: P1 | trigger: workflow_dispatch
- intent_ref: INTENT-USE-026
- [Error] L0:C0: jobs[caller].steps[0].uses: 格式错误：pluginname@version，其中 pluginname 为 1~50 位字母、数字、"-"、"_"，version（官方插件不填）为 00-99.00-99.00-99 三段两位数字
- [Error] L0:C0: stages[default].jobs[caller]: 插件./.gitcode/workflows/reusable-level1.yml不存在

**分析**: uses 路径指向不存在的文件或格式不符合 `pluginname@version` 规范。属于**case bug**（配置错误）。

### GitHub 表达式函数 vs GitCode 关键字 (3 cases)

**COMPAT-EXPR-01-013** — success() 带括号与不带括号的兼容性差异
- 维度: compatibility | 优先级: P1 | trigger: workflow_dispatch
- intent_ref: INTENT-COMPAT-004
- [Error] L0:C0: jobs[test-success-paren].steps[0].if: if表达式无法解析 表达式：success()第1位出现不支持的函数
- [Error] L0:C0: jobs[test-success-paren].steps[1].if: if表达式无法解析 表达式：success第1位出现不支持的关键字

**COMPAT-VARS-01-005** — vars 在条件表达式 if 中的可用性差异
- 维度: compatibility | 优先级: P1 | trigger: workflow_dispatch
- intent_ref: INTENT-COMPAT-022
- [Error] L0:C0: jobs[test-vars-if].steps[1].if: if表达式无法解析 表达式：vars.ENABLE_FEATURE == 'true'第1位出现不支持的关键字

**REL-RACE-01-048** — 取消与 needs 条件竞态——job A 被取消时 job B(if: failure())应正确判定
- 维度: reliability | 优先级: P1 | trigger: workflow_dispatch
- intent_ref: INTENT-REL-048
- [Error] L0:C0: jobs[job_b].if: if表达式无法解析 表达式：failure()第1位出现不支持的函数

**分析**: GitCode 不支持 GitHub Actions 的 `failure()`/`success()`/`always()` 函数调用语法，改用关键字 `failed`/`success`/`always`。属于**case bug** (用错语法)，已在 VALIDATION-RULES.md 规则 4d 记录。

### job 级 permissions 不支持 (3 cases)

**SEC-DEFPERM-01-002** — job 级覆盖后权限正确收窄
- 维度: security | 优先级: P0 | trigger: workflow_dispatch
- intent_ref: INTENT-SEC-036
- [Error] L0:C0: jobs[override-test].permissions: unknown property

**SEC-PERM-01-001** — 显式声明的 permissions 必须在 job 级实际生效并限制 ATOMGIT_TOKEN
- 维度: security | 优先级: P0 | trigger: workflow_dispatch
- intent_ref: INTENT-SEC-016
- [Error] L0:C0: jobs[perm-read].permissions: unknown property

**SEC-PERM-01-002** — permissions 声明 read 时写操作被平台拒绝
- 维度: security | 优先级: P0 | trigger: workflow_dispatch
- intent_ref: INTENT-SEC-016
- [Error] L0:C0: jobs[perm-write-denied].permissions: unknown property

**分析**: 文档 `token-permissions.md` 描述了 job 级 permissions 覆盖，但平台尚不支持 job 级 `permissions` 字段。属于**平台缺陷**（能力缺口）。

### post.steps/run_always 文档描述但平台拒 (2 cases)

**COMP-STAGES-01-003** — post.run_always true 时 workflow 失败仍执行 post
- 维度: completeness | 优先级: P1 | trigger: workflow_dispatch
- intent_ref: INTENT-COMP-007
- [Error] L14:C5: post.steps: unknown property
- [Error] L12:C15: post.run_always: unknown property

**COMP-WFLOW-01-065** — workflow post 后处理阶段字段验证
- 维度: completeness | 优先级: P1 | trigger: workflow_dispatch
- intent_ref: KEEP-TC-366~401
- [Error] L14:C5: post.steps: unknown property
- [Error] L12:C15: post.run_always: unknown property

**分析**: 文档 `core-concepts/workflow-job-step-action.md` 描述了 `post` 后处理阶段，`workflow-file-location-structure.md` 列出了 `post` 字段。平台校验器报 unknown property。属于**文档冲突**（文档超前于平台实现）。

### preemption events 取值限制 (2 cases)

**COMPAT-CONCUR-01-004** — concurrency preemption events 越界时行为差异
- 维度: compatibility | 优先级: P1 | trigger: workflow_dispatch
- intent_ref: INTENT-COMPAT-NEW-005
- [Error] L0:C0: concurrency.exceed-action: 值不能为空
- [Error] L0:C0: concurrency.max: 值不能小于1
- [Error] L7:C13: concurrency.preemption.events: 列表中存在非法值:[11] 允许值:[mr_id]

**REL-PREEMPT-01-005** — preemption events 边界值——配置 10 个应正常解析
- 维度: reliability | 优先级: P1 | trigger: workflow_dispatch
- intent_ref: INTENT-REL-005
- [Error] L7:C13: concurrency.preemption.events: 列表中存在非法值:[push] 允许值:[mr_id]

**分析**: 文档未声明 preemption events 仅支持 `mr_id`，其他值被拒绝。属于**文档缺失**。

### schedule 反序列化错误 (2 cases)

**COMPAT-SCHEDULE-01-001** — schedule cron 按 UTC 时间触发
- 维度: compatibility | 优先级: P1 | trigger: schedule
- intent_ref: INTENT-COMPAT-013
- [Error] L0:C0: Cannot deserialize value of type `java.util.ArrayList<com.huawei.devcloud.cloudpipeline.v2.domain.entity.pac2.gitcode.on.GitcodeScheduleOn>` from Object value (token `JsonToken.START_OBJECT`)
 at [Source: UNKNOWN; byte offset: #UNKNOWN] (through reference chain: com.huawei.devcloud.cloudpipeline.v2.domain.entity.pac2.gitcode.GitcodePipelineDefinition["on"]->com.huawei.devcloud.cloudpipeline.v2.domain.entity.pac2.gitcode.on.GitcodeOn["schedule"])

**COMPAT-SCHEDULE-01-002** — schedule 不支持 timezone 字段差异
- 维度: compatibility | 优先级: P1 | trigger: schedule
- intent_ref: INTENT-COMPAT-013
- [Error] L0:C0: Cannot deserialize value of type `java.util.ArrayList<com.huawei.devcloud.cloudpipeline.v2.domain.entity.pac2.gitcode.on.GitcodeScheduleOn>` from Object value (token `JsonToken.START_OBJECT`)
 at [Source: UNKNOWN; byte offset: #UNKNOWN] (through reference chain: com.huawei.devcloud.cloudpipeline.v2.domain.entity.pac2.gitcode.GitcodePipelineDefinition["on"]->com.huawei.devcloud.cloudpipeline.v2.domain.entity.pac2.gitcode.on.GitcodeOn["schedule"])


### YAML 语法错误 (2 cases)

**SEC-WCMD-01-003** — ATOMGIT_ENV 不被不可信输入污染提权
- 维度: security | 优先级: P0 | trigger: workflow_dispatch
- intent_ref: INTENT-SEC-030
- [Error] L0:C0: while scanning a simple key
 in 'string', line 11, column 1:
    INJECTED_VAR=bad" >> $ATOMGIT_ENV
    ^
could not find expected ':'
 in 'string', line 12, column 13:
          - name: Check no injection
                ^


**SEC-WCMD-01-004** — ATOMGIT_OUTPUT 不被不可信输入污染提权
- 维度: security | 优先级: P0 | trigger: workflow_dispatch
- intent_ref: INTENT-SEC-030
- [Error] L0:C0: while scanning a simple key
 in 'string', line 12, column 1:
    hijacked=bad" >> $ATOMGIT_OUTPUT
    ^
could not find expected ':'
 in 'string', line 13, column 13:
          - name: Check no hijack
                ^


**分析**: YAML 语法错误（缩进、引号等）。属于**case bug**。

### 未知字段静默拒绝 (应警告) (1 cases)

**COMP-UNKNOWN-01-001** — 包含未知顶层字段的 workflow 触发 YAML 校验失败
- 维度: completeness | 优先级: P1 | trigger: workflow_dispatch
- intent_ref: INTENT-COMP-002
- [Error] L1:C16: unknown_field: unknown property

**分析**: 未知字段被静默拒绝而非给出警告，测试期待的是'应被报错或警告'，但 case YAML 额外包含了不该有的字段。边界判定：如果 case 本身就是为了测试未知字段的报错，则属于预期行为。

### steps <=16 限制未在文档声明 (1 cases)

**REL-STEPS-01-042** — 超多 step——单 job 内 50 个 step 应全部串行执行无丢失
- 维度: reliability | 优先级: P1 | trigger: workflow_dispatch
- intent_ref: INTENT-REL-042
- [Error] L0:C0: jobs[test].steps: 列表长度必须在0到16之间

**分析**: 文档未声明每 job 最多 16 个 step。属于**文档缺失**。

---

## 五、逐条明细

| # | case_id | status | dimension | trigger | neg/pos | 标题 | 诊断首行 |
|---|---------|--------|-----------|---------|---------|------|---------|
| 1 | COMP-BOUND-01-085 | UNEXPECTED | completeness | schedule | 0/2 | cron 表达式格式与位置边界验证 | on.schedule[0].cron: 不是可识别的cron表达式 |
| 2 | COMP-EXPR-01-058 | UNEXPECTED | completeness | workflow_dispatch | 0/4 | 表达式运算符与优先级边界行为 | jobs[verify].steps[2].if: if表达式无法解析 {0} |
| 3 | COMP-RUNNER-01-003 | UNEXPECTED | completeness | workflow_dispatch | 1/0 | 不存在的标签组合导致 job 排队或失败 | jobs[verify].runs-on: runs-on以数组形式定义时，若为默认资源池则定义为[ |
| 4 | COMP-SCHEDULE-01-001 | UNEXPECTED | completeness | schedule | 0/2 | 合法 cron 在默认分支按时触发 | on.schedule[0].cron: 不是可识别的cron表达式 |
| 5 | COMP-SCHEDULE-01-002 | EXPECTED | completeness | schedule | 1/0 | 非默认分支的 schedule workflow 不应触发 | on.schedule[0].cron: 不是可识别的cron表达式 |
| 6 | COMP-SCHEDULE-01-003 | EXPECTED | completeness | schedule | 1/0 | cron 间隔短于 5 分钟时被拒绝或降级 | on.schedule[0].cron: 不是可识别的cron表达式 |
| 7 | COMP-STAGES-01-001 | UNEXPECTED | completeness | workflow_dispatch | 0/3 | stages 阶段间串行、阶段内 job 并行执行 | Cannot deserialize value of type `java.util.Linked |
| 8 | COMP-STAGES-01-002 | UNEXPECTED | completeness | workflow_dispatch | 1/1 | fail_fast true 时 stage 内任一 job 失败终止 | Cannot deserialize value of type `java.util.Linked |
| 9 | COMP-STAGES-01-003 | UNEXPECTED | completeness | workflow_dispatch | 0/2 | post.run_always true 时 workflow 失败仍 | post.steps: unknown property |
| 10 | COMP-TRIG-01-075 | UNEXPECTED | completeness | schedule | 0/1 | schedule 事件关键字段与 cron 格式验证 | on.schedule[0].cron: 不是可识别的cron表达式 |
| 11 | COMP-UNKNOWN-01-001 | UNEXPECTED | completeness | workflow_dispatch | 0/1 | 包含未知顶层字段的 workflow 触发 YAML 校验失败 | unknown_field: unknown property |
| 12 | COMP-WFLOW-01-065 | UNEXPECTED | completeness | workflow_dispatch | 0/2 | workflow post 后处理阶段字段验证 | post.steps: unknown property |
| 13 | COMPAT-ACTIONDEV-01-001 | UNEXPECTED | compatibility | workflow_dispatch | 0/2 | action.yml 元数据校验与 GitHub 差异 | jobs[test-action-meta].steps[1].uses: 格式错误：pluginn |
| 14 | COMPAT-CONCUR-01-001 | UNEXPECTED | compatibility | workflow_dispatch | 1/2 | concurrency cancel-in-progress fals | concurrency.exceed-action: 值不能为空 |
| 15 | COMPAT-CONCUR-01-002 | EXPECTED | compatibility | workflow_dispatch | 1/1 | concurrency 配置越界或不支持时应给出清晰报错 | Cannot deserialize value of type `java.lang.String |
| 16 | COMPAT-CONCUR-01-003 | UNEXPECTED | compatibility | workflow_dispatch | 1/1 | concurrency preemption enable 行为差异 | concurrency.exceed-action: 值不能为空 |
| 17 | COMPAT-CONCUR-01-004 | UNEXPECTED | compatibility | workflow_dispatch | 0/2 | concurrency preemption events 越界时行为 | concurrency.exceed-action: 值不能为空 |
| 18 | COMPAT-ENVIRON-01-001 | EXPECTED | compatibility | workflow_dispatch | 0/0 | 含 environment 字段的 job 应被报错或警告 | jobs[test].environment: unknown property |
| 19 | COMPAT-ENVIRON-01-002 | UNEXPECTED | compatibility | workflow_dispatch | 1/1 | environment 字段绑定 secrets 的行为差异 | jobs[test-environment].environment: unknown proper |
| 20 | COMPAT-EXPR-01-013 | UNEXPECTED | compatibility | workflow_dispatch | 0/2 | success() 带括号与不带括号的兼容性差异 | jobs[test-success-paren].steps[0].if: if表达式无法解析 表达 |
| 21 | COMPAT-EXPR-01-014 | UNEXPECTED | compatibility | workflow_dispatch | 0/2 | always() 带括号与不带括号的兼容性差异 | jobs[test-always-paren].steps[1].if: if表达式无法解析 表达式 |
| 22 | COMPAT-FIELD-01-001 | EXPECTED | compatibility | workflow_dispatch | 0/0 | 含 run-name 字段的 workflow 应被报错或警告 | run-name: unknown property |
| 23 | COMPAT-FIELD-01-002 | EXPECTED | compatibility | workflow_dispatch | 0/0 | 含 services 字段的 job 应被报错或警告 | jobs[test].services: unknown property |
| 24 | COMPAT-FIELD-01-003 | EXPECTED | compatibility | workflow_dispatch | 1/1 | 未知顶层字段不应被静默忽略而应给出警告 | custom_field: unknown property |
| 25 | COMPAT-MIGRATE-01-001 | EXPECTED | compatibility | workflow_dispatch | 1/1 | GitHub 风格 permissions 块迁移报错应给出可操作指引 | jobs[migrate-permissions].permissions: unknown pro |
| 26 | COMPAT-MIGRATE-01-002 | EXPECTED | compatibility | workflow_dispatch | 1/1 | GitHub 风格 run-name 语法迁移报错应给出可操作指引 | run-name: unknown property |
| 27 | COMPAT-PATHS-01-001 | UNEXPECTED | compatibility | push | 0/2 | paths 过滤器 300 条边界测试 | on.push: 列表长度超出限制，paths paths-ignore之和不能小于1或超过32 |
| 28 | COMPAT-PATHS-01-002 | UNEXPECTED | compatibility | push | 1/0 | paths 过滤器 301 条越界测试 | on.push: 列表长度超出限制，paths paths-ignore之和不能小于1或超过32 |
| 29 | COMPAT-PERM-01-003 | EXPECTED | compatibility | workflow_dispatch | 2/1 | permissions 命名差异——GitHub contents 权 | permissions.contents: unknown property |
| 30 | COMPAT-PR-01-002 | EXPECTED | compatibility | pull_request | 1/0 | pull_request types 命名差异 - GitHub 风格 | on.merge_requests.types: 列表中存在非法值:[opened] 允许值:[cl |
| 31 | COMPAT-PR-01-003 | UNEXPECTED | compatibility | pull_request | 1/1 | PR types 配置后匹配类型不触发与 GitHub 行为差异 | on.merge_requests: 列表长度超出限制，branches branches-igno |
| 32 | COMPAT-PR-01-004 | UNEXPECTED | compatibility | pull_request | 1/1 | PR types 含 merge 时不触发与 GitHub 行为差异 | on.merge_requests: 列表长度超出限制，branches branches-igno |
| 33 | COMPAT-PR-01-005 | UNEXPECTED | compatibility | pull_request | 1/1 | PR paths 过滤不工作时的兼容性差异 | on.merge_requests: 列表长度超出限制，branches branches-igno |
| 34 | COMPAT-RUNNER-01-004 | EXPECTED | compatibility | workflow_dispatch | 0/2 | 自定义特征标签不被支持时应给出可用标签列表 | jobs[test-custom-label].runs-on: runs-on以数组形式定义时，若 |
| 35 | COMPAT-RUNNER-01-005 | UNEXPECTED | compatibility | workflow_dispatch | 1/1 | 内网环境 Runner 不支持时的差异 | jobs[test-intranet].runs-on: runs-on以数组形式定义时，若为默认资 |
| 36 | COMPAT-SCHEDULE-01-001 | UNEXPECTED | compatibility | schedule | 0/2 | schedule cron 按 UTC 时间触发 | Cannot deserialize value of type `java.util.ArrayL |
| 37 | COMPAT-SCHEDULE-01-002 | UNEXPECTED | compatibility | schedule | 1/0 | schedule 不支持 timezone 字段差异 | Cannot deserialize value of type `java.util.ArrayL |
| 38 | COMPAT-SCHEDULE-01-003 | UNEXPECTED | compatibility | schedule | 1/1 | schedule 在非默认分支不触发与 GitHub 差异 | on.schedule[0].cron: 不是可识别的cron表达式 |
| 39 | COMPAT-SECRET-01-005 | UNEXPECTED | compatibility | workflow_dispatch | 1/2 | 环境级 secrets 不支持时应明确报错而非降级为项目级 | jobs[test-env-secret].environment: unknown propert |
| 40 | COMPAT-SHELL-01-003 | UNEXPECTED | compatibility | workflow_dispatch | 0/2 | Windows runner 默认 shell 差异 | jobs[test-windows-shell].runs-on: runs-on以数组形式定义时， |
| 41 | COMPAT-VARS-01-005 | UNEXPECTED | compatibility | workflow_dispatch | 1/1 | vars 在条件表达式 if 中的可用性差异 | jobs[test-vars-if].steps[1].if: if表达式无法解析 表达式：vars |
| 42 | REL-PREEMPT-01-005 | UNEXPECTED | reliability | workflow_dispatch | 0/1 | preemption events 边界值——配置 10 个应正常解析 | concurrency.preemption.events: 列表中存在非法值:[push] 允许值 |
| 43 | REL-PREEMPT-01-006 | EXPECTED | reliability | workflow_dispatch | 0/1 | preemption events 越界值——配置 11 个应被拒绝 | concurrency.preemption.events: 列表中存在非法值:[push] 允许值 |
| 44 | REL-RACE-01-048 | UNEXPECTED | reliability | workflow_dispatch | 0/2 | 取消与 needs 条件竞态——job A 被取消时 job B(if | jobs[job_b].if: if表达式无法解析 表达式：failure()第1位出现不支持的函数 |
| 45 | REL-STAGES-01-029 | UNEXPECTED | reliability | workflow_dispatch | 0/2 | stages fail_fast 机制——阶段内任一 job 失败应立 | Cannot deserialize value of type `java.util.Linked |
| 46 | REL-STEPS-01-042 | UNEXPECTED | reliability | workflow_dispatch | 0/2 | 超多 step——单 job 内 50 个 step 应全部串行执行无 | jobs[test].steps: 列表长度必须在0到16之间 |
| 47 | SEC-DEFPERM-01-002 | UNEXPECTED | security | workflow_dispatch | 1/1 | job 级覆盖后权限正确收窄 | jobs[override-test].permissions: unknown property |
| 48 | SEC-ENV-01-001 | UNEXPECTED | security | workflow_dispatch | 1/1 | 环境级 secret 必须经审批后才能被 workflow 访问 | jobs[env-secret-approved].environment: unknown pro |
| 49 | SEC-ENV-01-002 | UNEXPECTED | security | workflow_dispatch | 1/1 | 环境级 secret 审批前 workflow 不可读取 | jobs[env-secret-denied].environment: unknown prope |
| 50 | SEC-PERM-01-001 | UNEXPECTED | security | workflow_dispatch | 1/1 | 显式声明的 permissions 必须在 job 级实际生效并限制  | jobs[perm-read].permissions: unknown property |
| 51 | SEC-PERM-01-002 | UNEXPECTED | security | workflow_dispatch | 1/1 | permissions 声明 read 时写操作被平台拒绝 | jobs[perm-write-denied].permissions: unknown prope |
| 52 | SEC-SUPPLY-01-003 | UNEXPECTED | security | workflow_dispatch | 1/1 | 第三方 Action 来源应具备信任边界（typosquatting  | jobs[typo-test].steps[0].uses: 格式错误：pluginname@ver |
| 53 | SEC-WCMD-01-003 | UNEXPECTED | security | workflow_dispatch | 1/1 | ATOMGIT_ENV 不被不可信输入污染提权 | while scanning a simple key
 in 'string', line 11, |
| 54 | SEC-WCMD-01-004 | UNEXPECTED | security | workflow_dispatch | 1/1 | ATOMGIT_OUTPUT 不被不可信输入污染提权 | while scanning a simple key
 in 'string', line 12, |
| 55 | USE-CONC-01-002 | EXPECTED | usability | workflow_dispatch | 1/0 | concurrency.max 配置 -1 时报错应提示有效范围 | concurrency.max: 值不能小于1 |
| 56 | USE-EXPR-01-002 | EXPECTED | usability | workflow_dispatch | 1/0 | 调用未知函数时报错应提示函数名错误与修正方向 | jobs[bad].steps[0].if: if表达式无法解析 表达式：unknownFunc() |
| 57 | USE-LBL-01-001 | EXPECTED | usability | workflow_dispatch | 1/0 | runs-on 标签完全不匹配时应给出明确失败原因与可用标签列表 | jobs[bad].runs-on: runs-on以数组形式定义时，若为默认资源池则定义为['co |
| 58 | USE-NEST-01-001 | EXPECTED | usability | workflow_dispatch | 1/0 | workflow_call 嵌套 3 层时报错应明确提示上限为 2 层 | jobs[caller].steps[0].uses: 格式错误：pluginname@versio |
| 59 | USE-NEST-01-002 | UNEXPECTED | usability | workflow_dispatch | 0/1 | workflow_call 嵌套 2 层时应正常执行 | jobs[caller].steps[0].uses: 格式错误：pluginname@versio |
| 60 | USE-PERM-01-002 | EXPECTED | usability | workflow_dispatch | 1/0 | 使用 GitHub 权限域命名时报错应给出 GitCode 对照表 | permissions.contents: unknown property |
| 61 | USE-RUN-01-002 | EXPECTED | usability | workflow_dispatch | 1/0 | 使用单标签 ubuntu-latest 时报错应给出三段式格式指引 | jobs[bad-runner].runs-on: runs-on以数组形式定义时，若为默认资源池则 |
| 62 | USE-STAT-01-002 | EXPECTED | usability | workflow_dispatch | 1/0 | 使用 success() 带括号时报错应提示 GitCode 括号差异 | jobs[bad-stat].steps[0].if: if表达式无法解析 表达式：success( |
| 63 | USE-TYPE-01-002 | EXPECTED | usability | pull_request | 1/0 | 使用 GitHub types 命名 opened/synchroni | on.merge_requests.types: 列表中存在非法值:[opened] 允许值:[cl |
| 64 | USE-UNKN-01-001 | EXPECTED | usability | workflow_dispatch | 0/0 | 未知字段如 run-name 不应被静默忽略而应给出警告或错误 | run-name: unknown property |
| 65 | USE-YAML-01-001 | EXPECTED | usability | workflow_dispatch | 1/0 | 缺少必填字段 on 时报错应指出具体字段名与位置 | on: 值不能为空 |
| 66 | USE-YAML-01-002 | EXPECTED | usability | workflow_dispatch | 1/0 | YAML 缩进错误时报错应指出具体行号与列号 | while parsing a block mapping
 in 'string', line 5 |