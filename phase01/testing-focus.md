# GitCode Action / Workflow 型系统 · 测试关注点

> 需求 2：GitCode Action 是「workflow 运行」而非「API 请求-响应」，测试范式与常规 API 测试差异很大。本文件总结业界对 CI/CD workflow 平台的测试实践，作为各维度 agent 挖 intent 的**检查清单式底料**。
> 用法：每个维度 agent 在发散阶段应逐条扫过本文件对应章节，确保没有系统性遗漏一整类关注点。

---

## 0. 为什么 workflow 测试不同于 API 测试

| 维度 | API 测试 | Workflow 测试 |
|---|---|---|
| 输入 | 请求参数 | YAML 定义 + 触发事件 + 仓库状态 + secrets/vars + runner 环境 |
| 执行 | 单次同步/异步调用 | 多 job DAG、matrix 展开、并发、长时运行、可被取消 |
| 输出 | 响应体/状态码 | 运行状态 + 日志 + 注解 + artifact + 副作用（推送/评论/部署） |
| Oracle | 明确的响应契约 | 常需对标另一平台（GitHub）的真实行为 |
| 失败模式 | 4xx/5xx | 解析失败、卡死、超时、隔离逃逸、密钥泄露、非确定性 flaky |

**核心含义**：测试对象是「一段声明式定义在特定上下文下被解释执行后产生的行为与副作用」。因此每条用例都要显式布置 **YAML + 触发身份 + 仓库前置状态 + 环境**，并对**状态、日志、副作用**三条线分别断言。

---

## 1. Workflow 语法解析与静态校验（完备性 / 易用性）

- YAML schema 合法性：必填字段、类型、枚举值、缩进/锚点/多文档。
- 表达式语法 `${{ }}`：函数（`contains`/`startsWith`/`fromJSON`/`hashFiles`…）、运算符、上下文对象（`github`/`env`/`secrets`/`matrix`/`needs`/`steps`…）。
- 非法定义的**报错质量**：错在第几行、给不给可操作提示（易用性重点）。
- 未知/不支持字段的处理：报错？静默忽略？——这是兼容性差异高发区。

## 2. 触发器语义（完备性 / 安全性 / 兼容性）

- 事件类型：`push` / `pull_request` / **`pull_request_target`**（安全敏感）/ `workflow_dispatch` / `schedule` / `tag` / `release` / `issue_comment` 等。
- 触发过滤：`branches` / `paths` / `tags` 过滤及其取反、通配语义。
- **fork PR 场景**：来自 fork 的 PR 触发时的权限降级、secret 隔离、`GITHUB_TOKEN` 只读——安全命脉，见 §5。
- `schedule` cron 语义与时区；并发触发的去重/排队。
- 触发到实际排程的**幂等与去抖**：同一 push 连推是否重复触发。

## 3. 执行模型（完备性 / 稳定性）

- **job DAG**：`needs` 依赖、拓扑执行、失败传播、`if` 条件（含 `always()`/`failure()`/`success()`/`cancelled()`）。
- **matrix**：展开正确性、`include`/`exclude`、`fail-fast`、`max-parallel`。
- **并发控制**：`concurrency` group、`cancel-in-progress`、排队与抢占。
- job/step 级 `continue-on-error`、`timeout-minutes`、重试。
- **outputs 传递**：step→job→下游 job 的 outputs、`GITHUB_OUTPUT`/`GITHUB_ENV` 文件协议。
- 取消语义：手动取消/被抢占时，正在运行的 step 如何终止、清理钩子是否执行。

## 4. Runner 与执行环境隔离（稳定性 / 安全性）

- Runner 生命周期：是否**一次性（ephemeral）**、复用 runner 的残留污染（工作区/环境变量/缓存/进程）。
- 容器/VM 隔离边界：能否访问宿主、逃逸面、跨 job 文件可见性。
- 预装工具链、`PATH`、默认 shell、工作目录、`$HOME`。
- 网络出站策略：能否访问外网/内网、DNS、代理。
- 资源边界：CPU/内存/磁盘配额，超限时的行为（OOM kill / 磁盘满）。

## 5. Secrets 与权限（安全命脉）

- **fork PR 的 secret 隔离**：外部贡献者 PR 不应读到仓库 secrets（`pull_request` 事件）。`pull_request_target` 在 base 上下文运行，最易被滥用——重点验证。
- `GITHUB_TOKEN`（或 GitCode 对应令牌）的**默认权限范围**与 `permissions:` 收窄/放宽语义。
- secret **日志脱敏（masking）**：secret 出现在日志时是否被 `***` 遮蔽，包括 base64/拼接/多行变形后的泄露。
- 环境级 secret、组织级 secret、环境保护规则（reviewers/wait timer）。
- OIDC / 短时凭据（若支持）。

## 6. 表达式注入与不可信输入（安全性）

- **脚本注入**：把不可信输入（PR 标题/正文、分支名、issue 评论、提交信息）直接插进 `run:` 的 `${{ }}`，导致命令执行——业界最常见的 Actions 漏洞类。
- 环境变量注入、`GITHUB_ENV`/`GITHUB_OUTPUT`/`GITHUB_PATH` 文件写入被污染。
- 第三方 action 输入的信任边界。

## 7. 复用与供应链（安全性 / 完备性）

- **引用第三方 action**：`uses: owner/repo@ref` 的 ref 固定（tag/branch/**commit SHA**）、可变 tag 被重写的风险。
- reusable workflow（`workflow_call`）、composite action、本地 action 引用。
- action 的 marketplace/来源信任、私有 registry。
- 依赖 pin 与审计：不可变引用 vs 浮动引用。

## 8. Artifact / Cache（稳定性 / 安全性）

- artifact 上传/下载、保留期、跨 job/跨 run 传递。
- **cache 投毒**：fork PR 写缓存污染主分支缓存；cache key 作用域与隔离。
- 大 artifact/大 cache 的边界与配额。

## 9. 可观测性与结果契约（易用性 / 完备性）

- 运行状态机：queued→in_progress→completed(success/failure/cancelled/skipped)。
- 日志完整性、实时性、折叠分组、`::group::`/`::error::`/`::warning::` 等 workflow 命令。
- 注解（annotation）落到 PR/commit 的正确性。
- 退出码语义、step summary、状态回写（commit status / check run）。

## 10. 兼容性差异高发区（本次核心资产 · COMPAT）

对「看起来一样、行为不一样」的点，重点扫这些类别：

- **默认值差异**：未声明字段的默认行为（如默认 shell、默认 `permissions`、默认并发）。
- **表达式函数差异**：同名函数边界行为、类型转换、空值处理。
- **触发过滤语义差异**：`paths`/`branches` 通配、事件负载字段命名。
- **上下文对象差异**：`github.*` 字段是否齐全、值格式。
- **不支持能力的降级方式**：报错 vs 静默忽略 vs 部分支持。
- **内置 action 差异**：`actions/checkout`、`actions/cache` 等的对应实现是否等价。
- **runner 标签/环境差异**：`runs-on` 取值、预装软件版本。

## 11. 迁移摩擦（易用性）

- 直接把 GitHub 的 `.github/workflows` 搬到 GitCode，**开箱能跑多少 / 哪里断**。
- 报错能否指明「这是 GitCode 不支持/需改写」而非泛化报错。
- 文档是否明确列出差异清单与迁移指引。
- 从 GitHub 迁移的常见动作（secret 配置、runner 注册、变量）摩擦点。

## 12. 稳定性专项（REL）

- 并发洪泛：大量 workflow 同时触发的排队/限流/公平性。
- 大规模：超大 matrix、超多 step、超长日志、超大仓库 checkout。
- 长时运行：接近/超过 timeout 的行为；心跳/保活。
- 故障注入（混沌）：kill runner、网络分区、磁盘满、CPU 饱和、依赖服务不可用时的**重试与恢复**。
- 资源配额耗尽后的降级与报错清晰度。

---

## 附：每条 intent 建议自检的最小三问

1. **布置齐了吗**：YAML + 触发身份 + 仓库前置状态 + 环境，四要素是否都指定？
2. **Oracle 明确吗**：预期从 GitCode 规格、GitHub 行为、还是差异声明来？（见 `rules.md` §4）
3. **三条线都断言了吗**：状态 / 日志 / 副作用，是否有对应的 positive/negative/nonfunctional 断言？
