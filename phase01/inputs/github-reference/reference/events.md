<!-- source: https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows | fetched: 2026-07-20 -->

# Events that trigger workflows

You can configure your workflows to run when specific activity on GitHub happens, at a scheduled time, or when an event outside of GitHub occurs.

## Key events (compat-diff relevant)

### `pull_request`

| | |
|---|---|
| Activity types | `assigned`, `unassigned`, `labeled`, `unlabeled`, **`opened`**, `edited`, `closed`, **`reopened`**, **`synchronize`**, `converted_to_draft`, `locked`, `unlocked`, `enqueued`, `dequeued`, `milestoned`, `demilestoned`, `ready_for_review`, `review_requested`, `review_request_removed`, `auto_merge_enabled`, `auto_merge_disabled` |
| **Default types** | `opened`, `synchronize`, `reopened` |
| `GITHUB_SHA` | Last merge commit on the `GITHUB_REF` branch |
| `GITHUB_REF` | PR merge branch `refs/pull/<PR_NUMBER>/merge` |

- Runs the workflow file from the **merge commit** of the pull request.
- Fork PR: `GITHUB_TOKEN` read-only, secrets not passed except `GITHUB_TOKEN`.
- Workflows will NOT run on `pull_request` activity if the pull request has a merge conflict.
- `branches` filter matches **target** branch names (base branch).

### `pull_request_target`

| | |
|---|---|
| Activity types | Same as `pull_request` |
| **Default types** | `opened`, `synchronize`, `reopened` |
| `GITHUB_SHA` | Last commit on **default branch** |
| `GITHUB_REF` | **Default branch** |

- Runs in the context of the **default branch** of the base repository, NOT the merge commit.
- Workflow uses the workflow file from the **default branch** — cannot be modified by PR submitter.
- `GITHUB_TOKEN` is granted **read/write** repository permission, even when triggered from a public fork.
- **Avoid** if you need to build or run code from the pull request.
- **Runs even if the pull request has a merge conflict** (unlike `pull_request`).

### `push`

| | |
|---|---|
| `GITHUB_SHA` | Tip commit pushed to the ref (when deleting a branch, reverts to default branch SHA) |
| `GITHUB_REF` | Updated ref |

- Supports `branches`, `branches-ignore`, `tags`, `tags-ignore`, `paths`, `paths-ignore` filters.
- Events NOT created if >5,000 branches pushed at once, or >3 tags pushed at once.

### `schedule`

| | |
|---|---|
| `GITHUB_SHA` | Last commit on default branch |
| `GITHUB_REF` | Default branch |

- Runs on **default branch only**. Shortest interval: **5 minutes**.
- GitHub: supports `timezone` field; GitCode: UTC only.
- GitHub: public repo scheduled workflows auto-disabled after 60 days of no activity.

### `workflow_dispatch`

| | |
|---|---|
| `GITHUB_SHA` | Last commit on the `GITHUB_REF` branch or tag |
| `GITHUB_REF` | Branch or tag that received dispatch |

- Input types: `boolean`, `choice`, `number`, `environment`, `string`.
- Max 25 top-level inputs; payload max 65,535 chars.
- Triggered workflow file must be on the default branch.

### `workflow_call`

Same payload as the caller workflow. Used for reusable workflows.

### `issue_comment`

| | |
|---|---|
| Activity types | `created`, `edited`, `deleted` |

- Occurs for comments on **both issues and pull requests**.
- Use `github.event.issue.pull_request` to distinguish PR vs issue.

### `workflow_run`

| | |
|---|---|
| Activity types | `completed`, `requested`, `in_progress` |
| `GITHUB_SHA` | Last commit on default branch |

- Can access **secrets and write tokens**, even if the triggering workflow was not.
- Cannot chain more than **3 levels** of workflows.

### Other events (full list)

`branch_protection_rule`, `check_run`, `check_suite`, `create`, `delete`, `deployment`, `deployment_status`, `discussion`, `discussion_comment`, `fork`, `gollum`, `image_version`, `issues`, `label`, `merge_group`, `milestone`, `page_build`, `public`, `pull_request_review`, `pull_request_review_comment`, `registry_package`, `release`, `repository_dispatch`, `status`, `watch`.

---

> **关键差异提示（compat-diff）**:
> - `pull_request` types 命名: GitHub `opened/synchronize/reopened` vs GitCode `open/update/reopen`（命名+取值双重差异）
> - GitCode 有 `merge` activity type；GitHub 用 `closed` + `github.event.pull_request.merged` 判断
> - GitHub `pull_request_target` 下 GITHUB_TOKEN 是 **read/write**；GitCode 文档声称 fork PR `pull_request` 仅 read、`pull_request_target` 可访问 Secret——需实测确认隔离强度
> - GitCode 有 `pull_request_comment` 事件（带 comments 正则过滤）；GitHub 靠 `issue_comment` + `github.event.issue.pull_request` 判断
> - GitHub `schedule` 支持 `timezone`；GitCode 仅 UTC
> - GitHub `workflow_dispatch` inputs 支持 5 种类型；GitCode 仅 `string`
> - GitHub `workflow_run` 最多 3 层嵌套；GitCode 文档未提及此限制
