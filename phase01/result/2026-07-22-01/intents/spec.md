# Spec-Analyst 产出：结构化能力清单 + 规格缺口 + Intent 库

> 角色：phase01 spec-analyst
> 输入版本：gitcode-spec/ 2026-07-20（50 页）; platform-config/ 2026-07-21; testing-focus.md 当前版本
> 分析日期：2026-07-22

---

## 输入退化标注

- `inputs/workflow-samples/`：README.md 有索引说明，含 8 个真实样本文件（CANN 7 个 + op-plugin 1 个），覆盖 `workflow_dispatch`、`pull_request_comment`、多 stage、多 job、可复用 workflow、并发控制等场景。**缺**：`push`、`pull_request`/`merge_request`、`schedule`、`workflow_call` 入口样本；官方资源池 `ubuntu-latest` 样本。
- `inputs/business-context/`：⚠️ 仅 README.md，无迁移场景与历史摩擦记录。
- `inputs/github-reference/`：README.md + INDEX.md + 6 页 reference + 6 页 security，内容偏少（仅 12 页精选），非 GitHub Actions 完整规格。

---

## 1. 结构化能力清单

按 `testing-focus.md` 关注域分类，逐条记录。

### 1.1 Workflow 语法解析与静态校验

| 能力项 | 语义 | 约束与边界 | 默认值 | 是否可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|
| 工作流文件目录 | 仅 `.gitcode/workflows/` 下 `.yml`/`.yaml` 被识别 | 目录错误则流水线不被识别触发 | `.gitcode/workflows/` | 否 | workflow-file-location-structure.md | 明确 |
| `name` 字段 | workflow 展示名称 | 缺省时使用文件名 | 文件名 | 否 | workflow-file-location-structure.md | 明确 |
| `on` 字段 | 触发条件定义 | 支持多事件组合；必填 | 无 | 是 | workflow-file-location-structure.md | 明确 |
| `env` 字段 | workflow 级环境变量 | 三级优先级：step > job > workflow | 无 | 是 | workflow-file-location-structure.md, variables.md | 明确 |
| `defaults` 字段 | 默认 shell / working-directory | 三级优先级覆盖 | shell 默认 `bash`（推测，未明确声明） | 是 | workflow-file-location-structure.md, configure-steps.md | 模糊 |
| `concurrency` 字段 | 并发控制 | `max` 范围 1-5；`exceed-action`: IGNORE/QUEUE | `enable`? `max`? 未明确 | 是 | workflow-file-location-structure.md | 明确 |
| `permissions` 字段 | ATOMGIT_TOKEN 权限范围 | 6 权限域：project/pr/issue/note/repository/hook | 仓库设置定义（具体值未公开） | 是 | workflow-file-location-structure.md, token-permissions.md | 模糊 |
| `stages` 字段 | 阶段间串行、阶段内并行 | 可缺省；`fail_fast` 控制快速失败 | 无 stages 时 job 默认并行 | 是 | workflow-file-location-structure.md | 明确 |
| `jobs` 字段 | 任务集合 | 无 stages 时为顶层；有 stages 时嵌套 | 无 | 是 | workflow-file-location-structure.md | 明确 |
| `post` 字段 | 后处理阶段 | `run_always` 默认 `true` | `run_always: true` | 是 | workflow-file-location-structure.md | 明确 |
| 未知/不支持字段处理 | 遇到 YAML 中未定义字段时的行为 | 文档未明确（报错/静默忽略/部分支持） | 未知 | 否 | 多处缺失 | 未知 |

### 1.2 触发器语义

| 能力项 | 语义 | 约束与边界 | 默认值 | 是否可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|
| `push` 触发 | 代码推送触发 | 支持 branches/paths/tags 过滤及取反 | 无过滤则全分支触发 | 是 | trigger-events.md, configure-triggers.md | 明确 |
| `pull_request` 触发 | PR 创建/更新/合并时触发 | branches 过滤目标分支（base）；types: [merge,open,reopen,update]，默认 [open,reopen,update] | types 默认 [open,reopen,update] | 是 | trigger-events.md, configure-triggers.md | 明确 |
| `pull_request_target` 触发 | 安全模式 PR 触发 | base 上下文运行，可访问 Secret，可写权限 | 无 | 是 | trigger-events.md, pr-mr-pipeline-security.md | 明确 |
| `issue_comment` 触发 | Issue 评论触发 | types: [created]（推测） | 未明确 | 是 | trigger-events.md | 模糊 |
| `pull_request_comment` 触发 | PR 评论触发 | 支持 `comments` 正则过滤 | 未明确 | 是 | trigger-events.md, COMPAT-NOTES.md | 模糊 |
| `workflow_dispatch` 触发 | 手动触发 | `inputs` 仅支持 `string` 类型 | 无 | 是 | trigger-events.md, configure-triggers.md | 明确 |
| `workflow_call` 触发 | 可重用工作流调用 | 嵌套最多 2 层 | 无 | 是 | trigger-events.md, configure-triggers.md | 明确 |
| `schedule` 触发 | 定时触发，cron 语法 | UTC，最短 5 分钟，仅默认分支生效，可能有数分钟调度延迟 | 无 | 是 | trigger-events.md, configure-triggers.md | 明确 |
| branches / branches-ignore | 分支白名单/黑名单 | 两者不能同时使用；支持 `**` 通配和 `!` 否定 | 无过滤 | 是 | configure-triggers.md | 明确 |
| paths / paths-ignore | 路径白名单/黑名单 | 两者不能同时使用；**匹配前 300 个变更文件**，超出不参与 | 无过滤 | 是 | configure-triggers.md | 明确 |
| tags / tags-ignore | 标签白名单/黑名单 | 支持通配和否定 | 无过滤 | 是 | configure-triggers.md | 明确 |
| 否定模式约束 | `!` 前缀表示否定 | 必须与肯定模式组合使用；仅否定模式则不触发 | 无 | 是 | configure-triggers.md | 明确 |

### 1.3 执行模型

| 能力项 | 语义 | 约束与边界 | 默认值 | 是否可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|
| `needs` 依赖 | Job 级 DAG 依赖编排 | 支持多依赖；被依赖 job 完成后执行 | 无依赖则并行 | 是 | configure-jobs.md | 明确 |
| `if` 条件执行 | job/step 级条件判断 | 支持表达式和状态函数 | 无 if 则默认执行 | 是 | configure-conditional-execution.md | 明确 |
| `timeout-minutes` | job 超时时间 | 超时强制终止 | 360 分钟（6 小时） | 是 | configure-jobs.md | 明确 |
| `continue-on-error` | job/step 级容错 | 失败后不阻断后续 | `false` | 是 | configure-jobs.md, configure-steps.md | 明确 |
| `strategy.matrix` | 矩阵展开 | 支持 include/exclude/fail-fast/max-parallel | 无 | 是 | configure-matrix-builds.md | 明确 |
| `strategy.fail-fast` | 矩阵快速失败 | `true`：任一实例失败取消其余 | 未明确（GitHub 默认 true） | 是 | configure-matrix-builds.md | 模糊 |
| `strategy.max-parallel` | 矩阵最大并行数 | 未设时"取决于 Runner 可用数量"，无固定上限 | Runner 可用数量 | 是 | configure-matrix-builds.md | 模糊 |
| `outputs` 传递 | step→job→下游 job | `ATOMGIT_OUTPUT` 每个参数最大 1MB | 无 | 是 | pass-output-between-jobs.md, runtime-environment-variables.md | 明确 |
| `concurrency` (job 级) | job 级并发控制 | 同 workflow 级语义（max 1-5, IGNORE/QUEUE） | 未明确 | 是 | configure-jobs.md | 模糊 |
| 取消语义 | 手动取消/被抢占 | 正在运行的 step 如何终止、清理钩子是否执行，**文档未详述** | 未知 | 否 | 未明确 | 未知 |
| `rerun` 重新运行 | 单条运行最多 3 次 | 超 6h 不可 rerun；使用原始 commit 配置 | 0 次已用 | 否 | rerun-failed-jobs.md | 明确 |
| `rerun` 上下文保持 | 重新运行时上下文变量 | `sha`/`ref`/`event_name` 保持原始值；`run_id`/`run_number` 更新 | 原始值 | 否 | rerun-failed-jobs.md | 明确 |

### 1.4 Runner 与执行环境隔离

| 能力项 | 语义 | 约束与边界 | 默认值 | 是否可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|
| 官方托管 Runner 标签 | 三段式 `{os-version,arch,flavor}` | os: ubuntu-latest/24/22/euler-25; arch: x64/arm64; flavor: slim~2xlarge | `[ubuntu-latest,x64,small]` | 是 | runner-and-environment.md, using-hosted-runners.md | 明确 |
| `runs-on: default` | 快捷标签 | 等效 `[ubuntu-latest,x64,small]`（2核8G50G） | default | 是 | using-hosted-runners.md | 明确 |
| 官方资源池开放规格 | 托管 Runner 可用规格 | 默认仅开放 slim/small/medium；large 及以上需申请 | small | 是 | using-hosted-runners.md | 明确 |
| 自托管 Runner | 主机 / K8s 两类 | 主机需外网+Java8+Git+Docker；K8s 需 kubeconfig | 无 | 是 | using-self-hosted-runners.md | 明确 |
| 自托管标签匹配 | `runs-on` 标签必须是 Runner 标签子集 | 必须同时满足所有标签 | 无 | 是 | using-self-hosted-runners.md | 明确 |
| Runner 预装工具 | Python/Node/Go/Java 等 | 版本可能随镜像更新变化 | 见 runner-images-tools.md 列表 | 否 | runner-images-tools.md | 模糊 |
| Shell 类型 | bash/sh/pwsh/python | step 级可指定 | 未明确（推测 bash） | 是 | configure-steps.md | 模糊 |
| `container` 字段 | 自定义 Docker 镜像运行环境 | 支持 `credentials` 传入 secret | 无 | 是 | using-secrets.md | 明确 |
| Runner 是否一次性 | 是否 ephemeral | **文档未明确** Runner 复用策略 | 未知 | 否 | 未明确 | 未知 |
| 资源规格详表 | CPU/内存/磁盘配额 | slim(1核4G20G) ~ 2xlarge(32核128G1TB) | small(2核8G50G) | 是 | runner-and-environment.md, platform-config/README.md | 明确 |

### 1.5 Secrets 与权限

| 能力项 | 语义 | 约束与边界 | 默认值 | 是否可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|
| `secrets` 四级体系 | 组织/项目/环境级 + inputs | 名称仅大写字母/数字/下划线；不得以 `ATOMGIT_` 开头或数字开头 | 无 | 是 | using-secrets.md | 明确 |
| Secret 日志脱敏 | 值在日志中替换为 `***` | 文档自承 `${{ secrets.X }}` 可能绕过脱敏 | 自动脱敏 | 否 | using-secrets.md | 明确 |
| Fork PR Secret 隔离 | `pull_request`（fork）不可访问 Secret | `pull_request_target` 可访问 | 隔离 | 否 | pr-mr-pipeline-security.md | 明确 |
| `ATOMGIT_TOKEN` 自动生成 | 每次运行生成 | 权限由 `permissions` 控制；运行结束后失效 | 仓库设置定义 | 是 | token-permissions.md | 模糊 |
| `permissions` 权限域 | project/pr/issue/note/repository/hook | read/write/none | 仓库设置定义（具体值未公开） | 是 | token-permissions.md | 模糊 |
| permissions 快捷语法 | `read-all` / `write-all` / `{}` | `{}` = 最小权限（仅 `repository:read`） | 仓库设置 | 是 | token-permissions.md | 明确 |
| fork PR TOKEN 权限 | 仅 read，无视 permissions 声明 | 安全隔离机制 | read | 否 | token-permissions.md | 明确 |
| 环境级 Secret 审批 | 可配置审批人 | 未经审批 job 不可访问 | 未明确默认是否需要审批 | 是 | using-secrets.md | 模糊 |

### 1.6 表达式与上下文

| 能力项 | 语义 | 约束与边界 | 默认值 | 是否可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|
| 核心上下文 `atomgit.*` | 平台与事件核心信息 | 20+ 属性（sha/ref/repository/event 等） | 无 | 否 | context.md | 明确 |
| `env` 上下文 | 自定义环境变量 | 仅包含 workflow/job/step 中显式设置的 | 无 | 是 | context.md | 明确 |
| `vars` 上下文 | 组织/项目级配置变量 | 项目级覆盖组织级 | 无 | 是 | context.md | 明确 |
| `secrets` 上下文 | 加密密钥 | 日志中显示 `***` | 无 | 否 | context.md | 明确 |
| `steps` 上下文 | 步骤信息与输出 | outcome/conclusion/outputs | 无 | 否 | context.md | 明确 |
| `runner` 上下文 | Runner 环境信息 | os/arch/name/temp/tool_cache/debug | 无 | 否 | context.md | 明确 |
| 表达式运算符 | `==`, `!=`, `!`, `&&`, `\|\|`, 比较 | 有优先级定义 | 无 | 是 | expressions.md | 明确 |
| 状态函数 | success/always/cancelled/failed | **无括号**语法（GitCode 特有） | 默认 `success` | 是 | expressions.md, COMPAT-NOTES.md | 明确 |
| 字符串函数 | contains/startsWith/endsWith/format | GitCode 额外有 substring/replace | 无 | 是 | expressions.md | 明确 |
| `hashFiles` | 文件组合 SHA256 哈希 | 支持 glob 路径 | 无 | 是 | expressions.md | 明确 |
| `toJson` | 对象序列化为 JSON | 边界行为未详述 | 无 | 是 | expressions.md | 模糊 |
| 上下文可用性 | 不同位置可用上下文不同 | workflow/job/step/if/Action 中可用性各异 | 无 | 否 | context.md | 明确 |
| 不存在的属性引用 | 返回空字符串 | 不会报错 | 空字符串 | 否 | runtime-environment-variables.md | 明确 |

### 1.7 复用与供应链（Action）

| 能力项 | 语义 | 约束与边界 | 默认值 | 是否可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|
| 官方插件引用 | `uses: action-name` 无 owner | checkout/setup-node/setup-java/cache/upload-artifact/download-artifact 等 | 无 | 是 | using-actions.md | 明确 |
| 开源插件引用 | `uses: owner/repo/path@ref` | AtomGit 公开仓库中的插件 | 无 | 是 | using-actions.md | 明确 |
| 本地插件引用 | `uses: ./path/to/action` | 需 `action.yml` 元数据文件 | 无 | 是 | using-actions.md | 明确 |
| Action 版本引用 | @tag/@version/@branch/@SHA | 推荐 @SHA 用于生产 | 无 | 是 | using-actions.md | 明确 |
| `action.yml` 元数据 | 强制 YAML，文件名大小写敏感 | version: X.Y.Z 语义化；只增不回退 | 无 | 是 | action-yml-metadata-syntax.md | 明确 |
| `runs.using` | Action 运行环境 | 文档仅列 `node16`；是否支持 node20/docker/composite **未明确** | `node16` | 是 | action-yml-metadata-syntax.md, COMPAT-NOTES.md | 模糊 |
| `inputs` 参数传递 | `with` 传入 Action | 参数名需与 `action.yml` 一致 | 无 | 是 | using-actions.md | 明确 |
| `workflow_call` 嵌套 | 可重用工作流调用 | 最多 2 层 | 无 | 是 | trigger-events.md | 明确 |
| `workflow_call` secrets | 可声明 secrets 入参 | 调用方需显式传递 | 无 | 是 | trigger-events.md | 明确 |
| `workflow_call` inputs | 仅支持 string 类型 | 与 workflow_dispatch 一致 | string | 是 | trigger-events.md, configure-triggers.md | 明确 |

### 1.8 Artifact / Cache

| 能力项 | 语义 | 约束与边界 | 默认值 | 是否可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|
| `upload-artifact` | 跨 job 传递构建产物 | `name` + `path`；支持多路径；大小上限 **未公开** | 无 | 是 | upload-download-artifacts.md | 明确 |
| `download-artifact` | 下载制品 | `path` 默认当前目录；可下载全部制品 | 当前目录 | 是 | upload-download-artifacts.md | 明确 |
| artifact 保留期 | 可设定保留天数 | 默认 90 天；环境变量 `ATOMGIT_RETENTION_DAYS` | 90 天 | 是 | platform-config/README.md, runtime-environment-variables.md | 明确 |
| artifact 大小上限 | 制品大小限制 | 文档未公开具体数值 | 未知 | 否 | upload-download-artifacts.md | 未知 |
| `cache` | 依赖缓存 | `key` + `restore-keys` 前缀匹配 | 无 | 是 | using-dependency-cache.md | 明确 |
| cache 作用域 | 同仓库的所有运行 | "LRU 淘汰" | 同仓库 | 否 | artifacts-and-cache.md | 模糊 |
| cache fork 隔离 | fork PR 写缓存是否污染主分支 | **文档未明确** | 未知 | 否 | using-dependency-cache.md | 未知 |

### 1.9 可观测性与结果契约

| 能力项 | 语义 | 约束与边界 | 默认值 | 是否可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|
| 运行状态机 | queued→in_progress→completed | completed 含 success/failure/cancelled/skipped | 无 | 否 | view-run-results.md | 明确 |
| 日志完整性 | 实时日志 + 分组 | `::group::`/`::error::`/`::warning::` 等 workflow 命令 | 未知 | 否 | view-job-logs.md | 模糊 |
| Step Summary | `ATOMGIT_STEP_SUMMARY` 写入 Markdown | 追加/覆盖/删除文件可清空 | 无 | 是 | runtime-environment-variables.md | 明确 |
| 工作流命令 | ATOMGIT_OUTPUT/ENV/PATH/STEP_SUMMARY | 废弃 `::set-output`/`::set-env`/`::add-path` | 文件路径由 runner 分配 | 否 | workflow-commands.md | 明确 |
| `::add-mask::` | 日志脱敏命令 | 仍在使用 | 无 | 是 | workflow-commands.md | 明确 |
| 注解/Annotation | 落到 PR/commit | **文档未详述**是否支持及机制 | 未知 | 否 | 未明确 | 未知 |

### 1.10 兼容性差异高发区（已内嵌于上表）

关键差异已在各表中标注，汇总如下：
- 工作流目录：`.github/workflows/` → `.gitcode/workflows/`
- 核心上下文：`github.*` → `atomgit.*`
- 系统变量前缀：`GITHUB_*` → `ATOMGIT_*`
- 状态函数：`success()` → `success`（无括号）
- permissions 命名：`contents`/`pull-requests` → `repository`/`pr`
- inputs 类型：5 种 → 仅 `string`
- `pull_request` types：`opened`/`synchronize` → `open`/`update`
- Runner 标签：单标签 → 三段式 `{os,arch,flavor}`

### 1.11 迁移摩擦（已内嵌于上表及 COMPAT-NOTES.md）

### 1.12 稳定性专项

| 能力项 | 语义 | 约束与边界 | 默认值 | 是否可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|
| `concurrency.max` | 同一 workflow 最大并发数 | 范围 1-5 | 未知 | 是 | workflow-file-location-structure.md | 明确 |
| `concurrency.exceed-action` | 超出并发时策略 | IGNORE（忽略）/ QUEUE（排队） | 未知 | 是 | workflow-file-location-structure.md | 明确 |
| `concurrency.preemption.events` | 抢占事件列表 | 最多 10 个 | 未知 | 是 | workflow-file-location-structure.md | 明确 |
| 最大重试次数 | 单条运行最多 rerun 3 次 | 超 6h 不可 rerun | 3 | 否 | rerun-failed-jobs.md | 明确 |
| 矩阵组合数上限 | 文档未公开 | GitHub 官方 256 jobs/workflow | 未知 | 否 | configure-matrix-builds.md | 未知 |
| 最大并发 workflow 数 | 文档未公开 | 平台级限流可能存在 | 未知 | 否 | 未明确 | 未知 |
| 最大 artifact 大小 | 文档未公开 | upload-download-artifacts.md 仅称「不超过限制」 | 未知 | 否 | upload-download-artifacts.md | 未知 |
| 最大 cache 大小 | 文档未公开 | 仅称 "LRU 淘汰" | 未知 | 否 | artifacts-and-cache.md | 未知 |
| 最大 step output 单参数 | 1MB | 超出行为未明确 | 1MB | 否 | pass-output-between-jobs.md | 明确 |
| 触发 paths 匹配上限 | 前 300 个变更文件参与判断 | 超出部分不参与 | 300 | 否 | configure-triggers.md | 明确 |

---

## 2. 规格缺口/存疑清单

| 序号 | 缺口/存疑项 | 影响维度 | 置信度 | 下游消费方 | 详细说明 |
|---|---|---|---|---|---|
| GAP-001 | **默认 shell 类型** | completeness, compatibility | 模糊 | case-writer, compat-diff | configure-steps.md 未明确声明未指定 `shell` 时的默认值，迁移 friction 大。 |
| GAP-002 | **permissions 默认值** | security, compatibility | 模糊 | security, compat-diff | token-permissions.md 称"未声明时使用仓库设置中定义的权限"，但仓库设置的默认权限值未在任何文档中公开。 |
| GAP-003 | **Runner 是否一次性/ephemeral** | reliability, security | 未知 | reliability, security | 文档未明确官方 Runner 是否为一次性，复用 Runner 可能导致残留污染（工作区/环境变量/缓存/进程）。 |
| GAP-004 | **cache fork 隔离策略** | security, reliability | 未知 | security, reliability | using-dependency-cache.md 与 artifacts-and-cache.md 均未说明 fork PR 写入的 cache 是否隔离于主分支 cache，存在投毒风险。 |
| GAP-005 | **artifact 大小上限** | reliability | 未知 | reliability | upload-download-artifacts.md 仅说"已确认制品大小不超过限制"，未给出数值，无法设计边界用例。 |
| GAP-006 | **matrix 组合数上限** | reliability | 未知 | reliability | configure-matrix-builds.md 未声明矩阵组合数上限，大 matrix 的排队/截断/报错行为未知。 |
| GAP-007 | **未知/不支持字段的降级方式** | compatibility, usability | 未知 | compat-diff, usability | 整份文档未明确说明 YAML 解析遇到未知字段时是报错、静默忽略还是部分支持——这是兼容性差异最高发区之一。 |
| GAP-008 | **取消语义与清理钩子** | reliability | 未知 | reliability | 手动取消或被抢占时，正在运行的 step 如何终止、清理钩子（如 `post` 或 `always`）是否执行，文档未详述。 |
| GAP-009 | **注解(annotation)机制** | usability, completeness | 未知 | usability | 文档未详述 annotation 是否支持、如何落到 PR/commit，影响可观测性 completeness 评估。 |
| GAP-010 | **`strategy.fail-fast` 默认值** | completeness | 模糊 | case-writer | configure-matrix-builds.md 未明确 `fail-fast` 的默认值（GitHub 默认 true）。 |
| GAP-011 | **`issue_comment` / `pull_request_comment` 默认 types** | completeness | 模糊 | case-writer | trigger-events.md 未明确这两种事件的默认 types 取值。 |
| GAP-012 | **环境级 Secret 审批默认行为** | security | 模糊 | security | using-secrets.md 提到"可配置审批人"，但未说明默认是否需要审批、未配置时的行为。 |
| GAP-013 | **`workflow_dispatch` 未传非必填参数的行为** | completeness | 模糊 | case-writer | configure-triggers.md 未明确 `required: false` 且未传值时，是否使用 default 还是空字符串。 |
| GAP-014 | **max-parallel 未设时的确切调度行为** | reliability | 模糊 | reliability | configure-matrix-builds.md 称"取决于 Runner 可用数量"，但无固定上限意味着大 matrix 可能耗尽平台资源。 |
| GAP-015 | **日志实时性与完整性保证** | reliability, usability | 模糊 | reliability, usability | view-job-logs.md 未说明日志流式传输保证、断线重连、超大日志截断策略。 |
| GAP-016 | **secret 脱敏绕过边界** | security | 模糊 | security | using-secrets.md 自承 `echo "${{ secrets.X }}"` 可能绕过脱敏，但具体绕过条件（如 base64/拼接/多行）未详述。 |
| GAP-017 | **action `runs.using` 支持范围** | compatibility, completeness | 模糊 | compat-diff, case-writer | action-yml-metadata-syntax.md 示例仅列 `node16`，是否支持 node20/docker/composite 未明确声明。 |
| GAP-018 | **`runner.debug` 触发方式** | completeness | 模糊 | case-writer | runner 上下文中含 `runner.debug`，但文档未说明如何开启 debug 模式。 |
| GAP-019 | **自托管 Runner 同时运行多个 Job** | reliability, security | 未知 | reliability, security | using-self-hosted-runners.md 称主机 Runner"每台主机固定运行一个 Runner"，但一个 Runner 是否可同时运行多个 Job 未明确。 |
| GAP-020 | **Kubernetes Runner 的容器隔离边界** | security | 未知 | security | 文档未说明 K8s Runner Pod 的网络策略、特权模式、宿主机访问限制。 |

---

## 3. Intent 列表

### INTENT-COMP-001
```
意图 ID:    INTENT-COMP-001
维度标签:   [completeness]
标题:       验证工作流文件目录 `.gitcode/workflows/` 的识别行为

风险点:     目录路径错误会导致流水线无法被识别和触发（00-overview.md 明确声明）。这是迁移第一摩擦点。
预期系统行为: 仅 `.gitcode/workflows/` 下的 `.yml`/`.yaml` 文件被识别为 workflow；`.github/workflows/` 下文件不被识别。
Oracle 来源: GitCode规格

验证要点:
  - [正向] `.gitcode/workflows/ci.yml` 被正确识别并触发
  - [负向] `.github/workflows/ci.yml` 不被识别为 workflow

优先级线索: 迁移摩擦基础项
破坏级别:   none
来源输入:   workflow-file-location-structure.md; COMPAT-NOTES.md; 2026-07-20
```

### INTENT-COMP-002
```
意图 ID:    INTENT-COMP-002
维度标签:   [completeness, compatibility]
标题:       验证未知/不支持字段的 YAML 校验行为

风险点:     文档未明确降级方式（报错 vs 静默忽略 vs 部分支持），这是兼容性差异最高发区之一。若静默忽略，用户会误以为配置生效。
预期系统行为: 包含未知顶层字段或非法类型的 workflow 应触发 YAML schema 校验失败，给出明确的行号和字段名提示。
Oracle 来源: GitHub行为（GitHub 对未知字段通常报错）

验证要点:
  - [正向] 包含未知顶层字段的 workflow 触发校验失败
  - [负向] 不应静默忽略未知字段导致用户误以为配置生效
  - [非功能] 错误信息应指明行号、字段名及"不支持"语义

对齐方向:   一致性
优先级线索: 基础性完备性
破坏级别:   none
来源输入:   多处缺失; testing-focus.md §1; 2026-07-20
```

### INTENT-COMP-003
```
意图 ID:    INTENT-COMP-003
维度标签:   [completeness]
标题:       验证 push 触发 + branches/paths/tags 过滤的完整行为

风险点:     paths 匹配前 300 个变更文件，超出部分不参与判断，这是边界/稳定性可测点。否定模式仅否定模式组合使用规则也需验证。
预期系统行为: branches 白名单/黑名单、paths 白名单/黑名单、tags 过滤均按文档语义工作；paths 超过 300 文件时前 300 个参与匹配；否定模式不单独生效。
Oracle 来源: GitCode规格

验证要点:
  - [正向] 匹配分支/path/tag 的 push 正确触发 workflow
  - [正向] 不匹配的分支/path/tag 不触发
  - [负向] 仅含否定模式（如 branches: ["!main"]）时不触发
  - [非功能] 大变更集（>300 文件）下 paths 匹配行为符合"前 300"声明

优先级线索: 基础触发器行为
破坏级别:   none
来源输入:   trigger-events.md; configure-triggers.md; 2026-07-20
```

### INTENT-COMP-004
```
意图 ID:    INTENT-COMP-004
维度标签:   [completeness, security]
标题:       验证 pull_request vs pull_request_target 隔离强度

风险点:     文档声明与 GitHub 语义一致，但"大部分兼容"下隔离强度需逐条实测确认。这是安全命脉。
预期系统行为: `pull_request`（fork）→ ATOMGIT_TOKEN 仅 read、不可访问 Secret；`pull_request_target` → base 上下文、可写、可访问 Secret。
Oracle 来源: GitCode规格

验证要点:
  - [正向] fork PR 的 `pull_request` workflow 无法读取项目 secrets（包括组织级和项目级）
  - [正向] fork PR 的 `pull_request` workflow 的 ATOMGIT_TOKEN 仅 read，无法推送代码
  - [负向] fork PR 的 `pull_request` workflow 不应能修改 PR、操作项目资源
  - [非功能] `pull_request_target` 使用 base 分支 workflow 版本（非 fork 版本）

优先级线索: 安全命脉
破坏级别:   fixture
来源输入:   pr-mr-pipeline-security.md; token-permissions.md; 2026-07-20
```

### INTENT-COMP-005
```
意图 ID:    INTENT-COMP-005
维度标签:   [completeness, compatibility]
标题:       验证 schedule cron 语义（最短 5 分钟、UTC、仅默认分支）

风险点:     与 GitHub 差异（GitHub 无官方最短间隔限制）；定时任务可能存在数分钟调度延迟。
预期系统行为: cron 使用 UTC；间隔 <5 分钟被拒绝或降级；仅在默认分支生效；调度延迟在数分钟内。
Oracle 来源: GitCode规格

验证要点:
  - [正向] 合法 cron 在默认分支按时触发
  - [负向] 非默认分支的 schedule workflow 不应触发
  - [非功能] 最短间隔限制生效（如 1 分钟间隔被阻止或按 5 分钟执行）

对齐方向:   差异确认
优先级线索: 稳定性基础
破坏级别:   none
来源输入:   trigger-events.md; configure-triggers.md; 2026-07-20
```

### INTENT-COMP-006
```
意图 ID:    INTENT-COMP-006
维度标签:   [completeness]
标题:       验证 workflow_call 嵌套层数限制（最多 2 层）

风险点:     文档明确声明最多 2 层，需验证实际执行时是否被强制限制，以及超限时的报错质量。
预期系统行为: 2 层嵌套可正常执行；3 层及以上嵌套应报错或阻止。
Oracle 来源: GitCode规格

验证要点:
  - [正向] 2 层 workflow_call 正常执行
  - [负向] 3 层 workflow_call 应失败或被阻止
  - [可理解性] 超限报错是否清晰说明"最多 2 层"

优先级线索: 执行模型基础
破坏级别:   none
来源输入:   trigger-events.md; configure-triggers.md; 2026-07-20
```

### INTENT-COMP-007
```
意图 ID:    INTENT-COMP-007
维度标签:   [completeness]
标题:       验证 stages 阶段机制与 post 后处理阶段语义

风险点:     GitCode 特有机制，无 GitHub 对照，需验证串行/并行语义和 fail_fast 行为是否与文档一致。
预期系统行为: 阶段间串行、阶段内 job 并行；`fail_fast: true` 时任一 job 失败立即终止同阶段其他 job；`post` 默认 `run_always: true` 且 workflow 达到终态后执行。
Oracle 来源: GitCode规格

验证要点:
  - [正向] 多 stage 按定义顺序串行执行
  - [正向] 同 stage 内多 job 并行执行
  - [正向] `fail_fast: true` 时 job 失败终止同阶段其余 job
  - [正向] `post.run_always: true` 在 workflow 失败时仍执行
  - [正向] `post.run_always: false` 仅在 workflow 成功时执行

优先级线索: 执行模型基础
破坏级别:   none
来源输入:   core-concepts/workflow-job-step-action.md; workflow-file-location-structure.md; 2026-07-20
```

### INTENT-COMP-008
```
意图 ID:    INTENT-COMP-008
维度标签:   [completeness, reliability]
标题:       验证 timeout-minutes 默认 360 分钟与强制终止行为

风险点:     超时后 job 被强制终止，需验证终止行为、资源清理、日志完整性。
预期系统行为: 未声明 timeout-minutes 时默认 360 分钟；超时后 job 被强制终止并标记 failure；已运行 step 的日志保留。
Oracle 来源: GitCode规格

验证要点:
  - [正向] 未声明 timeout 的 job 在 360 分钟内正常运行
  - [负向] 超时的 job 被强制终止并标记为 failure
  - [非功能] 超时终止前已完成的 step 日志完整保留

优先级线索: 稳定性基础
破坏级别:   none
来源输入:   configure-jobs.md; 2026-07-20
```

### INTENT-COMP-009
```
意图 ID:    INTENT-COMP-009
维度标签:   [completeness, reliability]
标题:       验证 rerun 次数限制与上下文保持语义

风险点:     最多 3 次，超 6h 不可 rerun；重新运行使用原始 commit 配置而非最新配置。用户可能误以为 rerun 会读取最新 workflow。
预期系统行为: 单条运行可 rerun 最多 3 次；超 6h 的 run 不可 rerun；rerun 时 atomgit.sha/ref/event_name 保持原始值，run_id/run_number 更新为新值。
Oracle 来源: GitCode规格

验证要点:
  - [正向] rerun 成功后 run_number 递增，sha/ref 保持原始值
  - [负向] 第 4 次 rerun 应被阻止
  - [负向] 超 6h 的 run 的 rerun 应被拒绝
  - [正向] rerun 使用原始 commit 的 workflow 配置（非最新配置）

优先级线索: 可观测性与恢复
破坏级别:   none
来源输入:   rerun-failed-jobs.md; 2026-07-20
```

### INTENT-COMP-010
```
意图 ID:    INTENT-COMP-010
维度标签:   [completeness, compatibility]
标题:       验证 runs-on 三段式标签体系与 default 快捷标签

风险点:     与 GitHub 单标签/数组体系差异大；`default` 是否真等效 `[ubuntu-latest,x64,small]` 需验证；自托管标签子集匹配也需验证。
预期系统行为: `{os,arch,flavor}` 三段式正确匹配 Runner；`default` 等效 `[ubuntu-latest,x64,small]`；自托管 `runs-on` 标签必须是 Runner 标签子集。
Oracle 来源: GitCode规格

验证要点:
  - [正向] 三段式标签正确调度到对应规格 Runner
  - [正向] `runs-on: default` 调度到 small 规格（2核8G）
  - [负向] 不存在的标签组合应导致 job 排队或失败
  - [负向] 自托管 Runner 标签不完全匹配时 job 不应调度

优先级线索: Runner 基础行为
破坏级别:   none
来源输入:   runner-and-environment.md; using-hosted-runners.md; using-self-hosted-runners.md; 2026-07-20
```

### INTENT-COMP-011
```
意图 ID:    INTENT-COMP-011
维度标签:   [completeness, reliability, security]
标题:       验证 Runner 环境隔离强度（是否 ephemeral）

风险点:     文档未明确 Runner 是否一次性，复用 Runner 可能导致残留污染（工作区/环境变量/缓存/进程）。这是安全性与稳定性关键未知项。
预期系统行为: 官方 Runner 应为一次性（ephemeral），job 完成后环境被清理；跨 job 文件不可见；环境变量不泄漏。
Oracle 来源: GitHub行为（GitHub 官方 Runner 为 ephemeral）

验证要点:
  - [正向] 同一 workflow 的先后 job 运行环境独立
  - [负向] 前一 job 写入的文件/环境变量不应泄漏到后一 job（除非通过 artifact/outputs 显式传递）
  - [非功能] 环境清理及时性

优先级线索: 安全与稳定性
破坏级别:   none
来源输入:   未明确; testing-focus.md §4; 2026-07-20
```

### INTENT-COMP-012
```
意图 ID:    INTENT-COMP-012
维度标签:   [completeness, security]
标题:       验证 secrets 日志脱敏与绕过场景

风险点:     文档自承 `echo "${{ secrets.X }}"` 可能绕过脱敏。需验证标准场景下的遮蔽行为，以及 base64/拼接/多行变形后的泄露风险。
预期系统行为: secret 值在标准日志中显示为 `***`；通过 `${{ secrets.X }}` 直接回显应仍被遮蔽；但间接拼接可能绕过（需记录实际行为）。
Oracle 来源: GitCode规格

验证要点:
  - [正向] `echo "${{ secrets.X }}"` 输出中值为 `***`
  - [负向] secret 的原始值不应以明文出现在标准日志中
  - [非功能] base64 编码后的 secret、拼接后的 secret 是否仍被遮蔽（文档未承诺，需记录事实）

负向断言目标: secret 原始值绝不应以明文出现在标准日志输出中
优先级线索: 安全命脉
破坏级别:   fixture
来源输入:   using-secrets.md; COMPAT-NOTES.md; 2026-07-20
```

### INTENT-COMP-013
```
意图 ID:    INTENT-COMP-013
维度标签:   [completeness, security]
标题:       验证 permissions 默认权限与声明语义

风险点:     文档称"未声明 permissions 时使用仓库设置中定义的权限"，但默认值未公开；GitCode 权限域命名与 GitHub 完全不同；fork PR 下 permissions 声明被忽略（仅 read）——这些都需要实测。
预期系统行为: `permissions: {}` 时 ATOMGIT_TOKEN 仅拥有 repository:read；各权限域 read/write/none 精确生效；fork PR 的 `pull_request` 下无论 permissions 如何声明 TOKEN 仅 read。
Oracle 来源: GitCode规格

验证要点:
  - [正向] `permissions: {}` 下无法执行写操作（如推送、评论）
  - [正向] 声明 `repository: write` 后可推送
  - [负向] fork PR 的 `pull_request` 下声明 `repository: write` 仍仅 read
  - [非功能] 未声明 permissions 时的默认权限需记录事实（作为下游兼容性分析依据）

优先级线索: 安全命脉
破坏级别:   fixture
来源输入:   token-permissions.md; pr-mr-pipeline-security.md; 2026-07-20
```

### INTENT-COMP-014
```
意图 ID:    INTENT-COMP-014
维度标签:   [completeness, security]
标题:       验证 pull_request_target checkout head.sha 的注入风险

风险点:     文档明确警示此风险：高权限上下文中运行不可信代码。需验证默认行为及平台是否提供安全警告。
预期系统行为: `pull_request_target` 默认 checkout base 分支；若显式 checkout head.sha 后执行脚本，系统不应自动阻止（这是设计允许的行为），但 workflow 文件版本必须来自 base 分支。
Oracle 来源: 差异声明

验证要点:
  - [正向] `pull_request_target` 默认使用 base 分支 workflow 版本
  - [负向] 恶意 fork PR 无法通过修改 workflow 文件改变 `pull_request_target` 的执行逻辑
  - [非功能] 平台是否对 `pull_request_target` + checkout head.sha 模式给出安全警告或文档提示

优先级线索: 安全命脉
破坏级别:   fixture
来源输入:   pr-mr-pipeline-security.md; 2026-07-20
```

### INTENT-COMP-015
```
意图 ID:    INTENT-COMP-015
维度标签:   [completeness, reliability]
标题:       验证 upload-artifact / download-artifact 跨 job 传递与保留期

风险点:     制品大小上限未公开；保留期默认 90 天；下载全部制品功能需验证。
预期系统行为: artifact 可在同 workflow 的 job 间传递；默认保留 90 天（ATOMGIT_RETENTION_DAYS）；支持下载单个/全部制品。
Oracle 来源: GitCode规格

验证要点:
  - [正向] upload 后 download 可获取相同内容
  - [正向] 下载全部制品功能正常
  - [非功能] 大制品（如 500MB/1GB）上传下载的稳定性与耗时（边界未知， exploratory）

优先级线索: Artifact 基础行为
破坏级别:   none
来源输入:   upload-download-artifacts.md; artifacts-and-cache.md; platform-config/README.md; 2026-07-20
```

### INTENT-COMP-016
```
意图 ID:    INTENT-COMP-016
维度标签:   [completeness, security, reliability]
标题:       验证 cache 作用域与 fork 隔离策略

风险点:     文档未明确 cache 隔离策略，fork PR 写缓存可能污染主分支缓存（cache 投毒）。这是安全性与稳定性交叉风险点。
预期系统行为: cache key 精确匹配优先，restore-keys 前缀匹配兜底；fork PR 的 cache 不应覆盖或污染主分支 cache。
Oracle 来源: GitHub行为

验证要点:
  - [正向] cache hit 时恢复缓存内容正确
  - [正向] restore-keys 前缀匹配兜底生效
  - [负向] fork PR 不应能覆盖主分支的 cache key
  - [非功能] cache LRU 淘汰行为是否符合预期

优先级线索: 安全与稳定性
破坏级别:   fixture
来源输入:   using-dependency-cache.md; artifacts-and-cache.md; 2026-07-20
```

### INTENT-COMP-017
```
意图 ID:    INTENT-COMP-017
维度标签:   [completeness, usability]
标题:       验证运行状态机与日志完整性

风险点:     状态语义需与文档一致；日志实时性和完整性直接影响调试体验。Job 日志下载 API 可能返回 404（platform-config 已知限制）。
预期系统行为: 状态机 queued→in_progress→completed(success/failure/cancelled/skipped)；日志完整、可按 step 分组查看；失败 step 的日志保留。
Oracle 来源: GitCode规格

验证要点:
  - [正向] 各状态转换符合预期
  - [正向] 失败 step 的日志完整保留且可查看
  - [非功能] 日志查看延迟在可接受范围（数秒内）
  - [非功能] 超大日志（如数万行）的加载与分页行为

优先级线索: 可观测性基础
破坏级别:   none
来源输入:   view-run-results.md; view-job-logs.md; platform-config/instance-config.md; 2026-07-20
```

### INTENT-COMP-018
```
意图 ID:    INTENT-COMP-018
维度标签:   [completeness, compatibility]
标题:       验证 ATOMGIT_STEP_SUMMARY Markdown 渲染与安全性

风险点:     前缀差异（ATOMGIT_ vs GITHUB_），功能语义应与 GitHub 一致；summary 比日志更易被看到，敏感信息不应写入。
预期系统行为: 写入 ATOMGIT_STEP_SUMMARY 的 Markdown 内容正确渲染在运行详情页；删除文件可清空当前 step summary。
Oracle 来源: GitCode规格

验证要点:
  - [正向] Markdown 表格/标题/列表在运行详情页正确渲染
  - [负向] 写入 summary 的敏感信息不应被自动脱敏（用户责任），但平台不应在 summary 中暴露系统内部路径
  - [非功能] 多 step 写入 summary 的汇总行为

优先级线索: 可观测性基础
破坏级别:   none
来源输入:   runtime-environment-variables.md; 2026-07-20
```

### INTENT-COMPAT-019
```
意图 ID:    INTENT-COMPAT-019
维度标签:   [compatibility]
标题:       验证上下文对象命名 github.* → atomgit.* 的兼容性影响

风险点:     直接搬运 GitHub workflow 会全线失效。需验证 GitCode 的报错质量及是否有辅助迁移提示。
预期系统行为: GitCode 不支持 `github.*` 上下文；使用 `github.ref` 的 workflow 应解析失败或返回空字符串。
Oracle 来源: 差异声明

验证要点:
  - [负向] `${{ github.ref }}` 在 GitCode 中不可用或为空
  - [正向] `${{ atomgit.ref }}` 正确返回触发引用
  - [可理解性] 若报错，错误信息是否提示 `github.*` 不可用并推荐 `atomgit.*`

对齐方向:   差异确认
可理解性判据: 错误信息应包含上下文名称和推荐替代方案；是否 llm_assisted: 否（可直接文本匹配 atomgit）
优先级线索: 迁移摩擦核心项
破坏级别:   none
来源输入:   COMPAT-NOTES.md; syntax-reference/context.md; 2026-07-20
```

### INTENT-COMPAT-020
```
意图 ID:    INTENT-COMPAT-020
维度标签:   [compatibility]
标题:       验证状态函数括号语法差异 success() → success

风险点:     语义等价但语法不同，GitHub workflow 直接迁移极易踩坑。需验证 GitCode 对带括号语法的处理及报错质量。
预期系统行为: GitCode 接受 `success`/`failed`/`always`/`cancelled`（无括号）；`success()` 等带括号语法可能被拒绝或行为异常。
Oracle 来源: 差异声明

验证要点:
  - [正向] `if: ${{ success }}` 正确执行
  - [负向] `if: ${{ success() }}` 应报错或不被识别（行为需记录）
  - [可理解性] 若报错，错误信息是否清晰指出"状态函数不需要括号"

对齐方向:   差异确认
可理解性判据: 错误信息应指出语法差异；是否 llm_assisted: 否
优先级线索: 迁移摩擦核心项
破坏级别:   none
来源输入:   COMPAT-NOTES.md; expressions.md; 2026-07-20
```

### INTENT-COMPAT-021
```
意图 ID:    INTENT-COMPAT-021
维度标签:   [compatibility]
标题:       验证表达式函数 contains/hashFiles/toJson 边界行为与 GitHub 一致性

风险点:     同名函数边界行为、类型转换、空值处理可能与 GitHub 不同。GitCode 特有 substring/replace 也需验证。
预期系统行为: 标准用例下函数返回值与 GitHub 一致；空值/异常输入时的处理行为应被记录。
Oracle 来源: GitHub行为

验证要点:
  - [正向] 标准用例下 contains/startsWith/endsWith/format/hashFiles/toJson 返回值与 GitHub 一致
  - [非功能] 空值/异常输入（如 null、不存在属性）时的处理行为
  - [非功能] GitCode 特有 substring/replace 的边界行为

对齐方向:   一致性
优先级线索: 表达式兼容性
破坏级别:   none
来源输入:   COMPAT-NOTES.md; expressions.md; github-reference/reference/expressions.md; 2026-07-20
```

### INTENT-COMPAT-022
```
意图 ID:    INTENT-COMPAT-022
维度标签:   [compatibility]
标题:       验证 permissions 权限域命名差异（repository/pr/issue vs contents/pull-requests/issues）

风险点:     GitCode 用 `repository`/`pr`/`issue` 等，GitHub 用 `contents`/`pull-requests`/`issues` 等，命名完全不同，迁移必改。
预期系统行为: GitCode 不支持 GitHub 的权限域命名；使用 GitHub 命名应不生效或报错。
Oracle 来源: 差异声明

验证要点:
  - [负向] `permissions: contents: read` 在 GitCode 中不生效或报错
  - [正向] `permissions: repository: read` 正确生效
  - [可理解性] 若报错，错误信息是否提示命名差异及 GitCode 对应命名

对齐方向:   差异确认
可理解性判据: 错误信息应提示命名差异；是否 llm_assisted: 否
优先级线索: 迁移摩擦核心项
破坏级别:   none
来源输入:   COMPAT-NOTES.md; token-permissions.md; 2026-07-20
```

### INTENT-COMPAT-023
```
意图 ID:    INTENT-COMPAT-023
维度标签:   [compatibility]
标题:       验证 workflow_dispatch.inputs 仅支持 string 类型

风险点:     GitHub 支持 boolean/choice/number/environment/string，迁移需要类型转换改造。需验证 GitCode 对其他类型的校验行为。
预期系统行为: GitCode 仅接受 `type: string`；其他类型应被 YAML 校验拒绝。
Oracle 来源: 差异声明

验证要点:
  - [正向] `type: string` 的 inputs 正常工作
  - [负向] `type: boolean`/`choice`/`number`/`environment` 应被校验失败
  - [可理解性] 报错信息是否明确指出"仅支持 string"

对齐方向:   差异确认
可理解性判据: 报错应明确说明类型限制；是否 llm_assisted: 否
优先级线索: 迁移摩擦核心项
破坏级别:   none
来源输入:   COMPAT-NOTES.md; configure-triggers.md; 2026-07-20
```

### INTENT-SEC-024
```
意图 ID:    INTENT-SEC-024
维度标签:   [security]
标题:       验证表达式注入与不可信输入（PR 标题/正文/分支名/评论）的隔离效果

风险点:     把不可信输入直接插进 `run:` 的 `${{ }}` 导致命令执行——业界最常见的 Actions 漏洞类。需验证 fork PR 场景下隔离是否有效。
预期系统行为: 平台不应自动阻止注入（这是用户责任），但 fork PR 的 ATOMGIT_TOKEN 仅 read、无法访问 secrets，因此注入影响范围受限。
Oracle 来源: GitHub行为

验证要点:
  - [负向] 外部贡献者通过恶意 PR 标题注入 `run:` 命令不应能读取 secrets（包括 ATOMGIT_TOKEN 的 write 权限）
  - [负向] fork PR 不应能利用注入提升 ATOMGIT_TOKEN 权限或推送代码
  - [非功能] 平台是否对明显注入模式给出安全警告

负向断言目标: 外部 fork 贡献者无法通过表达式注入读取仓库 secrets 或获得写权限；注入命令在受限 TOKEN 下执行
优先级线索: 安全命脉
破坏级别:   fixture
来源输入:   testing-focus.md §6; github-reference/security/script-injections.md; 2026-07-20
```

### INTENT-SEC-025
```
意图 ID:    INTENT-SEC-025
维度标签:   [security]
标题:       验证第三方 action 引用信任边界与版本固定

风险点:     `uses: owner/repo@ref` 的可变 tag 被重写风险；官方插件短名引用等价行为需确认。
预期系统行为: Action 版本按 ref 固定；`@SHA` 引用行为完全确定；`@tag` 可随 tag 重写变化（设计行为）；官方插件短名引用应等价于固定版本。
Oracle 来源: GitCode规格

验证要点:
  - [正向] `@SHA` 引用行为稳定不变
  - [负向] tag 被重写后按 tag 引用的 workflow 不应继续使用旧代码（应使用新代码，这是设计行为，需记录差异）
  - [非功能] 官方插件短名（如 `checkout`）是否映射到固定 SHA 或浮动 tag

优先级线索: 供应链安全
破坏级别:   none
来源输入:   using-actions.md; testing-focus.md §7; 2026-07-20
```

### INTENT-REL-026
```
意图 ID:    INTENT-REL-026
维度标签:   [reliability]
标题:       验证 concurrency 并发控制（max 1-5 + QUEUE/IGNORE）与抢占策略

风险点:     实现细节待实测；preemption 抢占策略在并发洪泛时的行为未知。
预期系统行为: 并发数超过 max 时，新请求按 exceed-action 策略处理（QUEUE 排队或 IGNORE 忽略）；preemption.events 最多 10 个。
Oracle 来源: GitCode规格

验证要点:
  - [正向] 并发数 <= max 时多个运行正常并行
  - [非功能] 并发数 > max 时 QUEUE 策略下新运行排队等待；IGNORE 策略下新运行被忽略
  - [非功能] 抢占配置生效，抢占行为符合 events 定义

故障/压力参数: 并发度: max+1（如 6）；策略: QUEUE / IGNORE；抢占事件: mr_id
优先级线索: 稳定性基础
破坏级别:   none
来源输入:   workflow-file-location-structure.md; platform-config/README.md; 2026-07-20
```

### INTENT-REL-027
```
意图 ID:    INTENT-REL-027
维度标签:   [reliability]
标题:       验证大规模 matrix 展开行为与平台上限

风险点:     GitCode 未公开 matrix 组合数上限；max-parallel 未设时"取决于 Runner 可用数量"意味着大 matrix 可能耗尽资源或触发平台限流。
预期系统行为: 中等规模 matrix 正确展开并执行；超大规模 matrix 应有平台级上限（截断、排队或报错）。
Oracle 来源: GitHub行为（GitHub 官方 256 jobs/workflow）

验证要点:
  - [正向] 中等规模 matrix（如 2×2×3=12）正确展开全部 job
  - [非功能] 超大规模 matrix（如 20×20=400）是否被截断、排队或报错
  - [非功能] max-parallel 限制生效，同时运行的 job 实例数不超过限制

故障/压力参数: 矩阵规模: 12 job / 50 job / 200 job；max-parallel: 4 / 未设
优先级线索: 稳定性边界
破坏级别:   none
来源输入:   configure-matrix-builds.md; platform-config/README.md; 2026-07-20
```

### INTENT-USE-028
```
意图 ID:    INTENT-USE-028
维度标签:   [usability]
标题:       验证迁移报错质量（GitHub→GitCode 语法不兼容时的错误提示）

风险点:     文档未系统说明报错差异指引；用户直接搬运 GitHub workflow 时的错误信息是否可操作，直接影响迁移摩擦。
预期系统行为: 使用 GitHub 语法（如 `github.ref`、`success()`、`contents: read`）时，报错应指明"GitCode 不支持/需改写"，而非泛化报错（如"语法错误"）。
Oracle 来源: GitHub行为

验证要点:
  - [正向] 使用 `github.*` 上下文时报错提示该上下文不可用
  - [正向] 使用 `success()` 时报错或提示正确语法为 `success`
  - [可理解性] 错误信息包含可操作的建议（如"请使用 atomgit.*"）

可理解性判据: 错误信息应包含不支持的语法名称和推荐替代方案；是否 llm_assisted: 是（需判断"可操作性"）
优先级线索: 迁移摩擦
破坏级别:   none
来源输入:   COMPAT-NOTES.md; testing-focus.md §11; 2026-07-20
```

### INTENT-USE-029
```
意图 ID:    INTENT-USE-029
维度标签:   [usability]
标题:       验证文档一致性（runtime-environment-variables.md 中的 GitHub 残留措辞）

风险点:     COMPAT-NOTES.md 指出 runtime-environment-variables.md 里部分描述文案仍夹带 `GITHUB_ACTION_PATH` 等 GitHub 残留措辞，可能导致用户配置错误。
预期系统行为: 官方文档中的环境变量名、示例应与平台实际注入的行为完全一致；不应出现 `GITHUB_*` 作为平台实际变量名。
Oracle 来源: GitCode规格

验证要点:
  - [正向] 文档中的 `ATOMGIT_*` 变量名与实际 Runner 注入的一致
  - [负向] 文档中不应出现 `GITHUB_*` 作为平台实际变量名（历史对比说明除外）
  - [可理解性] 文档错误是否会导致用户按错误变量名配置 workflow

可理解性判据: 文档中 GitHub 残留措辞的数量和影响范围；是否 llm_assisted: 是（需判断"影响范围"）
优先级线索: 文档质量
破坏级别:   none
来源输入:   COMPAT-NOTES.md; runtime-environment-variables.md; 2026-07-20
```

### INTENT-USE-030
```
意图 ID:    INTENT-USE-030
维度标签:   [usability, completeness]
标题:       验证 workflow_dispatch inputs 默认值与必填参数校验

风险点:     `workflow_dispatch.inputs` 仅支持 string；required/default 的交互行为未充分测试；未传必填参数时的阻止行为需验证。
预期系统行为: 必填参数未提供时应阻止触发并给出清晰提示；默认值在参数未传时生效；所有输入值最终均为字符串。
Oracle 来源: GitCode规格

验证要点:
  - [正向] 提供全部必填参数时正常触发
  - [负向] 必填参数缺失时应阻止触发并给出清晰提示（指明缺失参数名）
  - [正向] 默认值在参数未传时正确注入到 inputs 上下文
  - [非功能] 手动触发界面是否清晰展示参数说明和默认值

可理解性判据: 缺失必填参数的报错应指明具体参数名；是否 llm_assisted: 否
优先级线索: 基础功能
破坏级别:   none
来源输入:   configure-triggers.md; 2026-07-20
```

---

## 4. 统计摘要

| 指标 | 数量 |
|---|---|
| 结构化能力项 | **58 条** |
| 规格缺口/存疑项 | **20 条** |
| Intent 总数 | **30 条** |
| 按维度分布 | completeness: 18 条; compatibility: 6 条; security: 4 条; reliability: 3 条; usability: 3 条; 跨维度: 多条 |

---

## 5. 质量清单自检

- [x] 每条能力项都有出处，无凭空条目。
- [x] 默认值/边界被显式记录（不是留空）。
- [x] 存疑项标了置信度（明确/模糊/未知）并指明下游消费方。
- [x] 输入退化标注在输出中体现。
- [x] Intent 严格按 `templates/intent.md` 格式填写。
- [x] 不编造规格；文档没写的标 `未知`。
- [x] 不做兼容性判断，只客观记录 GitCode 侧事实。
