<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/syntax-reference/variables | fetched: 2026-07-20 -->

# 变量（语法参考）

AtomGit Action 支持多种类型的变量，用于在工作流中传递配置信息和敏感数据。

## 4.1 变量类型

### env 变量（自定义环境变量）

在 workflow、job、step 级别通过 `env:` 关键字定义的环境变量，直接作为系统环境变量注入到 Runner 中。

```yaml
env:
  GLOBAL_VAR: global_value    # workflow 级别
jobs:
  build:
    env:
      JOB_VAR: job_value      # job 级别
    steps:
      - name: Step
        env:
          STEP_VAR: step_value  # step 级别
        run: echo "$GLOBAL_VAR $JOB_VAR $STEP_VAR"
```

> 在 `run:` 脚本中可直接作为系统环境变量使用（`$VAR_NAME`），在表达式中使用 `${{ env.VAR_NAME }}`。

### vars 变量（配置变量）

在 AtomGit 平台设置页面定义的**非敏感**配置变量，按组织/项目级别管理。

- 组织级别 vars：组织下所有项目可用
- 项目级别 vars：仅当前项目可用

访问：`${{ vars.VAR_NAME }}`

### secrets 变量（加密密钥）

在 AtomGit 平台设置页面定义的**敏感**加密数据，按组织/项目级别管理。

- 组织级别 secrets：组织下所有项目可用
- 项目级别 secrets：仅当前项目可用
- 环境级别 secrets：绑定到特定部署环境

访问：`${{ secrets.SECRET_NAME }}`

> **日志脱敏：** 所有 secrets 值在日志输出中自动替换为 `***`，无法通过日志泄露。

### inputs 变量（工作流输入参数）

在 `workflow_dispatch` 或 `workflow_call` 的 `inputs:` 中定义的参数。

访问：`${{ inputs.INPUT_NAME }}`

**inputs type 规格：**

AtomGit Action 的 `inputs` 仅支持 `string` 类型。所有输入值均为字符串。

| type | 值类型 | 必选字段 | 可选字段 | 说明 |
|------|--------|---------|---------|------|
| `string` | string | - | `description`, `required`, `default` | 任意字符串 |

## 4.2 变量优先级

当同名变量在不同级别定义时，优先级从高到低为：

**step > job > workflow**

即：step 级别 env > job 级别 env > workflow 级别 env。

对于 vars 和 secrets，项目级别 > 组织级别（项目级别同名变量覆盖组织级别）。

## 4.3 ATOMGIT_* 系统变量完整列表

AtomGit Runner 在每个工作流运行时自动注入以下系统环境变量：

| 系统变量 | 说明 | 示例值 |
|---------|------|--------|
| `ATOMGIT_TOKEN` | 工作流认证令牌（自动生成，用于 API 调用） | `ghs_xxxxx` |
| `ATOMGIT_SHA` | 触发提交的 SHA | `a1b2c3d4e5f6...` |
| `ATOMGIT_REF` | 触发引用全名 | `refs/heads/main` |
| `ATOMGIT_REF_NAME` | 触发引用短名 | `main` |
| `ATOMGIT_REF_TYPE` | 引用类型 | `branch` / `tag` |
| `ATOMGIT_EVENT_NAME` | 触发事件名称 | `push` |
| `ATOMGIT_EVENT_PATH` | 事件 payload JSON 文件路径 | `/home/runner/_temp/_atomgit_workflow/event.json` |
| `ATOMGIT_WORKSPACE` | Runner 工作区路径 | `/home/runner/workspace/repo` |
| `ATOMGIT_ACTION` | 当前 Action 名称 | `my-action` |
| `ATOMGIT_REPOSITORY` | 仓库全名 | `owner/repo` |
| `ATOMGIT_REPOSITORY_OWNER` | 仓库所属组织 | `myorg` |
| `ATOMGIT_RUN_ID` | 工作流运行 ID | `12345` |
| `ATOMGIT_RUN_NUMBER` | 工作流运行编号 | `42` |
| `ATOMGIT_RUN_ATTEMPT` | 重试次数 | `1` |
| `ATOMGIT_WORKFLOW` | 工作流名称 | `CI Pipeline` |
| `ATOMGIT_HEAD_REF` | PR 源分支（仅 PR 事件） | `feature/new-api` |
| `ATOMGIT_BASE_REF` | PR 目标分支（仅 PR 事件） | `main` |
| `ATOMGIT_SERVER_URL` | AtomGit 平台根 URL | `https://atomgit.com` |
| `ATOMGIT_API_URL` | AtomGit API 基础 URL | `https://api.atomgit.com` |
| `ATOMGIT_GRAPHQL_URL` | AtomGit GraphQL API URL | `https://api.atomgit.com/graphql` |
| `ATOMGIT_OUTPUT` | 步骤输出文件路径 | 见工作流命令参考 |
| `ATOMGIT_ENV` | 步骤环境变量文件路径 | 见工作流命令参考 |
| `ATOMGIT_PATH` | 步骤系统 PATH 文件路径 | 见工作流命令参考 |
| `ATOMGIT_STEP_SUMMARY` | 步骤摘要文件路径 | 见工作流命令参考 |
| `ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS` | 是否允许不安全命令 | `false`（默认） |
| `ATOMGIT_ACTION_REPOSITORY` | Action 来源仓库 | `owner/action-repo` |
| `ATOMGIT_ACTION_REF` | Action 来源引用 | `v1` |

> **注意：** `ATOMGIT_TOKEN` 仅在工作流运行期间有效，运行结束后失效。请勿将此令牌持久化存储。
