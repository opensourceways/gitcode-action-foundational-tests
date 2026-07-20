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
| `push` 触发 + branches 过滤 | 触发器 | 通配与取反支持 | ❓ | 待验证通配语义 | — | — |
| `pull_request_target` | 触发器 | base 上下文运行，有 secret | ❓ | 安全敏感，重点 | — | INTENT-SEC-xxx |
| `${{ contains() }}` | 表达式 | 见官方语义 | ❓ | 边界行为待比对 | — | — |
| `concurrency` + cancel-in-progress | 执行模型 | 抢占取消 | ❓ | — | — | — |
| 默认 `permissions` | 权限 | 仓库级默认 | ❓ | 默认值差异高发 | — | — |
| secret 日志 masking | 安全 | `***` 遮蔽 | ❓ | 变形泄露待测 | — | — |
| `actions/checkout` 等价实现 | 内置 action | — | ❓ | — | — | — |
| `runs-on` 标签 | runner | 标签匹配 | ❓ | 标签集差异 | — | — |

> 填写建议：先覆盖 `testing-focus.md` §2/§3/§5/§10 列出的高发差异类别，再逐步补全。每确认一项差异，回写「差异/备注」并挂上关联意图 ID。
