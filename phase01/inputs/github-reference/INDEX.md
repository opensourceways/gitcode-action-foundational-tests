# GitHub Actions 对标参考文档索引

> 来源：https://docs.github.com/en/actions ｜ 抓取日期：2026-07-20
> 共 **12 页**核心规格文档（从 200+ 页中筛选），精准对标 compat-diff 与 security agent 需求。
> 每个文件底部标注了 GitCode↔GitHub 关键差异线索。

## 用途

- **compat-diff agent（6 页 reference）**：GitHub 侧权威行为定义，作为差分测试的 oracle 基准
- **security agent（6 页 security）**：GitHub 安全加固清单，作为 GitCode 安全检查项对照

## 目录

### 行为参考（compat-diff oracle）

| # | 文件 | 对标 GitCode 文档 |
|---|---|---|
| 1 | [reference/workflow-syntax.md](reference/workflow-syntax.md) | writing-pipelines/ 全板块（jobs/steps/on/env/permissions/concurrency/defaults） |
| 2 | [reference/events.md](reference/events.md) | syntax-reference/trigger-events.md（事件名·types·filter·payload） |
| 3 | [reference/contexts.md](reference/contexts.md) | syntax-reference/context.md（`github.*` vs `atomgit.*` 全属性） |
| 4 | [reference/expressions.md](reference/expressions.md) | syntax-reference/expressions.md（函数签名·运算符·状态函数） |
| 5 | [reference/workflow-commands.md](reference/workflow-commands.md) | syntax-reference/workflow-commands.md（`GITHUB_*` vs `ATOMGIT_*` 环境文件） |
| 6 | [reference/variables.md](reference/variables.md) | syntax-reference/variables.md（`GITHUB_*` vs `ATOMGIT_*` 系统变量） |

### 安全参考（security agent 知识输入）

| # | 文件 | 用途 |
|---|---|---|
| 7 | [security/secure-use.md](security/secure-use.md) | 核心安全加固清单（secrets · 脚本注入 · 第三方 action · OIDC · 自托管 runner） |
| 8 | [security/secrets.md](security/secrets.md) | Secret 约束与最佳实践（命名·加密·脱敏·fork 隔离） |
| 9 | [security/github-token.md](security/github-token.md) | `GITHUB_TOKEN` 默认权限·生命周期·recursive run 防护 |
| 10 | [security/script-injections.md](security/script-injections.md) | CI/CD 最高危攻击面·注入模式·缓解 |
| 11 | [security/pull_request_target.md](security/pull_request_target.md) | `pull_request_target` 风险·pwn request·cache 只读·`allow-unsafe-pr-checkout` |

> 注：`permissions` 字段的完整定义已包含在 workflow-syntax.md 中（权限表含 18 项 scope），不再单列。

### 未抓取（不需要）

以下 200+ 页范畴不在对标需求内，未抓取：
- 教程 / Getting Started / How-to 指南（教学材料，非规格）
- 部署到云厂商的 OIDC 配置页（infra 特定，不相关）
- Runner 安装/管理操作指南（GitCode 有自己的 Runner 管理页）
- Marketplace / Billing / Metrics（不相关）
- Migration guides（不相关）
- 各语言 Build & Test 教程

## 与 GitCode 侧输入的关系

- 本目录 + `phase01/inputs/gitcode-spec/COMPAT-NOTES.md` = compat-diff agent 的完整输入（左 GitCode、右 GitHub）
- 差异线索已标注在每个文件末尾的 `> **关键差异提示**` 块中
