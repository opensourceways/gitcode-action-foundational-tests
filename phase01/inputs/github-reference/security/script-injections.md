<!-- source: https://docs.github.com/en/actions/concepts/security/script-injections | fetched: 2026-07-20 -->

# Script injections

Understand the security risks associated with script injections and GitHub Actions workflows.

## Understanding the risk of script injections

When creating workflows, custom actions, and composite actions, you should always consider whether your code might execute untrusted input from attackers. This can occur when an attacker adds malicious commands and scripts to a context. When your workflow runs, those strings might be interpreted as code which is then executed on the runner.

Attackers can add their own malicious content to the `github` context, which should be treated as potentially untrusted input. These contexts typically end with `body`, `default_branch`, `email`, `head_ref`, `label`, `message`, `name`, `page_name`, `ref`, and `title`. For example: `github.event.issue.title`, or `github.event.pull_request.body`.

In addition, there are other less obvious sources of potentially untrusted input, such as branch names and email addresses, which can be quite flexible in terms of their permitted content. For example, `zzz";echo${IFS}"hello";#` would be a valid branch name and would be a possible attack vector for a target repository.

### Example of a script injection attack

```yaml
      - name: Check PR title
        run: |
          title="${{ github.event.pull_request.title }}"
          if [[ $title =~ ^octocat ]]; then
          echo "PR title starts with 'octocat'"
          exit 0
          else
          echo "PR title did not start with 'octocat'"
          exit 1
          fi
```

This example is vulnerable because the `run` command executes within a temporary shell script on the runner. Expressions inside `${{ }}` are evaluated and substituted with the resulting values **before** the shell script runs.

To inject commands, the attacker could create a pull request with a title of `a"; ls $GITHUB_WORKSPACE"`:

```shell
Run title="a"; ls $GITHUB_WORKSPACE""
README.md
code.yml
example.js
```

## Mitigations (from secure-use reference)

1. **Use an action instead of an inline script** — pass the context value as an argument to a JavaScript action, avoiding shell script generation.
2. **Use an intermediate environment variable** — set the expression to an env var first:
   ```yaml
         - name: Check PR title
           env:
             TITLE: ${{ github.event.pull_request.title }}
           run: |
             if [[ "$TITLE" =~ ^octocat ]]; then ...
   ```
3. **Use code scanning** — CodeQL can detect script injection patterns in workflows.
4. **Restrict token permissions** — limit damage from a compromised token.

---

> **安全 agent 对接点**:
> - GitCode 同样有 `atomgit.event.pull_request.title` 等不可信输入——注入面完全一致
> - GitCode 文档未专门讨论脚本注入风险——这是安全 agent 的高优先级 intent
> - 需验证 GitCode 侧 `${{ }}` 表达式求值时机与 GitHub 是否一致（先求值再进 shell）
