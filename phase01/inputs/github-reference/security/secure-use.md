<!-- source: https://docs.github.com/en/actions/reference/security/secure-use | fetched: 2026-07-20 -->

# Secure use reference

Security practices for writing workflows and using GitHub Actions features.

Find information about security best practices when you are writing workflows and using GitHub Actions security features.

## Writing workflows

### Use secrets for sensitive information

Since secrets can be transformed in multiple ways, automatic redaction isn't guaranteed. Follow these best practices:

* **Principle of least privilege** — Anyone with write access to your repository can read all secrets configured there. Grant the `GITHUB_TOKEN` only the minimum required permissions. A good security practice is to set the default for repository contents to read-only, then increase per-job as needed.
* **Mask sensitive data** — Never store sensitive data as plaintext in workflow files. Use `::add-mask::VALUE` to mask non-secret sensitive info.
* **Delete and rotate exposed secrets** — Redaction happens on workflow runners. A secret is only redacted if it was used in a job and reachable by the runner. If an unredacted secret appears in logs, delete the log and rotate the secret.
* **Never use structured data as a secret** — Structured data can cause secret redaction within logs to fail, because redaction largely relies on finding an exact match. Don't use JSON, XML, or YAML blobs to encapsulate secrets. Create individual secrets for each sensitive value.
* **Register all secrets used within workflows** — If a secret generates another sensitive value within a workflow, register that generated value as a secret so it gets redacted if it appears in logs. This applies to any transformation or encoding (Base64, URL-encoding, etc.).
* **Audit how secrets are handled** — Review the source code and any actions used in the workflow to ensure secrets aren't sent to unintended hosts or printed to logs. Check workflow logs after testing valid and invalid inputs to verify secrets are properly redacted.
* **Audit and rotate registered secrets** — Periodically review registered secrets to confirm they're still needed; remove unused ones. Rotate secrets regularly.
* **Consider requiring review for access to secrets** — Use required reviewers to protect environment secrets. Jobs can't access environment secrets until a reviewer approves.

### Good practices for mitigating script injection attacks

Recommended approaches for reducing script injection risk:

1. **Use an action instead of an inline script** — Create a JavaScript action that receives the context value as an argument. This avoids injection because the value isn't used to generate a shell script.

   ```yaml
   uses: fakeaction/checktitle@v3
   with:
     title: ${{ github.event.pull_request.title }}
   ```

2. **Use an intermediate environment variable** — For inline scripts, set the expression's value to an intermediate environment variable.

   ```yaml
         - name: Check PR title
           env:
             TITLE: ${{ github.event.pull_request.title }}
           run: |
             if [[ "$TITLE" =~ ^octocat ]]; then
             echo "PR title starts with 'octocat'"
             exit 0
             else
             echo "PR title did not start with 'octocat'"
             exit 1
             fi
   ```

3. **Using workflow templates for code scanning** — Code scanning helps find security vulnerabilities before production. GitHub provides workflow templates for code scanning, including the CodeQL analysis workflow.

4. **Restricting permissions for tokens** — To reduce the risk from an exposed token, restrict its assigned permissions.

## Mitigating the risks of untrusted code checkout

Like script injection attacks, untrusted PR content that automatically triggers actions can pose security risks. The `pull_request_target` and `workflow_run` triggers, when combined with checking out untrusted PRs, expose the repository to compromise because these workflows are privileged — they share the same cache as the main branch, may have write access, and can access secrets. These vulnerabilities can be exploited to take over a repository.

### Good practices

* Avoid using `pull_request_target` unless truly necessary. For privilege separation, `workflow_run` is a better trigger.
* Avoid using `pull_request_target` or `workflow_run` with untrusted PR or code content. Workflows triggered on `workflow_run` should treat artifacts from other workflows with caution.
* CodeQL can scan for potentially vulnerable GitHub Actions workflows.
* OpenSSF Scorecards can identify potentially vulnerable workflows and other security risks.

## Using third-party actions

Individual jobs in a workflow can interact with and compromise other jobs. **A compromised action can access all repository secrets and potentially use the `GITHUB_TOKEN` to write to the repository.**

Mitigate this risk by following these practices:

* **Pin actions to a full-length commit SHA** — This is currently the only way to use an action as an immutable release.
* **Audit the source code of the action** — Verify the action handles your repository content and secrets as expected.
* **Pin actions to a tag only if you trust the creator** — While SHA pinning is most secure, tags are more convenient. The 'Verified creator' badge on GitHub Marketplace indicates identity verification by GitHub. However, a tag can be moved or deleted if a bad actor gains access.

### Reusing third-party workflows

The same principles for third-party actions apply to third-party workflows.

## GitHub's security features

GitHub provides many features to enhance code security:

* **Using `CODEOWNERS` to monitor changes** — Add `.github/workflows` to the code owners list so any proposed changes require approval from a designated reviewer.
* **Using OpenID Connect to access cloud resources** — Configure workflows to authenticate directly to the cloud provider, eliminating stored long-lived credentials.
* **Using Dependabot version updates** — Keep actions and reusable workflow references up to date.
* **Preventing GitHub Actions from creating or approving pull requests** — Can be a security risk if PRs are merged without proper oversight.
* **Using code scanning to secure workflows** — Code scanning can automatically detect and suggest improvements for common vulnerable patterns in GitHub Actions workflows.
* **Using OpenSSF Scorecards** — An automated security tool that flags risky supply chain practices.

## Hardening for self-hosted runners

Self-hosted runners can be persistently compromised by untrusted code in a workflow. Therefore, self-hosted runners should almost **never be used for public repositories**, since any user can open PRs and compromise the environment. Be cautious even on private/internal repos — anyone who can fork and open a PR can compromise the runner environment, including accessing secrets and the `GITHUB_TOKEN`.

### Using just-in-time runners

Use the REST API to create ephemeral, just-in-time (JIT) runners for improved registration security. These runners perform at most one job before being removed.

### Planning your management strategy for self-hosted runners

Self-hosted runners can be added at the enterprise, organization, or repository level. For a centralized team owning runners, add them at the highest mutual organization or enterprise level. If each team manages its own runners, add runners at the highest level of team ownership.

## Auditing GitHub Actions events

Use the security log (for your account) and audit log (for your organization) to monitor activity. These logs record the action type, when it ran, and which personal account performed the action.

For the full list of events per account type, see:
* [Security log events](/en/authentication/keeping-your-account-and-data-secure/security-log-events)
* [Audit log events for your organization](/en/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/audit-log-events-for-your-organization)

## Protecting actions you've created

GitHub enables collaboration between action maintainers and vulnerability reporters to promote secure coding. Repository security advisories allow maintainers of public repos to privately discuss and fix vulnerabilities. After collaborating on a fix, maintainers can publish the advisory to publicly disclose the vulnerability.
