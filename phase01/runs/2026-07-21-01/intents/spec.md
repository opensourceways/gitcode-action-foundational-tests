# 规格分析：GitCode Action 能力清单 + 完备性意图

> Agent: spec-analyst | 维度: completeness | Run: 2026-07-21-01
> 输入版本: `phase01/inputs/gitcode-spec/` (fetched 2026-07-20, 共 50 页)
> 已阅基线: `case-base-detail.md` (KEEP 260, DEPRECATE 307, NEEDS-UPDATE 62)

---

## 一、结构化能力清单

按 `testing-focus.md` 关注域分类。置信度: ✅明确 / 🔶模糊 / ❓未知。

### 1. Workflow 语法与静态校验 (§1)

| # | 能力项 | 语义 | 约束/边界 | 默认值 | 可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|---|
| 1.1 | `name` 字段 | workflow 展示名称 | 任意字符串 | 使用文件名 | 否 | `workflow-file-location-structure.md` | ✅ |
| 1.2 | `on` 触发声明 | 定义触发事件 | 必填字段 | — | — | 同上 | ✅ |
| 1.3 | `env` workflow级 | 全局环境变量 | — | — | — | 同上 | ✅ |
| 1.4 | `defaults.run.shell` | 默认 shell | `bash`/`sh`/`pwsh`/`python` | `bash`? | 是 | 同上 + `configure-steps.md` | 🔶 未明确默认值 |
| 1.5 | `defaults.run.working-directory` | 默认工作目录 | 相对仓库根目录 | 仓库根目录? | 是 | 同上 | 🔶 未明确默认值 |
| 1.6 | `concurrency` | workflow级并发控制 | max 1-5, exceed-action IGNORE/QUEUE | — | 是 | 同上 | ✅ |
| 1.7 | `permissions` 权限声明 | 控制 ATOMGIT_TOKEN 权限 | 6 个权限域 + 3 个快捷值 | 仓库设置中定义的默认权限 | 是 | 同上 + `token-permissions.md` | 🔶 默认值依仓库设置，非 docs 可判定 |
| 1.8 | `stages` 阶段定义 | 阶段间串行、阶段内并行 | 可选字段，省略时 jobs 并行 | 无 stages（jobs 顶层并行） | 是 | 同上 | ✅ |
| 1.9 | `jobs` 任务集合 | 有 stages 时嵌套于 stage；无 stages 时为顶层 | 必填字段 | — | — | 同上 | ✅ |
| 1.10 | `post` 后处理阶段 | 终态后执行收尾步骤 | `run_always: true`（默认），steps 列表 | `run_always: true` | 是 | 同上 | ✅ |
| 1.11 | YAML 文件识别 | `.gitcode/workflows/*.yml\|.yaml` | 仅 .yml/.yaml，大小写敏感 | — | — | 同上 | ✅ |
| 1.12 | 未知/不支持字段处理 | 报错还是静默忽略？ | — | — | — | 未声明 | ❓ 高发差异点 |

### 2. 触发器语义 (§2)

| # | 能力项 | 语义 | 约束/边界 | 默认值 | 可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|---|
| 2.1 | `push` | 代码推送触发 | 支持 branches/branches-ignore/tags/tags-ignore/paths/paths-ignore 过滤 | — | 是 | `configure-triggers.md`, `syntax-reference/trigger-events.md` | ✅ |
| 2.2 | `pull_request` | PR 创建/更新/合并触发 | types: [open,reopen,update,merge]，默认 [open,reopen,update] | — | 是 | 同上 | ✅ |
| 2.3 | `pull_request_target` | base 上下文 PR 触发 | 与 pull_request 类似但使用 target 分支上下文 | types 默认 [open,reopen,update] | 是 | 同上 + `pr-mr-pipeline-security.md` | ✅ |
| 2.4 | `issue_comment` | Issue/PR 评论触发 | types: [created,edited,deleted]；对 Issue 和 PR 评论均生效 | — | — | 同上 | ✅ |
| 2.5 | `pull_request_comment` | 仅 PR 评论触发 | types + branches + comments 正则过滤 | — | — | 同上 | 🔶 comments 正则语义未详述 |
| 2.6 | `workflow_dispatch` | 手动触发（有 inputs） | inputs 仅 string 类型；含 description/required/default | — | 是 | 同上 | ✅ |
| 2.7 | `workflow_call` | 可重用工作流调用 | 最多 2 层嵌套；支持 inputs + secrets | — | — | 同上 | 🔶 2 层限制需核实 |
| 2.8 | `schedule` | cron 定时触发 | 最短间隔 5 分钟、UTC 时区、仅默认分支；POSIX cron 五段式 | — | 是 | 同上 | 🔶 scheduler 已报告不工作(P1) |
| 2.9 | `branches`/`branches-ignore` | 分支过滤 | 白名单与黑名单互斥；支持 `!` 否定 + `**` 通配 | — | — | 同上 | ✅ |
| 2.10 | `paths`/`paths-ignore` | 路径过滤 | 白名单与黑名单互斥；匹配前 300 个变更文件 | — | — | 同上 | 🔶 300 限额边界待测 |
| 2.11 | `tags`/`tags-ignore` | 标签过滤 | 白名单与黑名单互斥；支持通配与否定 | — | — | 同上 | ✅ |
| 2.12 | 否定模式 `!` | 排除特定分支/路径/标签 | 必须与肯定模式组合使用 | — | — | 同上 | ✅ |
| 2.13 | 多事件组合 | 同一 workflow 响应多事件 | 按 `on:` 下各自事件配置并行生效 | — | — | 同上 | ✅ |
| 2.14 | 触发去抖 | 同一 push 连推是否重复触发 | — | — | — | 未声明 | ❓ |

### 3. 执行模型 (§3)

| # | 能力项 | 语义 | 约束/边界 | 默认值 | 可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|---|
| 3.1 | `needs` Job 依赖 | DAG 拓扑编排 | 多依赖汇聚、失败时下游默认不执行 | 无依赖时并行 | 是 | `configure-jobs.md`, `configure-dependencies-order.md` | ✅ |
| 3.2 | `stages` 阶段串行 | 阶段间串行、阶段内并行 | 缺省时 jobs 并行，可与 needs 组合 | — | 是 | `configure-dependencies-order.md` | ✅ |
| 3.3 | `stages.fail_fast` | 阶段级快速失败 | 任一 job 失败终止同阶段 + 跳过后续 stage | — | 是 | 同上 | ✅ |
| 3.4 | `strategy.matrix` | 矩阵并行构建 | 多维展开、include/exclude、max-parallel | — | 是 | `configure-matrix-builds.md` | ✅ |
| 3.5 | `strategy.fail-fast` | 矩阵级快速失败 | 区别于 stages.fail_fast，仅控制矩阵内 | — | 是 | 同上 | ✅ |
| 3.6 | `strategy.max-parallel` | 矩阵最大并发 | 不设置时取决于 Runner 可用数 | Runner 可用数 | 是 | 同上 | ✅ |
| 3.7 | `concurrency` (workflow级) | 全局并发控制 | enable/max(1-5)/exceed-action(QUEUE\|IGNORE)/preemption | — | 是 | `workflow-file-location-structure.md` | ✅ |
| 3.8 | `concurrency` (job级) | Job 级并发控制 | 同上 | — | 是 | `configure-jobs.md` | 🔶 与 workflow 级交互未说明 |
| 3.9 | `concurrency.preemption` | 抢占策略 | enable + events 列表（最多10个） | enable=true（默认） | 是 | `workflow-file-location-structure.md` | 🔶 抢占语义未详述 |
| 3.10 | `if` 条件执行 (job/step) | 表达式+状态函数控制 | job级 if 推迟整个 job；step级 if 控制单步 | 无 if 时默认执行 | 是 | `configure-conditional-execution.md` | ✅ |
| 3.11 | 状态函数 | success/always/cancelled/failed | 不带括号（非函数调用形式） | — | — | 同上 + `expressions.md` | ✅ |
| 3.12 | `continue-on-error` | Job/Step 失败不阻断 | job级: 失败后下游需用 `${{ always }}`；step级: 记 outcome/conclusion | false | 是 | `configure-jobs.md`, `configure-steps.md` | ✅ |
| 3.13 | `timeout-minutes` (job) | Job 超时时间（分） | 默认 360 分钟（6小时），超时强制终止 | 360 | 是 | `configure-jobs.md` | ✅ |
| 3.14 | `timeout-minutes` (step) | Step 超时时间（分） | 无默认独立限制，受 job 级控制 | 无（继承 job） | 是 | `configure-steps.md` | ✅ |
| 3.15 | job `outputs` 传递 | Step → Job → Needs 三级映射 | 每参数最大 1MB；多行需分隔符语法 | — | 是 | `pass-output-between-jobs.md` + `runtime-environment-variables.md` | ✅ |
| 3.16 | 取消语义 | 手动取消时的行为 | 正在运行的 step 终止、清理钩子是否执行 | — | — | 未详述 | ❓ |
| 3.17 | 重运行语义 | Re-run all / Re-run failed | 最多 3 次；超 6h 不可重跑；使用原始 commit 配置 | — | — | `rerun-failed-jobs.md` | ✅ |
| 3.18 | workflow_call 嵌套 | 被调用工作流执行 | 最多 2 层，inputs + secrets 传递 | — | — | 同上 | 🔶 2 层限制需核实 |

### 4. Runner 与执行环境

| # | 能力项 | 语义 | 约束/边界 | 默认值 | 可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|---|
| 4.1 | 三段式标签 | `{os-version},{arch},{flavor}` | 托管 Runner：6 档 flavor（slim~2xlarge） | `default=[ubuntu-latest,x64,small]` | 是 | `runner-and-environment.md`, `using-hosted-runners.md` | ✅ |
| 4.2 | `runs-on: default` | 快捷标签 | 等价 `[ubuntu-latest, x64, small]` | — | — | `using-hosted-runners.md` | ✅ |
| 4.3 | 自托管 Runner | 主机/K8s 两类 | self-hosted+自定义标签，全匹配规则 | — | 是 | `using-self-hosted-runners.md` | ✅ |
| 4.4 | `container.image` | 自定义 Docker 镜像 | 支持 credentials/volumes/options/env | — | 是 | `configuring-images-toolchains.md` | 🔶 container 已有的测试报告不可用(TC-273) |
| 4.5 | Runner 预装工具链 | 多语言多版本工具链 | 随镜像更新可能变化 | — | — | `runner-images-tools.md` | ✅ |
| 4.6 | Runner 资源配额 | CPU/内存/磁盘 | 6 档，默认 small(2C8G)；large+ 需申请 | — | — | `using-hosted-runners.md` | ✅ |
| 4.7 | Runner 网络出站 | 外网/内网/DNS/代理 | — | — | — | 未详述 | ❓ |
| 4.8 | Runner 复用/污染 | 是否 ephemeral？ | 复用 Runner 的残留污染 | — | — | 未声明 | ❓ 稳定性敏感 |

### 5. 变量与密钥

| # | 能力项 | 语义 | 约束/边界 | 默认值 | 可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|---|
| 5.1 | `env` 三级作用域 | workflow → job → step | 同名覆盖: step > job > workflow | — | 是 | `using-variables-secrets.md` | ✅ |
| 5.2 | `vars` 配置变量 | 组织/项目级非敏感配置 | 项目级覆盖组织级 | — | — | 同上 | 🔶 vars 上下文已有 SKIP 用例 |
| 5.3 | `secrets` 加密密钥 | 组织/项目/环境级 | 日志自动脱敏 `***`；不可查看原值 | — | — | `using-secrets.md` | ✅ |
| 5.4 | `inputs` 输入参数 | workflow_dispatch/workflow_call 入参 | 仅 string 类型 | — | — | `configure-triggers.md`, `variables.md` | ✅ |
| 5.5 | `ATOMGIT_*` 系统变量 | Runner 自动注入 ~27 个变量 | 禁止创建 ATOMGIT_ 前缀项目变量 | — | — | `variables.md`, `runtime-environment-variables.md` | 🔶 个别变量注入异常(TC-206) |
| 5.6 | 变量引用 | 表达式 `${{ env.VAR }}` vs Shell `$VAR` | YAML 层 vs Runner 层不同语义 | — | — | `using-variables-secrets.md` | ✅ |
| 5.7 | 优先级链 | step env > job env > workflow env > vars > ATOMGIT_* | — | — | — | 同上 | 🔶 含 ATOMGIT_* 的完整链待验证 |
| 5.8 | secret 日志脱敏 | `***` 遮蔽 | `echo "${{ secrets.X }}"` 可能绕过脱敏 | — | — | `using-secrets.md` | 🔶 文档自承可能绕过, 安全命脉 |

### 6. 表达式与上下文

| # | 能力项 | 语义 | 约束/边界 | 默认值 | 可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|---|
| 6.1 | `${{ }}` 表达式 | 嵌入 YAML 值中 | 支持字面量/运算符/函数 | — | — | `expressions.md` | ✅ |
| 6.2 | 比较运算符 | `==`/`!=`/`>`/`<`/`>=`/`<=` | 运算符优先级: () → ! → <> → ==,!= → && → \|\| | — | — | 同上 | ✅ |
| 6.3 | 状态函数 | `success`/`always`/`cancelled`/`failed` | 不带括号 | — | — | 同上 | ✅ |
| 6.4 | 字符串函数 | `contains`/`startsWith`/`endsWith`/`format`/`substring`/`replace` | substring 和 replace 为 GitCode 特有 | — | — | 同上 + `COMPAT-NOTES.md` | ✅ |
| 6.5 | `hashFiles` | SHA256 哈希 | 用于 cache key 生成 | — | — | 同上 | ✅ |
| 6.6 | `toJson` | 对象序列化 | — | — | — | 同上 | ✅ |
| 6.7 | `atomgit` 上下文 | 20 个属性 | 各属性类型与取值见 reference | — | — | `context.md` | 🔶 部分属性值异常(如 run_id FAIL) |
| 6.8 | `runner` 上下文 | os/arch/name/temp/tool_cache/debug | os 字面值与 GitHub 不同（Linux vs linux） | — | — | 同上 | 🔶 大小写差异已知(P3) |
| 6.9 | 上下文可用性表 | 11 种上下文 × 5 个位置 | 见 `context.md` §2.5 | — | — | 同上 | ✅ |
| 6.10 | 含括号表达式 | `${{ }}` 中嵌套括号 | 如 `hashFiles('package-lock.json')` | — | — | `expressions.md` | 🔶 已有 TC-163 字面量整数问题 |

### 7. 复用与供应链 (§7)

| # | 能力项 | 语义 | 约束/边界 | 默认值 | 可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|---|
| 7.1 | 官方 Action 引用 | `uses: action-name@ref` | 无 owner 短名（如 `checkout`/`setup-node`） | — | — | `using-actions.md` | ✅ |
| 7.2 | 开源 Action 引用 | `uses: owner/repo/path@ref` | — | — | — | 同上 | ✅ |
| 7.3 | 本地 Action 引用 | `uses: ./path/to/action` | 需同仓 action.yml | — | — | 同上 | ✅ |
| 7.4 | Action 版本 pin | tag / full version / branch / SHA | 文档推荐 tag（推荐）→ SHA（生产） | — | — | 同上 | ✅ |
| 7.5 | `runs.using` | Action 运行时 | 仅 `node16` 在文档中出现 | — | — | 同上 + `action-yml-metadata-syntax.md` | 🔶 GitHub 支持 node20/docker/composite |
| 7.6 | Action `inputs`/`outputs` | action.yml 元数据 | 含 default/required | — | — | `action-yml-metadata-syntax.md` | ✅ |
| 7.7 | `with` 参数传递 | step 级向 Action 传参 | — | — | — | `using-actions.md` | ✅ |
| 7.8 | 第三方 Action 信任 | 引用外部仓库的信任边界 | — | — | — | 未详述 | ❓ 安全敏感 |

### 8. Artifact / Cache (§8)

| # | 能力项 | 语义 | 约束/边界 | 默认值 | 可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|---|
| 8.1 | `upload-artifact` | 上传构建产物 | name/path 必填，支持 glob/多路径 | 保留天数字段已提及 | — | `upload-download-artifacts.md` | ✅ |
| 8.2 | `download-artifact` | 下载制品 | 可下载指定 name 或全部 | 下载到当前工作目录 | — | 同上 | ✅ |
| 8.3 | `cache` 插件 | 缓存依赖加速 | key（精确）/ restore-keys（前缀降级）/ path | — | — | `using-dependency-cache.md` | ✅ |
| 8.4 | cache 匹配机制 | 精确→前缀→新建 | 前缀匹配取最近同前缀缓存 | — | — | 同上 | ✅ |
| 8.5 | 制品保留期 | 可设定保留天数 | — | — | — | `core-concepts/artifacts-and-cache.md` | 🔶 未细化天数上下限 |
| 8.6 | cache LRU 淘汰 | 长期保留，LRU 淘汰 | — | — | — | 同上 | 🔶 淘汰阈值未声明 |

### 9. 可观测性 (§9)

| # | 能力项 | 语义 | 约束/边界 | 默认值 | 可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|---|
| 9.1 | 运行状态机 | queued→in_progress→completed | completed 子状态: success/failure/cancelled/skipped | — | — | `view-run-results.md` | ✅ |
| 9.2 | 日志结构 | 按 step 顺序，含时间戳 | 折叠/搜索/下载；UTF-8 编码 | — | — | `view-job-logs.md` | ✅ |
| 9.3 | `ATOMGIT_OUTPUT` | step 输出文件 | 写入后通过 `steps.<id>.outputs` 引用 | — | — | `workflow-commands.md` + `runtime-environment-variables.md` | ✅ |
| 9.4 | `ATOMGIT_ENV` | 后续 step 环境变量文件 | 当前 step 写入后不可自读，后续 step 生效 | — | — | 同上 | ✅ |
| 9.5 | `ATOMGIT_PATH` | PATH 追加文件 | 后续 step 生效 | — | — | 同上 | ✅ |
| 9.6 | `ATOMGIT_STEP_SUMMARY` | Markdown Job Summary | `>>`追加, `>`覆盖；step 完成后上传不可改 | — | — | 同上 | ✅ |
| 9.7 | `::add-mask::` | 日志脱敏命令 | 对后续日志中的值进行 `***` 遮蔽 | — | — | `using-script-commands.md` | ✅ |
| 9.8 | `::error::`/`::warning::` | 注解命令 | 创建带文件/行/列的注解 | — | — | 未在 GitCode docs 中显式声明 | ❓ GitHub 兼容点 |
| 9.9 | 状态徽标 | README 嵌入 SVG | `https://atomgit.com/{owner}/{repo}/badges/{workflow}/pipeline.svg` | — | — | `view-run-results.md` | 🔶 格式已声明，需验证 |
| 9.10 | 运行筛选 | 按 status 筛选运行列表 | Failed/Success/Running等 | — | — | 同上 | ✅ |
| 9.11 | 重运行上下文保持 | sha/ref/event_name 不变，run_id/run_number 更新 | — | — | — | `rerun-failed-jobs.md` | ✅ |

### 10. 安全与权限

| # | 能力项 | 语义 | 约束/边界 | 默认值 | 可配 | 出处 | 置信度 |
|---|---|---|---|---|---|---|---|
| 10.1 | `permissions` 六域 | project/pr/issue/note/repository/hook | 每域 read/write/none | 仓库设置默认值 | 是 | `token-permissions.md` | ✅ |
| 10.2 | 快捷语法 | `read-all`/`write-all`/`{}` | `{}` 最小权限（仅 repository:read） | — | 是 | 同上 | ✅ |
| 10.3 | Fork PR 隔离 | 自动读权限 + 不可访问 Secret | 仅 `pull_request` 事件 | — | — | `pr-mr-pipeline-security.md` | ✅ |
| 10.4 | `pull_request_target` 写权限 | base 上下文 + 完整权限 + Secret | 代码来自目标仓库，非 fork | — | — | 同上 | ✅ |
| 10.5 | 环境审批 | 环境级 Secret 可配置审批人 | — | — | — | `using-secrets.md` | 🔶 文档提及但语法未详 |
| 10.6 | Secret 命名规则 | 大写字母+数字+下划线 | 不得 ATOMGIT_ 开头，不得数字开头 | — | — | 同上 | ✅ |

---

## 二、规格缺口与存疑清单

以下项影响多个维度，供下游 agent（compat-diff / security / reliability / usability）消费。

| # | 缺口点 | 影响维度 | 说明 |
|---|---|---|---|---|
| GAP-01 | **未知/不支持字段的处理方式** | compatibility, usability | 文档未声明：非法字段是报错还是静默忽略？这是兼容性差异高发区（testing-focus §1）。 |
| GAP-02 | **`defaults.run.shell` 默认值** | compatibility | 文档未明确默认 shell（GitHub 行为取决于 runner OS），差异即迁移摩擦。 |
| GAP-03 | **`defaults.run.working-directory` 默认路径** | completeness | 未声明默认工作目录是仓库根还是其他。 |
| GAP-04 | **Runner 是否 ephemeral？** | reliability, security | 未声明 Runner 复用策略——残留污染（工作区/环境变量/缓存/进程）是稳定性与安全敏感点。 |
| GAP-05 | **`concurrency.preemption` 抢占语义不详** | reliability | 文档仅列出字段，未说明抢占条件与具体行为。 |
| GAP-06 | **`concurrency` workflow 级 vs job 级交互** | completeness | 两者可同时配置，交互语义（取最小？独立？）未声明。 |
| GAP-07 | **`paths` 匹配上限 300 文件的精确行为** | completeness, compatibility | 超 300 时是截断前 300 还是按序选取？未匹配文件是否可能误触发？ |
| GAP-08 | **`schedule` 行为目前已报告不工作** | completeness, reliability | 已知 blocker（S3 × 24 + TC-391），cron 触发的全部声明无法验证。 |
| GAP-09 | **`pull_request_comment` 的 `comments` 正则语义** | completeness | 正则引擎（POSIX/PCRE?）、锚定（部分匹配 vs 完整匹配？）、大小写敏感性未声明。 |
| GAP-10 | **取消语义细节缺失** | reliability | 手动取消时 step 收到什么信号（SIGTERM? SIGKILL? timeout?）、`post` 阶段是否仍执行、清理钩子行为——均未声明。 |
| GAP-11 | **`container` 的 `volumes` 和 `options` 已文档化但已有报告不可用** | completeness | TC-273: job 容器不可用（P2），需确认是普遍不可用还是特定场景。 |
| GAP-12 | **`runs-on` 多标签匹配中的 AND/OR 语义** | completeness | 三段式标签 `{os,arch,flavor}` 内部是 AND？与 `self-hosted` 的 `[self-hosted, linux, gpu]` 是子集匹配？文档隐含但未形式化。 |
| GAP-13 | **`::error::` / `::warning::` workflow 命令未显式声明** | compatibility, usability | GitHub 的标准注解命令，GitCode 文档未覆盖。支持否？不支持时替代方案？ |
| GAP-14 | **expression 中 `runs-on: ${{ matrix.os }},${{ matrix.arch }},small` 的逗号分隔写法** | completeness | 这种用法在三段式标签规范中未出现形式化定义——表达式解析后再做标签匹配？ |
| GAP-15 | **`needs` 指向 matrix 父 job 导致"任务初始化错误"** | completeness, reliability | 已知 P1（TC-486/481/499），spec 中 needs 与 matrix 交互未说明。 |
| GAP-16 | **`atomgit.*` 上下文属性值不符合 spec** | completeness, compatibility | 已知 FAIL: run_id (TC-040)、repository_owner (TC-038)、head_ref (TC-044)、runner.os 大小写 (TC-023)、runner.arch 格式 (TC-095)。 |
| GAP-17 | **`actions/checkout` 等内置 action 等价行为** | compatibility | 同名的内置 action（checkout/setup-node/...）行为是否与 GitHub 实现一致？文档未详细说明。 |

---

## 三、完备性意图 (INTENT-COMP-xxx)

> 格式: `INTENT-COMP-<NNN> / 标题 / 维度: completeness / 来源 / 优先级 / 简要说明`

### 3.1 语法 & 结构校验

**INTENT-COMP-001** | 未知字段的报错行为
- **维度**: completeness, compatibility
- **来源**: GAP-01, `testing-focus.md` §1
- **优先级**: P1
- **说明**: 在工作流 YAML 中引入文档未声明的字段（如非法顶层键），验证平台是报错并指明位置，还是静默忽略。静默忽略会导致用户误以为该字段生效——兼容性差异高发区。
- **Oracle**: 期望：报错并指明非法字段位置（与 GitHub 行为一致）。若静默忽略则为差异。
- **溯源风险**: RISK-COMPAT-01 (默认值/静默差异)

**INTENT-COMP-002** | `defaults.run.shell` 与 `defaults.run.working-directory` 默认值
- **维度**: completeness
- **来源**: GAP-02, GAP-03, `configure-steps.md`
- **优先级**: P1
- **说明**: 未声明 `defaults.run.shell` 和 `defaults.run.working-directory` 时，验证实际生效的 shell 类型和工作目录是什么。这直接影响所有 `run:` 步骤的行为。
- **Oracle**: 期望：shell 默认值应与 GitHub 一致（不同 OS 默认不同）。working-directory 默认应为仓库根目录（`$ATOMGIT_WORKSPACE`）。
- **溯源风险**: RISK-COMPAT-01

**INTENT-COMP-003** | `defaults.run` 三级优先级级联
- **维度**: completeness
- **来源**: `configure-steps.md` 三级优先级规则 (`working-directory.md`)、GAP-03
- **优先级**: P1
- **说明**: 验证 `defaults.run.shell` 和 `defaults.run.working-directory` 在 workflow 级→job 级→step 级的覆盖规则。配置 job 级 `defaults.run.working-directory: src`，step 级不指定时是否继承 job 级；step 级显式指定时是否覆盖。
- **Oracle**: 期望：step 级 > job 级 > workflow 级（与文档声明一致）。
- **溯源风险**: — (无已有风险项直接映射)

### 3.2 触发器

**INTENT-COMP-004** | `paths` 过滤 300 文件上限边界
- **维度**: completeness, reliability
- **来源**: GAP-07, `configure-triggers.md`
- **优先级**: P1
- **说明**: 在超过 300 个文件的 push 中，验证 paths 过滤仅在「前 300 个变更文件」中匹配的行为。超出部分不参与判断：是否仍正确匹配属于前 300 内的变更？是否可能因超限误触发？
- **Oracle**: 期望：前 300 个变更文件中包含匹配路径时触发；不包含时不触发；不因超限导致误触发或漏触发。
- **溯源风险**: — (新发现边界)

**INTENT-COMP-005** | `schedule` cron 触发完整链路
- **维度**: completeness
- **来源**: GAP-08, `configure-triggers.md` + `syntax-reference/trigger-events.md` §1.9
- **优先级**: P0 (已知 blocker)
- **说明**: 已知 scheduler 不工作（S3 × 24 + TC-391, P1 blocker）。验证 cron 定时触发从配置→调度→执行的全链路：cron 表达式解析、UTC 时区、默认分支生效、最短 5 分钟间隔约束。
- **Oracle**: 期望：配置 cron 后在指定 UTC 时刻于默认分支触发 workflow 运行。API 可验 `atomgit.event_name=schedule`。
- **溯源风险**: — (直接对应已知 blocker)

**INTENT-COMP-006** | `pull_request_comment` comments 正则过滤语义
- **维度**: completeness
- **来源**: GAP-09, `syntax-reference/trigger-events.md` §1.5
- **优先级**: P2
- **说明**: 验证 `pull_request_comment.comments` 的正则过滤行为：部分匹配还是完整匹配？区分大小写？正则引擎类型？多 patterns 间是 OR 关系？
- **Oracle**: 期望：与文档声明的正则匹配规则一致，明确匹配语义。
- **溯源风险**: — (新发现边界)

**INTENT-COMP-007** | 触发去抖：同一 push 连推是否去重
- **维度**: completeness
- **来源**: GAP-14, `testing-focus.md` §2
- **优先级**: P2
- **说明**: 快速连续推送同一分支（如 `git push && git push -f`），验证是否每次都触发 workflow 运行（无去抖），还是有去重/队列机制。
- **Oracle**: 期望：每次 push 都应产生独立的 workflow run（与 GitHub 行为一致）。若去重则为差异。
- **溯源风险**: RISK-COMPAT-01

### 3.3 执行模型

**INTENT-COMP-008** | `concurrency` workflow 级并发控制完整行为
- **维度**: completeness, reliability
- **来源**: GAP-05, `workflow-file-location-structure.md`
- **优先级**: P1
- **说明**: 验证 `concurrency` 的完整行为链：(1) `max: 3` 时第 4 个触发按 `exceed-action: QUEUE` 排队还是 `IGNORE` 丢弃；(2) 排队触发在前序运行完成后自动调度；(3) `preemption.enable: true` + 事件列表的抢占条件与行为。
- **Oracle**: 期望：QUEUE 时后续触发排队、前序完成后依次执行；IGNORE 时丢弃；preemption 按事件条件抢占。
- **溯源风险**: RISK-REL-01 (并发公平性)

**INTENT-COMP-009** | `concurrency` workflow 级与 job 级同时配置的交互
- **维度**: completeness
- **来源**: GAP-06, `workflow-file-location-structure.md` + `configure-jobs.md`
- **优先级**: P2
- **说明**: 同时配置 workflow 级和 job 级 `concurrency` 时，验证实际生效的并发限制是取最小值、独立生效还是后者覆盖前者。
- **Oracle**: 期望：若文档明确规则则按规则；否则记录实测行为（取最小值是最安全推断）。
- **溯源风险**: RISK-REL-01

**INTENT-COMP-010** | `stages.fail_fast` 与 `strategy.fail-fast` 独立性
- **维度**: completeness, reliability
- **来源**: `configure-dependencies-order.md` + `configure-matrix-builds.md`
- **优先级**: P1
- **说明**: 文档指出两者是不同层面的控制。验证：(1) stages.fail_fast 不影响其他 stage 的矩阵内行为；(2) strategy.fail-fast 不影响同 stage 其他 job；(3) 两者同时为 true 时的综合行为。
- **Oracle**: 期望：两者独立生效，不交叉影响。
- **溯源风险**: — (无已有风险项直接映射)

**INTENT-COMP-011** | `continue-on-error` 对 `if` 条件中状态函数的影响
- **维度**: completeness
- **来源**: `configure-jobs.md` + `configure-conditional-execution.md`
- **优先级**: P1
- **说明**: 文档声称 `continue-on-error: true` 的 job 失败后，后续 job 中 `if: ${{ success }}` 条件不满足、需用 `if: ${{ always }}`。验证此语义是否正确，以及 step 级 `continue-on-error` 对 `steps.<id>.outcome` vs `steps.<id>.conclusion` 的影响。
- **Oracle**: 期望：job 级 `continue-on-error: true` 时，该 job 的 outcome 为非 success，但 workflow 不终止；下游 job 的 `if: ${{ success }}` 应不满足。
- **溯源风险**: — (新发现边界)

**INTENT-COMP-012** | `workflow_call` 最大 2 层嵌套限制
- **维度**: completeness
- **来源**: COMPAT-NOTES §5, `configure-triggers.md`
- **优先级**: P1
- **说明**: 文档声明可重用工作流最多 2 层嵌套。验证第 3 层嵌套时平台的行为：报错？静默不触发？还是实际可执行但文档保守？
- **Oracle**: 期望：第 3 层嵌套应被拦截并给出明确错误（而非静默失败）。
- **溯源风险**: — (新发现边界)

### 3.4 Runner & 环境

**INTENT-COMP-013** | Runner 是否 ephemeral（一次性）
- **维度**: completeness, reliability, security
- **来源**: GAP-04, `testing-focus.md` §4
- **优先级**: P1
- **说明**: 验证托管 Runner 是否一次性（每次 Job 分配全新 Runner）还是可复用。复用场景下验证：工作区残留、环境变量残留、缓存/进程残留。
- **Oracle**: 期望：托管 Runner 应为 ephemeral（每次新实例）。若可复用，残留风险需记录为已知差异。
- **溯源风险**: RISK-REL-01

**INTENT-COMP-014** | `container` 完整字段实际可用性
- **维度**: completeness
- **来源**: GAP-11, `configuring-images-toolchains.md` + TC-273
- **优先级**: P1
- **说明**: 已知 TC-273 报告 Job 容器不可用（P2）。验证 `container` 全字段：`image`（公共/私有镜像）、`credentials`（私仓认证）、`volumes`（卷挂载）、`options`（Docker 附加参数）、`env`（容器内环境变量）——哪些实际可用、哪些不可用。
- **Oracle**: 期望：至少 `container.image` 可正常拉取镜像并执行；私仓认证应生效。不可用的字段应明确报错。
- **溯源风险**: — (对应 TC-273 已知问题)

**INTENT-COMP-015** | `runs-on` 多标签匹配语义
- **维度**: completeness, compatibility
- **来源**: GAP-12, `selecting-runner-labels.md` + `runner-and-environment.md`
- **优先级**: P1
- **说明**: 验证：(1) 三段式 `{ubuntu-24,x64,small}` 与 `[ubuntu-latest, x64, small]` 是否等效？(2) 自托管标签 `[self-hosted, linux, gpu]` 的子集匹配；(3) 无匹配 Runner 时的等待/超时/报错行为。
- **Oracle**: 期望：三段式与数组式等效；自托管为全匹配子集规则；无匹配时超时报错并给出可操作提示。
- **溯源风险**: — (新发现边界)

**INTENT-COMP-016** | 托管 Runner 资源超限行为
- **维度**: completeness, reliability
- **来源**: `using-hosted-runners.md` 六档规格, `testing-focus.md` §4
- **优先级**: P1
- **说明**: 验证 Runner 在内存/磁盘超出规格时的行为：OOM kill 是否可观测？磁盘满时 step 报错信息是否清晰？超限后 Job 的状态标记。
- **Oracle**: 期望：OOM 时应标记 job failure + 日志中可见 OOM 信号；磁盘满时应给出明确"磁盘不足"报错而非泛化 failure。
- **溯源风险**: RISK-REL-01

### 3.5 变量 & 输出

**INTENT-COMP-017** | `job.outputs` 三级传递完整链路
- **维度**: completeness
- **来源**: `pass-output-between-jobs.md` + `runtime-environment-variables.md`, GAP-15
- **优先级**: P1
- **说明**: 验证完整传递链: Step 写 `ATOMGIT_OUTPUT` → `steps.<id>.outputs.xxx` → Job `outputs` 映射 → `needs.<job_id>.outputs.xxx`。覆盖：单值、多行值（分隔符语法）、1MB 上限边界、矩阵 job 内部 outputs 传递（修复已知 bug）。
- **Oracle**: 期望：三级映射均正确传递；矩阵 job 内 outputs 应可正常传递（当前 P1 FAIL: TC-486/481/499）。
- **溯源风险**: — (直接对应已知 P1 FAIL)

**INTENT-COMP-018** | `ATOMGIT_*` 系统变量完整注入验证
- **维度**: completeness
- **来源**: GAP-16, `variables.md` + `runtime-environment-variables.md`
- **优先级**: P1
- **说明**: 验证文档声明的 ~27 个系统变量全部注入且值符合 spec。重点修复已知 FAIL：`ATOMGIT_RUN_ID`、`ATOMGIT_REPOSITORY_OWNER`、`ATOMGIT_HEAD_REF`、`runner.os`/`runner.arch` 格式。
- **Oracle**: 期望：所有声明变量可读且值格式符合 spec。`runner.os: Linux`(非 linux)；`runner.arch: X64`(非 x86_64)。
- **溯源风险**: — (直接对应已知 FAIL)

**INTENT-COMP-019** | 变量优先级完整链验证 (step > job > workflow > vars > ATOMGIT_*)
- **维度**: completeness
- **来源**: GAP-17, `using-variables-secrets.md`
- **优先级**: P1
- **说明**: 文档声明的优先级链为 `step env > job env > workflow env > vars > ATOMGIT_*`。验证：同名变量在不同层级定义时，实际取值是否按此优先级。特别验证 `vars > ATOMGIT_*` 这环节（已知不能创建 ATOMGIT_ 前缀 vars）。
- **Oracle**: 期望：优先级链按文档声明生效。平台禁止创建 ATOMGIT_ 前缀 vars 时，vars > ATOMGIT_* 环节实际为 N/A，应记录。
- **溯源风险**: — (新发现边界)

### 3.6 表达式 & 上下文

**INTENT-COMP-020** | `substring` 和 `replace` 函数行为
- **维度**: completeness, compatibility
- **来源**: COMPAT-NOTES §3, `expressions.md` §3.3
- **优先级**: P1
- **说明**: GitCode 独有的 `substring(str, start, len)` 和 `replace(str, old, new)`。验证：(1) start 越界行为；(2) len 超出字符串长度时行为；(3) replace 的 old 不存在时行为；(4) 空字符串/特殊字符处理。
- **Oracle**: 期望：遵循常见字符串库语义：substring 越界返回空或截断；replace 无匹配返回原字符串。
- **溯源风险**: RISK-COMPAT-01

**INTENT-COMP-021** | `hashFiles` 多文件与 glob 组合
- **维度**: completeness
- **来源**: `expressions.md` §3.3
- **优先级**: P2
- **说明**: 验证 `hashFiles` 对多个 glob pattern 的组合哈希（`hashFiles('src/**', 'package.json')`）、无匹配文件时的行为、以及大文件/大量文件时的性能。
- **Oracle**: 期望：多 pattern 为组合哈希；无匹配文件时应有明确行为（报错或返回空哈希）。
- **溯源风险**: — (新发现边界)

**INTENT-COMP-022** | 含括号表达式的嵌套解析
- **维度**: completeness
- **来源**: `expressions.md` §3.3, `configure-conditional-execution.md`
- **优先级**: P2
- **说明**: 验证嵌套括号的表达式（如 `${{ contains(atomgit.ref, 'main') }}`、`${{ format('{0}', matrix.version) }}`）在 `if` 条件、`env` 赋值、`runs-on` 等不同上下文中的解析正确性。
- **Oracle**: 期望：嵌套括号表达式在所有上下文中正确求值。已知 TC-163 字面量整数问题应已修复。
- **溯源风险**: RISK-COMPAT-01

### 3.7 Artifact & Cache

**INTENT-COMP-023** | 制品保留期边界
- **维度**: completeness
- **来源**: GAP-05, `upload-download-artifacts.md` + `core-concepts/artifacts-and-cache.md`
- **优先级**: P2
- **说明**: 验证 artifact 的保留天数配置实际生效：设置 N 天后，制品在 N 天内可下载、超过 N 天后被清除。同时验证保留天数的最小/最大允许范围。
- **Oracle**: 期望：配置的保留天数内制品可下载；超出后被清除（API 不返回）。
- **溯源风险**: — (新发现边界)

**INTENT-COMP-024** | cache 恢复-键降级匹配
- **维度**: completeness
- **来源**: `using-dependency-cache.md`
- **优先级**: P2
- **说明**: 验证 cache 的精确→前缀降级→新建的完整匹配链：(1) 精确 key 命中时直接恢复；(2) 无精确匹配时按 restore-keys 前缀顺序匹配最近缓存；(3) 全部未命中时 step 执行后保存新缓存。
- **Oracle**: 期望：匹配链按文档描述的降级逻辑工作；第二次运行时精确命中且无重复下载。
- **溯源风险**: — (新发现边界)

### 3.8 可观测性

**INTENT-COMP-025** | `ATOMGIT_STEP_SUMMARY` 的 Markdown 渲染与上传
- **维度**: completeness, usability
- **来源**: `workflow-commands.md` + `runtime-environment-variables.md` §5
- **优先级**: P2
- **说明**: 验证 (1) Step Summary 写入 Markdown 后在运行详情页正确渲染（表格、标题、代码块等）；(2) 多个 step 写入时 append 语义；(3) step 完成后内容不可改。
- **Oracle**: 期望：运行详情页可见渲染后的 Markdown Summary；多 step 追加内容合并显示。
- **溯源风险**: — (新发现边界)

**INTENT-COMP-026** | `::add-mask::` 脱敏命令
- **维度**: completeness, security
- **来源**: `using-script-commands.md`
- **优先级**: P1
- **说明**: 验证 `echo "::add-mask::$VALUE"` 后，该值在后续所有日志输出中被 `***` 遮蔽，包括 echo 打印、命令输出中的出现。
- **Oracle**: 期望：add-mask 后该值在所有日志行中被替换为 `***`。
- **溯源风险**: RISK-SEC-02 (注入/脱敏)

**INTENT-COMP-027** | 状态徽章 URL 生成与可访问性
- **维度**: completeness
- **来源**: `view-run-results.md`
- **优先级**: P2
- **说明**: 验证文档声明的徽章 URL 格式 (`https://atomgit.com/{owner}/{repo}/badges/{workflow_name}/pipeline.svg`) 实际可访问并返回对应 workflow 的运行状态 SVG。
- **Oracle**: 期望：URL 可访问并返回 SVG；状态与最新运行一致。
- **溯源风险**: — (新发现边界)

### 3.9 Post 阶段

**INTENT-COMP-028** | `post` 阶段的 `run_always` 默认行为
- **维度**: completeness
- **来源**: `workflow-file-location-structure.md` + `core-concepts/workflow-job-step-action.md`
- **优先级**: P1
- **说明**: 验证 `post` 阶段默认 `run_always: true` 行为：(1) workflow 成功时 post 执行；(2) workflow 失败时 post 仍执行（默认 run_always）；(3) `run_always: false` 时仅成功执行。
- **Oracle**: 期望：默认 run_always=true 时无论成败都执行 post；run_always=false 仅成功时执行。
- **溯源风险**: — (新发现边界)

### 3.10 Permissions & Token

**INTENT-COMP-029** | `permissions: {}` 最小权限语义
- **维度**: completeness, security
- **来源**: `token-permissions.md`, `workflow-file-location-structure.md`
- **优先级**: P1
- **说明**: 验证 `permissions: {}`（空对象）的实际权限范围：文档声称仅 repository:read。验证 ATOMGIT_TOKEN 是否可写 PR、写 Issue、读 hook 等——应全部被拒绝。
- **Oracle**: 期望：`permissions: {}` 时 ATOMGIT_TOKEN 仅可读仓库，所有其他操作应被拒绝（403/401）。
- **溯源风险**: RISK-SEC-01 (权限越界)

**INTENT-COMP-030** | `permissions` 快捷语法 `read-all` / `write-all`
- **维度**: completeness
- **来源**: `token-permissions.md`
- **优先级**: P1
- **说明**: 验证 `permissions: read-all` 将 6 个权限域均设为 read；`permissions: write-all` 均设为 write。每域的 read/write 实际权限范围是否与文档一致。
- **Oracle**: 期望：`read-all` 时所有域只读、写操作被拒绝；`write-all` 时所有域可写。
- **溯源风险**: RISK-SEC-01

**INTENT-COMP-031** | 未声明 `permissions` 时的默认权限
- **维度**: completeness, compatibility
- **来源**: GAP-01, `token-permissions.md`, COMPAT-NOTES §6
- **优先级**: P1
- **说明**: 文档声称"未声明 permissions 时使用仓库设置定义的权限"。验证默认行为：是沿用仓库设置？是沿用平台全局默认？与 GitHub 的 "permissive by default" 是否一致？
- **Oracle**: 期望：未声明时的实际权限范围应明确。若宽于用户预期则为安全风险。
- **溯源风险**: RISK-SEC-01, RISK-COMPAT-01

---

## 四、覆盖度总览

### 按 testing-focus.md 章节

| 章节 | 能力项数量 | 意图数量 | 备注 |
|---|---|---|---|
| §1 Workflow 语法解析与静态校验 | 12 | 3 | GAP-01~03 |
| §2 触发器语义 | 14 | 4 | schedule blocker (P0) |
| §3 执行模型 | 18 | 5 | concurrency/stages/matrix |
| §4 Runner 与执行环境 | 8 | 4 | ephemeral/container/runs-on |
| §5 Variables & Secrets | 8 | 3 | 优先级链/ATOMGIT_* |
| §6 Expressions & Context | 10 | 3 | substring/replace/hashFiles |
| §7 复用与供应链 | 8 | 0 | 已被其他维度或已有用例覆盖 |
| §8 Artifact/Cache | 6 | 2 | 保留期/cache降级 |
| §9 可观测性 | 11 | 3 | summary/mask/badge |
| §10 安全与权限 | 6 | 3 | permissions 语义 |
| **合计** | **101** | **31** | |

### 按优先级

| 优先级 | 意图数量 | 说明 |
|---|---|---|
| P0 (blocker) | 1 | INTENT-COMP-005: schedule 完全不可用 |
| P1 | 22 | 核心能力验证 + 已知 bug 跟踪 |
| P2 | 8 | 边界与体验完善 |

### 与已有 KEEP 用例的关系

- 260 条 KEEP 用例已覆盖大部分基本语法、上下文、变量、触发器、矩阵等。
- 本批 31 条意图定位于 **KEEP 用例未覆盖的规格声明与边界验证**（如 concurrency 完整行为、post 阶段默认 run_always、permissions 快捷语法等）。
- 与 case-base-detail 中 NEEDS-UPDATE 的 62 条（含 25 个独立 bug 分类）无重复——本批定位的是"文档声明了、但尚无测试覆盖"的能力，而非已知 bug 重新验证。

---

## 五、质量清单自检

- [x] 每条能力项都有出处（文件+描述），无凭空条目。
- [x] 默认值/边界被显式记录（见"默认值"列；未声明处标注 `🔶模糊` 或 `❓未知`）。
- [x] 存疑项标了置信度并指明下游消费方（GAP 清单标注影响维度）。
- [x] 不编造规格；文档没写的标 `❓未知`。
- [x] 不做兼容性判断（compat-diff 职责），仅客观记录 GitCode 侧事实。
- [x] 意图不重复已有 KEEP 用例；每个 intent 指向明确的 spec 出处。
