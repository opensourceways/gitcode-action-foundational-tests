# Intent Library（汇总意图库）

> Run: 2026-07-22-01
> 评审角色: orchestrator + review-gate
> 评审日期: 2026-07-22
> 原始 intent 总数: 195 条（spec 30 + compat 35 + security 36 + reliability 66 + usability 28）
> 准入: 186 条 | 打回: 9 条 | ID 冲突: 6 组

---

## 统计摘要

| 维度 | 原始数量 | 准入数量 | P0 | P1 | P2 | 打回 | 已有覆盖 |
|---|---|---|---|---|---|---|---|
| completeness | 18 | 16 | 6 | 9 | 1 | 2 | 14 |
| compatibility | 40 | 35 | 6 | 26 | 3 | 5 | 22 |
| security | 36 | 36 | 35 | 1 | 0 | 0 | 12 |
| reliability | 66 | 66 | 0 | 64 | 2 | 0 | 28 |
| usability | 28 | 28 | 1 | 26 | 1 | 0 | 18 |
| spec-usability (增补) | 3 | 1 | 0 | 1 | 0 | 2 | 1 |
| **合计** | **195** | **186** | **48** | **132** | **6** | **9** | **95** |

> 注：spec.md 产出的 3 条 usability intent 中，2 条因粗粒度/重复被打回，1 条（USE-030）保留；spec.md 产出的 5 条 compatibility intent（COMPAT-019~023）与 compat.md 编号冲突且内容被后者细化覆盖，全部打回。

---

## 准入意图清单

### 维度：completeness

| 意图 ID | 标题 | 优先级 | 覆盖风险/能力项 | 去重关系 | 已有覆盖 |
|---|---|---|---|---|---|
| INTENT-COMP-001 | 验证工作流文件目录 `.gitcode/workflows/` 的识别行为 | P1 | RISK-COMPAT-01 / 目录识别 | 独立 | TC-366, TC-383 |
| INTENT-COMP-002 | 验证未知/不支持字段的 YAML 校验行为 | P1 | RISK-COMPAT-01 / 未知字段降级 | 独立 | TC-274, TC-336 等 |
| INTENT-COMP-003 | 验证 push 触发 + branches/paths/tags 过滤的完整行为 | P1 | RISK-REL-01 / 触发器核心 | 独立 | TC-223, TC-229~233 |
| INTENT-COMP-004 | 验证 pull_request vs pull_request_target 隔离强度 | P0 | RISK-SEC-01 / 安全命脉 | 独立 | TC-445, TC-461~463 |
| INTENT-COMP-005 | 验证 schedule cron 语义（最短 5 分钟、UTC、仅默认分支） | P1 | RISK-COMPAT-01 / 定时触发 | 独立 | TC-427~430 |
| INTENT-COMP-006 | 验证 workflow_call 嵌套层数限制（最多 2 层） | P1 | RISK-REL-01 / 可重用工作流 | 独立 | TC-426, TC-564 |
| INTENT-COMP-007 | 验证 stages 阶段机制与 post 后处理阶段语义 | P1 | RISK-REL-01 / 执行模型 | 独立 | TC-402~404, TC-406~407 |
| INTENT-COMP-008 | 验证 timeout-minutes 默认 360 分钟与强制终止行为 | P1 | RISK-REL-01 / 超时机制 | 独立 | TC-270 |
| INTENT-COMP-009 | 验证 rerun 次数限制与上下文保持语义 | P1 | RISK-REL-01 / 可观测性 | 独立 | TC-350 |
| INTENT-COMP-010 | 验证 runs-on 三段式标签体系与 default 快捷标签 | P1 | RISK-COMPAT-01 / Runner 基础 | 独立 | TC-363, TC-365, TC-446~457 |
| INTENT-COMP-011 | 验证 Runner 环境隔离强度（是否 ephemeral） | P0 | RISK-SEC-01 / 安全与稳定性 | 独立 | — |
| INTENT-COMP-012 | 验证 secrets 日志脱敏与绕过场景 | P0 | RISK-SEC-01 / 安全命脉 | 独立 | TC-011, TC-354 |
| INTENT-COMP-013 | 验证 permissions 默认权限与声明语义 | P0 | RISK-SEC-01 / 安全命脉 | 独立 | TC-351~416 |
| INTENT-COMP-014 | 验证 pull_request_target checkout head.sha 的注入风险 | P0 | RISK-SEC-01 / 安全命脉 | 独立 | TC-461~463 |
| INTENT-COMP-015 | 验证 upload-artifact / download-artifact 跨 job 传递与保留期 | P1 | RISK-REL-01 / Artifact 基础 | 独立 | TC-294~300, TC-378~380 |
| INTENT-COMP-016 | 验证 cache 作用域与 fork 隔离策略 | P0 | RISK-SEC-01 / 安全与稳定性 | 独立 | TC-301~303 |
| INTENT-COMP-017 | 验证运行状态机与日志完整性 | P1 | RISK-USE-01 / 可观测性 | 独立 | TC-347, TC-348 |
| INTENT-COMP-018 | 验证 ATOMGIT_STEP_SUMMARY Markdown 渲染与安全性 | P1 | RISK-USE-01 / 可观测性 | 独立 | TC-219, TC-246, TC-497 |


### 维度：compatibility

| 意图 ID | 标题 | 优先级 | 覆盖风险/能力项 | 去重关系 | 已有覆盖 |
|---|---|---|---|---|---|
| INTENT-COMPAT-001 | 默认 shell 与默认工作目录在未声明时的隐式行为差异 | P1 | RISK-COMPAT-01 / 默认值差异 | 独立 | TC-288 |
| INTENT-COMPAT-002 | 未声明 permissions 时的默认 TOKEN 权限范围差异 | P0 | RISK-SEC-01 / 默认权限 | 独立 | TC-351~416 |
| INTENT-COMPAT-003 | step/job 级 if 条件未显式声明时的默认状态检查差异 | P1 | RISK-COMPAT-01 / 默认值差异 | 独立 | TC-176~179 |
| INTENT-COMPAT-004 | 状态函数括号语法差异：GitHub `success()` vs GitCode `success` | P1 | RISK-COMPAT-01 / 语法差异 | 独立 | TC-176~179, TC-317~321 |
| INTENT-COMPAT-005 | 失败状态函数命名差异：`failure()` vs `failed` | P1 | RISK-COMPAT-01 / 语法差异 | 变体自 COMPAT-004 | TC-178, TC-320 |
| INTENT-COMPAT-006 | `contains` 函数边界行为差异（大小写、空值、数组元素） | P1 | RISK-COMPAT-01 / 表达式差异 | 独立 | TC-180, TC-543~544 |
| INTENT-COMPAT-007 | `hashFiles` 函数边界行为差异（无匹配文件、glob 语义） | P1 | RISK-COMPAT-01 / 表达式差异 | 独立 | TC-186, TC-550 |
| INTENT-COMPAT-008 | `toJson` 输出格式差异（pretty-print vs 压缩） | P1 | RISK-COMPAT-01 / 表达式差异 | 独立 | TC-187, TC-549 |
| INTENT-COMPAT-009 | 表达式 loose equality 与类型强制转换规则差异 | P1 | RISK-COMPAT-01 / 表达式差异 | 独立 | TC-160~175 |
| INTENT-COMPAT-010 | 缺失表达式函数 `join()` / `fromJSON()` / `case()` 的降级行为 | P1 | RISK-USE-01 / 迁移报错 | 独立 | — |
| INTENT-COMPAT-011 | `pull_request` 事件 types 命名与取值差异 | P1 | RISK-USE-01 / 触发器差异 | 独立 | TC-234, TC-560 |
| INTENT-COMPAT-012 | `paths` 匹配文件数上限差异：GitHub 3,000 vs GitCode 300 | P1 | RISK-COMPAT-01 / 触发器差异 | 独立 | TC-422, TC-514~515 |
| INTENT-COMPAT-013 | `schedule` cron timezone 支持差异：GitHub IANA vs GitCode UTC | P1 | RISK-COMPAT-01 / 定时触发 | 独立 | TC-427~430 |
| INTENT-COMPAT-014 | `workflow_dispatch` / `workflow_call` inputs 类型限制：仅支持 string | P1 | RISK-USE-01 / 输入类型 | 独立 | TC-014, TC-193, TC-581 |
| INTENT-COMPAT-015 | `workflow_call` 可复用工作流嵌套层数差异：GitHub 无上限 vs GitCode 2 层 | P1 | RISK-COMPAT-01 / 可重用工作流 | 独立 | TC-426, TC-564 |
| INTENT-COMPAT-016 | 核心上下文对象前缀差异：`github.*` vs `atomgit.*` | P1 | RISK-USE-01 / 上下文差异 | 独立 | TC-017~018 |
| INTENT-COMPAT-017 | 系统环境变量前缀差异：`GITHUB_*` vs `ATOMGIT_*` | P1 | RISK-USE-01 / 环境变量差异 | 独立 | TC-197~218 |
| INTENT-COMPAT-018 | `runner.os` 值格式差异：GitHub `Linux` vs GitCode `linux` | P1 | RISK-COMPAT-01 / Runner 上下文 | 独立 | TC-023, TC-094, TC-136~139 |
| INTENT-COMPAT-019 | `runner.arch` 值格式差异：GitHub `X64` vs GitCode `x86_64` | P1 | RISK-COMPAT-01 / Runner 上下文 | 独立 | TC-095, TC-442 |
| INTENT-COMPAT-020 | 自动令牌命名差异：`GITHUB_TOKEN` vs `ATOMGIT_TOKEN` | P1 | RISK-USE-01 / 令牌差异 | 独立 | TC-036, TC-196 |
| INTENT-COMPAT-021 | 未知/不支持字段的降级方式：报错 vs 静默忽略 vs 部分支持 | P1 | RISK-USE-01 / 未知字段 | 已关联 COMP-002 | TC-274, TC-336 |
| INTENT-COMPAT-022 | `vars` 上下文不支持时的降级行为 | P1 | RISK-COMPAT-01 / 上下文差异 | 独立 | TC-019, TC-115~119 |
| INTENT-COMPAT-023 | `jobs.<id>.environment` 字段支持情况与降级行为 | P1 | RISK-USE-01 / 环境字段 | 独立 | TC-010, TC-274 |
| INTENT-COMPAT-024 | 内置 action 短名引用行为等价性：`actions/checkout@v4` vs `checkout` | P1 | RISK-COMPAT-01 / Action 引用 | 独立 | TC-304, TC-354 |
| INTENT-COMPAT-025 | 内置 action `cache` 行为等价性与 fork 隔离 | P0 | RISK-SEC-01 / cache 投毒 | 已关联 SEC-018 | TC-301~303 |
| INTENT-COMPAT-026 | 内置 action `upload-artifact`/`download-artifact` 行为等价性 | P1 | RISK-COMPAT-01 / Artifact 差异 | 已关联 COMP-015 | TC-294~300 |
| INTENT-COMPAT-027 | `runs-on` 标签体系差异：GitHub 单标签 vs GitCode 三段式 | P1 | RISK-USE-01 / Runner 标签 | 已关联 COMP-010 | TC-363, TC-365, TC-571~573 |
| INTENT-COMPAT-028 | Runner 环境隔离与复用策略未明确 | P0 | RISK-SEC-01 / Runner 隔离 | 已关联 SEC-020 | — |
| INTENT-COMPAT-029 | 工作流文件目录差异：`.github/workflows/` vs `.gitcode/workflows/` | P1 | RISK-USE-01 / 目录差异 | 已关联 COMP-001 | TC-366, TC-383 |
| INTENT-COMPAT-030 | `permissions` 权限域命名完全差异 | P0 | RISK-SEC-01 / 权限命名 | 已关联 USE-005 | TC-351~416 |
| INTENT-COMPAT-031 | 迁移报错质量：遇到不兼容语法时错误信息是否指明 GitCode 差异 | P1 | RISK-USE-01 / 迁移报错 | 独立 | — |
| INTENT-COMPAT-032 | `pull_request_target` 语义一致性：fork PR 高权限运行不可信代码风险 | P0 | RISK-SEC-01 / Pwn Request | 已关联 SEC-035 | TC-461~463 |
| INTENT-COMPAT-033 | Secret 日志脱敏绕过风险：`echo "${{ secrets.X }}"` 可能泄露 | P0 | RISK-SEC-01 / 脱敏绕过 | 已关联 SEC-004~008 | TC-011 |
| INTENT-COMPAT-034 | `concurrency` 字段结构与语义差异 | P1 | RISK-COMPAT-01 / 并发控制 | 已关联 REL-001~006 | TC-289~293, TC-518~523 |
| INTENT-COMPAT-035 | `steps` 上下文中的 `outcome` 与 `conclusion` 语义差异 | P1 | RISK-COMPAT-01 / 步骤结果 | 独立 | TC-090~092 |


### 维度：security

| 意图 ID | 标题 | 优先级 | 覆盖风险/能力项 | 去重关系 | 已有覆盖 |
|---|---|---|---|---|---|
| INTENT-SEC-001 | fork PR 触发 pull_request 时不可读取项目 secrets | P0 | RISK-SEC-01 / fork PR secret 隔离 | 独立 | TC-445 |
| INTENT-SEC-002 | pull_request_target 事件下显式 checkout 不可信 PR 代码时，secrets 与写权限仍应受控 | P0 | RISK-SEC-01 / Pwn Request | 变体自 SEC-035 | TC-461~463 |
| INTENT-SEC-003 | fork PR 触发 pull_request 时 ATOMGIT_TOKEN 必须仅拥有 read 权限 | P0 | RISK-SEC-01 / TOKEN 降级 | 独立 | TC-445 |
| INTENT-SEC-004 | Secret 值在运行日志、step summary 和错误堆栈中必须被自动脱敏为 *** | P0 | RISK-SEC-01 / 脱敏基础 | 独立 | TC-011, TC-354 |
| INTENT-SEC-005 | Secret 日志脱敏不可通过 base64 编码绕过 | P0 | RISK-SEC-01 / 脱敏绕过 | 变体自 SEC-004 | — |
| INTENT-SEC-006 | Secret 日志脱敏不可通过字符串拼接或插值绕过 | P0 | RISK-SEC-01 / 脱敏绕过 | 变体自 SEC-004 | — |
| INTENT-SEC-007 | Secret 日志脱敏不可通过多行值输出绕过 | P0 | RISK-SEC-01 / 脱敏绕过 | 变体自 SEC-004 | — |
| INTENT-SEC-008 | Secret 日志脱敏不可通过分片输出绕过 | P0 | RISK-SEC-01 / 脱敏绕过 | 变体自 SEC-004 | — |
| INTENT-SEC-009 | 不可信 PR 标题/正文不可直接插进 run 脚本导致命令注入 | P0 | RISK-SEC-02 / 表达式注入 | 独立 | — |
| INTENT-SEC-010 | 不可信分支名/标签名不可直接插进 run 脚本导致命令注入 | P0 | RISK-SEC-02 / 表达式注入 | 变体自 SEC-009 | — |
| INTENT-SEC-011 | 不可信 issue/PR 评论内容不可直接插进 run 脚本导致命令注入 | P0 | RISK-SEC-02 / 表达式注入 | 变体自 SEC-009 | — |
| INTENT-SEC-012 | 不可信 commit message / author email 不可直接插进 run 脚本导致命令注入 | P0 | RISK-SEC-02 / 表达式注入 | 变体自 SEC-009 | — |
| INTENT-SEC-013 | 表达式求值必须防止双重模板渲染（二次求值） | P0 | RISK-SEC-02 / 模板注入 | 独立 | — |
| INTENT-SEC-014 | 第三方 Action 引用应支持完整 commit hash 固定 | P0 | RISK-SEC-02 / 供应链安全 | 独立 | TC-628 |
| INTENT-SEC-015 | 第三方 Action 来源应具备信任边界（typosquatting / 未审核 Action 限制） | P0 | RISK-SEC-02 / 供应链安全 | 独立 | — |
| INTENT-SEC-016 | 显式声明的 permissions 必须在 job 级实际生效并限制 ATOMGIT_TOKEN | P0 | RISK-SEC-01 / 权限最小化 | 独立 | TC-351~416 |
| INTENT-SEC-017 | 未声明 permissions 时 ATOMGIT_TOKEN 默认权限必须最小化（read-only） | P0 | RISK-SEC-01 / 默认权限 | 独立 | TC-351~416 |
| INTENT-SEC-018 | fork PR 写入的 cache 必须不可被主仓后续 workflow 读取 | P0 | RISK-SEC-01 / cache 投毒 | 独立 | TC-301~303 |
| INTENT-SEC-019 | fork PR 上传的 artifact 必须不可被主仓 workflow 下载或执行 | P0 | RISK-SEC-01 / artifact 投毒 | 独立 | — |
| INTENT-SEC-020 | Job 结束后 workspace 与临时文件必须被彻底清理，防止跨 job 敏感信息泄露 | P0 | RISK-SEC-01 / Runner 残留 | 独立 | — |
| INTENT-SEC-021 | Runner 环境变量与共享目录（/tmp 等）必须跨 job 隔离 | P0 | RISK-SEC-01 / Runner 残留 | 变体自 SEC-020 | — |
| INTENT-SEC-022 | 自托管 Runner 跨项目残留必须被隔离，防止项目间信息泄露 | P0 | RISK-SEC-01 / 多租户隔离 | 变体自 SEC-020 | — |
| INTENT-SEC-023 | Runner 网络出站必须受控，防止 SSRF 与内网跳板 | P0 | RISK-SEC-02 / 网络边界 | 独立 | — |
| INTENT-SEC-024 | Secret/变量名含特殊字符（如中划线）时不可导致意外求值或权限绕过 | P0 | RISK-SEC-02 / 输入处理 | 独立 | TC-531 |
| INTENT-SEC-025 | 通过 printenv 或进程枚举获取 ATOMGIT_TOKEN/secrets 时，日志中必须保持脱敏 | P0 | RISK-SEC-01 / 侧信道脱敏 | 变体自 SEC-004 | TC-011 |
| INTENT-SEC-026 | issue_comment / pull_request_comment 触发关键字过滤必须不可被绕过 | P0 | RISK-SEC-02 / 评论触发 | 独立 | TC-464~470 |
| INTENT-SEC-027 | 环境级 secret 必须经审批后才能被 workflow 访问 | P0 | RISK-SEC-01 / 环境审批 | 独立 | TC-010 |
| INTENT-SEC-028 | Workflow 命令（如 add-mask）的响应本身不可泄露被遮蔽前的 secret 值 | P0 | RISK-SEC-01 / 脱敏时序 | 变体自 SEC-004 | TC-436 |
| INTENT-SEC-029 | 跨运行 artifact 必须被视为不可信数据（artifact 投毒防护） | P0 | RISK-SEC-02 / 供应链安全 | 变体自 SEC-019 | — |
| INTENT-SEC-030 | 工作流写协议（ATOMGIT_ENV/OUTPUT/PATH）不被不可信输入污染提权 | P0 | RISK-SEC-02 / 协议注入 | 独立 | TC-243~245, TC-434~435 |
| INTENT-SEC-031 | TOCTOU：审批后推送新 commit / 评论触发不绕过审批与代码固定 | P0 | RISK-SEC-02 / 审批绕过 | 独立 | — |
| INTENT-SEC-032 | Secret 不经 output / artifact / step summary 侧信道绕过脱敏外泄 | P0 | RISK-SEC-01 / 侧信道 | 变体自 SEC-004 | TC-246, TC-497 |
| INTENT-SEC-033 | 大 artifact / 大 cache 必须受配额与边界限制，防止资源耗尽型攻击 | P0 | RISK-SEC-02 / DoS | 独立 | — |
| INTENT-SEC-034 | OIDC / 短时凭据支持若缺失，必须明确标注为平台限制并提供替代安全方案 | P1 | RISK-SEC-01 / 云部署凭证 | 独立 | — |
| INTENT-SEC-035 | 验证 pull_request_target 使用 base 分支的 workflow 版本 | P0 | RISK-SEC-01 / Pwn Request | 独立 | TC-461~463 |
| INTENT-SEC-036 | ATOMGIT_TOKEN 默认权限范围与 job 级覆盖必须正确生效 | P0 | RISK-SEC-01 / 权限生效 | 变体自 SEC-016 | TC-351~416 |


### 维度：reliability

| 意图 ID | 标题 | 优先级 | 覆盖风险/能力项 | 去重关系 | 已有覆盖 |
|---|---|---|---|---|---|
| INTENT-REL-001 | concurrency.max 边界值——同时触发 5 个运行应全部进入执行态 | P1 | RISK-REL-01 / 并发边界 | 独立 | TC-289~293 |
| INTENT-REL-002 | concurrency.max 越界值——配置 max=6 时系统应拒绝或明确报错 | P1 | RISK-REL-01 / 并发越界 | 独立 | TC-522 |
| INTENT-REL-003 | concurrency 排队策略 QUEUE——超上限运行应排队等待而非丢失 | P1 | RISK-REL-01 / 并发排队 | 独立 | TC-518 |
| INTENT-REL-004 | concurrency 忽略策略 IGNORE——超上限运行应直接执行不排队 | P1 | RISK-REL-01 / 并发忽略 | 独立 | TC-519 |
| INTENT-REL-005 | preemption events 边界值——配置 10 个抢占事件应正常解析 | P1 | RISK-REL-01 / 抢占边界 | 独立 | TC-291~292 |
| INTENT-REL-006 | preemption events 越界值——配置 11 个抢占事件应被拒绝 | P1 | RISK-REL-01 / 抢占越界 | 独立 | — |
| INTENT-REL-007 | job timeout 边界值——运行 359 分钟后在 360 分钟边界前正常完成 | P1 | RISK-REL-01 / 超时边界 | 独立 | TC-270 |
| INTENT-REL-008 | job timeout 越界触发——运行 361 分钟时应在 360 分钟被强制终止 | P1 | RISK-REL-01 / 超时越界 | 独立 | TC-270 |
| INTENT-REL-009 | 自定义短超时——timeout-minutes=1 时 step 运行 2 分钟应被强制终止 | P1 | RISK-REL-01 / 短超时 | 独立 | TC-270 |
| INTENT-REL-010 | 默认超时（未声明 timeout-minutes）——运行 361 分钟应被强制终止 | P1 | RISK-REL-01 / 默认超时 | 独立 | TC-270 |
| INTENT-REL-011 | rerun 边界值——单条运行连续重新运行 3 次应全部成功 | P1 | RISK-REL-01 / 重试边界 | 独立 | TC-350 |
| INTENT-REL-012 | rerun 越界值——尝试第 4 次重新运行应被系统拒绝 | P1 | RISK-REL-01 / 重试越界 | 独立 | TC-350 |
| INTENT-REL-013 | rerun 6 小时年龄限制——超期运行不可重新运行 | P1 | RISK-REL-01 / 重试过期 | 独立 | TC-350 |
| INTENT-REL-014 | paths 匹配边界值——变更恰好 300 个文件时 paths 过滤应生效 | P1 | RISK-REL-01 / 触发匹配边界 | 独立 | TC-422, TC-514 |
| INTENT-REL-015 | paths 匹配越界值——第 301 个变更文件不参与 paths 匹配判断 | P1 | RISK-REL-01 / 触发匹配越界 | 独立 | TC-515 |
| INTENT-REL-016 | step output 边界值——ATOMGIT_OUTPUT 写入 1 MB 参数应成功传递 | P1 | RISK-REL-01 / 输出边界 | 独立 | TC-331, TC-434 |
| INTENT-REL-017 | step output 越界值——ATOMGIT_OUTPUT 写入 1 MB+1 byte 应被拒绝或报错 | P1 | RISK-REL-01 / 输出越界 | 独立 | TC-554~555 |
| INTENT-REL-018 | Runner 磁盘边界——small runner（50 GB）写入 49 GB 应成功 | P1 | RISK-REL-01 / 资源边界 | 独立 | TC-447~455 |
| INTENT-REL-019 | Runner 磁盘越界——small runner（50 GB）写入 51 GB 应失败并报磁盘满 | P1 | RISK-REL-01 / 资源越界 | 独立 | TC-447~455 |
| INTENT-REL-020 | Runner 内存边界——small runner（8 GB）分配 7.5 GB 应成功 | P1 | RISK-REL-01 / 资源边界 | 独立 | TC-447~455 |
| INTENT-REL-021 | Runner 内存越界/OOM——small runner（8 GB）分配 9 GB 应被 OOM kill | P1 | RISK-REL-01 / 资源越界 | 独立 | TC-447~455 |
| INTENT-REL-022 | Runner CPU 饱和——small runner（2 核）运行 4 个 CPU 密集型进程应完成但耗时延长 | P1 | RISK-REL-01 / CPU 饱和 | 独立 | TC-447~455 |
| INTENT-REL-023 | workflow_call 嵌套边界——2 层嵌套调用应成功执行 | P1 | RISK-REL-01 / 可重用工作流边界 | 独立 | TC-426 |
| INTENT-REL-024 | workflow_call 嵌套越界——3 层嵌套调用应被拒绝 | P1 | RISK-REL-01 / 可重用工作流越界 | 独立 | TC-564 |
| INTENT-REL-025 | needs 失败传播——上游 job 失败时下游 job 应被 skip | P1 | RISK-REL-01 / 依赖传播 | 独立 | TC-313~316 |
| INTENT-REL-026 | matrix fail-fast=true——任意 job 实例失败应立即取消其余实例 | P1 | RISK-REL-01 / 矩阵快速失败 | 独立 | TC-277, TC-329 |
| INTENT-REL-027 | matrix max-parallel=4——9 个组合应最多同时运行 4 个 | P1 | RISK-REL-01 / 矩阵并行限制 | 独立 | TC-278, TC-330 |
| INTENT-REL-028 | 手动取消 workflow——运行中取消时 always() cleanup step 仍应执行 | P1 | RISK-REL-01 / 取消语义 | 独立 | TC-350 |
| INTENT-REL-029 | stages fail_fast 机制——阶段内任一 job 失败应立即终止同阶段其他 jobs | P1 | RISK-REL-01 / stages 快速失败 | 独立 | TC-403~404 |
| INTENT-REL-030 | continue-on-error=true——job 失败后 workflow 不应终止 | P1 | RISK-REL-01 / 容错机制 | 独立 | TC-272 |
| INTENT-REL-031 | 故障注入——job 执行中 runner 进程被 SIGKILL 后应记录失败并保留已执行日志 | P1 | RISK-REL-01 / 故障恢复 | 独立 | — |
| INTENT-REL-032 | 故障注入——artifact 上传时网络分区 30 秒后应失败并报网络错误 | P1 | RISK-REL-01 / 网络故障 | 独立 | — |
| INTENT-REL-033 | 故障注入——runner 磁盘接近满时写入操作应失败并报磁盘满 | P1 | RISK-REL-01 / 磁盘故障 | 独立 | — |
| INTENT-REL-034 | 故障注入——cache 服务 503 不可用时 job 应优雅降级为 cache miss | P1 | RISK-REL-01 / 依赖服务故障 | 独立 | TC-301~303 |
| INTENT-REL-035 | 故障注入——artifact 下载服务 503 不可用时 job 应失败并报依赖服务错误 | P1 | RISK-REL-01 / 依赖服务故障 | 独立 | TC-294~300 |
| INTENT-REL-036 | 并发洪泛——同一仓库 10 个 push 同时触发 10 个 workflow 运行应无丢失 | P1 | RISK-REL-01 / 并发洪泛 | 独立 | — |
| INTENT-REL-037 | 并发洪泛——同一仓库 50 个 push 同时触发应正确排队/限流不崩溃 | P1 | RISK-REL-01 / 并发洪泛 | 独立 | — |
| INTENT-REL-038 | 大规模 matrix——20 个组合（4 维×5 值）应全部生成并正确调度 | P1 | RISK-REL-01 / 矩阵规模 | 独立 | TC-325~328 |
| INTENT-REL-039 | 大规模 matrix——50 个组合（5 维×10 值）应全部生成并正确调度 | P1 | RISK-REL-01 / 矩阵规模 | 独立 | TC-325~328 |
| INTENT-REL-040 | 超长日志——单 job 输出 100 MB 日志应完整保留且可下载查看 | P1 | RISK-REL-01 / 日志规模 | 独立 | TC-348 |
| INTENT-REL-041 | 超大 artifact——100 MB artifact 上传后下游 job 应成功下载 | P1 | RISK-REL-01 / 制品规模 | 独立 | TC-378~380 |
| INTENT-REL-042 | 超多 step——单 job 内 50 个 step 应全部串行执行无丢失 | P1 | RISK-REL-01 / step 规模 | 独立 | TC-279~288 |
| INTENT-REL-043 | 长时运行接近 timeout 边界——350 分钟运行应成功且心跳保活正常 | P1 | RISK-REL-01 / 长时运行 | 独立 | TC-270 |
| INTENT-REL-044 | 并发资源公平性——2 个 workflow 各 3 个 jobs 应被公平调度 | P1 | RISK-REL-01 / 调度公平性 | 独立 | — |
| INTENT-REL-045 | 自托管 K8s Runner 弹性伸缩——min=1/max=1 时并发 3 个 jobs 应排队执行 | P1 | RISK-REL-01 / K8s 弹性 | 独立 | TC-450 |
| INTENT-REL-046 | 缓存 LRU 淘汰压力——连续写入 10 个大缓存后最旧缓存应被正确淘汰 | P1 | RISK-REL-01 / 缓存策略 | 独立 | TC-301~303 |
| INTENT-REL-047 | artifact 保留期 90 天边界——第 91 天应不可下载 | P1 | RISK-REL-01 / 保留期边界 | 独立 | TC-296, TC-380 |
| INTENT-REL-048 | 取消与 needs 条件竞态——job A 被取消时 job B（if: failure()）应正确判定 | P1 | RISK-REL-01 / 取消竞态 | 独立 | TC-350 |
| INTENT-REL-049 | Runner 规格真实性——small/medium/large 实际 CPU/内存/磁盘 vs 声明值 | P1 | RISK-REL-01 / 资源真实性 | 独立 | TC-447~455 |
| INTENT-REL-050 | 调度延迟基准——queued→running P50/P95 等待时间 | P1 | RISK-REL-01 / 调度性能 | 独立 | — |
| INTENT-REL-051 | 日志加载性能——50MB/200MB 日志下载与查看耗时 | P1 | RISK-REL-01 / 日志性能 | 独立 | TC-348 |
| INTENT-REL-052 | 镜像拉取性能——自定义 container 环境准备耗时基准 | P1 | RISK-REL-01 / 镜像性能 | 独立 | TC-262~263, TC-458~460 |
| INTENT-REL-053 | 制品传输性能——100MB/500MB/1GB artifact 上传下载耗时 | P1 | RISK-REL-01 / 制品性能 | 独立 | TC-294~300 |
| INTENT-REL-054 | 缓存加速比——cache 命中 vs 未命中构建耗时对比 | P2 | RISK-REL-01 / 缓存性能 | 独立 | TC-301~303 |
| INTENT-REL-055 | 并发压测——concurrency.max=5 时触发 20 个 workflow 的排队与完成率 | P1 | RISK-REL-01 / 并发压测 | 独立 | TC-289~293 |
| INTENT-REL-056 | 矩阵调度公平性——20 实例 matrix 配 max-parallel=4 的无饿死验证 | P1 | RISK-REL-01 / 矩阵公平性 | 独立 | TC-325~328 |
| INTENT-REL-057 | 资源调度状态一致性——空闲 runner 存在时 job 不应死等 | P1 | RISK-REL-01 / 调度一致性 | 独立 | — |
| INTENT-REL-058 | Runner 状态机正确性——空闲/运行/离线转换与时序一致性 | P1 | RISK-REL-01 / 状态机 | 独立 | — |
| INTENT-REL-059 | 日志系统稳定性——6 万行日志无乱序/无丢失/无截断 | P1 | RISK-REL-01 / 日志稳定性 | 独立 | TC-348 |
| INTENT-REL-060 | Workflow YAML 缓存失效——修改后无旧代码残留 | P1 | RISK-REL-01 / YAML 缓存 | 独立 | — |
| INTENT-REL-061 | 取消操作可靠性——queued/running/post 各阶段取消状态正确过渡 | P1 | RISK-REL-01 / 取消可靠性 | 独立 | TC-350 |
| INTENT-REL-062 | 网络依赖容错——workflow 中访问不可达地址的明确失败与有界超时 | P2 | RISK-REL-01 / 网络容错 | 独立 | — |
| INTENT-REL-063 | 制品并发写一致性——多 job 同时 upload-artifact 同名 artifact | P1 | RISK-REL-01 / 制品并发 | 独立 | TC-294~300 |
| INTENT-REL-064 | 子任务状态传播——workflow_call 失败/未拉起时不应假阳性完成 | P1 | RISK-REL-01 / 状态传播 | 独立 | TC-426, TC-564 |
| INTENT-REL-065 | API 限流与一致性——10 QPS 高频查询 run/job 状态不丢数据 | P2 | RISK-REL-01 / API 限流 | 独立 | — |
| INTENT-REL-066 | 大规格资源调度稳定性——xlarge/2xlarge 反复编译成功率 | P1 | RISK-REL-01 / 大规格调度 | 独立 | TC-447~455 |

### 维度：usability

| 意图 ID | 标题 | 优先级 | 覆盖风险/能力项 | 去重关系 | 已有覆盖 |
|---|---|---|---|---|---|
| INTENT-USE-001 | 工作流目录差异报错质量 — .github/workflows 搬运到 GitCode 时的路径指引 | P1 | RISK-USE-01 / 目录报错 | 已关联 COMP-001 | TC-366, TC-383 |
| INTENT-USE-002 | 上下文命名差异报错质量 — github.* 表达式失效时是否指明 atomgit.* 替代 | P1 | RISK-USE-01 / 上下文报错 | 已关联 COMPAT-016 | TC-017~018 |
| INTENT-USE-003 | 环境变量前缀差异 — Shell 脚本引用 GITHUB_* 空值/报错时的提示质量 | P1 | RISK-USE-01 / 环境变量报错 | 已关联 COMPAT-017 | TC-197~218 |
| INTENT-USE-004 | 状态函数括号差异 — success() 语法报错是否提示「GitCode 不带括号」 | P1 | RISK-USE-01 / 状态函数报错 | 已关联 COMPAT-004 | TC-176~179 |
| INTENT-USE-005 | permissions 权限域命名差异 — GitHub 命名被使用时报错是否给出 GitCode 对照 | P1 | RISK-USE-01 / 权限报错 | 已关联 COMPAT-030 | TC-351~416 |
| INTENT-USE-006 | runs-on 标签不匹配时报错质量 — 是否给出三段式标签格式指引 | P1 | RISK-USE-01 / Runner 标签报错 | 已关联 COMP-010 | TC-571~573 |
| INTENT-USE-007 | Action 引用写法差异 — actions/checkout@v4 被使用时报错是否给出迁移指引 | P1 | RISK-USE-01 / Action 引用报错 | 已关联 COMPAT-024 | TC-304 |
| INTENT-USE-008 | workflow_dispatch inputs 类型限制报错 — 非 string 类型声明是否提示转换指引 | P1 | RISK-USE-01 / 输入类型报错 | 已关联 COMPAT-014 | TC-014, TC-193 |
| INTENT-USE-009 | pull_request types 命名差异 — 使用 GitHub 命名时是否静默失败或有可理解提示 | P1 | RISK-USE-01 / 触发器报错 | 已关联 COMPAT-011 | TC-234, TC-560 |
| INTENT-USE-010 | 废弃 workflow 命令报错质量 — ::set-output/::set-env/::add-path 是否给出替代命令 | P1 | RISK-USE-01 / 废弃命令报错 | 独立 | TC-239~241, TC-552~553 |
| INTENT-USE-011 | stages / post 特有概念的文档可发现性 — 迁移者能否在显眼位置找到说明 | P1 | RISK-COMPAT-01 / 文档可发现性 | 已关联 COMP-007 | TC-402~404 |
| INTENT-USE-012 | 文档残留措辞一致性 — runtime-environment-variables.md 中是否夹带 GitHub 专属变量名 | P1 | RISK-COMPAT-01 / 文档一致性 | 独立 | TC-206, TC-220 |
| INTENT-USE-013 | runner.os 支持平台文档声明与实际一致性 | P1 | RISK-COMPAT-01 / 平台文档 | 已关联 COMPAT-018 | TC-023, TC-094 |
| INTENT-USE-014 | vars 上下文文档与样本注释矛盾澄清 | P1 | RISK-COMPAT-01 / 文档矛盾 | 已关联 COMPAT-022 | TC-019, TC-115~119 |
| INTENT-USE-015 | paths 300 文件上限差异是否在文档与行为中一致且明示 | P1 | RISK-COMPAT-01 / 文档行为一致 | 已关联 COMPAT-012 | TC-422, TC-514~515 |
| INTENT-USE-016 | secret 日志脱敏绕过风险 — 文档自承行为与实际是否一致 | P0 | RISK-SEC-01 / 文档安全一致 | 已关联 SEC-004~008 | TC-011 |
| INTENT-USE-017 | 日志按 step 时间线组织的清晰度与可读性 | P1 | RISK-COMPAT-01 / 日志可读性 | 独立 | TC-348 |
| INTENT-USE-018 | 日志搜索/下载/关键词高亮的交互可用性 | P1 | RISK-COMPAT-01 / 日志交互 | 独立 | TC-348 |
| INTENT-USE-019 | 运行状态回写可读性 — Commits 页面与 PR Checks 标签页的状态徽标 | P1 | RISK-COMPAT-01 / 状态回写 | 独立 | TC-347 |
| INTENT-USE-020 | ATOMGIT_STEP_SUMMARY Markdown 渲染质量与可读性 | P1 | RISK-COMPAT-01 / 摘要渲染 | 已关联 COMP-018 | TC-246, TC-497 |
| INTENT-USE-021 | workflow 命令 ::error:: / ::warning:: 的注解生成与关联可读性 | P1 | RISK-COMPAT-01 / 注解可读性 | 独立 | TC-248~250 |
| INTENT-USE-022 | YAML 语法/必填字段缺失报错的行号与可操作性 | P1 | RISK-USE-01 / YAML 报错 | 独立 | TC-393~401 |
| INTENT-USE-023 | 未知/不支持字段处理的报错信息质量 | P1 | RISK-USE-01 / 未知字段报错 | 已关联 COMP-002 | TC-274, TC-336 |
| INTENT-USE-024 | 表达式语法错误（非法上下文/函数）的报错信息质量 | P1 | RISK-USE-01 / 表达式报错 | 独立 | TC-160~187 |
| INTENT-USE-025 | Runner 标签无匹配时的报错信息质量 | P1 | RISK-USE-01 / Runner 标签报错 | 已关联 COMP-010 | TC-571~573 |
| INTENT-USE-026 | workflow_call 嵌套超过 2 层时的报错清晰度 | P1 | RISK-COMPAT-01 / 嵌套报错 | 已关联 REL-024 | TC-564 |
| INTENT-USE-027 | 并发控制 max 超出 1-5 范围时的报错信息 | P1 | RISK-COMPAT-01 / 并发报错 | 已关联 REL-002 | TC-522 |
| INTENT-USE-028 | Secret 名称规则违规的报错质量 | P1 | RISK-SEC-01 / Secret 命名报错 | 独立 | TC-531 |
| INTENT-USE-030 (spec) | 验证 workflow_dispatch inputs 默认值与必填参数校验 | P1 | RISK-USE-01 / 输入校验 | 独立 | TC-012~016, TC-581~583 |

---

## 打回/待补意图清单

| 意图 ID | 标题 | 打回原因 | 可操作改进建议 |
|---|---|---|---|
| INTENT-COMP-021 (spec) | 验证表达式函数 contains/hashFiles/toJson 边界行为与 GitHub 一致性 | 粗粒度、无独立验证价值；compat-diff agent 已拆分为 COMPAT-006~010 共 5 条细化 intent | 删除；由 COMPAT-006~010 覆盖各函数边界 |
| INTENT-COMP-026 (spec) | 验证大规模 matrix 展开行为与平台上限 | 粗粒度、无独立验证价值；reliability agent 已拆分为 REL-027/038/039/056 共 4 条细化 intent | 删除；由 REL-027/038/039/056 覆盖矩阵规模与公平性 |
| spec-COMPAT-019 | 验证上下文对象命名 github.* → atomgit.* 的兼容性影响 | **ID 冲突**（与 compat.md COMPAT-019 重复），且内容被 COMPAT-016 完全覆盖 | 删除；复用 compat.md 的 COMPAT-016 |
| spec-COMPAT-020 | 验证状态函数括号语法差异 success() → success | **ID 冲突**（与 compat.md COMPAT-020 重复），且内容被 COMPAT-004/005 完全覆盖 | 删除；复用 compat.md 的 COMPAT-004/005 |
| spec-COMPAT-021 | 验证表达式函数边界行为与 GitHub 一致性 | **ID 冲突**（与 compat.md COMPAT-021 重复），且内容被 COMPAT-006~010 覆盖 | 删除；复用 compat.md 的 COMPAT-006~010 |
| spec-COMPAT-022 | 验证 permissions 权限域命名差异 | **ID 冲突**（与 compat.md COMPAT-022 重复），且内容被 COMPAT-030 完全覆盖 | 删除；复用 compat.md 的 COMPAT-030 |
| spec-COMPAT-023 | 验证 workflow_dispatch.inputs 仅支持 string 类型 | **ID 冲突**（与 compat.md COMPAT-023 重复），且内容被 COMPAT-014 完全覆盖 | 删除；复用 compat.md 的 COMPAT-014 |
| spec-USE-028 | 验证迁移报错质量（GitHub→GitCode 语法不兼容时的错误提示） | 粗粒度、无独立验证价值；usability agent 已拆分为 USE-001~010 共 10 条具体差异项报错 intent，且 COMPAT-031 覆盖整体迁移报错质量；**ID 冲突**（与 usability.md USE-028 重复） | 删除；由 USE-001~010 及 COMPAT-031 覆盖 |
| spec-USE-029 | 验证文档一致性（runtime-environment-variables.md 中的 GitHub 残留措辞） | 与 usability.md 的 USE-012「文档残留措辞一致性」完全重叠 | 删除；复用 USE-012 |

---

## 跨维度意图索引

| 意图 ID | 维度标签 | 关联意图 |
|---|---|---|
| INTENT-COMP-004 | [completeness, security] | SEC-001, SEC-002, SEC-003, SEC-035, COMPAT-032 |
| INTENT-COMP-011 | [completeness, reliability, security] | SEC-020, SEC-021, SEC-022, COMPAT-028 |
| INTENT-COMP-012 | [completeness, security] | SEC-004~008, COMPAT-033, USE-016 |
| INTENT-COMP-013 | [completeness, security] | SEC-016, SEC-017, SEC-036, COMPAT-002 |
| INTENT-COMP-014 | [completeness, security] | SEC-002, SEC-035, COMPAT-032 |
| INTENT-COMP-015 | [completeness, reliability] | REL-041, COMPAT-026 |
| INTENT-COMP-016 | [completeness, security, reliability] | SEC-018, COMPAT-025 |
| INTENT-COMP-017 | [completeness, usability] | USE-017, USE-018, REL-059 |
| INTENT-COMP-018 | [completeness, compatibility] | USE-020 |
| INTENT-COMP-022 | [completeness, compatibility] | COMPAT-030, USE-005 |
| INTENT-COMP-023 | [completeness, compatibility] | COMPAT-014, USE-008 |
| INTENT-COMPAT-002 | [compatibility, security] | SEC-017, COMP-013 |
| INTENT-COMPAT-010 | [compatibility, usability] | — |
| INTENT-COMPAT-011 | [compatibility, usability] | USE-009 |
| INTENT-COMPAT-012 | [compatibility, reliability] | REL-014/015, USE-015 |
| INTENT-COMPAT-014 | [compatibility, usability] | USE-008, COMP-023 |
| INTENT-COMPAT-016 | [compatibility, usability] | USE-002 |
| INTENT-COMPAT-017 | [compatibility, usability] | USE-003 |
| INTENT-COMPAT-020 | [compatibility, security] | SEC-004~008 |
| INTENT-COMPAT-024 | [compatibility, usability] | USE-007 |
| INTENT-COMPAT-025 | [compatibility, security] | SEC-018, COMP-016 |
| INTENT-COMPAT-028 | [compatibility, security] | SEC-020, COMP-011 |
| INTENT-COMPAT-029 | [compatibility, usability] | USE-001, COMP-001 |
| INTENT-COMPAT-030 | [compatibility, security, usability] | USE-005, COMP-022 |
| INTENT-COMPAT-032 | [compatibility, security] | SEC-035, COMP-004, COMP-014 |
| INTENT-COMPAT-033 | [compatibility, security] | SEC-004~008, COMP-012 |
| INTENT-COMPAT-034 | [compatibility] | REL-001~006, USE-027 |
| INTENT-COMPAT-035 | [compatibility] | REL-048 |
| INTENT-SEC-024 | [security, compatibility] | — |
| INTENT-SEC-034 | [security, compatibility] | — |
| INTENT-REL-048 | [reliability, compatibility] | COMPAT-035 |
| INTENT-REL-050 | [reliability, usability] | — |
| INTENT-REL-051 | [reliability, usability] | USE-017/018 |
| INTENT-REL-059 | [reliability, usability] | USE-017, COMP-017 |
| INTENT-REL-060 | [reliability, completeness] | — |
| INTENT-REL-063 | [reliability, completeness] | — |
| INTENT-REL-064 | [reliability, completeness] | — |
| INTENT-USE-002 | [usability, compatibility] | COMPAT-016 |
| INTENT-USE-003 | [usability, compatibility] | COMPAT-017 |
| INTENT-USE-005 | [usability, compatibility] | COMPAT-030 |
| INTENT-USE-006 | [usability, compatibility] | COMP-010, COMPAT-027 |
| INTENT-USE-007 | [usability, compatibility] | COMPAT-024 |
| INTENT-USE-008 | [usability, compatibility] | COMPAT-014 |
| INTENT-USE-009 | [usability, compatibility] | COMPAT-011 |
| INTENT-USE-010 | [usability, compatibility] | — |
| INTENT-USE-011 | [usability] | COMP-007 |
| INTENT-USE-013 | [usability, compatibility] | COMPAT-018 |
| INTENT-USE-014 | [usability, compatibility] | COMPAT-022 |
| INTENT-USE-015 | [usability, compatibility] | COMPAT-012 |
| INTENT-USE-016 | [usability, security] | SEC-004~008, COMP-012 |
| INTENT-USE-019 | [usability] | — |
| INTENT-USE-020 | [usability] | COMP-018 |
| INTENT-USE-021 | [usability] | — |
| INTENT-USE-023 | [usability, compatibility] | COMP-002, COMPAT-021 |
| INTENT-USE-025 | [usability] | COMP-010 |
| INTENT-USE-026 | [usability] | REL-024 |
| INTENT-USE-027 | [usability] | REL-002 |
| INTENT-USE-028 | [usability, security] | — |
| INTENT-USE-030 (spec) | [usability, completeness] | — |
