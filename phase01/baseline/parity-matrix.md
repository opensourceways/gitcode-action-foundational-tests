# Feature Parity Matrix（对标 GitHub Actions 的完备性标尺）

> L0 基线之一。左列能力项来自 spec-analyst 的能力清单；支持状态需人+agent 共同确认。
> 这是覆盖度评审的坐标系之一：每个「部分/不支持/未知」项都应能反查到覆盖它的用例。
> **本文件是模板+示例，请用真实能力项替换示例行。**

## 支持状态图例
- ✅ 完全支持（行为与 GitHub 一致）
- 🟡 部分支持（有差异或子集）
- ❌ 不支持
- ❓ 未知（规格未明，需验证）

## 能力对标表

| 能力项 | 分类 | GitHub 行为（oracle） | GitCode 支持状态 | 差异/备注 | 出处 | 关联意图 |
|---|---|---|---|---|---|---|
| 工作流文件目录 `.github/workflows/` | 语法 | `.github/workflows/` 目录 | 🟡 | GitCode 用 `.gitcode/workflows/` | workflow-file-location-structure.md | INTENT-COMP-001 |
| 未知/不支持字段处理 | 语法 | 报错或静默忽略依字段而定 | ❓ | 文档未明确降级方式 | 多处缺失 | INTENT-COMP-002 |
| `push` 触发 + branches/paths 过滤 | 触发器 | 通配与取反支持 | ✅ | 语法一致，paths 上限 300 | trigger-events.md | INTENT-COMP-003 |
| `pull_request` vs `pull_request_target` 隔离 | 触发器/安全 | fork PR 严格隔离 secret | ✅ | 语义与 GitHub 一致，需实测确认强度 | pr-mr-pipeline-security.md | INTENT-COMP-004 |
| `schedule` cron 最短间隔 | 触发器 | 无官方最短间隔限制 | 🟡 | GitCode 声明最短 5 分钟，UTC，仅默认分支 | trigger-events.md | INTENT-COMP-005 |
| `workflow_call` 嵌套层数 | 执行模型 | 理论无上限（实际有限） | 🟡 | GitCode 最多 2 层 | trigger-events.md | INTENT-COMP-006 |
| `stages` 阶段机制 | 执行模型 | 无 stages 概念（仅有 job DAG） | ❌ | GitCode 特有，阶段间串行+阶段内并行 | core-concepts/workflow-job-step-action.md | INTENT-COMP-007 |
| `post` 后处理阶段 | 执行模型 | 无顶层 post（仅 action 内 post） | ❌ | GitCode 特有，默认 run_always: true | workflow-file-location-structure.md | INTENT-COMP-007 |
| `timeout-minutes` 默认 360 分钟 | 执行模型 | 默认 360 分钟（job） | ✅ | 与 GitHub 一致 | configure-jobs.md | INTENT-COMP-008 |
| `rerun` 次数限制 | 执行模型 | 无官方次数限制 | 🟡 | GitCode 最多 3 次，超 6h 不可 rerun | rerun-failed-jobs.md | INTENT-COMP-009 |
| `runs-on` 标签体系 | Runner | 单标签或数组匹配 | 🟡 | GitCode 三段式 `{os,arch,flavor}` | using-hosted-runners.md | INTENT-COMP-010 |
| Runner 环境隔离 / 一次性 | Runner | 官方 Runner 为 ephemeral | ❓ | 文档未明确 GitCode Runner 是否复用 | 未明确 | INTENT-COMP-011 |
| `secrets` 日志脱敏 `***` | 安全 | `***` 遮蔽 | 🟡 | 文档自承 `${{ secrets.X }}` 可能绕过 | using-secrets.md | INTENT-COMP-012 |
| `permissions` 默认权限 | 安全 | 默认 read/write 依仓库设置 | ❓ | GitCode 称"使用仓库设置"，默认值未明确 | token-permissions.md | INTENT-COMP-013 |
| `permissions` 权限域命名 | 安全 | `contents`/`pull-requests`/`issues`/`actions` | ❌ | GitCode 用 `repository`/`pr`/`issue`/`hook` 等 | token-permissions.md | INTENT-COMP-022 |
| `pull_request_target` checkout head.sha 风险 | 安全 | 高权限运行不可信代码风险 | ✅ | 语义与 GitHub 一致，需实测确认 | pr-mr-pipeline-security.md | INTENT-COMP-014 |
| `upload-artifact` / `download-artifact` | Artifact | 跨 job 传递，保留期可配 | 🟡 | 保留期默认 90 天；大小上限未公开 | upload-download-artifacts.md | INTENT-COMP-015 |
| `cache` fork 场景隔离 | Artifact | 未明确跨 fork 隔离 | ❓ | GitCode 文档未明确 cache 隔离策略 | using-dependency-cache.md | INTENT-COMP-016 |
| 运行状态机 + 日志完整性 | 可观测性 | queued→in_progress→completed | ✅ | 状态语义与 GitHub 一致 | view-run-results.md | INTENT-COMP-017 |
| `ATOMGIT_STEP_SUMMARY` Markdown | 可观测性 | GitHub 对应 `GITHUB_STEP_SUMMARY` | 🟡 | 前缀差异，功能语义一致 | runtime-environment-variables.md | INTENT-COMP-018 |
| 上下文对象命名 `github.*` | 兼容性 | `github.ref`/`github.sha` 等 | ❌ | GitCode 用 `atomgit.*` | syntax-reference/context.md | INTENT-COMP-019 |
| 状态函数括号语法 `success()` | 兼容性 | 必须带括号 `success()`/`failure()` | ❌ | GitCode 无括号 `success`/`failed` | expressions.md | INTENT-COMP-020 |
| 表达式函数 `contains`/`hashFiles`/`toJson` | 兼容性 | 见 GitHub 官方语义 | ❓ | 边界行为待比对 | expressions.md | INTENT-COMP-021 |
| `workflow_dispatch.inputs` 类型 | 兼容性 | 支持 boolean/choice/number/environment | 🟡 | GitCode 仅支持 `string` | trigger-events.md | INTENT-COMP-023 |
| 迁移报错质量（GitHub→GitCode） | 易用性 | — | ❓ | 文档未系统说明报错差异指引 | COMPAT-NOTES.md | INTENT-COMP-024 |
| `concurrency.max` 1-5 + QUEUE/IGNORE | 稳定性 | workflow 级并发控制 | 🟡 | 实现细节待实测 | workflow-file-location-structure.md | INTENT-COMP-025 |
| `strategy.matrix` 组合数上限 | 稳定性 | 官方上限 256 jobs / workflow | ❓ | GitCode 未公开上限 | configure-matrix-builds.md | INTENT-COMP-026 |

> 填写建议：先覆盖 `testing-focus.md` §2/§3/§5/§10 列出的高发差异类别，再逐步补全。每确认一项差异，回写「差异/备注」并挂上关联意图 ID。
