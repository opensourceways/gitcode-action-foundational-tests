<!-- source: https://docs.github.com/en/actions/reference/security/securely-using-pull_request_target | fetched: 2026-07-20 -->

# Securely using pull_request_target

Learn about the security risks of the pull_request_target event.

This guide helps you assess whether your workflow should use the `pull_request_target` event and understand the security risks involved. It also explains the protection GitHub applies to `actions/checkout` v7 and later to reduce these risks by default, and when to opt out of that protection if necessary.

## The risks of the pull_request_target event

Workflows triggered by `pull_request_target` run with elevated trust: the job receives the base repository's `GITHUB_TOKEN` and access to repository and organization secrets. This is the same trust given to events like `push` that only collaborators can trigger, and it is what makes `pull_request_target` useful for automation that responds to pull requests from forks, such as labeling, triage, or for posting authenticated status checks.

The `pull_request` event (along with `pull_request_review` and `pull_request_review_comment`) runs the workflow file from the **merge commit of the pull request**. For a pull request opened from a fork, that commit is controlled by someone without write access to the base repository. To run untrusted workflow code safely, GitHub restricts these events to a read-only `GITHUB_TOKEN`, withholds access to other secrets, and applies fork approval policies to prevent compute abuse.

`pull_request_target` makes one critical and subtle change: the workflow, and any subsequent `actions/checkout` call that does not specify a `ref`, is taken from the **base repository's default branch**, not from the pull request. Because only trusted code from the default branch runs, it is safe to grant secrets and a read/write token. No code from the fork is executed by default.

You introduce risk when a workflow author overrides this default to run the fork's code:

```yaml
# INSECURE. Provided as an example only.
on:
  pull_request_target:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
        with:
          ref: ${{ github.event.pull_request.head.sha }}
      - name: Test
        run: make test
```

The checkout step alone does not execute untrusted code. The workflow file itself still comes from the default branch. The vulnerability is completed by the *next* step that runs code checked out into the current working directory. Here, `make test` executes a `Makefile` taken from the pull request head. An attacker only needs to open a pull request from a fork whose `Makefile` contains malicious commands. Those commands then run with the base repository's secrets and token.

This pattern is known as a "pwn request" and has been the root cause of multiple supply-chain compromises. Common vulnerable shapes include:

* Checking out a pull request's head or merge commit in `actions/checkout` (`ref: ${{ github.event.pull_request.head.sha }}`, `ref: refs/pull/${{ github.event.pull_request.number }}/merge`) and then building, testing, or otherwise executing the result.
* Setting `repository:` to the fork (`repository: ${{ github.event.pull_request.head.repo.full_name }}`) to pull the fork's branch directly.
* Fetching the pull request code outside of `actions/checkout` (e.g. with `git fetch`, `gh pr checkout`, or by downloading an artifact from a fork's `pull_request` run) and then running it.

Pwn requests are also not unique to `pull_request_target`. Any event that runs with secrets can introduce a pwn request if it checks out or downloads and executes untrusted code.

## Deciding whether to use pull_request_target

Consider the questions below before using `pull_request_target` or opting into the `allow-unsafe-pr-checkout` flag in `actions/checkout`.

* **Can you use `pull_request` instead?** `pull_request` triggers on the same events as `pull_request_target` and runs the workflow code from the `pull_request` merge branch. It does this safely on pull requests from forks. If additional secret access is not needed, use `pull_request`.

* **Is the checked-out code ever executed?** This is the flaw that introduces pwn request vulnerabilities. It is most commonly introduced with `actions/checkout` by checking out a pull request head into the working directory and then running it. Execution is not limited to your own steps: build and test commands such as `npm install` and `npm run build`, as well as configuration files and dependencies the code brings with it, can all run attacker-controlled code. **You must ensure the checked-out code is only ever inspected as data and never executed before using a `pull_request_target` event.**

## Hardening a pull_request_target workflow

If you have confirmed you need `pull_request_target`, apply these controls:

* **Restrict secrets.** Confirm that the permissions set on the `GITHUB_TOKEN` have the least privileges and that only the necessary repository and organization secrets are used for the workflow.
* **Understand the impact to caching.** To reduce the risk of cache poisoning, workflows triggered by `pull_request_target` have read-only access to the cache in the default branch's scope. These workflows can restore existing cache entries but cannot create or overwrite them.
* **Ensure the underlying compute is isolated and ephemeral.** If self-hosted runners are used, confirm that the runner environment is properly restricted from internal resources and is not reused across GitHub Actions runs.
* **Enforce GitHub Actions security best practices.** Other common vulnerabilities, such as command injection, can exist and impact the code executed in this privileged event.

## Opting out of built-in protections

If you have worked through the questions above and confirmed your workflow requires `pull_request_target` and uses it safely, you can opt out of the `actions/checkout` protection by setting `allow-unsafe-pr-checkout: true`.

## Restricting the use of pull_request_target

If a repository has no legitimate use for `pull_request_target`, restricting the event removes the risk regardless of how individual workflows are written. Administrators can use workflow execution protections to control which events and actors can trigger workflows.

---

> **关键差异提示（compat-diff / security agent）**: GitHub 的 `pull_request_target` 语义与 GitCode 文档声称的一致——但 GitCode 侧隔离强度需实测确认（secret 访问限制、token 降级、cache 读写限制）。GitHub `actions/checkout` v7+ 有 `allow-unsafe-pr-checkout` 内置保护；GitCode 的 `checkout` 实现是否有等价保护待验证。pwn request 模式通用——GitCode 同样需要在文档中明确标注此风险。
