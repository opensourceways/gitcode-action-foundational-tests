<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/syntax-reference/context | fetched: 2026-07-20 -->

# 上下文（语法参考）

AtomGit Action 提供 12 种上下文，用于在工作流中访问运行环境信息。每个上下文是一个 JSON 对象，可通过表达式 `${{ context.property }}` 访问。

## 2.1 上下文总览

| 上下文 | 说明 | 常用访问方式 |
|------|------|----------|
| `atomgit` | AtomGit 平台与事件信息 | `${{ atomgit.event_name }}`, `${{ atomgit.sha }}` |
| `env` | 当前步骤/Job/Workflow 的自定义环境变量 | `${{ env.MY_VAR }}` |
| `vars` | 组织/项目级别配置变量 | `${{ vars.DEPLOY_ENV }}` |
| `job` | 当前 Job 信息 | `${{ job.status }}` |
| `jobs` | 可复用工作流中已运行 Job 的结果 | `${{ jobs.deploy.result }}` |
| `steps` | 当前 Job 中各步骤信息 | `${{ steps.build.outputs.result }}` |
| `runner` | Runner 执行环境信息 | `${{ runner.os }}`, `${{ runner.arch }}` |
| `secrets` | 加密密钥 | `${{ secrets.DEPLOY_TOKEN }}` |
| `strategy` | 矩阵策略信息 | `${{ strategy.job-index }}` |
| `matrix` | 当前矩阵实例的变量值 | `${{ matrix.version }}` |
| `inputs` | workflow_dispatch/workflow_call 的输入参数 | `${{ inputs.environment }}` |

## 2.2 atomgit 上下文完整属性

`atomgit` 是 AtomGit 特有的核心上下文，提供平台和事件相关的所有信息。

| 属性 | 类型 | 说明 |
|------|------|------|
| `atomgit.event_name` | string | 当前触发事件名称 |
| `atomgit.sha` | string | 触发提交的 SHA |
| `atomgit.ref` | string | 触发引用（分支或标签全名，如 `refs/heads/main`） |
| `atomgit.ref_name` | string | 触发引用短名（如 `main`, `v1.0`） |
| `atomgit.ref_type` | string | 引用类型：`branch` 或 `tag` |
| `atomgit.event` | object | 事件完整 payload 对象 |
| `atomgit.workspace` | string | Runner 工作区路径 |
| `atomgit.action` | string | 当前 Action 名称 |
| `atomgit.token` | string | ATOMGIT_TOKEN 令牌（用于 API 调用） |
| `atomgit.repository` | string | 仓库全名（如 `owner/repo`） |
| `atomgit.repository_owner` | string | 仓库所属组织/用户名 |
| `atomgit.repositoryUrl` | string | 仓库 URL |
| `atomgit.run_id` | string | 工作流运行唯一 ID |
| `atomgit.run_number` | number | 工作流运行编号 |
| `atomgit.run_attempt` | number | 工作流重试次数 |
| `atomgit.workflow` | string | 工作流名称 |
| `atomgit.head_ref` | string | PR 源分支（仅 PR 事件） |
| `atomgit.base_ref` | string | PR 目标分支（仅 PR 事件） |
| `atomgit.server_url` | string | AtomGit 平台根 URL |
| `atomgit.api_url` | string | AtomGit API 基础 URL |

## 2.3 atomgit.event 各事件字段

### push 事件

| 字段 | 说明 |
|------|------|
| `atomgit.event.ref` | 推送的完整 ref |
| `atomgit.event.before` | 推送前的 SHA |
| `atomgit.event.after` | 推送后的 SHA |
| `atomgit.event.commits` | 提交列表数组 |
| `atomgit.event.commits[].id` | 单个提交 SHA |
| `atomgit.event.commits[].message` | 提交消息 |
| `atomgit.event.commits[].author` | 提交作者 |
| `atomgit.event.commits[].added` | 新增文件列表 |
| `atomgit.event.commits[].modified` | 修改文件列表 |
| `atomgit.event.commits[].removed` | 删除文件列表 |
| `atomgit.event.base_ref` | 基础 ref（标签推送时为空） |
| `atomgit.event.created` | 是否为新创建的 ref |
| `atomgit.event.deleted` | 是否为删除的 ref |

### pull_request 事件

| 字段 | 说明 |
|------|------|
| `atomgit.event.pull_request.number` | PR 编号 |
| `atomgit.event.pull_request.title` | PR 标题 |
| `atomgit.event.pull_request.body` | PR 描述 |
| `atomgit.event.pull_request.state` | PR 状态（open/closed） |
| `atomgit.event.pull_request.user.login` | PR 创建者 |
| `atomgit.event.pull_request.head.ref` | PR 源分支名 |
| `atomgit.event.pull_request.head.sha` | PR 源分支最新 SHA |
| `atomgit.event.pull_request.head.repo.full_name` | PR 源仓库全名 |
| `atomgit.event.pull_request.base.ref` | PR 目标分支名 |
| `atomgit.event.pull_request.base.repo.full_name` | PR 目标仓库全名 |
| `atomgit.event.pull_request.labels` | PR 标签列表 |
| `atomgit.event.pull_request.merged` | PR 是否已合并 |
| `atomgit.event.pull_request.draft` | PR 是否为 Draft |
| `atomgit.event.action` | PR 事件动作类型 |

### issue_comment 事件

| 字段 | 说明 |
|------|------|
| `atomgit.event.comment.id` | 评论 ID |
| `atomgit.event.comment.body` | 评论内容 |
| `atomgit.event.comment.user.login` | 评论者 |
| `atomgit.event.comment.created_at` | 评论创建时间 |
| `atomgit.event.issue.number` | Issue 编号 |
| `atomgit.event.issue.title` | Issue 标题 |
| `atomgit.event.issue.state` | Issue 状态 |
| `atomgit.event.issue.pull_request` | 是否为 PR 评论（存在则为 PR） |
| `atomgit.event.action` | 动作类型 |

### workflow_dispatch 事件

| 字段 | 说明 |
|------|------|
| `atomgit.event.inputs` | 手动触发输入参数对象 |

### schedule 事件

| 字段 | 说明 |
|------|------|
| `atomgit.event.schedule` | cron 表达式列表 |

## 2.4 其他上下文详细属性

### env 上下文

`env` 上下文包含已在工作流、作业或步骤中设置的变量。它不包含执行环境进程继承的变量。

```json
{
  "first_name": "Mona",
  "super_duper_var": "totally_awesome"
}
```

```yaml
name: Hi Mascot
on: push
env:
  mascot: Mona
  super_duper_var: totally_awesome
jobs:
  windows_job:
    runs-on: windows-latest
    steps:
      - run: echo 'Hi ${{ env.mascot }}'  # Hi Mona
      - run: echo 'Hi ${{ env.mascot }}'  # Hi Octocat
        env:
          mascot: Octocat
  linux_job:
    runs-on: ubuntu-latest
    env:
      mascot: Tux
    steps:
      - run: echo 'Hi ${{ env.mascot }}'  # Hi Tux
```

### vars 上下文

`vars` 上下文包含在组织、仓库和环境级别设置的自定义配置变量。

```json
{ "mascot": "Mona" }
```

```yaml
on:
  workflow_dispatch:
env:
  env_var: ${{ vars.ENV_CONTEXT_VAR }}
jobs:
  display-variables:
    name: ${{ vars.JOB_NAME }}
    if: ${{ vars.USE_VARIABLES == 'true' }}
    runs-on: ${{ vars.RUNNER }}
    environment: ${{ vars.ENVIRONMENT_STAGE }}
    steps:
      - name: Use variables
        run: |
          echo "repository variable : $REPOSITORY_VAR"
          echo "organization variable : $ORGANIZATION_VAR"
          echo "overridden variable : $OVERRIDE_VAR"
          echo "variable from shell environment : $env_var"
        env:
          REPOSITORY_VAR: ${{ vars.REPOSITORY_VAR }}
          ORGANIZATION_VAR: ${{ vars.ORGANIZATION_VAR }}
          OVERRIDE_VAR: ${{ vars.OVERRIDE_VAR }}
```

### job 上下文

```json
{ "status": "success" }
```

| 字段 | 说明 |
|------|------|
| `job.status` | 当前 Job 状态：`success`, `failure`, `cancelled` |
| `job.container` | Object 类型，当 Job 使用自定义构建环境时，查看环境信息 |

### steps 上下文

```json
{
  "checkout": { "outputs": {}, "outcome": "success", "conclusion": "success" },
  "generate_number": { "outputs": { "random_number": "1" }, "outcome": "success", "conclusion": "success" }
}
```

| 属性 | 说明 |
|------|------|
| `steps.<step_id>.outputs` | 步骤输出对象 |
| `steps.<step_id>.outputs.<name>` | 单个输出值 |
| `steps.<step_id>.outcome` | 应用 `continue-on-error` 之前完成的步骤的结果 |
| `steps.<step_id>.conclusion` | 应用 `continue-on-error` 后完成的步骤的结果 |

### runner 上下文

```json
{
  "os": "Linux",
  "arch": "X64",
  "name": "Atomgit Actions 2",
  "tool_cache": "/opt/hostedtoolcache",
  "temp": "/home/runner/work/_temp"
}
```

| 属性 | 说明 |
|------|------|
| `runner.os` | 操作系统：`Linux`, `Windows`, `macOS` |
| `runner.arch` | 架构：`X64`, `ARM`, `ARM64` |
| `runner.name` | Runner 名称 |
| `runner.temp` | Runner 临时目录路径 |
| `runner.tool_cache` | Runner 工具缓存目录路径 |
| `runner.debug` | 是否开启 debug 模式 |

### secrets 上下文

```json
{ "atomgit_token": "***", "NPM_TOKEN": "***", "SUPERSECRET": "***" }
```

| 属性 | 说明 |
|------|------|
| `secrets.<NAME>` | 获取名为 NAME 的加密密钥 |

```yaml
name: Open new issue
on: workflow_dispatch
jobs:
  open-issue:
    runs-on: ubuntu-latest
    permissions:
      repository: read
      issue: write
    steps:
      - run: |
          gh issue --repo ${{ atomgit.repository }} \
            create --title "Issue title" --body "Issue body"
        env:
          GH_TOKEN: ${{ secrets.ATOMGIT_TOKEN }}
```

### matrix 上下文

```json
{ "os": "ubuntu-latest", "node": 16 }
```

访问：`${{ matrix.version }}`, `${{ matrix.os }}`

### inputs 上下文

```json
{ "build_id": "123456768", "deploy_target": "deployment_sys_1a", "perform_deploy": "true" }
```

| 属性 | 说明 |
|------|------|
| `inputs.<name>` | workflow_dispatch 或 workflow_call 中定义的输入参数值 |

## 2.5 上下文可用性表

不同位置可使用的上下文不同：

| 上下文 | workflow 级别 | job 级别 | step 级别 | 条件表达式(if) | Action 中 |
|------|--------------|---------|---------|--------------|---------|
| `atomgit` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `env` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `vars` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `job` | ❌ | ✅ | ✅ | ✅ | ✅ |
| `jobs` | ✅(调用方) | ✅(调用方) | ✅(调用方) | ✅ | ❌ |
| `steps` | ❌ | ✅(步骤后) | ✅(当前步骤后) | ✅ | ✅ |
| `runner` | ❌ | ✅ | ✅ | ✅ | ✅ |
| `secrets` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `strategy` | ❌ | ✅ | ✅ | ✅ | ❌ |
| `matrix` | ❌ | ✅ | ✅ | ✅ | ❌ |
| `inputs` | ✅ | ✅ | ✅ | ✅ | ✅ |
