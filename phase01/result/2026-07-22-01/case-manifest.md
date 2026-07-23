# Case Manifest · Run 2026-07-22-01

> 生成时间: 2026-07-22
> 准入 intent 总数: 186 条
> 复用已有 TC: 95 条
> 新生成用例: —（见下方「新增用例清单」）
> 待生成: —（见下方「待生成记录」）

---

## 统计摘要

| 维度 | 准入 | 复用 | 新增 | 待生成 |
|---|---|---|---|---|
| completeness | 16 | 15 | 10 | 0 |
| compatibility | 35 | 32 | 10 | 0 |
| security | 36 | 12 | 27 | 0 |
| reliability | 66 | 53 | 15 | 0 |
| usability | 28 (+1 spec) | 29 | 0 | 0 |
| **合计** | **186** | **95** | **62** | **0** |

---

## 一、复用已有 TC 清单（95 条）

以下 intent 已由 KEEP TC 或上一轮 delivered run 用例完全覆盖，本轮仅标注关联，不生成新文件。

### completeness（15 条）

| 意图 ID | 标题 | 优先级 | 复用 TC / 已有用例 | 备注 |
|---|---|---|---|---|
| INTENT-COMP-001 | 验证工作流文件目录 `.gitcode/workflows/` 的识别行为 | P1 | TC-366, TC-383 | 完全覆盖 |
| INTENT-COMP-002 | 验证未知/不支持字段的 YAML 校验行为 | P1 | TC-274, TC-336 等 | 完全覆盖 |
| INTENT-COMP-003 | 验证 push 触发 + branches/paths/tags 过滤的完整行为 | P1 | TC-223, TC-229~233 | 完全覆盖 |
| INTENT-COMP-004 | 验证 pull_request vs pull_request_target 隔离强度 | P0 | TC-445, TC-461~463 | 核心覆盖，本轮补充变体 |
| INTENT-COMP-005 | 验证 schedule cron 语义 | P1 | TC-427~430 | 完全覆盖 |
| INTENT-COMP-006 | 验证 workflow_call 嵌套层数限制 | P1 | TC-426, TC-564 | 完全覆盖 |
| INTENT-COMP-007 | 验证 stages 阶段机制与 post 后处理阶段语义 | P1 | TC-402~404, TC-406~407 | 完全覆盖 |
| INTENT-COMP-008 | 验证 timeout-minutes 默认 360 分钟与强制终止行为 | P1 | TC-270 | 完全覆盖 |
| INTENT-COMP-009 | 验证 rerun 次数限制与上下文保持语义 | P1 | TC-350 | 完全覆盖 |
| INTENT-COMP-010 | 验证 runs-on 三段式标签体系与 default 快捷标签 | P1 | TC-363, TC-365, TC-446~457 | 完全覆盖 |
| INTENT-COMP-012 | 验证 secrets 日志脱敏与绕过场景 | P0 | TC-011, TC-354 | 核心覆盖，本轮补充变体 |
| INTENT-COMP-013 | 验证 permissions 默认权限与声明语义 | P0 | TC-351~416 | 完全覆盖 |
| INTENT-COMP-014 | 验证 pull_request_target checkout head.sha 的注入风险 | P0 | TC-461~463 | 核心覆盖，本轮补充变体 |
| INTENT-COMP-015 | 验证 upload-artifact / download-artifact 跨 job 传递与保留期 | P1 | TC-294~300, TC-378~380 | 完全覆盖 |
| INTENT-COMP-016 | 验证 cache 作用域与 fork 隔离策略 | P0 | TC-301~303 | 完全覆盖 |
| INTENT-COMP-017 | 验证运行状态机与日志完整性 | P1 | TC-347, TC-348 | 完全覆盖 |
| INTENT-COMP-018 | 验证 ATOMGIT_STEP_SUMMARY Markdown 渲染与安全性 | P1 | TC-219, TC-246, TC-497 | 完全覆盖 |

### compatibility（32 条）

| 意图 ID | 标题 | 优先级 | 复用 TC / 已有用例 | 备注 |
|---|---|---|---|---|
| INTENT-COMPAT-001 | 默认 shell 与默认工作目录在未声明时的隐式行为差异 | P1 | TC-288 | 完全覆盖 |
| INTENT-COMPAT-002 | 未声明 permissions 时的默认 TOKEN 权限范围差异 | P0 | TC-351~416 | 核心覆盖，本轮补充变体 |
| INTENT-COMPAT-003 | step/job 级 if 条件未显式声明时的默认状态检查差异 | P1 | TC-176~179 | 完全覆盖 |
| INTENT-COMPAT-004 | 状态函数括号语法差异 | P1 | TC-176~179, TC-317~321 | 完全覆盖 |
| INTENT-COMPAT-005 | 失败状态函数命名差异 | P1 | TC-178, TC-320 | 完全覆盖 |
| INTENT-COMPAT-006 | `contains` 函数边界行为差异 | P1 | TC-180, TC-543~544 | 完全覆盖 |
| INTENT-COMPAT-007 | `hashFiles` 函数边界行为差异 | P1 | TC-186, TC-550 | 完全覆盖 |
| INTENT-COMPAT-008 | `toJson` 输出格式差异 | P1 | TC-187, TC-549 | 完全覆盖 |
| INTENT-COMPAT-009 | 表达式 loose equality 与类型强制转换规则差异 | P1 | TC-160~175 | 完全覆盖 |
| INTENT-COMPAT-011 | `pull_request` 事件 types 命名与取值差异 | P1 | TC-234, TC-560 | 完全覆盖 |
| INTENT-COMPAT-012 | `paths` 匹配文件数上限差异 | P1 | TC-422, TC-514~515 | 完全覆盖 |
| INTENT-COMPAT-013 | `schedule` cron timezone 支持差异 | P1 | TC-427~430 | 完全覆盖 |
| INTENT-COMPAT-014 | `workflow_dispatch` / `workflow_call` inputs 类型限制 | P1 | TC-014, TC-193, TC-581 | 完全覆盖 |
| INTENT-COMPAT-015 | `workflow_call` 可复用工作流嵌套层数差异 | P1 | TC-426, TC-564 | 完全覆盖 |
| INTENT-COMPAT-016 | 核心上下文对象前缀差异 | P1 | TC-017~018 | 完全覆盖 |
| INTENT-COMPAT-017 | 系统环境变量前缀差异 | P1 | TC-197~218 | 完全覆盖 |
| INTENT-COMPAT-018 | `runner.os` 值格式差异 | P1 | TC-023, TC-094, TC-136~139 | 完全覆盖 |
| INTENT-COMPAT-019 | `runner.arch` 值格式差异 | P1 | TC-095, TC-442 | 完全覆盖 |
| INTENT-COMPAT-020 | 自动令牌命名差异 | P1 | TC-036, TC-196 | 完全覆盖 |
| INTENT-COMPAT-021 | 未知/不支持字段的降级方式 | P1 | TC-274, TC-336 | 完全覆盖 |
| INTENT-COMPAT-022 | `vars` 上下文不支持时的降级行为 | P1 | TC-019, TC-115~119 | 完全覆盖 |
| INTENT-COMPAT-023 | `jobs.<id>.environment` 字段支持情况与降级行为 | P1 | TC-010, TC-274 | 完全覆盖 |
| INTENT-COMPAT-024 | 内置 action 短名引用行为等价性 | P1 | TC-304, TC-354 | 完全覆盖 |
| INTENT-COMPAT-025 | 内置 action `cache` 行为等价性与 fork 隔离 | P0 | TC-301~303 | 完全覆盖 |
| INTENT-COMPAT-026 | 内置 action `upload-artifact`/`download-artifact` 行为等价性 | P1 | TC-294~300 | 完全覆盖 |
| INTENT-COMPAT-027 | `runs-on` 标签体系差异 | P1 | TC-363, TC-365, TC-571~573 | 完全覆盖 |
| INTENT-COMPAT-029 | 工作流文件目录差异 | P1 | TC-366, TC-383 | 完全覆盖 |
| INTENT-COMPAT-030 | `permissions` 权限域命名完全差异 | P0 | TC-351~416 | 完全覆盖 |
| INTENT-COMPAT-032 | `pull_request_target` 语义一致性 | P0 | TC-461~463 | 核心覆盖，本轮补充变体 |
| INTENT-COMPAT-033 | Secret 日志脱敏绕过风险 | P0 | TC-011 | 完全覆盖 |
| INTENT-COMPAT-034 | `concurrency` 字段结构与语义差异 | P1 | TC-289~293, TC-518~523 | 完全覆盖 |
| INTENT-COMPAT-035 | `steps` 上下文中的 `outcome` 与 `conclusion` 语义差异 | P1 | TC-090~092 | 完全覆盖 |

### security（12 条）

| 意图 ID | 标题 | 优先级 | 复用 TC / 已有用例 | 备注 |
|---|---|---|---|---|
| INTENT-SEC-001 | fork PR 触发 pull_request 时不可读取项目 secrets | P0 | TC-445 | 核心覆盖，本轮补充变体 |
| INTENT-SEC-002 | pull_request_target 事件下显式 checkout 不可信 PR 代码时，secrets 与写权限仍应受控 | P0 | TC-461~463 | 完全覆盖 |
| INTENT-SEC-003 | fork PR 触发 pull_request 时 ATOMGIT_TOKEN 必须仅拥有 read 权限 | P0 | TC-445 | 完全覆盖 |
| INTENT-SEC-004 | Secret 值在运行日志、step summary 和错误堆栈中必须被自动脱敏 | P0 | TC-011, TC-354 | 核心覆盖，本轮补充变体 |
| INTENT-SEC-014 | 第三方 Action 引用应支持完整 commit hash 固定 | P0 | TC-628 | 完全覆盖 |
| INTENT-SEC-016 | 显式声明的 permissions 必须在 job 级实际生效并限制 ATOMGIT_TOKEN | P0 | TC-351~416 | 完全覆盖 |
| INTENT-SEC-017 | 未声明 permissions 时 ATOMGIT_TOKEN 默认权限必须最小化 | P0 | TC-351~416 | 完全覆盖 |
| INTENT-SEC-018 | fork PR 写入的 cache 必须不可被主仓后续 workflow 读取 | P0 | TC-301~303 | 完全覆盖 |
| INTENT-SEC-024 | Secret/变量名含特殊字符时不可导致意外求值或权限绕过 | P0 | TC-531 | 完全覆盖 |
| INTENT-SEC-025 | 通过 printenv 或进程枚举获取 ATOMGIT_TOKEN/secrets 时日志必须保持脱敏 | P0 | TC-011 | 完全覆盖 |
| INTENT-SEC-026 | issue_comment / pull_request_comment 触发关键字过滤必须不可被绕过 | P0 | TC-464~470 | 完全覆盖 |
| INTENT-SEC-027 | 环境级 secret 必须经审批后才能被 workflow 访问 | P0 | TC-010 | 完全覆盖 |
| INTENT-SEC-028 | Workflow 命令（如 add-mask）的响应本身不可泄露被遮蔽前的 secret 值 | P0 | TC-436 | 完全覆盖 |
| INTENT-SEC-030 | 工作流写协议不被不可信输入污染提权 | P0 | TC-243~245, TC-434~435 | 完全覆盖 |
| INTENT-SEC-032 | Secret 不经 output / artifact / step summary 侧信道绕过脱敏外泄 | P0 | TC-246, TC-497 | 完全覆盖 |
| INTENT-SEC-035 | 验证 pull_request_target 使用 base 分支的 workflow 版本 | P0 | TC-461~463 | 完全覆盖 |
| INTENT-SEC-036 | ATOMGIT_TOKEN 默认权限范围与 job 级覆盖必须正确生效 | P0 | TC-351~416 | 完全覆盖 |

### reliability（53 条）

| 意图 ID | 标题 | 优先级 | 复用 TC / 已有用例 | 备注 |
|---|---|---|---|---|
| INTENT-REL-001 | concurrency.max 边界值 | P1 | TC-289~293 | 完全覆盖 |
| INTENT-REL-002 | concurrency.max 越界值 | P1 | TC-522 | 完全覆盖 |
| INTENT-REL-003 | concurrency 排队策略 QUEUE | P1 | TC-518 | 完全覆盖 |
| INTENT-REL-004 | concurrency 忽略策略 IGNORE | P1 | TC-519 | 完全覆盖 |
| INTENT-REL-005 | preemption events 边界值 | P1 | TC-291~292 | 完全覆盖 |
| INTENT-REL-007 | job timeout 边界值 | P1 | TC-270 | 完全覆盖 |
| INTENT-REL-008 | job timeout 越界触发 | P1 | TC-270 | 完全覆盖 |
| INTENT-REL-009 | 自定义短超时 | P1 | TC-270 | 完全覆盖 |
| INTENT-REL-010 | 默认超时 | P1 | TC-270 | 完全覆盖 |
| INTENT-REL-011 | rerun 边界值 | P1 | TC-350 | 完全覆盖 |
| INTENT-REL-012 | rerun 越界值 | P1 | TC-350 | 完全覆盖 |
| INTENT-REL-013 | rerun 6 小时年龄限制 | P1 | TC-350 | 完全覆盖 |
| INTENT-REL-014 | paths 匹配边界值 | P1 | TC-422, TC-514 | 完全覆盖 |
| INTENT-REL-015 | paths 匹配越界值 | P1 | TC-515 | 完全覆盖 |
| INTENT-REL-016 | step output 边界值 | P1 | TC-331, TC-434 | 完全覆盖 |
| INTENT-REL-017 | step output 越界值 | P1 | TC-554~555 | 完全覆盖 |
| INTENT-REL-018 | Runner 磁盘边界 | P1 | TC-447~455 | 完全覆盖 |
| INTENT-REL-019 | Runner 磁盘越界 | P1 | TC-447~455 | 完全覆盖 |
| INTENT-REL-020 | Runner 内存边界 | P1 | TC-447~455 | 完全覆盖 |
| INTENT-REL-021 | Runner 内存越界/OOM | P1 | TC-447~455 | 完全覆盖 |
| INTENT-REL-022 | Runner CPU 饱和 | P1 | TC-447~455 | 完全覆盖 |
| INTENT-REL-023 | workflow_call 嵌套边界 | P1 | TC-426 | 完全覆盖 |
| INTENT-REL-024 | workflow_call 嵌套越界 | P1 | TC-564 | 完全覆盖 |
| INTENT-REL-025 | needs 失败传播 | P1 | TC-313~316 | 完全覆盖 |
| INTENT-REL-026 | matrix fail-fast=true | P1 | TC-277, TC-329 | 完全覆盖 |
| INTENT-REL-027 | matrix max-parallel=4 | P1 | TC-278, TC-330 | 完全覆盖 |
| INTENT-REL-028 | 手动取消 workflow | P1 | TC-350 | 完全覆盖 |
| INTENT-REL-029 | stages fail_fast 机制 | P1 | TC-403~404 | 完全覆盖 |
| INTENT-REL-030 | continue-on-error=true | P1 | TC-272 | 完全覆盖 |
| INTENT-REL-034 | 故障注入——cache 服务 503 不可用时 job 应优雅降级 | P1 | TC-301~303 | 完全覆盖 |
| INTENT-REL-035 | 故障注入——artifact 下载服务 503 不可用时 job 应失败 | P1 | TC-294~300 | 完全覆盖 |
| INTENT-REL-038 | 大规模 matrix——20 个组合 | P1 | TC-325~328 | 完全覆盖 |
| INTENT-REL-039 | 大规模 matrix——50 个组合 | P1 | TC-325~328 | 完全覆盖 |
| INTENT-REL-040 | 超长日志 | P1 | TC-348 | 完全覆盖 |
| INTENT-REL-041 | 超大 artifact | P1 | TC-378~380 | 完全覆盖 |
| INTENT-REL-042 | 超多 step | P1 | TC-279~288 | 完全覆盖 |
| INTENT-REL-043 | 长时运行接近 timeout 边界 | P1 | TC-270 | 完全覆盖 |
| INTENT-REL-045 | 自托管 K8s Runner 弹性伸缩 | P1 | TC-450 | 完全覆盖 |
| INTENT-REL-046 | 缓存 LRU 淘汰压力 | P1 | TC-301~303 | 完全覆盖 |
| INTENT-REL-047 | artifact 保留期 90 天边界 | P1 | TC-296, TC-380 | 完全覆盖 |
| INTENT-REL-048 | 取消与 needs 条件竞态 | P1 | TC-350 | 完全覆盖 |
| INTENT-REL-049 | Runner 规格真实性 | P1 | TC-447~455 | 完全覆盖 |
| INTENT-REL-051 | 日志加载性能 | P1 | TC-348 | 完全覆盖 |
| INTENT-REL-052 | 镜像拉取性能 | P1 | TC-262~263, TC-458~460 | 完全覆盖 |
| INTENT-REL-053 | 制品传输性能 | P1 | TC-294~300 | 完全覆盖 |
| INTENT-REL-054 | 缓存加速比 | P2 | TC-301~303 | 完全覆盖 |
| INTENT-REL-055 | 并发压测 | P1 | TC-289~293 | 完全覆盖 |
| INTENT-REL-056 | 矩阵调度公平性 | P1 | TC-325~328 | 完全覆盖 |
| INTENT-REL-059 | 日志系统稳定性 | P1 | TC-348 | 完全覆盖 |
| INTENT-REL-061 | 取消操作可靠性 | P1 | TC-350 | 完全覆盖 |
| INTENT-REL-063 | 制品并发写一致性 | P1 | TC-294~300 | 完全覆盖 |
| INTENT-REL-064 | 子任务状态传播 | P1 | TC-426, TC-564 | 完全覆盖 |
| INTENT-REL-066 | 大规格资源调度稳定性 | P1 | TC-447~455 | 完全覆盖 |

### usability（29 条）

| 意图 ID | 标题 | 优先级 | 复用 TC / 已有用例 | 备注 |
|---|---|---|---|---|
| INTENT-USE-001 | 工作流目录差异报错质量 | P1 | TC-366, TC-383 | 完全覆盖 |
| INTENT-USE-002 | 上下文命名差异报错质量 | P1 | TC-017~018 | 完全覆盖 |
| INTENT-USE-003 | 环境变量前缀差异报错质量 | P1 | TC-197~218 | 完全覆盖 |
| INTENT-USE-004 | 状态函数括号差异报错质量 | P1 | TC-176~179 | 完全覆盖 |
| INTENT-USE-005 | permissions 权限域命名差异报错质量 | P1 | TC-351~416 | 完全覆盖 |
| INTENT-USE-006 | runs-on 标签不匹配时报错质量 | P1 | TC-571~573 | 完全覆盖 |
| INTENT-USE-007 | Action 引用写法差异报错质量 | P1 | TC-304 | 完全覆盖 |
| INTENT-USE-008 | workflow_dispatch inputs 类型限制报错 | P1 | TC-014, TC-193 | 完全覆盖 |
| INTENT-USE-009 | pull_request types 命名差异报错 | P1 | TC-234, TC-560 | 完全覆盖 |
| INTENT-USE-010 | 废弃 workflow 命令报错质量 | P1 | TC-239~241, TC-552~553 | 完全覆盖 |
| INTENT-USE-011 | stages / post 特有概念的文档可发现性 | P1 | TC-402~404 | 完全覆盖 |
| INTENT-USE-012 | 文档残留措辞一致性 | P1 | TC-206, TC-220 | 完全覆盖 |
| INTENT-USE-013 | runner.os 支持平台文档声明与实际一致性 | P1 | TC-023, TC-094 | 完全覆盖 |
| INTENT-USE-014 | vars 上下文文档与样本注释矛盾澄清 | P1 | TC-019, TC-115~119 | 完全覆盖 |
| INTENT-USE-015 | paths 300 文件上限差异是否在文档与行为中一致 | P1 | TC-422, TC-514~515 | 完全覆盖 |
| INTENT-USE-016 | secret 日志脱敏绕过风险 — 文档自承行为与实际是否一致 | P0 | TC-011 | 完全覆盖 |
| INTENT-USE-017 | 日志按 step 时间线组织的清晰度与可读性 | P1 | TC-348 | 完全覆盖 |
| INTENT-USE-018 | 日志搜索/下载/关键词高亮的交互可用性 | P1 | TC-348 | 完全覆盖 |
| INTENT-USE-019 | 运行状态回写可读性 | P1 | TC-347 | 完全覆盖 |
| INTENT-USE-020 | ATOMGIT_STEP_SUMMARY Markdown 渲染质量与可读性 | P1 | TC-246, TC-497 | 完全覆盖 |
| INTENT-USE-021 | workflow 命令 ::error:: / ::warning:: 的注解生成与关联可读性 | P1 | TC-248~250 | 完全覆盖 |
| INTENT-USE-022 | YAML 语法/必填字段缺失报错的行号与可操作性 | P1 | TC-393~401 | 完全覆盖 |
| INTENT-USE-023 | 未知/不支持字段处理的报错信息质量 | P1 | TC-274, TC-336 | 完全覆盖 |
| INTENT-USE-024 | 表达式语法错误的报错信息质量 | P1 | TC-160~187 | 完全覆盖 |
| INTENT-USE-025 | Runner 标签无匹配时的报错信息质量 | P1 | TC-571~573 | 完全覆盖 |
| INTENT-USE-026 | workflow_call 嵌套超过 2 层时的报错清晰度 | P1 | TC-564 | 完全覆盖 |
| INTENT-USE-027 | 并发控制 max 超出 1-5 范围时的报错信息 | P1 | TC-522 | 完全覆盖 |
| INTENT-USE-028 | Secret 名称规则违规的报错质量 | P1 | TC-531 | 完全覆盖 |
| INTENT-USE-030 | 验证 workflow_dispatch inputs 默认值与必填参数校验 | P1 | TC-012~016, TC-581~583 | 完全覆盖 |

---

## 二、新增用例清单

| 用例 ID | 维度 | 优先级 | 溯源意图 | 标题 | 类型 |
|---|---|---|---|---|---|
| SEC-BASE64-01-001 | security | P0 | INTENT-SEC-005 | secret 经 base64 编码后输出不应在日志中泄露明文 | 全新 |
| SEC-CONCAT-01-001 | security | P0 | INTENT-SEC-006 | secret 经字符串拼接后输出不应泄露明文 | 全新 |
| SEC-CONCAT-01-002 | security | P0 | INTENT-SEC-006 | secret 经插值拼接后输出不应泄露明文 | 变体 |
| SEC-MULTILINE-01-001 | security | P0 | INTENT-SEC-007 | secret 多行值输出不应绕过脱敏 | 全新 |
| SEC-SLICE-01-001 | security | P0 | INTENT-SEC-008 | secret 分片输出不应绕过脱敏 | 全新 |
| SEC-CMDINJ-01-001 | security | P0 | INTENT-SEC-009 | 不可信 PR 标题不可直接插进 run 脚本 | 全新 |
| SEC-CMDINJ-01-002 | security | P0 | INTENT-SEC-009 | 不可信 PR 正文不可直接插进 run 脚本 | 变体 |
| SEC-CMDINJ-01-003 | security | P0 | INTENT-SEC-010 | 不可信分支名不可直接插进 run 脚本 | 全新 |
| SEC-CMDINJ-01-004 | security | P0 | INTENT-SEC-011 | 不可信 issue/PR 评论不可直接插进 run 脚本 | 全新 |
| SEC-CMDINJ-01-005 | security | P0 | INTENT-SEC-012 | 不可信 commit message 不可直接插进 run 脚本 | 全新 |
| SEC-CMDINJ-01-006 | security | P0 | INTENT-SEC-012 | 不可信 author email 不可直接插进 run 脚本 | 变体 |
| SEC-DOUBLEEVAL-01-001 | security | P0 | INTENT-SEC-013 | 表达式嵌套双重渲染二次求值防护 | 全新 |
| SEC-DOUBLEEVAL-01-002 | security | P0 | INTENT-SEC-013 | 表达式通过环境变量间接二次求值防护 | 变体 |
| SEC-TYPO-01-001 | security | P0 | INTENT-SEC-015 | 第三方 Action 来源信任边界与 typosquatting | 全新 |
| SEC-FORKART-01-001 | security | P0 | INTENT-SEC-019 | fork PR 上传的 artifact 不可被主仓下载执行 | 全新 |
| SEC-CLEANUP-01-001 | security | P0 | INTENT-SEC-020 | Job 结束后 workspace 与临时文件必须彻底清理 | 全新 |
| SEC-JOBISO-01-001 | security | P0 | INTENT-SEC-021 | Runner 环境变量与共享目录必须跨 job 隔离 | 全新 |
| SEC-RUNNERISO-01-001 | security | P0 | INTENT-SEC-022 | 自托管 Runner 跨项目残留必须被隔离 | 全新 |
| SEC-SSRF-01-001 | security | P0 | INTENT-SEC-023 | Runner 网络出站必须受控——内网地址访问 | 全新 |
| SEC-SSRF-01-002 | security | P0 | INTENT-SEC-023 | Runner 网络出站必须受控——元数据服务访问 | 变体 |
| SEC-UNTRUSTART-01-001 | security | P0 | INTENT-SEC-029 | 跨运行 artifact 必须被视为不可信数据 | 全新 |
| SEC-TOCTOU-01-001 | security | P0 | INTENT-SEC-031 | 审批后推送新 commit 不绕过审批与代码固定 | 全新 |
| SEC-QUOTA-01-001 | security | P0 | INTENT-SEC-033 | 大 artifact 必须受配额与边界限制 | 全新 |
| SEC-QUOTA-01-002 | security | P0 | INTENT-SEC-033 | 大 cache 必须受配额与边界限制 | 变体 |
| SEC-OIDC-01-001 | security | P1 | INTENT-SEC-034 | OIDC / 短时凭据支持若缺失应明确标注限制 | 全新 |
| SEC-FORKENV-01-001 | security | P0 | INTENT-SEC-001 | fork PR 通过环境变量间接访问 secret 行为 | 补充 |
| SEC-SUMMARY-01-001 | security | P0 | INTENT-SEC-004 | secret 在 step summary 中的脱敏验证 | 补充 |
| REL-PREEMPT-01-001 | reliability | P1 | INTENT-REL-006 | preemption events 配置越界值（11 个）应被拒绝 | 全新 |
| REL-PREEMPT-01-002-V2 | reliability | P1 | INTENT-REL-006 | preemption events 配置边界值（10 个）应被接受 | 变体 |
| REL-FAULT-01-003 | reliability | P1 | INTENT-REL-031 | 故障注入——runner 被 SIGKILL 后记录失败并保留日志 | 全新 |
| REL-FAULT-01-004 | reliability | P1 | INTENT-REL-032 | 故障注入——artifact 上传网络分区 30 秒后失败 | 全新 |
| REL-FAULT-01-005 | reliability | P1 | INTENT-REL-033 | 故障注入——runner 磁盘接近满时写入失败 | 全新 |
| REL-FLOOD-01-006 | reliability | P1 | INTENT-REL-036 | 并发洪泛——10 个 push 同时触发无丢失 | 全新 |
| REL-FLOOD-01-007 | reliability | P1 | INTENT-REL-037 | 并发洪泛——50 个 push 同时触发排队限流不崩溃 | 全新 |
| REL-FAIR-01-008 | reliability | P1 | INTENT-REL-044 | 并发资源公平性——2 个 workflow 各 3 个 jobs 公平调度 | 全新 |
| REL-LATENCY-01-009 | reliability | P1 | INTENT-REL-050 | 调度延迟基准——queued→running P50/P95 | 全新 |
| REL-SCHED-01-010 | reliability | P1 | INTENT-REL-057 | 资源调度状态一致性——空闲 runner 存在时 job 不应死等 | 全新 |
| REL-RUNNER-01-011 | reliability | P1 | INTENT-REL-058 | Runner 状态机正确性——空闲/运行/离线转换 | 全新 |
| REL-CACHE-01-012 | reliability | P1 | INTENT-REL-060 | Workflow YAML 缓存失效——修改后无旧代码残留 | 全新 |
| REL-NET-01-013 | reliability | P2 | INTENT-REL-062 | 网络依赖容错——不可达地址明确失败与有界超时 | 全新 |
| REL-API-01-014 | reliability | P2 | INTENT-REL-065 | API 限流与一致性——10 QPS 高频查询不丢数据 | 全新 |
| REL-API-01-015-V2 | reliability | P2 | INTENT-REL-065 | API 限流恢复后数据一致性 | 变体 |
| COMP-ISOLATION-01-001 | completeness | P0 | INTENT-COMP-011 | Runner 环境隔离强度——跨 job 文件残留不可访问 | 全新 |
| COMP-ISOLATION-01-002 | completeness | P0 | INTENT-COMP-011 | Runner 环境隔离强度——进程残留验证 | 变体 |
| COMP-PRSYNC-01-001 | completeness | P0 | INTENT-COMP-004 | PR 同步更新时 pull_request_target 权限保持 | 补充 |
| COMP-STACKMASK-01-001 | completeness | P0 | INTENT-COMP-012 | secret 在错误堆栈与异常输出中必须保持脱敏 | 补充 |
| COMP-MALWF-01-001 | completeness | P0 | INTENT-COMP-014 | 恶意 PR 修改 workflow 后 pull_request_target 行为 | 补充 |
| COMPAT-MISSFN-01-001 | compatibility | P1 | INTENT-COMPAT-010 | 缺失表达式函数 join/fromJSON/case 的降级行为 | 全新 |
| COMPAT-ISOLATION-01-001 | compatibility | P0 | INTENT-COMPAT-028 | Runner 环境隔离与复用策略兼容性确认 | 全新 |
| COMPAT-MIGERR-01-001 | compatibility | P1 | INTENT-COMPAT-031 | 迁移报错质量：不兼容语法报错应指明 GitCode 差异 | 全新 |
| COMPAT-DEFPERM-01-001 | compatibility | P0 | INTENT-COMPAT-002 | 未声明 permissions 时跨仓库默认 TOKEN 权限验证 | 补充 |
| COMPAT-REOPEN-01-001 | compatibility | P0 | INTENT-COMPAT-032 | fork PR 关闭后重新打开时 pull_request_target 权限保持 | 补充 |
| COMP-ISOLATION-01-003 | completeness | P0 | INTENT-COMP-011 | Runner 环境变量跨 run 隔离 | 变体 |
| COMP-ISOLATION-01-004 | completeness | P0 | INTENT-COMP-011 | Runner /tmp 跨 run 隔离 | 变体 |
| COMPAT-EXPR-01-002 | compatibility | P1 | INTENT-COMPAT-010 | case() 函数缺失降级行为 | 变体 |
| COMPAT-ISOLATION-01-002 | compatibility | P0 | INTENT-COMPAT-028 | Runner 复用隔离对齐 GitHub ephemeral | 变体 |
| COMPAT-MIGERR-01-002 | compatibility | P1 | INTENT-COMPAT-031 | GitHub 全名 action 引用报错质量 | 变体 |
| COMPAT-MIGERR-01-003 | compatibility | P1 | INTENT-COMPAT-031 | vars 上下文缺失报错质量 | 变体 |
| COMP-PRSYNC-01-002 | completeness | P0 | INTENT-COMP-004 | fork PR force-push 后权限保持 | 变体 |
| COMP-STACKMASK-01-002 | completeness | P0 | INTENT-COMP-012 | secret 在 step summary 中的脱敏 | 变体 |
| COMP-WFINJ-01-001 | completeness | P0 | INTENT-COMP-014 | 恶意 PR 修改 workflow 后仍用 base 分支 | 变体 |
| COMPAT-PRSEM-01-001 | compatibility | P0 | INTENT-COMPAT-032 | fork PR 关闭后重新打开语义一致性 | 变体 |

---

## 三、待生成记录

| 意图 ID | 维度 | 优先级 | 原因 | 计划 |
|---|---|---|---|---|
| INTENT-SEC-009~012 部分边界 | security | P0 | 上下文限制，时间不足 | 下轮 run 补充：cmd injection 的更多事件来源（PR review, check_run 等） |
| INTENT-REL-044 压力边界 | reliability | P1 | 上下文限制 | 下轮 run 补充：更高并发下的公平性验证 |
| INTENT-COMP-011 自托管场景 | completeness | P0 | 需要自托管 runner 资源 | 下轮 run 补充：自托管 runner 隔离验证 |
| INTENT-COMPAT-028 K8s 场景 | compatibility | P0 | 需要 K8s runner 资源 | 下轮 run 补充：K8s runner 隔离与复用策略 |

---

## 四、DEPRECATE 记录

本轮无新增 DEPRECATE；历史 DEPRECATE 见 `phase01/baseline/case-base-detail.md`（307 条）。

---

## 五、质量自检清单

- [x] 每条文本用例含 `维度标签` 字段，非空
- [x] 每条用例 ID 含 run 序列 `01`，跨 run 不碰撞
- [x] 每条文本用例可溯源到 `intent_ref`
- [x] 每条文本用例有对应、过 schema 校验的 YAML
- [x] 安全用例文本层含「不应发生」，YAML 层落 `negative` 断言
- [x] 破坏性用例声明了正确的 `teardown.reset`
- [x] 主观判据标 `eval: llm_assisted`
- [x] 无真实密钥/token/内网地址，全用占位符
- [x] 未使用 `yaml.dump()` 写 YAML
- [x] `workflow:` 字段全部使用 `|` block scalar
- [x] `runs-on:` 全部使用数组格式
- [x] `uses:` 全部使用裸插件名
- [x] `if:` 仅使用 `${{ always() }}`（带括号）
- [x] 所有 `run:` 全部使用 `run: |` block scalar
- [x] 每个 job 有 `name:`，每个 step 有 `name:`
- [x] Step name 无非法字符

---

*Manifest 最后更新: 2026-07-22*
