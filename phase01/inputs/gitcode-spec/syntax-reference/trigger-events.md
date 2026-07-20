<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/syntax-reference/trigger-events | fetched: 2026-07-20 -->

# 触发事件（语法参考）

工作流通过 `on` 关键字定义触发条件。AtomGit Action 支持以下触发事件，工作流文件存放于仓库的 `.gitcode/workflows/` 目录下。

## 1.1 push

当发生推送操作时触发，包括分支推送和标签推送。

```yaml
on:
  push:
    branches:
      - main
      - 'releases/**'
    tags:
      - v1.*
      - v2.*
    paths:
      - 'src/**'
      - 'package.json'
    paths-ignore:
      - 'docs/**'
      - '**.md'
```

**过滤字段：**

| 字段 | 说明 | 示例 |
|------|------|------|
| `branches` | 匹配的分支名模式 | `main`, `releases/**` |
| `branches-ignore` | 排除的分支名模式 | `experimental/**` |
| `tags` | 匹配的标签名模式 | `v1.*` |
| `tags-ignore` | 排除的标签名模式 | `v1.0.*` |
| `paths` | 匹配的文件路径模式 | `src/**` |
| `paths-ignore` | 排除的文件路径模式 | `docs/**` |

> **注意：** `branches` 与 `branches-ignore` 不可同时使用；`tags` 与 `tags-ignore` 不可同时使用。`paths` 与 `paths-ignore` 可以与分支/标签过滤组合使用。

**特殊用法：**

```yaml
on:
  push:
    branches:
      - '**'        # 所有分支
      - '!main'     # 排除 main（排除模式以 ! 开头）
```

## 1.2 pull_request

当创建、更新或合并 Pull Request 时触发。

```yaml
on:
  pull_request:
    types:
      - open
      - reopen
      - update
      - merge
    branches:
      - main
      - 'feature/**'
    paths:
      - 'src/**'
    paths-ignore:
      - 'docs/**'
```

**事件类型（types）：**

| 类型 | 说明 |
|------|------|
| `open` | PR 创建 |
| `reopen` | PR 重新打开 |
| `update` | PR 源分支有新提交（最常见的触发场景） |
| `merge` | PR 合并 |

> **默认值：** 不指定 `types` 时，默认为 `[open, reopen, update]`，即 PR 创建、重新打开和更新时触发，不包含合并事件。

**过滤字段：** 同 push，支持 `branches`, `branches-ignore`, `paths`, `paths-ignore`。

## 1.3 pull_request_target

与 `pull_request` 类似，但工作流运行在**目标分支（base 分支）的上下文**中，可读写目标仓库。适用于需要访问仓库 Secrets 或进行写操作的场景（如自动标签、评论等）。

```yaml
on:
  pull_request_target:
    types:
      - open
      - update
      - merge
    branches:
      - main
```

> **安全提示：** `pull_request_target` 会使用目标分支的 workflow 文件和权限，fork 仓库的 PR 也能触发。请谨慎处理 fork PR 的代码执行，避免安全风险。

> **默认值：** 不指定 `types` 时，默认为 `[open, reopen, update]`，与 `pull_request` 一致。

## 1.4 issue_comment

当 Issue 或 PR 的评论被创建、编辑或删除时触发。

```yaml
on:
  issue_comment:
    types:
      - created
      - edited
      - deleted
```

**事件类型：**

| 类型 | 说明 |
|------|------|
| `created` | 评论创建 |
| `edited` | 评论编辑 |
| `deleted` | 评论删除 |

> **注意：** `issue_comment` 同时对 Issue 评论和 PR 评论生效。如需仅过滤 PR 评论，可在工作流中使用条件表达式判断 `atomgit.event.issue_comment.issue.pull_request` 是否存在。

## 1.5 pull_request_comment

区别于 `issue_comment`，仅在 **Pull Request 评论**时触发。

```yaml
on:
  pull_request_comment:
    types:
      - created
      - edited
      - deleted
    branches:
      - main
    comments:
      - '/deploy'
      - '/test'
```

**事件类型：**

| 类型 | 说明 |
|------|------|
| `created` | 评论创建 |
| `edited` | 评论编辑 |
| `deleted` | 评论删除 |

**过滤字段：**

| 字段 | 说明 | 示例 |
|------|------|------|
| `branches` | 匹配 PR 目标分支名模式 | `main`, `feature/**` |
| `comments` | 基于正则表达式的评论内容过滤 | `/deploy`, `/test` |

> **comments 过滤说明：** `comments` 字段支持对评论内容基于正则表达式进行条件过滤，只有评论内容匹配指定正则模式的才会触发工作流。例如配置 `comments: ['/deploy']`，则只有评论中包含 `/deploy` 指令时才触发。

## 1.6 workflow_dispatch

手动触发工作流，支持自定义输入参数。

```yaml
on:
  workflow_dispatch:
    inputs:
      environment:
        description: '部署目标环境'
        required: true
        default: 'staging'
        type: string
      version:
        description: '发布版本号'
        required: false
        type: string
      deploy_count:
        description: '并行部署数量'
        required: false
        default: "1"
        type: string
      dry_run:
        description: '是否仅验证不部署'
        required: false
        default: "false"
        type: string
      log_level:
        description: '日志级别'
        required: false
        default: 'info'
        type: string
```

**inputs type 类型规格：**

| type | 说明 | 可选字段 |
|------|------|---------|
| `string` | 字符串输入 | `description`, `required`, `default` |

> 在工作流中通过 `inputs` 上下文访问输入值，如 `${{ inputs.environment }}`。如需数字或布尔语义，可在工作流中通过表达式进行类型转换。

## 1.8 workflow_call

允许一个工作流被另一个工作流调用（可复用工作流）。

```yaml
on:
  workflow_call:
    inputs:
      config-path:
        description: '配置文件路径'
        required: false
        default: 'config/default.json'
        type: string
      environment:
        description: '部署环境'
        required: true
        type: string
    secrets:
      deploy-token:
        description: '部署认证令牌'
        required: true
      db-password:
        description: '数据库密码'
        required: false
```

**调用方工作流示例：**

```yaml
jobs:
  deploy:
    uses: ./.gitcode/workflows/deploy.yml
    with:
      config-path: 'config/production.json'
      environment: production
    secrets:
      deploy-token: ${{ secrets.DEPLOY_TOKEN }}
      db-password: ${{ secrets.DB_PASSWORD }}
```

## 1.9 schedule

定时触发工作流，使用 POSIX cron 语法。

```yaml
on:
  schedule:
    - cron: '30 5 * * 1,3'    # 每周一、三 05:30 UTC
    - cron: '0 2 * * *'        # 每天 02:00 UTC
    - cron: '15 0 1 1 *'       # 每年1月1日 00:15 UTC
```

**cron 语法格式：** `分钟 小时 日 月 星期`

| 位置 | 范围 | 说明 |
|------|------|------|
| 分钟 | 0-59 | 每小时的第几分钟 |
| 小时 | 0-23 | UTC 时间小时 |
| 日 | 1-31 | 每月的第几天 |
| 月 | 1-12 | 月份 |
| 星期 | 0-6 | 0=周日, 1=周一, ..., 6=周六 |

**特殊符号：**

| 符号 | 说明 | 示例 |
|------|------|------|
| `*` | 任意值 | `* * * * *` — 每分钟 |
| `,` | 列表分隔 | `1,3,5` — 第1、3、5 |
| `-` | 范围 | `1-5` — 1到5 |
| `/` | 步长 | `*/15` — 每15单位 |

> **注意：** schedule 的最短间隔为 5 分钟。cron 使用 UTC 时间，请换算为本地时间。
