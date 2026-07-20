<!-- source: https://docs.github.com/en/actions/reference/workflows-and-actions/contexts | fetched: 2026-07-20 -->
<!-- 注：原文 597KB，此处精简为核心上下文属性定义 + 可用性矩阵，完整事件 payload 字段已在 events.md 中覆盖 -->

# Contexts reference

Find information about contexts available in GitHub Actions workflows.

## Available contexts

| Context name | Type | Description |
| --- | --- | --- |
| `github` | `object` | Information about the workflow run. |
| `env` | `object` | Variables set in a workflow, job, or step. |
| `vars` | `object` | Variables set at repository, organization, or environment levels. |
| `job` | `object` | Information about the currently running job. |
| `jobs` | `object` | For reusable workflows only, outputs of jobs from the reusable workflow. |
| `steps` | `object` | Information about the steps that have been run in the current job. |
| `runner` | `object` | Information about the runner that is running the current job. |
| `secrets` | `object` | Names and values of secrets available to a workflow run. |
| `strategy` | `object` | Information about the matrix execution strategy. |
| `matrix` | `object` | Matrix parameters defined in the workflow. |
| `inputs` | `object` | Inputs passed to an action, reusable workflow, or manually triggered workflow. |

## `github` context (core)

| Property | Type | Description |
| --- | --- | --- |
| `github.action` | `string` | Current action name or step `id`. |
| `github.action_path` | `string` | Path where the action is located. |
| `github.action_ref` | `string` | Step running the action. |
| `github.action_repository` | `string` | Owner and repository of the action (e.g. `actions/checkout`). |
| `github.actor` | `string` | Person or app that initiated the workflow. |
| `github.actor_id` | `string` | Account ID of the initiating person/app. |
| `github.api_url` | `string` | API URL (e.g. `https://api.github.com`). |
| `github.base_ref` | `string` | Base ref or target branch of PR (only `pull_request`/`pull_request_target`). |
| `github.event` | `object` | Full event webhook payload. |
| `github.event_name` | `string` | Event that triggered the workflow (e.g. `push`, `pull_request`). |
| `github.event_path` | `string` | Path to full event payload file on runner. |
| `github.graphql_url` | `string` | GraphQL API URL. |
| `github.head_ref` | `string` | Head ref or source branch of PR (only `pull_request`/`pull_request_target`). |
| `github.job` | `string` | `job_id` of the current job. |
| `github.ref` | `string` | Fully-formed ref of branch/tag. Branch: `refs/heads/<name>`. PR (except `pull_request_target`, not merged): `refs/pull/<number>/merge`. Tag: `refs/tags/<name>`. |
| `github.ref_name` | `string` | Short ref name. PR (not merged): `<number>/merge`. |
| `github.ref_protected` | `boolean` | Whether branch protections/rulesets are configured. |
| `github.ref_type` | `string` | `branch` or `tag`. |
| `github.repository` | `string` | Owner and repository name (e.g. `octocat/Hello-World`). |
| `github.repository_owner` | `string` | Repository owner's name. |
| `github.repositoryUrl` | `string` | Repository URL. |
| `github.run_id` | `string` | Unique ID for each workflow run. |
| `github.run_number` | `number` | Unique number for each run of a workflow. |
| `github.run_attempt` | `number` | Attempt number, starting at 1. |
| `github.server_url` | `string` | GitHub server URL. |
| `github.sha` | `string` | Commit SHA that triggered the workflow. |
| `github.token` | `string` | `GITHUB_TOKEN` for authentication (masked in logs). |
| `github.triggering_actor` | `string` | User who initiated the workflow run. |
| `github.workflow` | `string` | Workflow name. |
| `github.workflow_ref` | `string` | Ref path to workflow (e.g. `owner/repo/.github/workflows/file.yml@ref`). |
| `github.workflow_sha` | `string` | Commit SHA for the workflow file. |
| `github.workspace` | `string` | Default working directory on runner. |

## `runner` context

```json
{
  "os": "Linux", "arch": "X64",
  "name": "GitHub Actions 2",
  "tool_cache": "/opt/hostedtoolcache",
  "temp": "/home/runner/work/_temp"
}
```

## `job` context

```json
{ "status": "success" }
```

| Property | Description |
| --- | --- |
| `job.status` | `success`, `failure`, `cancelled` |
| `job.container` | Container info (when using `jobs.<job_id>.container`) |

## `steps` context

```json
{
  "checkout": {
    "outputs": {},
    "outcome": "success",
    "conclusion": "success"
  }
}
```

| Property | Description |
| --- | --- |
| `steps.<step_id>.outputs` | Step outputs |
| `steps.<step_id>.outcome` | Result BEFORE `continue-on-error` |
| `steps.<step_id>.conclusion` | Result AFTER `continue-on-error` |

## `strategy` context

| Property | Description |
| --- | --- |
| `strategy.fail-fast` | Whether fail-fast is enabled |
| `strategy.job-index` | Index of current job in the matrix (0-based) |
| `strategy.job-total` | Total number of jobs in the matrix |
| `strategy.max-parallel` | Maximum parallel jobs |

## Context availability matrix

| Context | workflow level | job level | step level | `if` condition | Action |
| --- | :---: | :---: | :---: | :---: | :---: |
| `github` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `env` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `vars` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `job` | ❌ | ✅ | ✅ | ✅ | ✅ |
| `jobs` | ✅(caller) | ✅(caller) | ✅(caller) | ✅ | ❌ |
| `steps` | ❌ | ✅(after) | ✅(after) | ✅ | ✅ |
| `runner` | ❌ | ✅ | ✅ | ✅ | ✅ |
| `secrets` | ✅ | ✅ | ✅ | ✅ | ✅ |
| `strategy` | ❌ | ✅ | ✅ | ✅ | ❌ |
| `matrix` | ❌ | ✅ | ✅ | ✅ | ❌ |
| `inputs` | ✅ | ✅ | ✅ | ✅ | ✅ |

---

> **关键差异提示（compat-diff）**:
> - GitHub 上下文对象是 `github.*`；GitCode 是 `atomgit.*`（一一对应但前缀不同）
> - GitHub `github.token` 可直接获取 TOKEN；GitCode 用 `secrets.ATOMGIT_TOKEN` 或 `atomgit.token`
> - GitHub `runner` 三平台（Linux/Windows/macOS）；GitCode 目前是 Linux（ubuntu/euler）
> - GitHub `strategy.job-total`/`strategy.job-index` 需验证 GitCode 是否支持
