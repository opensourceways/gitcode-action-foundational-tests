<!-- source: https://docs.github.com/en/actions/concepts/security/github_token | fetched: 2026-07-20 -->

# GITHUB_TOKEN

Learn what GITHUB_TOKEN is, how it works, and why it matters for secure automation.

## About the `GITHUB_TOKEN`

At the start of every workflow job, GitHub automatically generates a unique `GITHUB_TOKEN` secret for use in that workflow. This token can be used for authentication within the job.

When GitHub Actions is enabled, a GitHub App gets installed on the repository. The `GITHUB_TOKEN` secret is essentially a GitHub App installation access token. The token's permissions are scoped only to the repository containing the workflow.

Before each job starts, GitHub fetches a fresh installation access token. The `GITHUB_TOKEN` expires when the job finishes or after its effective maximum lifetime.

**Effective maximum lifetime by runner type:**

| Runner type | Max job time | Token lifetime |
|---|---|---|
| GitHub-hosted | 6 hours | ≤ 6 hours |
| Self-hosted | 5 days | ≤ 24 hours (installation token refresh limit) |

For jobs running longer than 24 hours, use a personal access token or another authentication method.

The token is also accessible through the `github.token` context.

## When `GITHUB_TOKEN` triggers workflow runs

Events triggered by `GITHUB_TOKEN` will generally **not** create a new workflow run, preventing accidental recursive runs. Exceptions:

- `workflow_dispatch` and `repository_dispatch` always create workflow runs.
- `pull_request` events (`opened`, `synchronize`, `reopened`): run in **approval-required** state when created by a `GITHUB_TOKEN` workflow. A user with write access must approve them.

Commits pushed by a workflow using `GITHUB_TOKEN` do not trigger a GitHub Pages build.

> **Note**: If you need workflow runs from workflow-created PRs to execute without requiring approval, use a GitHub App installation access token or a personal access token instead of `GITHUB_TOKEN`.

---

> **安全 agent 对接点**:
> - GitCode 对应物是 `ATOMGIT_TOKEN`，声明为「自动生成」
> - 需验证：GitCode 的 token 过期时间、权限继承规则、recursive run 防护是否与 GitHub 一致
> - 关键安全验证：`pull_request` fork 场景下 `ATOMGIT_TOKEN` 是否确实降为只读
