# GitCode Actions 校验报告 — 2026-07-23 INVALID 分类

**执行批次**: 2026-07-23-waf-v9
**用例来源**: `phase01/runs/2026-07-23-01/cases/yaml/`
**校验引擎**: `validate_workflow.py` · `POST /api/v2/projects/{project}/actions/valid`
**对照文档**: `phase01/inputs/gitcode-spec/` (GitCode 官方参考文档)

---

## 一、执行摘要

| 指标 | 数值 |
|------|------|
| 校验总数 | 43 |
| ✅ 预期无效（负向用例，已通过设计） | 34 (79.1%) |
| ❌ 意外无效（需修复 YAML） | 9 (20.9%) |
| 数据源 | `phase02/classify-experiment/2026-07-23/INVALID/` |

---

## 二、分类判断逻辑

每条被平台拒绝（INVALID）的用例按以下标准分类：

| 分类 | 判断依据 | 含义 |
|------|---------|------|
| **预期无效** | assertions 含 `type: negative` 或 `target=error_message` | 用例**故意**构造非法 YAML，验证平台能否正确拒绝——这是正确的测试行为 |
| **意外无效（Bug）** | assertions 全为 `type: positive` | 用例**期望** workflow 正常运行，但 YAML 写法违反平台规则——需要修复 |

---

## 三、预期无效 — 34 条（负向用例，正确）

这些用例的 workflow YAML 被平台拒绝是**预期行为**——它们测试平台对非法输入的错误提示质量。

| 序号 | 用例 ID | 标题 | 维度 | 校验错误 |
|:---:|---|---|---|---|
| 1 | COMP-RUNNER-01-003 | 不存在的标签组合导致 job 排队或失败 | completeness | `runs-on` 格式非法 |
| 2 | COMP-STAGES-01-002 | fail_fast true 时 stage 内任一 job 失败终止同阶段其余 job | completeness | `stages` 数组格式不支持 |
| 3 | COMP-UNKNOWN-01-001 | 包含未知顶层字段的 workflow 触发 YAML 校验失败 | completeness | `unknown_field: unknown property` |
| 4 | COMPAT-CONCUR-01-001 | concurrency cancel-in-progress false 时应排队而非报错 | compatibility | `exceed-action` 为空、`max` < 1 |
| 5 | COMPAT-CONCUR-01-002 | concurrency 配置越界或不支持时应给出清晰报错 | compatibility | concurrency 反序列化失败 |
| 6 | COMPAT-ENVIRON-01-001 | 含 environment 字段的 job 应被报错或警告 | compatibility | `environment: unknown property` |
| 7 | COMPAT-FIELD-01-001 | 含 run-name 字段的 workflow 应被报错或警告 | compatibility | `run-name: unknown property` |
| 8 | COMPAT-FIELD-01-002 | 含 services 字段的 job 应被报错或警告 | compatibility | `services: unknown property` |
| 9 | COMPAT-MIGRATE-01-001 | GitHub 风格 permissions 块迁移报错应给出可操作指引 | compatibility | `permissions: unknown property` |
| 10 | COMPAT-MIGRATE-01-002 | GitHub 风格 run-name 语法迁移报错应给出可操作指引 | compatibility | `run-name: unknown property` |
| 11 | COMPAT-PATHS-01-002 | paths 过滤器 301 条越界测试 | compatibility | `paths+paths-ignore` 之和超过 32 |
| 12 | COMPAT-PERM-01-003 | permissions 命名差异——GitHub contents 权限项应报错 | compatibility | `permissions.contents: unknown property` |
| 13 | COMPAT-PR-01-002 | pull_request types 命名差异 - GitHub 风格 types 应报错 | compatibility | `types: [opened]` → 应为 `open` |
| 14 | COMPAT-SCHEDULE-01-002 | schedule 不支持 timezone 字段差异 | compatibility | `schedule` 数组→对象格式错误 |
| 15 | REL-PREEMPT-01-006 | preemption events 越界值——配置 11 个应被拒绝 | reliability | events 长度 > 10、含非法值 `push` |
| 16 | SEC-DEFPERM-01-002 | job 级覆盖后权限正确收窄 | security | `permissions: unknown property` |
| 17 | SEC-ENV-01-001 | 环境级 secret 必须经审批后才能被 workflow 访问 | security | `environment: unknown property` |
| 18 | SEC-ENV-01-002 | 环境级 secret 审批前 workflow 不可读取 | security | `environment: unknown property` |
| 19 | SEC-PERM-01-001 | 显式声明的 permissions 必须在 job 级实际生效并限制 ATOMGIT_TOKEN | security | `permissions: unknown property` |
| 20 | SEC-PERM-01-002 | permissions 声明 read 时写操作被平台拒绝 | security | `permissions: unknown property` |
| 21 | SEC-SUPPLY-01-003 | 第三方 Action 来源应具备信任边界（typosquatting 限制） | security | `uses` 格式错误 + 插件不存在 |
| 22 | SEC-WCMD-01-003 | ATOMGIT_ENV 不被不可信输入污染提权 | security | YAML 解析错误（注入内容含 `"`） |
| 23 | SEC-WCMD-01-004 | ATOMGIT_OUTPUT 不被不可信输入污染提权 | security | YAML 解析错误（注入内容含 `"`） |
| 24 | USE-CONC-01-002 | concurrency.max 配置 -1 时报错应提示有效范围 | usability | `concurrency.max` < 1 |
| 25 | USE-EXPR-01-002 | 调用未知函数时报错应提示函数名错误与修正方向 | usability | `unknownFunc()` 不支持 |
| 26 | USE-LBL-01-001 | runs-on 标签完全不匹配时应给出明确失败原因与可用标签列表 | usability | `runs-on` 格式非法 |
| 27 | USE-NEST-01-001 | workflow_call 嵌套 3 层时报错应明确提示上限为 2 层 | usability | `uses` 格式错误 + 插件不存在 |
| 28 | USE-PERM-01-002 | 使用 GitHub 权限域命名时报错应给出 GitCode 对照表 | usability | `permissions.contents: unknown property` |
| 29 | USE-RUN-01-002 | 使用单标签 ubuntu-latest 时报错应给出三段式格式指引 | usability | `runs-on` 格式非法 |
| 30 | USE-STAT-01-002 | 使用 success() 带括号时报错应提示 GitCode 括号差异 | usability | `success()` 不支持 |
| 31 | USE-TYPE-01-002 | 使用 GitHub types 命名 opened/synchronize 时应给出可理解提示 | usability | `types: [opened]` → 应为 `open` |
| 32 | USE-UNKN-01-001 | 未知字段如 run-name 不应被静默忽略而应给出警告或错误 | usability | `run-name: unknown property` |
| 33 | USE-YAML-01-001 | 缺少必填字段 on 时报错应指出具体字段名与位置 | usability | `on:` 值不能为空 |
| 34 | USE-YAML-01-002 | YAML 缩进错误时报错应指出具体行号与列号 | usability | YAML 缩进解析错误 |

---

## 四、意外无效（Bug）— 9 条需要修复

这些用例的断言全为 `type: positive`（期望 workflow 成功运行），但 YAML 写法违反平台校验规则。

### 4.1 COMP-STAGES-01-001 — `stages` 数组格式不支持

| 项目 | 值 |
|------|-----|
| **用例 ID** | COMP-STAGES-01-001 |
| **标题** | stages 阶段间串行、阶段内 job 并行执行 |
| **维度** | completeness |
| **断言** | `type=positive target=run_status` / `target=stage_order` / `target=job_parallelism` |
| **校验错误** | `Cannot deserialize Map from Array` — `stages:` 必须是 map 格式 `{default: {jobs: {...}}}`，不能是数组 `[{...}]` |
| **修复** | 将 `stages:` 从数组格式改为 map 格式 |

### 4.2 COMP-STAGES-01-003 — `post` 块不支持

| 项目 | 值 |
|------|-----|
| **用例 ID** | COMP-STAGES-01-003 |
| **标题** | post.run_always true 时 workflow 失败仍执行 post |
| **维度** | completeness |
| **断言** | `type=positive target=run_status` / `target=post_logs` |
| **校验错误** | `post.steps: unknown property` / `post.run_always: unknown property` |
| **修复** | GitCode 平台不支持 `post` 块，此测试在当前平台无法执行 |

### 4.3 COMPAT-PATHS-01-001 — paths 超过 32 条限制

| 项目 | 值 |
|------|-----|
| **用例 ID** | COMPAT-PATHS-01-001 |
| **标题** | paths 过滤器 300 条边界测试 |
| **维度** | compatibility |
| **断言** | `type=positive target=run_status` / `target=run_logs` |
| **校验错误** | `on.push: paths+paths-ignore 之和不能超过 32` |
| **修复** | 将 paths 减少到 ≤32 条，或将用例改为负向测试（期望拒绝） |

### 4.4 COMPAT-SCHEDULE-01-001 — `schedule` 对象格式错误

| 项目 | 值 |
|------|-----|
| **用例 ID** | COMPAT-SCHEDULE-01-001 |
| **标题** | schedule cron 按 UTC 时间触发 |
| **维度** | compatibility |
| **断言** | `type=positive target=run_status` / `target=run_event` / `eval=llm_assisted target=run_logs` |
| **校验错误** | `Cannot deserialize Object from Array` — `schedule:` 必须用对象格式 `schedule:\n  - cron: "..."` 而非数组 |
| **修复** | `on:\n  schedule:\n    - cron: "*/5 * * * *"` → `on:\n  schedule:\n      cron: "*/5 * * * *"` |

### 4.5 REL-PREEMPT-01-005 — `preemption.events` 含非法值

| 项目 | 值 |
|------|-----|
| **用例 ID** | REL-PREEMPT-01-005 |
| **标题** | preemption events 边界值——配置 10 个应正常解析 |
| **维度** | reliability |
| **断言** | `type=positive target=run_status` |
| **校验错误** | `preemption.events: [push] 不允许，仅允许 [mr_id]` |
| **修复** | events 从 `[push]` 改为 `[mr_id]`，或改为测试 10 条 `mr_id` |

### 4.6 REL-RACE-01-048 — `failure()` 函数不支持

| 项目 | 值 |
|------|-----|
| **用例 ID** | REL-RACE-01-048 |
| **标题** | 取消与 needs 条件竞态——job A 被取消时 job B(if: failure())应正确判定 |
| **维度** | reliability |
| **断言** | `type=positive target=job_a_status` / `target=job_b_status` |
| **校验错误** | `if 表达式无法解析：failure() 第1位出现不支持的函数` |
| **修复** | 将 `if: failure()` 替换为 `if: always()` 或删除状态门控 |

### 4.7 REL-STAGES-01-029 — `stages` 数组格式不支持

| 项目 | 值 |
|------|-----|
| **用例 ID** | REL-STAGES-01-029 |
| **标题** | stages fail_fast 机制——阶段内任一 job 失败应立即终止同阶段其他 jobs |
| **维度** | reliability |
| **断言** | `type=positive target=job_status` / `target=cancelled_jobs_count` |
| **校验错误** | `Cannot deserialize Map from Array` |
| **修复** | 将 `stages:` 从数组格式改为 map 格式 |

### 4.8 REL-STEPS-01-042 — 50 个 step 超过 16 限制

| 项目 | 值 |
|------|-----|
| **用例 ID** | REL-STEPS-01-042 |
| **标题** | 超多 step——单 job 内 50 个 step 应全部串行执行无丢失 |
| **维度** | reliability |
| **断言** | `type=positive target=step_count` / `target=step_order` |
| **校验错误** | `jobs[test].steps: 列表长度必须在 0 到 16 之间` |
| **修复** | 拆分为多个 job（每个 ≤16 step）或减少 step 数量 |

### 4.9 USE-NEST-01-002 — step 级不支持 `.yml` 工作流路径

| 项目 | 值 |
|------|-----|
| **用例 ID** | USE-NEST-01-002 |
| **标题** | workflow_call 嵌套 2 层时应正常执行 |
| **维度** | usability |
| **断言** | `type=positive target=run_status` |
| **校验错误** | `jobs[caller].steps[0].uses: 格式错误` — step 级 `uses` 不支持 `.yml` 路径 |
| **修复** | 将 `uses: ./.gitcode/workflows/xxx.yml` 从 step 级移到 job 级 |

---

## 五、分维度统计

| 维度 | 总数 | 预期无效 | 意外无效（Bug） |
|------|------|---------|----------------|
| completeness | 4 | 3 | 2 |
| compatibility | 12 | 11 | 2 |
| reliability | 5 | 1 | 4 |
| security | 8 | 8 | 0 |
| usability | 14 | 13 | 1 |
| **合计** | **43** | **34** | **9** |

---

## 六、根因归类

| 根因 | 涉 Bug 用例 | 平台校验错误 | 官方文档 |
|------|-----------|-------------|---------|
| `stages` 数组→map 格式 | COMP-STAGES-01-001, REL-STAGES-01-029 | `Cannot deserialize Map from Array` | `configure-dependencies-order.md` — 同文档展示了 array 和 map 两种格式，未声明 array 不可用 |
| `schedule` 对象→数组格式 | COMPAT-SCHEDULE-01-001 | `Cannot deserialize Object from Array` | `configure-triggers.md` / `trigger-events.md` — 一致使用 array 格式 `schedule:\n  - cron: "..."` |
| `preemption.events` 仅允许 `mr_id` | REL-PREEMPT-01-005 | `列表中存在非法值:[push] 允许值:[mr_id]` | `workflow-file-location-structure.md` — 示例仅 `[mr_id]`，未枚举允许值 |
| `failure()` 函数不支持 | REL-RACE-01-048 | `if表达式无法解析：failure()` | `configure-conditional-execution.md` / `COMPAT-NOTES.md` — GitCode 用 `failed` 无括号，非 `failure()` |
| step 数量 > 16 | REL-STEPS-01-042 | `列表长度必须在 0-16 之间` | `configure-steps.md` — 未提及任何 step 数量限制 |
| paths > 32 | COMPAT-PATHS-01-001 | `paths+paths-ignore 之和不能超过 32` | `configure-triggers.md` — 仅提到 300 文件匹配上限，未提及 32 条限制 |
| `post` 块不支持 | COMP-STAGES-01-003 | `post.steps: unknown property` / `post.run_always: unknown property` | `workflow-job-step-action.md` — 描述了 Post 阶段和 `run_always`，但平台拒绝 |
| step 级 `uses` 不支持 `.yml` | USE-NEST-01-002 | `uses: 格式错误` | `trigger-events.md` — 支持 `uses: ./.gitcode/workflows/xxx.yml` 格式，但应在 job 级非 step 级 |

---

## 七、执行环境

| 项目 | 值 |
|------|-----|
| API Base URL | `https://web-api.gitcode.com` |
| 校验端点 | `POST /api/v2/projects/ComputingActionTest%2Ffoundational-tests/actions/workflows/{id}/valid` |
| 目标仓库 | `ComputingActionTest/foundational-tests` |

---

*报告由 validate_workflow.py 生成 · 2026-07-23*
*规则参照: `phase01/schema/VALIDATION-RULES.md`*
