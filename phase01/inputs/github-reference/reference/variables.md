<!-- source: https://docs.github.com/en/actions/reference/workflows-and-actions/variables | fetched: 2026-07-20 -->

# Variables reference

Find information for supported variables, naming conventions, limits, and contexts in GitHub Actions workflows.

## Default environment variables

The default environment variables that GitHub sets are available to every step in a workflow. Because default environment variables are set by GitHub and not defined in a workflow, they are not accessible through the `env` context. However, most of the default variables have a corresponding, and similarly named, context property.

You can't overwrite the value of the default environment variables named `GITHUB_*` and `RUNNER_*`.

We strongly recommend that actions use variables to access the filesystem rather than using hardcoded file paths.

| Variable | Description |
| --- | --- |
| `CI` | Always set to `true`. |
| `GITHUB_ACTION` | The name of the action currently running, or the `id` of a step. |
| `GITHUB_ACTION_PATH` | The path where an action is located. This property is only supported in composite actions. |
| `GITHUB_ACTION_REPOSITORY` | For a step executing an action, this is the owner and repository name of the action. For example, `actions/checkout`. |
| `GITHUB_ACTIONS` | Always set to `true` when GitHub Actions is running the workflow. |
| `GITHUB_ACTOR` | The name of the person or app that initiated the workflow. |
| `GITHUB_ACTOR_ID` | The account ID of the person or app that triggered the initial workflow run. |
| `GITHUB_API_URL` | Returns the API URL. For example: `https://api.github.com`. |
| `GITHUB_BASE_REF` | The name of the base ref or target branch of the pull request in a workflow run. This is only set when the event is `pull_request` or `pull_request_target`. |
| `GITHUB_ENV` | The path on the runner to the file that sets variables from workflow commands. Unique to the current step. |
| `GITHUB_EVENT_NAME` | The name of the event that triggered the workflow. |
| `GITHUB_EVENT_PATH` | The path to the file on the runner that contains the full event webhook payload. |
| `GITHUB_GRAPHQL_URL` | Returns the GraphQL API URL. |
| `GITHUB_HEAD_REF` | The head ref or source branch of the pull request in a workflow run. Only set for `pull_request` or `pull_request_target`. |
| `GITHUB_JOB` | The job_id of the current job. |
| `GITHUB_OUTPUT` | The path on the runner to the file that sets the current step's outputs. Unique to the current step. |
| `GITHUB_PATH` | The path on the runner to the file that sets system `PATH` variables. Unique to the current step. |
| `GITHUB_REF` | The fully-formed ref of the branch or tag that triggered the workflow run. For branches: `refs/heads/<branch_name>`. For pull requests (not merged): `refs/pull/<pr_number>/merge`. For tags: `refs/tags/<tag_name>`. |
| `GITHUB_REF_NAME` | The short ref name of the branch or tag. For pull requests (not merged): `<pr_number>/merge`. |
| `GITHUB_REF_PROTECTED` | `true` if branch protections or rulesets are configured for the ref. |
| `GITHUB_REF_TYPE` | The type of ref that triggered the workflow run. Valid values are `branch` or `tag`. |
| `GITHUB_REPOSITORY` | The owner and repository name. For example, `octocat/Hello-World`. |
| `GITHUB_REPOSITORY_ID` | The ID of the repository. |
| `GITHUB_REPOSITORY_OWNER` | The repository owner's name. |
| `GITHUB_REPOSITORY_OWNER_ID` | The repository owner's account ID. |
| `GITHUB_RETENTION_DAYS` | The number of days that workflow run logs and artifacts are kept. |
| `GITHUB_RUN_ATTEMPT` | A unique number for each attempt of a particular workflow run in a repository. |
| `GITHUB_RUN_ID` | A unique number for each workflow run within a repository. |
| `GITHUB_RUN_NUMBER` | A unique number for each run of a particular workflow in a repository. |
| `GITHUB_SERVER_URL` | The URL of the GitHub server. For example: `https://github.com`. |
| `GITHUB_SHA` | The commit SHA that triggered the workflow. |
| `GITHUB_STEP_SUMMARY` | The path on the runner to the file that contains job summaries from workflow commands. |
| `GITHUB_TRIGGERING_ACTOR` | The username of the user that initiated the workflow run. |
| `GITHUB_WORKFLOW` | The name of the workflow. |
| `GITHUB_WORKFLOW_REF` | The ref path to the workflow. |
| `GITHUB_WORKFLOW_SHA` | The commit SHA for the workflow file. |
| `GITHUB_WORKSPACE` | The default working directory on the runner for steps. |
| `RUNNER_ARCH` | The architecture of the runner executing the job. Possible values: `X86`, `X64`, `ARM`, `ARM64`. |
| `RUNNER_DEBUG` | Set only if debug logging is enabled, always has value `1`. |
| `RUNNER_ENVIRONMENT` | Possible values: `github-hosted` for GitHub-hosted runners, `self-hosted` for self-hosted runners. |
| `RUNNER_NAME` | The name of the runner executing the job. |
| `RUNNER_OS` | The operating system of the runner executing the job. Possible values: `Linux`, `Windows`, `macOS`. |
| `RUNNER_TEMP` | The path to a temporary directory on the runner. This directory is emptied at the beginning and end of each job. |
| `RUNNER_TOOL_CACHE` | The path to the directory containing preinstalled tools for GitHub-hosted runners. |

## Configuration variable precedence

If a variable with the same name exists at multiple levels, the variable at the lowest level takes precedence: environment > repository > organization.

For reusable workflows, the variables from the caller workflow's repository are used. Variables from the repository that contains the called workflow are not made available to the caller workflow.

## Limits for configuration variables

Individual variables are limited to 48 KB in size.

You can store up to 1,000 organization variables, 500 variables per repository, and 100 variables per environment. The total combined size limit for organization and repository variables is 256 KB per workflow run.

## Supported contexts

| Context | Use case | Example |
| --- | --- | --- |
| `env` | Reference custom variables defined in the workflow. | `${{ env.MY_VARIABLE }}` |
| `github` | Reference information about the workflow run and the event that triggered the run. | `${{ github.repository }}` |

> **WARNING:** Do not print the `github` context to logs. It contains sensitive information.

---

> **关键差异提示（compat-diff）**: GitHub 用 `GITHUB_*` 前缀，GitCode 用 `ATOMGIT_*` 前缀。变量表基本一一对应，但需验证 GitCode 侧是否全量支持。GitHub 有 `GITHUB_GRAPHQL_URL`、`RUNNER_DEBUG` 等额外变量。GitHub `RUNNER_ENVIRONMENT` 值为 `github-hosted`，GitCode 为 `gitcode-hosted`。`GITHUB_RUN_ATTEMPT` vs `ATOMGIT_RUN_ATTEMPT` 语义一致但前缀不同。
