# 规格分析产出 · GitCode Action（AtomGit Action）能力清单

> 产出 Agent：spec-analyst
> Run：2026-07-21-02
> 来源输入：`inputs/gitcode-spec/`（53 文件，官方文档镜像，fetched 2026-07-20） + `inputs/platform-config/`（README，2026-07-21）
> 用途：本清单为 Parity Matrix 左列来源、各维度 agent 的公共词汇表。**仅客观记录 GitCode 侧事实，不做兼容性判断**（差异判断归 compat-diff）。
> 置信度取值：`明确`（文档有明确声明）｜`模糊`（文档提及但语焉不详/自相矛盾/示例与正文冲突）｜`未知`（文档未涉及，标注待实测）。

---

## 0. 阅读约定

- **出处**：`文件相对路径:行号区间`，均相对 `inputs/gitcode-spec/`；platform-config 项标 `platform-config/README.md:行`。
- **默认值/边界**：显式记录；文档未给的写 `未声明`，并在 §缺口清单登记。
- 分类骨架取自 `testing-focus.md` 关注域（§1 语法解析 / §2 触发器 / §3 执行模型 / §4 Runner 隔离 / §5 Secrets 权限 / §6 注入 / §7 复用供应链 / §8 Artifact/Cache / §9 可观测性 / §12 稳定性配额）。

---

## 1. 结构化能力清单

### 1.1 工作流文件与顶层结构（testing-focus §1）

| # | 能力项 | 语义 | 约束与边界 | 默认值 | 是否可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|---|
| C-STRUCT-01 | 工作流文件目录 | workflow 文件存放于 `.gitcode/workflows/` | 仅识别 `.yml`/`.yaml` 后缀；目录错误则不被识别/触发 | `.gitcode/workflows/` | 否（固定） | `writing-pipelines/workflow-file-location-structure.md:35-41`；`01-quick-start.md:15-23` | 明确 |
| C-STRUCT-02 | 顶层字段集 | 合法顶层字段：`name`/`on`/`env`/`defaults`/`concurrency`/`permissions`/`stages`/`jobs`/`post` | `on` 与 `jobs` 必填（无 stages 时 jobs 顶层，有 stages 时嵌套于 stages 内）；其余可选 | — | 部分必填 | `writing-pipelines/workflow-file-location-structure.md:54-66` | 明确 |
| C-STRUCT-03 | `name` 字段 | workflow 展示名称 | 缺省时使用文件名（`runtime-environment-variables` 称缺省为工作流文件完整路径） | 文件名 | 是 | `workflow-file-location-structure.md:57`；`runtime-environment-variables.md:42` | 模糊（缺省回退值两处表述不一：文件名 vs 完整路径） |
| C-STRUCT-04 | 执行层级模型 | `Event → Workflow → Stages → Jobs → Runner → Steps → Scripts/Actions` | Stages 间串行、Stage 内 Jobs 默认并行、Steps 串行 | — | — | `core-concepts/workflow-job-step-action.md:5-11`；`00-overview.md:41-45` | 明确 |
| C-STRUCT-05 | `stages` 阶段机制 | 顶层阶段编排；阶段间串行，阶段内 job 并行 | 可缺省（单阶段时省略，所有 job 默认并行） | 缺省（无 stages） | 是 | `writing-pipelines/configure-dependencies-order.md:146-194`；`workflow-file-location-structure.md:103-140` | 明确 |
| C-STRUCT-06 | `stages.fail_fast` | 阶段级快速失败：某 job 失败时的处理 | `true`=立即终止本 stage 其他 job 并跳过后续所有 stage；`false`=本 stage 其他 job 继续但后续 stage 不执行 | `未声明`（示例常显式写 true） | 是 | `configure-dependencies-order.md:150-154`；`workflow-file-location-structure.md:105-107` | 模糊（默认值未声明） |
| C-STRUCT-07 | `post` 后处理阶段 | 顶层后处理阶段，流水线达终态后执行 | `run_always: false` 时仅 workflow 成功才执行 | `run_always: true` | 是 | `workflow-file-location-structure.md:142-165,232-234`；`00-overview.md:49` | 明确 |
| C-STRUCT-08 | `defaults.run` | 默认 shell 与 working-directory | 三级优先级 Workflow→Job→Step（低到高） | `未声明`（示例用 bash） | 是 | `configure-steps.md:136-155`；`workflow-file-location-structure.md:78-80` | 模糊（默认 shell 具体值未声明） |
| C-STRUCT-09 | stages 定义写法 | stages 可为列表项（`- name:`）或映射（`stage1:`）两种写法 | 文档多处示例混用两种语法 | — | 是 | `configure-dependencies-order.md:49-73` vs `156-192`；`core-concepts/workflow-job-step-action.md:52-62` | 模糊（两种写法并存，且 workflow-job-step-action.md:22-40 示例 stages 缩进疑似错误） |

### 1.2 触发器与事件（testing-focus §2）

| # | 能力项 | 语义 | 约束与边界 | 默认值 | 是否可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|---|
| C-TRIG-01 | `push` 事件 | 分支/标签推送触发 | 支持 `branches`/`branches-ignore`/`tags`/`tags-ignore`/`paths`/`paths-ignore` 过滤 | — | 是 | `syntax-reference/trigger-events.md:7-49`；`writing-pipelines/configure-triggers.md:33-43` | 明确 |
| C-TRIG-02 | `pull_request` 事件 | PR 创建/更新/合并触发；`branches` 过滤目标分支 | types 取值 `[merge, open, reopen, update]`；使用 PR 源分支代码运行 | types 默认 `[open, reopen, update]` | 是 | `syntax-reference/trigger-events.md:51-83`；`configure-triggers.md:45-71` | 明确 |
| C-TRIG-03 | `pull_request_target` 事件 | PR 触发但运行于 base 分支上下文，可读写目标仓库、访问 secret | 使用目标分支 workflow 文件与权限；fork PR 亦可触发 | types 默认 `[open, reopen, update]` | 是 | `syntax-reference/trigger-events.md:85-102`；`security-permissions/pr-mr-pipeline-security.md:46-78` | 明确 |
| C-TRIG-04 | `issue_comment` 事件 | Issue/PR 评论创建/编辑/删除触发 | 同时对 Issue 与 PR 评论生效；过滤 PR 评论需判断 `atomgit.event.issue_comment.issue.pull_request` | types `未声明默认` | 是 | `syntax-reference/trigger-events.md:104-125` | 模糊（types 默认值未声明） |
| C-TRIG-05 | `pull_request_comment` 事件 | 仅 PR 评论触发（GitCode 特有） | 支持 `branches`（目标分支）与 `comments`（正则内容过滤） | types `未声明默认` | 是 | `syntax-reference/trigger-events.md:127-160` | 模糊（types 默认值未声明；正则引擎/语法未声明） |
| C-TRIG-06 | `workflow_dispatch` 事件 | 手动触发，支持 inputs | inputs 仅 `string` 类型；界面表单选分支触发 | — | 是 | `syntax-reference/trigger-events.md:162-202`；`running-pipelines/manually-trigger-pipeline.md:13-52` | 明确 |
| C-TRIG-07 | `workflow_call` 事件 | 可重用工作流被调用 | 嵌套最多 2 层（可重用工作流不能再调另一个）；inputs 仅 string；可声明 secrets | — | 是 | `syntax-reference/trigger-events.md:204-242`；`configure-triggers.md:105-124` | 明确 |
| C-TRIG-08 | `schedule` 事件 | POSIX cron 定时触发 | 五段式 `分 时 日 月 周`；最短间隔 5 分钟；UTC 时区；仅默认分支生效；有数分钟调度延迟 | — | 是 | `syntax-reference/trigger-events.md:244-275`；`configure-triggers.md:126-141` | 明确 |
| C-TRIG-09 | `branches`/`branches-ignore` 过滤 | 分支白/黑名单，支持通配 `**` 与取反 `!` | 二者不可同时使用；仅否定模式（如 `["!main"]`）不触发 | — | 是 | `configure-triggers.md:159-179,226-241`；`syntax-reference/trigger-events.md:38-49` | 明确 |
| C-TRIG-10 | `paths`/`paths-ignore` 过滤 | 路径白/黑名单，支持通配与取反 | 二者不可同时使用；**匹配前 300 个变更文件**，超出不参与判断 | — | 是 | `configure-triggers.md:181-207`；`platform-config/README.md:26` | 明确 |
| C-TRIG-11 | `tags`/`tags-ignore` 过滤 | 标签白/黑名单 | 二者不可同时使用 | — | 是 | `syntax-reference/trigger-events.md:38-39`；`configure-triggers.md:209-224` | 明确 |
| C-TRIG-12 | 多事件组合 | 同一 workflow 可组合多个触发事件 | — | — | 是 | `configure-triggers.md:142-157`；`core-concepts/trigger-events.md:24-31` | 明确 |
| C-TRIG-13 | 触发调度延迟/去抖 | schedule 声明「数分钟调度延迟」 | 连推去重/幂等行为未声明 | — | — | `configure-triggers.md:138` | 未知（同一 push 连推是否重复触发、并发触发去重未声明） |

### 1.3 执行模型：Job / Step / needs / matrix / 条件 / 并发（testing-focus §3）

| # | 能力项 | 语义 | 约束与边界 | 默认值 | 是否可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|---|
| C-EXEC-01 | `jobs.<id>` 定义 | Stage/顶层内可执行单元，调度到一台 Runner | 核心字段 `stage`/`runs-on`/`needs`/`if`/`env`/`steps`/`timeout-minutes`/`continue-on-error`/`strategy`/`concurrency`/`outputs` | — | 是 | `core-concepts/workflow-job-step-action.md:70-84`；`writing-pipelines/configure-jobs.md` | 明确 |
| C-EXEC-02 | `needs` 依赖 | Job 级 DAG 依赖 | 多依赖并行完成后才执行；依赖 job 失败则当前默认不执行（除非 `if: always`）；支持多依赖汇聚 | — | 是 | `configure-jobs.md:74-95`；`configure-dependencies-order.md:77-144` | 明确 |
| C-EXEC-03 | job 级 `if` 条件 | 推迟整个 job 执行 | if 由平台处理，结果 true 才下发执行环境 | 缺省=`success` | 是 | `configure-jobs.md:97-108`；`runtime-environment-variables.md:88-89` | 明确 |
| C-EXEC-04 | job `timeout-minutes` | job 超时强制终止 | 默认 360 分钟（6 小时） | `360` | 是 | `configure-jobs.md:110-121`；`platform-config/README.md:15` | 明确 |
| C-EXEC-05 | job 级 `env` | job 内所有 step 可见 | 优先级 step>job>workflow | — | 是 | `configure-jobs.md:123-137`；`writing-pipelines/using-variables-secrets.md:63-81` | 明确 |
| C-EXEC-06 | job `outputs` | 从 step 输出映射为 job 输出 | 下游经 `needs.<job>.outputs.<key>` 访问 | — | 是 | `configure-jobs.md:139-150`；`writing-pipelines/pass-output-between-jobs.md:29-44` | 明确 |
| C-EXEC-07 | job `continue-on-error` | job 失败不阻断 workflow | 下游依赖 job 需 `if: always` 才继续 | `false`（隐含） | 是 | `configure-jobs.md:172-197` | 模糊（默认值未显式声明，由语义推断为 false） |
| C-EXEC-08 | `steps` 与类型 | Step 为 job 内最小串行单元 | `run`（脚本）与 `uses`（Action）两类 | — | 是 | `core-concepts/workflow-job-step-action.md:86-104`；`configure-steps.md` | 明确 |
| C-EXEC-09 | step `id` | 唯一标识，供 `steps.<id>.outputs` 引用 | 设置 output 的 step 必须配 id | — | 是 | `configure-steps.md:38-47`；`runtime-environment-variables.md:136` | 明确 |
| C-EXEC-10 | step `shell` | 指定执行 shell | 支持 `bash`/`sh`/`pwsh`/`python` | `未声明默认` | 是 | `configure-steps.md:106-122` | 模糊（默认 shell 未声明；示例注释 `Write-Host` 于 bash 疑似文档错误） |
| C-EXEC-11 | `working-directory` | step 执行工作目录 | 三级优先级 Workflow→Job→Step | `未声明`（仓库根） | 是 | `configure-steps.md:124-155` | 明确 |
| C-EXEC-12 | step `if` / 状态函数 | step 级条件执行 | 支持 `success`/`failed`/`cancelled`/`always`（无括号） | 缺省=`success` | 是 | `configure-steps.md:172-188`；`configure-conditional-execution.md:62-91` | 明确 |
| C-EXEC-13 | step `continue-on-error` | step 失败不致 job 失败，后续 step 继续 | 影响 `steps.<id>.outcome` vs `conclusion` | `false`（隐含） | 是 | `configure-steps.md:190-199`；`syntax-reference/context.md:202-207` | 模糊（默认值未显式声明） |
| C-EXEC-14 | step `timeout-minutes` | step 独立超时 | 默认无独立超时，受 job timeout 控制 | `none`（受 job 控制） | 是 | `configure-steps.md:201-210`；`platform-config/README.md:16` | 明确 |
| C-EXEC-15 | `strategy.matrix` 展开 | 多维矩阵组合生成 job 实例 | 一/二/三维；N×M 笛卡尔积 | — | 是 | `writing-pipelines/configure-matrix-builds.md:44-76` | 明确 |
| C-EXEC-16 | matrix `include` | 追加组合或为组合加额外变量 | 未在基础矩阵定义的变量会被追加 | — | 是 | `configure-matrix-builds.md:78-92` | 明确 |
| C-EXEC-17 | matrix `exclude` | 排除特定组合 | — | — | 是 | `configure-matrix-builds.md:94-108` | 明确 |
| C-EXEC-18 | `strategy.fail-fast` | 矩阵级快速失败 | `true`=一实例失败即取消其余；与 `stages.fail_fast` 不同层面 | `未声明默认` | 是 | `configure-matrix-builds.md:110-121` | 模糊（默认值未声明；GitHub 惯例为 true 但 GitCode 未写） |
| C-EXEC-19 | `strategy.max-parallel` | 限制矩阵并发实例数 | 不设时「取决于 Runner 可用数量」，无固定上限 | 未设=取决 Runner 数 | 是 | `configure-matrix-builds.md:123-129`；`platform-config/README.md:31` | 明确 |
| C-EXEC-20 | matrix 动态 `runs-on` | runs-on 可引用 matrix 变量 | — | — | 是 | `configure-matrix-builds.md:131-143` | 明确 |
| C-EXEC-21 | workflow 级 `concurrency` | 限制同一 workflow 并行运行数 | `max` 范围 1-5；`exceed-action` = IGNORE/QUEUE | — | 是 | `workflow-file-location-structure.md:167-188`；`platform-config/README.md:10-12` | 明确 |
| C-EXEC-22 | `concurrency.preemption` | 抢占策略 | `preemption.events` 最多 10 个 | `preemption.enable: true` | 是 | `workflow-file-location-structure.md:176-188`；`platform-config/README.md:12` | 模糊（preemption 语义仅示例，抢占触发条件与效果未详述） |
| C-EXEC-23 | job 级 `concurrency` | job 级并发控制 | 同字段 enable/max/exceed-action | — | 是 | `configure-jobs.md:152-166` | 明确 |
| C-EXEC-24 | 取消语义 | 手动停止 / 抢占取消运行中 step | post 阶段/action post 在停止时被调用清理 | — | — | `action-development/top-level-fields.md:122-144`；`action-development/plugin-development-guide.md:119-139` | 模糊（step 级取消如何终止、清理钩子保证程度未系统声明） |

### 1.4 表达式、上下文与变量（testing-focus §1 表达式 / §10）

| # | 能力项 | 语义 | 约束与边界 | 默认值 | 是否可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|---|
| C-EXPR-01 | `${{ }}` 表达式 | 在 if/赋值/参数处求值 | 支持字面量 bool/null/number/string（单引号） | — | — | `syntax-reference/expressions.md:3-15` | 明确 |
| C-EXPR-02 | 运算符集 | `==`/`!=`/`!`/`&&`/`||`/`>`/`<`/`>=`/`<=` | 优先级：`()`→`!`→比较→等值→`&&`→`||` | — | — | `syntax-reference/expressions.md:17-30` | 明确 |
| C-EXPR-03 | 状态函数 | `success`/`always`/`cancelled`/`failed`（无括号） | if 缺省条件为 success | — | — | `syntax-reference/expressions.md:36-39,50-54`；`core-concepts/variables-secrets-context-expressions.md:46-54` | 明确 |
| C-EXPR-04 | 字符串/集合函数 | `contains`/`startsWith`/`endsWith`/`format`/`substring`/`replace`/`hashFiles`/`toJson` | `substring(str,start,len)`、`replace(str,old,new)` 为 GitCode 列出项；startsWith/endsWith 区分大小写；contains 支持子串与数组元素 | — | — | `syntax-reference/expressions.md:40-58` | 明确（边界行为如空值/类型转换未详述→见缺口） |
| C-EXPR-05 | `atomgit` 上下文 | 平台与事件核心信息 | 属性含 event_name/sha/ref/ref_name/ref_type/event/workspace/token/repository/run_id/run_number/run_attempt/head_ref/base_ref/server_url/api_url 等 | — | — | `syntax-reference/context.md:23-49` | 明确 |
| C-EXPR-06 | `atomgit.event` 事件负载 | 各事件的 payload 字段 | push/pull_request/issue_comment/workflow_dispatch/schedule 分别列字段；引用不存在属性求值为空字符串 | — | — | `syntax-reference/context.md:50-113`；`runtime-environment-variables.md:74` | 明确 |
| C-EXPR-07 | 12 种上下文 | atomgit/env/vars/secrets/job/jobs/steps/runner/strategy/matrix/inputs | 各上下文可用位置不同（见可用性表） | — | — | `syntax-reference/context.md:5-21,275-292` | 明确（正文称 12 种，表仅列 11 行→见缺口） |
| C-EXPR-08 | 上下文可用性矩阵 | 不同位置（workflow/job/step/if/action）可用上下文不同 | 如 job/runner/steps/matrix/strategy 在 workflow 级不可用 | — | — | `syntax-reference/context.md:275-292` | 明确 |
| C-EXPR-09 | `steps.<id>.outcome`/`conclusion` | continue-on-error 前/后的步骤结果 | outcome=应用前，conclusion=应用后 | — | — | `syntax-reference/context.md:194-207` | 明确 |
| C-EXPR-10 | `runner` 上下文 | os/arch/name/temp/tool_cache/debug | os∈Linux/Windows/macOS；arch∈X64/ARM/ARM64 | — | — | `syntax-reference/context.md:209-228` | 明确 |
| C-VAR-01 | 四级变量体系 | `env`/`vars`/`secrets`/`inputs` | env 三级作用域；vars/secrets 组织+项目（+环境级 secret）；inputs 仅 string | — | 是 | `writing-pipelines/using-variables-secrets.md:54-121`；`00-overview.md:62-68` | 明确 |
| C-VAR-02 | env 优先级 | step>job>workflow | 同名 step 级覆盖 job/workflow 级 | — | 是 | `using-variables-secrets.md:81`；`syntax-reference/variables.md:64-72` | 明确 |
| C-VAR-03 | 变量总优先级 | step env>job env>workflow env>vars>系统变量(ATOMGIT_*) | — | — | — | `using-variables-secrets.md:140-145` | 明确 |
| C-VAR-04 | `ATOMGIT_*` 系统变量 | Runner 自动注入的系统环境变量全集 | 含 TOKEN/SHA/REF/REF_NAME/REF_TYPE/EVENT_NAME/EVENT_PATH/WORKSPACE/REPOSITORY/RUN_ID/RUN_NUMBER/RUN_ATTEMPT/HEAD_REF/BASE_REF/SERVER_URL/API_URL/GRAPHQL_URL/OUTPUT/ENV/PATH/STEP_SUMMARY 等 | — | 否（系统） | `syntax-reference/variables.md:74-108`；`action-development/runtime-environment-variables.md:6-52` | 明确 |
| C-VAR-05 | `RUNNER_*` 系统变量 | RUNNER_ARCH/ENVIRONMENT/NAME/OS/TEMP/TOOL_CACHE | ENVIRONMENT∈gitcode-hosted/self-hosted | — | 否 | `runtime-environment-variables.md:47-52` | 明确 |
| C-VAR-06 | `CI` / `ATOMGIT_ACTIONS` | CI 恒为 true；ATOMGIT_ACTIONS 运行时为 true | 用于区分本地/平台运行 | `true` | 否 | `runtime-environment-variables.md:11,15` | 明确 |
| C-VAR-07 | inputs 类型限制 | workflow_dispatch/workflow_call inputs 仅 string | 数字/布尔需表达式转换 | — | 是 | `syntax-reference/variables.md:56-62`；`manually-trigger-pipeline.md:54-67` | 明确 |
| C-VAR-08 | 系统变量键位不一致 | `RUNNER_OS/ARCH` vs `ATOMGIT_RUNNER_OS/ARCH` | 两文档给出不同前缀命名 | — | 否 | `using-variables-secrets.md:136-138` vs `runtime-environment-variables.md:47-50` | 模糊（同一含义两套变量名，文档不一致） |

### 1.5 Runner 与运行环境（testing-focus §4）

| # | 能力项 | 语义 | 约束与边界 | 默认值 | 是否可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|---|
| C-RUN-01 | 官方托管三段式标签 | `{os-version},{arch},{flavor}` | os∈ubuntu-latest/ubuntu-24/ubuntu-22/euler-25（多文档并集）；arch∈x64/arm64；flavor 6 档 | — | 是 | `core-concepts/runner-and-environment.md:7-15`；`runner-management/using-hosted-runners.md:9-21`；`platform-config/README.md:44-49` | 明确（os 取值各文档不一，取并集） |
| C-RUN-02 | `runs-on: default` | 默认标签快捷值 | 等价 `[ubuntu-latest, x64, small]`（2核8G50G） | `[ubuntu-latest,x64,small]` | 是 | `runner-management/selecting-runner-labels.md:33-35`；`using-hosted-runners.md:61-69` | 明确 |
| C-RUN-03 | 资源规格 6 档 | slim/small/medium/large/xlarge/2xlarge | 1核4G20G ~ 32核128G1T；**托管默认仅提供 slim/small/medium，large 及以上需申请客服** | 默认 small | 是 | `runner-and-environment.md:19-28`；`using-hosted-runners.md:23-34`；`syntax-reference/runner-images-tools.md:22-33` | 明确 |
| C-RUN-04 | runs-on 多种写法 | 数组 `[ubuntu-latest,x64,small]` / 花括号 `{ubuntu-24,x64,small}` / `default` / 自托管映射 | 文档示例三种写法混用 | — | 是 | `configure-jobs.md:35-65`；`using-hosted-runners.md:38-58` | 模糊（数组式与花括号式并存，是否等价未声明） |
| C-RUN-05 | 标签匹配规则 | runs-on 所有标签须为 Runner 标签集合子集（全匹配） | 自托管须含 `self-hosted` | — | — | `selecting-runner-labels.md:19-31`；`syntax-reference/runner-images-tools.md:76-93` | 明确 |
| C-RUN-06 | 自托管 Runner | 主机 / Kubernetes 两类 | 主机固定 1 Runner 不伸缩；K8s 支持 min/max 弹性伸缩 | K8s min=max=1（不伸缩） | 是 | `runner-management/using-self-hosted-runners.md`；`platform-config/README.md:61-81` | 明确 |
| C-RUN-07 | 自托管前置环境 | 主机需外网访问 + Java8 + Git + Docker | 支持自动安装 JDK/Git/Docker/重启免注册 | 四选项默认勾选 | 是 | `using-self-hosted-runners.md:37-52`；`platform-config/README.md:68` | 明确 |
| C-RUN-08 | Runner 注册级别 | 组织级 / 项目级 | 组织级服务所有项目（可限指定项目）；项目级仅本项目 | — | 是 | `using-self-hosted-runners.md:177-184`；`platform-config/README.md:80` | 明确 |
| C-RUN-09 | `container` 自定义镜像 | job 在指定 Docker 镜像内运行 | 字段 image/credentials/env/volumes/options | — | 是 | `runner-management/configuring-images-toolchains.md:9-52` | 明确 |
| C-RUN-10 | container 私有镜像认证 | credentials 引用 secret | username/password | — | 是 | `configuring-images-toolchains.md:26-43`；`security-permissions/using-secrets.md:49-60` | 明确 |
| C-RUN-11 | 预装工具链 | Ubuntu 24.04 预装语言/构建/CI/云工具 | Python3.10-3.12/Node18-22/Go1.21-1.23/Java8-21/Ruby/PHP/Rust/.NET；Maven/Gradle/npm/pip/yarn/pnpm；git/jq/yq/shellcheck/kubectl/helm/aws-cli | — | 否（随镜像变） | `syntax-reference/runner-images-tools.md:36-62`；`using-hosted-runners.md:92-98` | 模糊（两文档版本列表不一致，且「随镜像更新变化」） |
| C-RUN-12 | Runner 生命周期/隔离 | 主机 Runner 同主机多 Job 共享环境；K8s Pod 独立隔离 | 是否 ephemeral、复用残留污染未系统声明 | — | — | `using-self-hosted-runners.md:144-153` | 未知（托管 Runner 是否一次性、跨 job 残留未声明；`RUNNER_TEMP` 每 job 起止清空是唯一线索，见 `runtime-environment-variables.md:51`） |
| C-RUN-13 | 网络出站 | 声明「有访问外网权限」 | 内网/DNS/代理策略未声明 | 允许外网 | — | `platform-config/README.md:97` | 模糊（仅一句，出站范围/限制未详） |
| C-RUN-14 | 资源边界与超限行为 | flavor 规定 CPU/内存/磁盘 | 超限（OOM/磁盘满）行为未声明 | 见 flavor 表 | — | `runner-and-environment.md:19-28`；`platform-config/README.md:50-57` | 未知（超配额行为未声明） |

### 1.6 Secrets 与权限（testing-focus §5，安全命脉）

| # | 能力项 | 语义 | 约束与边界 | 默认值 | 是否可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|---|
| C-SEC-01 | Secret 作用域 | 组织级 / 项目级 / 环境级 | 项目级覆盖组织级；环境级绑定部署环境可配审批人 | — | 是 | `security-permissions/using-secrets.md:14-25,63-71`；`syntax-reference/variables.md:39-48` | 明确 |
| C-SEC-02 | Secret 命名规则 | `${{ secrets.NAME }}` 引用 | 仅大写字母/数字/下划线；不得以 `ATOMGIT_` 开头；不得数字开头 | — | 是 | `using-secrets.md:43-48` | 明确 |
| C-SEC-03 | Secret 日志脱敏 | 值在日志自动替换为 `***` | **文档自承 `echo "${{ secrets.X }}"` 可能绕过脱敏**；不应依赖脱敏作为安全边界 | 自动开启 | 否 | `syntax-reference/variables.md:48`；`using-variables-secrets.md:116-120`；`runtime-environment-variables.md:208` | 明确（脱敏可被绕过为明确声明的弱点） |
| C-SEC-04 | Secret 不可查看 | 创建后无法界面查看原值，仅可更新覆盖 | — | — | — | `using-secrets.md:63-70` | 明确 |
| C-SEC-05 | Fork Secret 隔离 | `pull_request` 来自 fork 不可访问项目/组织 Secret | 需 secret 时用 `pull_request_target` | — | 否（隔离固定） | `using-secrets.md:68-71`；`security-permissions/pr-mr-pipeline-security.md:42-44` | 明确 |
| C-SEC-06 | `ATOMGIT_TOKEN` 自动令牌 | 每次运行自动生成，用于 clone/push/PR/Issue 评论/操作资源 | 仅运行期有效，运行后失效；勿持久化 | — | 否（自动） | `security-permissions/token-permissions.md:11-20`；`syntax-reference/variables.md:108` | 明确 |
| C-SEC-07 | `permissions` 权限域 | `project`/`pr`/`issue`/`note`/`repository`/`hook`，值 read/write/none | 顶层默认，job 级可覆盖 | 未声明时用仓库设置权限 | 是 | `token-permissions.md:24-47`；`workflow-file-location-structure.md:189-211` | 明确 |
| C-SEC-08 | permissions 快捷语法 | `read-all`/`write-all`/`{}` | `{}` = 全 none（最小权限，文档另称 repository:read） | — | 是 | `workflow-file-location-structure.md:212-224`；`token-permissions.md:99-104` | 模糊（`{}` 到底全 none 还是仅 repository:read，两处表述冲突） |
| C-SEC-09 | Fork Token 降权 | `pull_request` 来自 fork 时 TOKEN 仅 read，无视 permissions 声明 | 安全隔离机制，强制降权 | read | 否 | `token-permissions.md:105`；`pr-mr-pipeline-security.md:8-16,40-42` | 明确 |
| C-SEC-10 | pull_request vs _target 安全模型 | 代码来源/Token 权限/Secret 可达性/workflow 文件版本/checkout 默认来源 五维差异 | _target 用 base 分支 workflow 文件，PR 提交者无法改执行逻辑；显式 checkout head.sha 执行=高权限跑不可信代码（注入点） | — | — | `pr-mr-pipeline-security.md:7-78` | 明确 |
| C-SEC-11 | `::add-mask::` 命令 | 运行时对日志敏感值遮掩 | 未废弃（对比 set-output 等已废弃） | — | 是 | `writing-pipelines/using-script-commands.md:84-96`；`syntax-reference/workflow-commands.md:70` | 明确 |
| C-SEC-12 | container credentials Secret | 私有镜像/registry 登录用 secret | — | 是 | `using-secrets.md:49-60` | 明确 |
| C-SEC-13 | `ATOMGIT_REF_PROTECTED` | 触发 ref 有分支保护/规则集则为真 | — | — | 否 | `runtime-environment-variables.md:28` | 明确 |
| C-SEC-14 | 环境保护规则 | 环境级 secret 可配审批人 | reviewers/wait timer 细节未详 | — | 是 | `using-secrets.md:70` | 模糊（仅提「可配审批人」，机制未详） |

### 1.7 脚本命令、Action 复用与供应链（testing-focus §6/§7）

| # | 能力项 | 语义 | 约束与边界 | 默认值 | 是否可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|---|
| C-ACT-01 | `run` 脚本命令 | 执行 shell，单行/多行 | 需先 checkout 才能跑仓库脚本；脚本可能无执行权限 | — | 是 | `writing-pipelines/using-script-commands.md:12-46` | 明确 |
| C-ACT-02 | 工作流命令文件协议 | `ATOMGIT_OUTPUT`/`ATOMGIT_ENV`/`ATOMGIT_PATH`/`ATOMGIT_STEP_SUMMARY` | 必须 `>>` 追加；当前 step 写入后续 step 生效；每 step 路径唯一 | — | 是 | `syntax-reference/workflow-commands.md:7-58`；`runtime-environment-variables.md:95-208` | 明确 |
| C-ACT-03 | 废弃命令 | `::set-output`/`::set-env`/`::add-path` 已废弃 | 改用 `>> $ATOMGIT_*` 文件协议 | — | — | `workflow-commands.md:60-68` | 明确（但 `plugin-development-guide.md:66` 仍示例 `::set-output`，见缺口） |
| C-ACT-04 | step 输出上限 | `ATOMGIT_OUTPUT` 每参数最大 1MB | 超限行为未声明 | 1MB/参数 | — | `pass-output-between-jobs.md:23`；`platform-config/README.md:29` | 明确（上限明确，超限行为未知） |
| C-ACT-05 | 三级输出传递 | step→job→workflow_call 输出 | 多行用随机 delimiter | — | 是 | `pass-output-between-jobs.md:16-49`；`runtime-environment-variables.md:149-165` | 明确 |
| C-ACT-06 | `uses` 三种引用 | 官方短名 / `owner/repo/path@ref` / 本仓 `./path` | 本地 action 需 `action.yml` | — | 是 | `writing-pipelines/using-actions.md:30-91` | 明确 |
| C-ACT-07 | Action 版本引用 | Tag `@v4` / 完整 `@v4.1.0` / 分支 `@main` / SHA `@a1b2c3d` | 文档给推荐度：SHA 生产推荐，@main 不推荐 | — | 是 | `using-actions.md:94-100` | 明确 |
| C-ACT-08 | 内置官方 action | checkout/setup-node/setup-java/setup-go/setup-python/cache/upload-artifact/download-artifact | 无 owner 短名引用 | — | 是 | `using-actions.md:44-50`；examples 各文件 | 明确 |
| C-ACT-09 | checkout 参数 | `ref`/`fetch-depth` | PR 场景常 checkout `head.sha` | — | 是 | `pr-mr-pipeline-security.md:61-64`；`examples/pr-code-check-example.md:31-35` | 明确 |
| C-ACT-10 | setup-* 参数 | node-version/java-version+distribution/go-version/python-version + cache | cache 值 npm/maven/pip 等 | — | 是 | `examples/nodejs-ci.md`、`java-maven-ci.md:40-45`、`go-ci.md:41-45`、`python-ci.md:38-42` | 明确（仅由示例观察，无独立参数规格页） |
| C-ACT-11 | Action 元数据 `action.yml` | 插件核心配置 | 强制命名 `action.yml`（大小写敏感）；YAML 格式 | — | 是 | `action-development/action-yml-metadata-syntax.md:31-37`；`top-level-fields.md` | 明确 |
| C-ACT-12 | action `runs.using` | 执行运行时 | 文档仅列 `node16`（唯一列出值） | — | 是 | `action-yml-metadata-syntax.md:25-28`；`top-level-fields.md:94-100`；`using-actions.md:88` | 明确（仅 node16，无 docker/composite） |
| C-ACT-13 | action `runs.post` | 终止时清理入口 | 主动停止调度调用 / 自然调用需 main 内监听 SIGINT | — | 是 | `top-level-fields.md:110-144` | 明确 |
| C-ACT-14 | action inputs 环境变量 | 生成 `INPUT_<NAME>` 环境变量 | 名转大写、空格转 `_`；`required:true` 缺失不自动报错，需代码校验 | — | 是 | `top-level-fields.md:41-70` | 明确 |
| C-ACT-15 | action 版本号规范 | 语义化 `X.Y.Z` | 只增不回退；不含字母（预发布标识 -alpha/-beta/-rc 例外） | — | 是 | `action-yml-metadata-syntax.md:39-53` | 明确 |
| C-ACT-16 | 插件安全规范 | 敏感数据禁硬编码、经安全输入、加密、及时清理、输入校验 | 面向插件开发者的规范（非平台强制约束） | — | — | `action-development/plugin-security-specification.md` | 明确 |
| C-ACT-17 | 插件打包 | ncc 打包为单文件 js，`dist/` 产物 | 推荐 TypeScript；`@actions/core` 等 toolkit | — | 是 | `action-development/plugin-packaging.md`；`plugin-project-structure.md`；`plugin-development-guide.md:30-36` | 明确 |

### 1.8 Artifact 与 Cache（testing-focus §8）

| # | 能力项 | 语义 | 约束与边界 | 默认值 | 是否可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|---|
| C-ART-01 | upload-artifact | 上传构建产物跨 job 传递 | `name`（workflow 内唯一）+`path`（必填，支持 glob/多路径）；`retention-days` 可配 | — | 是 | `writing-pipelines/upload-download-artifacts.md:49-77`；examples | 明确 |
| C-ART-02 | download-artifact | 下载制品 | `name` 必填、`path` 选填（默认当前工作目录）；不指定 name 下载全部 | path 默认当前目录 | 是 | `upload-download-artifacts.md:79-103` | 明确 |
| C-ART-03 | 制品保留期 | 可设定保留天数 | 默认 90 天（platform-config）；`ATOMGIT_RETENTION_DAYS` 暴露 | 90 天 | 是 | `platform-config/README.md:86-89`；`runtime-environment-variables.md:34` | 明确（示例用 7/30 天，默认 90） |
| C-ART-04 | 制品大小上限 | 文档仅称「已确认不超过限制」 | 具体数值未公开 | — | — | `upload-download-artifacts.md:10`；`platform-config/README.md:34` | 未知（无具体上限值） |
| C-ART-05 | cache 插件 | key 精确匹配 + restore-keys 前缀兜底 | path/key 必填，restore-keys 选填；未命中则 step 后保存新缓存 | — | 是 | `writing-pipelines/using-dependency-cache.md:41-66` | 明确 |
| C-ART-06 | 缓存作用域/淘汰 | 同仓库所有运行共享；长期保留 LRU 淘汰 | 容量上限未公开 | — | — | `core-concepts/artifacts-and-cache.md:36-42`；`platform-config/README.md:35,91-93` | 明确（策略明确，容量上限未知） |
| C-ART-07 | 多路径缓存 | path 支持多路径 | hashFiles 多参数生成 key | — | 是 | `using-dependency-cache.md:68-79` | 明确 |

### 1.9 可观测性与结果契约（testing-focus §9）

| # | 能力项 | 语义 | 约束与边界 | 默认值 | 是否可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|---|
| C-OBS-01 | 运行状态徽标 | ✅成功/❌失败/🟡运行中/⏸取消/🔶跳过 | Actions 页/Commits/PR Checks 三入口 | — | — | `running-pipelines/view-run-results.md:9-27` | 明确 |
| C-OBS-02 | 运行详情结构 | 按 stages→jobs→steps→post 纵向排列 | fail_fast 导致 stage 跳过 | — | — | `view-run-results.md:29-68` | 明确 |
| C-OBS-03 | 日志查看 | 逐 step 标准输出/错误 | 折叠/搜索/下载（UTF-8）；`***` 遮掩不可查看原值 | — | — | `running-pipelines/view-job-logs.md:9-83` | 明确 |
| C-OBS-04 | Step Summary | Markdown 写入 `ATOMGIT_STEP_SUMMARY` | `>>`追加 `>`覆盖；step 完成后上传，后续 step 不能改；多 job 按完成时间展示 | — | 是 | `syntax-reference/workflow-commands.md:49-58`；`runtime-environment-variables.md:186-200` | 明确 |
| C-OBS-05 | 状态徽标嵌入 | README badge SVG | `.../badges/{workflow}/pipeline.svg` | — | 是 | `view-run-results.md:71-76` | 明确 |
| C-OBS-06 | 重新运行 | Re-run all / Re-run failed jobs | 最多重试 3 次；超 6 小时不可重跑；用原始 commit 配置与参数；RUN_ID 不变、RUN_NUMBER 更新（另一文档称 RUN_ID 也更新→冲突） | — | 是 | `running-pipelines/rerun-failed-jobs.md:11-47`；`platform-config/README.md:18-21` | 模糊（RUN_ID 重跑是否变，rerun-failed-jobs.md:25 与 runtime-environment-variables.md:36 冲突） |
| C-OBS-07 | 手动触发操作 | Actions 页 Run workflow 按钮 | 仅含 workflow_dispatch 的 workflow 显示；用所选分支的 workflow 文件 | — | — | `manually-trigger-pipeline.md:69-115` | 明确 |
| C-OBS-08 | 日志上下文展开 | atomgit.* / ATOMGIT_* 在日志展开实际值 | 引用 `atomgit.actor`（context 页未列该属性，见缺口） | — | — | `view-job-logs.md:37-69` | 模糊（`atomgit.actor` 被示例引用但未在 context.md 属性表列出） |

### 1.10 稳定性配额与限额（testing-focus §12，来源 platform-config）

| # | 能力项 | 语义 | 约束与边界 | 默认值 | 是否可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|---|
| C-QUOTA-01 | workflow 并发上限 | concurrency.max | 范围 1-5 | — | 是 | `platform-config/README.md:10-11` | 明确 |
| C-QUOTA-02 | 抢占事件上限 | preemption.events ≤ 10 | — | — | 是 | `platform-config/README.md:12` | 明确 |
| C-QUOTA-03 | job 默认超时 | 360 分钟（6 小时） | 超时强制终止 | 360 | 是 | `platform-config/README.md:15` | 明确 |
| C-QUOTA-04 | 重跑限制 | 最多 3 次；超 6 小时不可重跑 | — | — | 否 | `platform-config/README.md:19-20` | 明确 |
| C-QUOTA-05 | paths 匹配上限 | 前 300 个变更文件 | 超出不参与判断 | 300 | 否 | `platform-config/README.md:26` | 明确 |
| C-QUOTA-06 | step 输出上限 | 每参数 1MB | — | 1MB | 否 | `platform-config/README.md:29` | 明确 |
| C-QUOTA-07 | 账户/仓库级全局并发 | 仅有单 workflow concurrency.max=1-5 | 无账户/仓库级全局并发上限声明 | — | — | `platform-config/README.md:30` | 未知（文档未公开） |
| C-QUOTA-08 | 矩阵组合数上限 | 未声明 | 仅示例展开算法，无组合数上限 | — | — | `platform-config/README.md:32`；`configure-matrix-builds.md` | 未知 |
| C-QUOTA-09 | 日志/制品/缓存/文件大小/secret 数上限 | 均未公开 | max_log_size / max_artifact_size / max_cache_size / max_workflow_file_size / max_secrets_per_repo 全未公开 | — | — | `platform-config/README.md:33-37` | 未知（5 项配额缺口） |

---

## 2. 规格缺口 / 存疑清单

> 标注：类型（`默认值缺失`/`边界未知`/`文档自相矛盾`/`语焉不详`/`能力未声明`）、影响维度、下游消费方。维度取值见 rules §1.1。

### 2.1 默认值缺失（default 未显式声明）

| G# | 缺口 | 关联能力项 | 影响维度 | 下游消费方 | 出处 |
|---|---|---|---|---|---|
| G-01 | `stages.fail_fast` 默认值未声明 | C-STRUCT-06 | compatibility, reliability | compat-diff, reliability | `configure-dependencies-order.md:150-154` |
| G-02 | `strategy.fail-fast` 默认值未声明（GitHub 惯例 true） | C-EXEC-18 | compatibility, reliability | compat-diff, reliability | `configure-matrix-builds.md:110-121` |
| G-03 | 默认 `shell` 未声明（step/defaults） | C-EXEC-10, C-STRUCT-08 | compatibility, usability | compat-diff, usability | `configure-steps.md:106-122` |
| G-04 | `continue-on-error` 默认值（job/step）仅可由语义推断为 false | C-EXEC-07, C-EXEC-13 | compatibility | compat-diff | `configure-jobs.md:172-197` |
| G-05 | `issue_comment`/`pull_request_comment` 的 types 默认值未声明 | C-TRIG-04, C-TRIG-05 | completeness, compatibility | compat-diff, spec-analyst | `syntax-reference/trigger-events.md:104-160` |
| G-06 | 未声明 permissions 时的「仓库设置默认权限」具体范围未给 | C-SEC-07 | security, compatibility | security, compat-diff | `token-permissions.md:99-104` |

### 2.2 边界/超限行为未知

| G# | 缺口 | 关联能力项 | 影响维度 | 下游消费方 | 出处 |
|---|---|---|---|---|---|
| G-07 | 制品大小上限无具体值 | C-ART-04 | reliability | reliability | `upload-download-artifacts.md:10` |
| G-08 | 缓存容量上限无具体值（仅 LRU） | C-ART-06 | reliability | reliability | `artifacts-and-cache.md:36-42` |
| G-09 | 日志/workflow 文件大小/单仓 secret 数上限未公开 | C-QUOTA-09 | reliability, usability | reliability | `platform-config/README.md:33-37` |
| G-10 | 矩阵组合数上限未声明 | C-QUOTA-08 | reliability | reliability | `platform-config/README.md:32` |
| G-11 | 账户/仓库级全局并发上限未声明（仅单 workflow max 1-5） | C-QUOTA-07 | reliability | reliability | `platform-config/README.md:30` |
| G-12 | step 输出超 1MB 的行为（截断/报错）未声明 | C-ART-04 | reliability, usability | reliability, usability | `pass-output-between-jobs.md:23` |
| G-13 | Runner 资源超限（OOM/磁盘满）行为未声明 | C-RUN-14 | reliability | reliability | `platform-config/README.md:50-57` |
| G-14 | 网络出站范围（内网/DNS/代理）未详 | C-RUN-13 | reliability, security | reliability, security | `platform-config/README.md:97` |

### 2.3 隔离/安全语义未系统声明

| G# | 缺口 | 关联能力项 | 影响维度 | 下游消费方 | 出处 |
|---|---|---|---|---|---|
| G-15 | 托管 Runner 是否 ephemeral、跨 job 残留污染未声明（仅 RUNNER_TEMP 每 job 清空） | C-RUN-12 | security, reliability | security, reliability | `using-self-hosted-runners.md:144-153`；`runtime-environment-variables.md:51` |
| G-16 | Secret 脱敏可被 `echo "${{ secrets.X }}"` 绕过（明确弱点，需负向验证脱敏对 base64/拼接/多行变形的覆盖） | C-SEC-03 | security | security | `using-variables-secrets.md:116-120` |
| G-17 | `pull_request_target` + checkout head.sha 执行不可信代码的注入面（文档自承风险，未给防护约束） | C-SEC-10 | security | security | `pr-mr-pipeline-security.md:72-78` |
| G-18 | `pull_request_comment` 的 comments 正则引擎/语法/注入面未声明 | C-TRIG-05 | security, compatibility | security, compat-diff | `syntax-reference/trigger-events.md:153-160` |
| G-19 | fork PR 的 cache 作用域是否与主分支隔离未声明（cache 声明「同仓库所有运行共享」，含 fork PR？→投毒面） | C-ART-06 | security, reliability | security, reliability | `artifacts-and-cache.md:36-42` |
| G-20 | 环境保护规则（reviewers/wait timer）机制未详 | C-SEC-14 | security, usability | security, usability | `using-secrets.md:70` |

### 2.4 文档自相矛盾 / 一致性问题（易用性线索）

| G# | 缺口 | 关联能力项 | 影响维度 | 下游消费方 | 出处 |
|---|---|---|---|---|---|
| G-21 | `permissions: {}` 语义冲突：一处称全 none，一处称 repository:read | C-SEC-08 | security, usability | security, usability | `workflow-file-location-structure.md:216-223` vs `token-permissions.md:103` |
| G-22 | 重跑后 `ATOMGIT_RUN_ID` 是否变化：rerun 页称更新，运行时变量页称重跑不变 | C-OBS-06 | usability, reliability | usability, reliability | `rerun-failed-jobs.md:25` vs `runtime-environment-variables.md:36` |
| G-23 | 系统变量 `RUNNER_OS/ARCH` 与 `ATOMGIT_RUNNER_OS/ARCH` 两套命名并存 | C-VAR-08 | usability, compatibility | usability, compat-diff | `using-variables-secrets.md:136-138` vs `runtime-environment-variables.md:47-50` |
| G-24 | 废弃 `::set-output` 与插件开发指南示例仍用 `::set-output var=` 冲突（且语法 `var=` 与正文 `name=` 不一致） | C-ACT-03 | usability | usability | `plugin-development-guide.md:66` vs `workflow-commands.md:60-68` |
| G-25 | `name` 缺省回退值：一处文件名、一处工作流文件完整路径 | C-STRUCT-03 | usability | usability | `workflow-file-location-structure.md:57` vs `runtime-environment-variables.md:42` |
| G-26 | stages 两种写法（列表 `- name:` vs 映射 `stage1:`）并存，等价性/正确性未澄清；workflow-job-step-action.md:22-40 示例缩进疑似错误 | C-STRUCT-09 | usability, compatibility | usability, compat-diff | `configure-dependencies-order.md:49-73,156-192` |
| G-27 | runs-on 数组式 `[..]` 与花括号式 `{..}` 并存，是否等价未声明 | C-RUN-04 | usability, compatibility | compat-diff, usability | `configure-jobs.md:35-65` vs `using-hosted-runners.md:38-58` |
| G-28 | `atomgit.actor`/`atomgit.actor_id` 被 example/日志页引用，但 context.md 属性表未列 | C-OBS-08, C-EXPR-05 | completeness, usability | spec-analyst, compat-diff | `view-job-logs.md:42` vs `syntax-reference/context.md:23-49` |
| G-29 | 上下文正文称 12 种，可用性表仅列 11 行（缺 1 种，疑 `env` 或 `job`/`jobs` 计数差异） | C-EXPR-07 | completeness | spec-analyst, compat-diff | `syntax-reference/context.md:5,275-292` |
| G-30 | 托管 Runner 预装工具链两文档版本列表不一致（Node 18/20 vs 18/20/22 等） | C-RUN-11 | usability, compatibility | compat-diff, usability | `runner-images-tools.md:36-62` vs `using-hosted-runners.md:92-98` |
| G-31 | runtime-environment-variables.md 夹带 GitHub 残留措辞（octocat/Hello-World、actions/checkout 等示例值） | C-VAR-04 | usability | usability | `runtime-environment-variables.md:14,30-32` |
| G-32 | os 取值各文档不一（using-hosted 列 ubuntu-latest/24/22；runner-and-environment 列 ubuntu-24/euler-25） | C-RUN-01 | completeness, compatibility | compat-diff, reliability | `platform-config/README.md:46-47` |

### 2.5 能力未声明（表达式/事件边界）

| G# | 缺口 | 关联能力项 | 影响维度 | 下游消费方 | 出处 |
|---|---|---|---|---|---|
| G-33 | 表达式函数（contains/format/hashFiles/toJson 等）空值处理、类型转换、边界行为未详述 | C-EXPR-04 | compatibility | compat-diff | `syntax-reference/expressions.md:40-58` |
| G-34 | 同一 push 连推的触发去重/幂等、并发触发排队公平性未声明 | C-TRIG-13 | reliability | reliability | `configure-triggers.md:138` |
| G-35 | 非法 YAML / 未知字段处理（报错 vs 静默忽略）未声明——报错质量与兼容性高发区 | C-STRUCT-02 | usability, compatibility | usability, compat-diff | 全文档未涉及 |
| G-36 | `jobs` 上下文（可重用工作流 job 输出）具体可用性与 workflow_call outputs 映射细节未详（pass-output 页为摘要待勘误） | C-EXEC-06, C-EXPR-07 | completeness | compat-diff | `pass-output-between-jobs.md:2,45` |

---

## 3. Intent（针对「规格声明本身需被验证」的点）

> 定位：这些不是完整覆盖，而是 spec-analyst 视角下「文档如此声明、但声明本身可疑或需实测坐实」的验证意图。维度按 rules §1.1；ID 用 `INTENT-COMP-NNN`。
> 展开归 case-writer；优先级线索因 L0 risk-register 为模板态，暂标注对齐存疑（见各条）。

```
意图 ID:    INTENT-COMP-001
维度标签:   [completeness, reliability]
标题:       验证托管 Runner 声明的 6 档规格与实际可用性一致（尤其 large 及以上「需申请」）

风险点:     文档一面列全 6 档规格（slim~2xlarge），一面注明「托管默认仅 slim/small/medium，large 及以上需咨询客服」。规格声明与实际可用池不一致，用户按文档写 large 标签可能排不到 Runner。
预期系统行为: 请求 slim/small/medium 可正常调度；请求未开通的 large+ 应有明确、可操作的报错（而非无限排队/静默失败）。
Oracle 来源: GitCode规格（using-hosted-runners.md:34 的「需申请」声明）

验证要点:
  - [正向] slim/small/medium 三档标签能成功分配 Runner 并运行。
  - [负向] 未申请时请求 large/xlarge/2xlarge 不应静默挂起无反馈。
  - [非功能] 排不到 Runner 时应在合理时限内给出可理解报错。

故障/压力参数: 分别提交 6 档 flavor 的最小 job；观察调度结果与超时/报错时限。
优先级线索: 无法对齐（risk-register 模板态）；价值在于坐实容量声明，建议门禁据 testing-focus §4/§12 定级。
来源输入:   inputs/gitcode-spec/runner-management/using-hosted-runners.md（fetched 2026-07-20）；platform-config/README.md（2026-07-21）
```

```
意图 ID:    INTENT-COMP-002
维度标签:   [completeness, reliability]
标题:       验证 concurrency.max 声明的取值范围 1-5 与越界拒绝行为

风险点:     platform-config 与文档均声明 concurrency.max 范围 1-5，但未声明 max=0、max=6、非整数等越界值的处理。规格若不校验，可能导致不可预期的并发行为。
预期系统行为: max∈[1,5] 生效；越界值应被校验层拒绝并给出明确报错，而非静默取边界或放行。
Oracle 来源: GitCode规格（workflow-file-location-structure.md:185；platform-config/README.md:11）

验证要点:
  - [正向] max=1 与 max=5 均按声明限制并发。
  - [负向] max=6 / max=0 / max=abc 不应被静默接受产生未定义并发。
  - [非功能] exceed-action=QUEUE 时超额运行排队、IGNORE 时被忽略，行为与声明一致。

故障/压力参数: 并发提交超过 max 的运行数（如 max=2 时并发 5 次触发），观察 QUEUE/IGNORE 分流。
优先级线索: 无法对齐（risk-register 模板态）；testing-focus §12 稳定性。
来源输入:   inputs/gitcode-spec/writing-pipelines/workflow-file-location-structure.md；platform-config/README.md
```

```
意图 ID:    INTENT-COMP-003
维度标签:   [completeness, reliability]
标题:       验证 paths 过滤「仅匹配前 300 个变更文件」的边界声明

风险点:     文档声明 paths 匹配前 300 个变更文件、超出不参与判断。若一次提交变更 > 300 文件，第 301+ 个匹配 paths 的文件将不触发——这是易被忽略、可能导致「该触发却没触发」的静默边界。
预期系统行为: 变更文件数 ≤300 时 paths 精确判断；>300 时按声明只看前 300，且此截断行为可被观测/文档化。
Oracle 来源: GitCode规格（configure-triggers.md:186；platform-config/README.md:26）

验证要点:
  - [正向] 300 以内命中 paths 的变更正常触发。
  - [负向] 仅第 301+ 个文件命中 paths（前 300 不命中）时，按声明不触发——确认截断真实存在且一致。
  - [非功能] 截断发生时是否有任何提示（日志/文档），评估可理解性。

故障/压力参数: 构造单次 push 变更 350 个文件，命中 paths 的文件分别置于第 1-300 与第 301+ 位。
优先级线索: 无法对齐（risk-register 模板态）；testing-focus §2/§12。
来源输入:   inputs/gitcode-spec/writing-pipelines/configure-triggers.md；platform-config/README.md
```

```
意图 ID:    INTENT-COMP-004
维度标签:   [completeness, compatibility]
标题:       验证 workflow_call 嵌套「最多 2 层」的声明与超限拒绝

风险点:     文档声明可重用工作流嵌套最多 2 层（不能再套一层）。未声明第 3 层调用时的具体行为（报错？截断？）。深层复用编排常见，需坐实上限与越界反馈。
预期系统行为: 2 层嵌套正常执行；第 3 层调用应被明确拒绝并给出可操作报错。
Oracle 来源: GitCode规格（configure-triggers.md:124；syntax-reference/trigger-events.md:204）

验证要点:
  - [正向] A→B（1 层）与 A→B→C（2 层）可重用工作流链正常运行。
  - [负向] A→B→C→D（3 层）不应静默执行或产生不可预期行为，应报错。
  - [非功能] 超限报错信息应指明「嵌套超过 2 层」而非泛化失败。

对齐方向:   差异确认（GitCode 显式限 2 层，GitHub 上限不同，此处仅验证 GitCode 侧声明成立）
优先级线索: 无法对齐（risk-register 模板态）；testing-focus §7。
来源输入:   inputs/gitcode-spec/writing-pipelines/configure-triggers.md
```

```
意图 ID:    INTENT-COMP-005
维度标签:   [completeness, security]
标题:       验证 inputs「仅支持 string 类型」声明——非 string 定义的处理

风险点:     文档反复声明 workflow_dispatch/workflow_call 的 inputs 仅支持 string。若用户按 GitHub 习惯写 `type: boolean`/`choice`/`number`，规格未声明是报错还是静默降级为 string——影响迁移正确性与参数语义安全（如布尔被当字符串 'false' 仍为真值）。
预期系统行为: type: string 正常；非 string 类型应被明确处理（报错或文档化的降级规则），不产生静默的语义误判。
Oracle 来源: GitCode规格（syntax-reference/variables.md:56-62；manually-trigger-pipeline.md:54）

验证要点:
  - [正向] type: string 的 inputs 按声明工作，默认值/required 生效。
  - [负向] type: boolean/number/choice 不应被静默接受却按字符串语义误用（如 'false' 在 if 中判真）。
  - [非功能] 非法 type 的报错应可指引用户改用 string + 表达式转换。

负向断言目标: 布尔/数字语义不应因静默转字符串而被误判为真值；判定证据=条件分支实际走向。
优先级线索: 无法对齐（risk-register 模板态）；testing-focus §1/§11。
来源输入:   inputs/gitcode-spec/syntax-reference/variables.md；running-pipelines/manually-trigger-pipeline.md
```

```
意图 ID:    INTENT-COMP-006
维度标签:   [completeness, usability]
标题:       验证 permissions:{} 的实际权限——澄清「全 none」vs「repository:read」矛盾

风险点:     两份文档对 `permissions: {}` 给出冲突定义：workflow-file-location-structure 称「所有权限设为 none」，token-permissions 称「仅拥有最小默认权限 repository:read」。这直接影响最小权限模式下 job 能否 clone 代码，是安全+易用双敏感点。
预期系统行为: `permissions: {}` 有唯一确定的实际权限集，且与至少一处文档一致；能据此判定 checkout 是否可用。
Oracle 来源: 差异声明（两处 GitCode 文档冲突，需实测确立权威值回写 Parity Matrix）

验证要点:
  - [正向] 设 `permissions: {}` 后，可确定 ATOMGIT_TOKEN 的实际权限集。
  - [负向] 不应出现「文档 A 说 none 但实际能 clone」这类与声明背离且无记录的行为。
  - [非功能] 实测结果应能消解文档矛盾，供 usability 出文档勘误、compat-diff 定 oracle。

可理解性判据: 最终以实测权限为准；文档矛盾本身作为 usability 缺陷记录（关联 G-21）。
优先级线索: 无法对齐（risk-register 模板态）；testing-focus §5/§11。
来源输入:   inputs/gitcode-spec/writing-pipelines/workflow-file-location-structure.md:216-223；security-permissions/token-permissions.md:103
```

```
意图 ID:    INTENT-COMP-007
维度标签:   [completeness, reliability, usability]
标题:       验证重跑后 ATOMGIT_RUN_ID 是否变化——澄清两文档冲突声明

风险点:     rerun-failed-jobs.md 称重跑时 RUN_ID 与 RUN_NUMBER 均更新为新值；runtime-environment-variables.md 称 RUN_ID 重新运行不变、仅 RUN_ATTEMPT 递增。RUN_ID 语义（是否跨重跑稳定）影响用户以 RUN_ID 做幂等键/追踪的正确性。
预期系统行为: RUN_ID 有唯一确定语义（跨重跑稳定或变化二选一），与其中一处文档一致，RUN_ATTEMPT 每次重跑递增。
Oracle 来源: 差异声明（两处 GitCode 文档冲突，需实测定权威）

验证要点:
  - [正向] 触发一次运行并重跑，记录 RUN_ID/RUN_NUMBER/RUN_ATTEMPT 前后值。
  - [负向] RUN_ID 语义不应在文档间含糊到用户无法据其做幂等键。
  - [非功能] 实测消解矛盾，供 usability 勘误。

故障/压力参数: 对同一运行执行 Re-run failed jobs 与 Re-run all jobs 各一次，比对三个变量。
优先级线索: 无法对齐（risk-register 模板态）；testing-focus §9。
来源输入:   inputs/gitcode-spec/running-pipelines/rerun-failed-jobs.md:25；action-development/runtime-environment-variables.md:35-37
```

```
意图 ID:    INTENT-COMP-008
维度标签:   [completeness, compatibility]
标题:       验证状态函数无括号写法（success/failed/cancelled/always）为唯一合法形式

风险点:     GitCode 文档全程用无括号状态函数（`if: ${{ success }}`），且失败函数名为 `failed`（非 GitHub 的 failure()）。需坐实：带括号 `success()` 是否报错、`failure()` 是否不被识别——直接影响从 GitHub 迁移的 workflow 行为正确性。
预期系统行为: 无括号 `success`/`failed`/`cancelled`/`always` 按声明求值；GitHub 式 `success()`/`failure()` 应有确定处理（报错或不识别），不应静默恒真/恒假。
Oracle 来源: GitCode规格（expressions.md:36-54；configure-conditional-execution.md:66-72）

验证要点:
  - [正向] `if: ${{ failed }}` 在前置失败时为真、成功时为假。
  - [负向] `if: ${{ success() }}`（带括号）或 `${{ failure() }}` 不应被静默当作恒真/未知而错误放行或跳过。
  - [非功能] 非法表达式报错应指明状态函数应无括号。

对齐方向:   差异确认（GitCode 语法与 GitHub 有意不同，验证 GitCode 侧声明成立）
负向断言目标: GitHub 式带括号写法不应产生与用户预期相反的默认求值。
优先级线索: 无法对齐（risk-register 模板态）；testing-focus §1/§10。
来源输入:   inputs/gitcode-spec/syntax-reference/expressions.md；writing-pipelines/configure-conditional-execution.md
```

---

## 4. 交接说明

- **回流 Parity Matrix**：§1 的 133 条能力项（C-* 前缀）即 Parity Matrix 左列候选；建议按分类（触发器/执行模型/表达式/Runner/安全/Action/Artifact/可观测/配额）填入，「GitCode 支持状态」列由后续人+agent 确认。
- **给 compat-diff**：所有标 `模糊`/`未知` 且影响 compatibility 的能力项 + §2.4 文档矛盾，是差异确认高价值种子（与 COMPAT-NOTES.md 互补，本清单只记 GitCode 侧事实，未做对齐判断）。
- **给 security**：C-SEC-*、G-15~G-20 为安全命脉（fork 隔离、脱敏绕过、_target 注入、cache 投毒）。
- **给 reliability**：C-QUOTA-*、G-07~G-14 为配额边界源头；多项上限「未公开·待实测」需 reliability 设计探测用例。
- **给 usability**：§2.4 十余条文档自相矛盾/GitHub 残留措辞，是迁移摩擦与文档质量 intent 来源。
- **输入版本**：gitcode-spec fetched 2026-07-20；platform-config 2026-07-21。若刷新需按 rules §12 重审带该来源标注的项。
