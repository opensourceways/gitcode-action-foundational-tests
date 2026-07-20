<!-- source: https://docs.github.com/en/actions/concepts/security/secrets + reference/secrets | fetched: 2026-07-20 -->

# Secrets

Learn about secrets as they are used in GitHub Actions workflows.

## About secrets

Secrets let you store sensitive information across your organization, repositories, or repository environments. GitHub Actions can only read a secret if you explicitly include the secret in a workflow.

Secrets rely on Libsodium sealed boxes for encryption before reaching GitHub. This encryption happens at submission time — either using the UI or through the REST API.

## Organization-level / repository-level / environment-level secrets

- **Organization-level**: Share across multiple repositories. Can set access policy (all repos, private only, specific list).
- **Repository-level**: Scoped to a single repository.
- **Environment-level**: Can enable required reviewers — jobs cannot access environment secrets until approval is granted.

## Naming rules

- Can only contain alphanumeric characters (`[a-z]`, `[A-Z]`, `[0-9]`) or underscores (`_`).
- Must not start with `GITHUB_` prefix.
- Must not start with a number.
- Case insensitive when referenced. GitHub stores secret names as uppercase.

## Precedence

If a secret with the same name exists at multiple levels: environment > repository > organization.

## Limits

- Individual secrets: 48 KB
- Organization: up to 1,000 secrets
- Repository: up to 100 secrets
- Environment: up to 100 secrets
- Workflow can access: all 100 repository secrets + first 100 organization secrets (alphabetical) + all 100 environment secrets

## Automatically redacted secrets

GitHub automatically redacts the contents of all GitHub secrets that are printed to workflow logs. It also redacts recognized sensitive information not stored as a secret (e.g. Azure keys, DB connection strings, HTTP Bearer tokens, JWTs, NPM tokens, NuGet keys).

> **Important**: Because there are multiple ways a secret value can be transformed, this redaction is **not guaranteed**. The runner can only redact secrets used within the current job.

## Limiting credential permissions

- Grant the minimum permissions possible. Consider read-only if that's all that's needed.
- Consider using a GitHub App instead of a PAT (fine-grained permissions, short-lived tokens, not tied to a user).

## Security best practices (from secure-use reference)

1. Never store sensitive data as plaintext in workflow files.
2. Use `::add-mask::VALUE` to mask non-secret sensitive info.
3. Never use structured data (JSON, XML, YAML) as a secret — redaction depends on exact match.
4. If a secret generates another sensitive value, register that new value as a secret.
5. Rotate secrets regularly and remove unused ones.
6. Check workflow logs after testing to verify secrets are properly redacted.
7. Fork PR: `pull_request` from fork **cannot access** repository secrets (only `GITHUB_TOKEN` is passed, read-only).

---

> **安全 agent 对接点**:
> - GitCode 文档声称 secret 日志脱敏 `***`，但自承 `echo "${{ secrets.X }}"` 可能绕过——直接的 negative 断言
> - GitCode secret 命名规则与 GitHub 一致（大写/下划线，不以 ATOMGIT_ 开头）
> - 需验证 GitCode 的 secret 存储加密方案是否等价于 Libsodium sealed box
> - 需验证 fork PR 下 secret 隔离：`pull_request`（不可访问）vs `pull_request_target`（可访问）
