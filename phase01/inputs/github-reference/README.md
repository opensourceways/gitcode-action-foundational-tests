# inputs/github-reference/ （**必需**）— 已补充 ✅

GitHub Actions 官方核心参考文档的离线镜像，精准筛选 12 页对标 compat-diff 与 security agent 需求的规格页。
抓取自 https://docs.github.com/en/actions （2026-07-20）。

## 导航
- **[INDEX.md](INDEX.md)** — 12 页索引 + 用途说明
- `reference/` — 6 页行为参考（compat-diff 的 oracle）
- `security/` — 6 页安全参考（security agent 的知识输入）

## 消费方
compat-diff（差分测试 oracle）· security（GitHub 安全清单对照 GitCode 覆盖度）

## 关键兼容差异速查

| 差异域 | GitHub | GitCode |
|---|---|---|
| 工作流目录 | `.github/workflows/` | `.gitcode/workflows/` |
| 核心上下文 | `github.*` | `atomgit.*` |
| 系统变量前缀 | `GITHUB_*` | `ATOMGIT_*` |
| 自动令牌 | `GITHUB_TOKEN` | `ATOMGIT_TOKEN` |
| 状态函数 | `success()` / `failure()` / `cancelled()`（带括号） | `success` / `failed` / `cancelled`（无括号） |
| permissions 权限域 | `contents`/`pull-requests`/`issues`… | `repository`/`pr`/`issue`/`project`/`note`/`hook` |
| workflow_dispatch inputs | 5 种类型（boolean/choice/number/environment/string） | 仅 `string` |
| pull_request types | `opened`/`synchronize`/`reopened` | `open`/`update`/`reopen`/`merge` |
| 特有事件 | — | `pull_request_comment`（带正则过滤） |
| 特有编排 | — | `stages`（阶段）· `post`（后处理） |
| Runner 标签 | `ubuntu-latest` | 三段式 `{os,arch,flavor}` |

**已补充 / 12 页 / 2026-07-20**
