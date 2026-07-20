<!-- source: https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax | fetched: 2026-07-20 -->
<!-- 注：本文件为 80.8KB 完整抓取。关键对齐字段：name, run-name, on, permissions, env, defaults, concurrency, jobs, jobs.<id>.steps, jobs.<id>.strategy 等全部留有原始定义 -->

# Workflow syntax for GitHub Actions

A workflow is a configurable automated process made up of one or more jobs. You must create a YAML file to define your workflow configuration.

Workflow files use YAML syntax, and must have either a `.yml` or `.yaml` file extension. You must store workflow files in the **`.github/workflows`** directory of your repository.

## `name`

The name of the workflow. GitHub displays the names under your repository's "Actions" tab. If you omit `name`, GitHub displays the workflow file path relative to the root of the repository.

## `run-name`

The name for workflow runs generated from the workflow. Can include expressions referencing the `github` and `inputs` contexts.

```yaml
run-name: Deploy to ${{ inputs.deploy_target }} by @${{ github.actor }}
```

## `on` (trigger)

Defines which events can cause the workflow to run. Supports single event, multiple events, activity types, and filters (branches, tags, paths).

### `on.<event_name>.types`
Narrows down activity that causes the workflow to run.
```yaml
on:
  label:
    types: [created, edited]
```

### `on.<push|pull_request|pull_request_target>.<branches|branches-ignore>`
Filter branches using glob patterns. Cannot use both `branches` and `branches-ignore` for the same event.

### `on.<push|pull_request|pull_request_target>.<paths|paths-ignore>`
Filter based on changed file paths. Cannot use both `paths` and `paths-ignore` for the same event.

**Git diff comparisons:**
- Pull requests: three-dot diffs
- Pushes to existing branches: two-dot diffs
- If a push contains >1,000 commits, the workflow will **always** run
- If diff contains >3,000 files and matched files are not in first 3,000, workflow will **not** run

### `on.schedule`
POSIX cron syntax, default UTC. Supports `timezone` (IANA). Shortest interval: 5 minutes.
```yaml
on:
  schedule:
    - cron: '30 5 * * 1-5'
      timezone: "America/New_York"
```

### `on.workflow_call`
Define inputs (`boolean`, `number`, `string`), outputs, and secrets for reusable workflows.

### `on.workflow_dispatch`
Manual trigger. Input types: `boolean`, `choice`, `number`, `environment`, `string`.
Max 25 top-level properties, max 65,535 characters payload.

## `permissions`

Modify default permissions granted to `GITHUB_TOKEN`. Can be set at workflow level (all jobs) or job level.

**Available permissions** (access: `read`, `write`, `none`):

| Permission | Purpose |
|---|---|
| `actions` | Work with GitHub Actions |
| `artifact-metadata` | Work with artifact metadata |
| `attestations` | Work with artifact attestations |
| `checks` | Work with check runs and check suites |
| `code-quality` | Work with code quality |
| `contents` | Work with repository contents |
| `deployments` | Work with deployments |
| `discussions` | Work with GitHub Discussions |
| `id-token` | Fetch an OIDC token (requires `write`) |
| `issues` | Work with issues |
| `models` | Generate AI inference responses |
| `packages` | Work with GitHub Packages |
| `pages` | Work with GitHub Pages |
| `pull-requests` | Work with pull requests |
| `security-events` | Work with code scanning alerts |
| `statuses` | Work with commit statuses |
| `vulnerability-alerts` | Read Dependabot alerts (`read`/`none` only) |

Shortcuts: `read-all`, `write-all`, `{}` (disable all).

**Fork PR**: `GITHUB_TOKEN` is read-only (unless "Send write tokens" is selected). For `pull_request_target`, `GITHUB_TOKEN` is granted read/write repository permission even from public forks.

## `env`

Map of variables available to the steps of all jobs. Step env > Job env > Workflow env.

## `defaults`

Default `shell` and `working-directory` for all `run` steps.
```yaml
defaults:
  run:
    shell: bash
    working-directory: ./scripts
```

Supported shells: unspecified (bash -e), `bash`, `pwsh`, `python`, `sh`, `cmd` (Windows), `powershell`.

## `concurrency`

Ensure only a single job or workflow using the same concurrency group runs at a time.

```yaml
concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true
```

`queue` property: `single` (default) or `max` (up to 100 pending). `queue: max` + `cancel-in-progress: true` is invalid.

## `jobs` / `jobs.<job_id>`

Each job runs in a runner environment specified by `runs-on`.

### `jobs.<job_id>.name`
Display name for the job.

### `jobs.<job_id>.permissions`
Job-level permissions override workflow-level.

### `jobs.<job_id>.needs`
Dependencies on other jobs.

### `jobs.<job_id>.runs-on`
Runner type. GitHub-hosted: `ubuntu-latest`, `windows-latest`, `macos-latest` or specific version labels. Self-hosted: `self-hosted` + custom labels.

### `jobs.<job_id>.if`
Conditional execution using expressions.

### `jobs.<job_id>.steps`
Array of steps within a job.

### `jobs.<job_id>.steps[*].uses`
Action reference: `owner/repo@ref` or `./path/to/action`.

### `jobs.<job_id>.steps[*].run`
Shell command(s).

### `jobs.<job_id>.steps[*].shell`
Overrides default shell. See `defaults.run.shell` table.

### `jobs.<job_id>.steps[*].working-directory`
Overrides default working directory.

### `jobs.<job_id>.steps[*].env`
Step-level environment variables.

### `jobs.<job_id>.steps[*].if`
Step-level conditional.

### `jobs.<job_id>.steps[*].continue-on-error`
Step does not fail the job.

### `jobs.<job_id>.steps[*].timeout-minutes`
Step timeout.

### `jobs.<job_id>.timeout-minutes`
Job timeout (default 360, i.e. 6 hours for GitHub-hosted).

### `jobs.<job_id>.strategy`
Matrix strategy: `matrix`, `fail-fast`, `max-parallel`.

### `jobs.<job_id>.continue-on-error`
Prevents workflow run from failing.

### `jobs.<job_id>.container`
Run job inside a Docker container.

### `jobs.<job_id>.outputs`
Map of outputs for the job.

### `jobs.<job_id>.env`
Job-level environment variables.

### `jobs.<job_id>.environment`
Deployment environment.

### `jobs.<job_id>.concurrency`
Job-level concurrency.

## Filter pattern cheat sheet

| Pattern | Description |
|---|---|
| `*` | Matches zero or more characters, but not `/` |
| `**` | Matches zero or more of any character |
| `?` | Matches exactly one any character except `/` |
| `+` | Matches one or more of the preceding character |
| `[]` | Matches one character in the set |
| `!` | Negation (exclude) |

---

> **关键差异提示（compat-diff）**:
> - 目录: `.github/workflows/` vs `.gitcode/workflows/`
> - `on.<event>.types` 取值命名不同：GitHub `opened/synchronize/reopened` vs GitCode `open/update/reopen`
> - `workflow_dispatch.inputs` 类型: GitHub 支持 `boolean/choice/number/environment/string`；GitCode 仅 `string`
> - `permissions` 权限域：GitHub `contents/pull-requests/issues/actions...` vs GitCode `repository/pr/issue/project/note/hook`
> - `concurrency`: GitHub 用 `group`+`cancel-in-progress`+`queue`；GitCode 用 `enable/max/exceed-action/preemption`
> - `runs-on`: GitHub `ubuntu-latest` 等单标签 vs GitCode 三段式 `{os,arch,flavor}`
> - GitHub 有 `run-name` 字段；GitCode 文档未提及
> - GitHub `strategy.max-parallel`；GitCode 文档用 `strategy.max-parallel` 但需验证语义一致性
> - **paths diff 限制差异**：GitHub 有 1,000 commits / 3,000 files 阈值；GitCode 有 300 files 上限
