# Spec-Analyst Output: Completeness Dimension

> Agent: spec-analyst | Run: 2026-07-20-01 | Dimensions: completeness
> Coverage domain: `testing-focus.md` §1 (语法解析), §2 (触发器), §3 (执行模型), §7 (复用/供应链), §8 (Artifact/Cache), §9 (可观测性)

---

## Part A: Structured Capability Catalog

Capacity items extracted from `inputs/gitcode-spec/` (50 pages, fetched 2026-07-20), organized by `testing-focus.md` focus areas.

### A.1 Workflow Syntax Parsing (§1)

| # | Capability | Semantics | Constraints / Boundaries | Default | Configurable? | Source | Confidence |
|---|---|---|---|---|---|---|---|
| 1 | YAML file discovery | `.gitcode/workflows/*.yml` / `*.yaml` recognized; other extensions ignored | Only `.yml` / `.yaml` | N/A | No | writing-pipelines/workflow-file-location-structure.md | Clear |
| 2 | `name` field | Workflow display name; falls back to filename | Optional | filename | — | writing-pipelines/workflow-file-location-structure.md | Clear |
| 3 | `on` field | Trigger conditions (required) | Required | N/A | — | writing-pipelines/workflow-file-location-structure.md | Clear |
| 4 | `env` (workflow level) | Workflow-level env vars | — | — | Yes (job/step override) | writing-pipelines/using-variables-secrets.md | Clear |
| 5 | `defaults.run.shell` | Default shell for all `run:` steps | `bash`, `sh`, `pwsh`, `python` | Unknown | Yes | writing-pipelines/configure-steps.md | Fuzzy — default shell not explicitly stated |
| 6 | `defaults.run.working-directory` | Default working directory | Relative to repo root | Unknown | Yes | writing-pipelines/configure-steps.md | Clear |
| 7 | `permissions` | ATOMGIT_TOKEN scope control; 6 domains | `read`/`write`/`none` per domain | "仓库设置中定义的权限" | Yes (per job) | security-permissions/token-permissions.md | Fuzzy — default permissions when undeclared not documented |
| 8 | `permissions: {}` | Minimal permissions: all `none` | — | N/A | — | security-permissions/token-permissions.md | Clear |
| 9 | `read-all` / `write-all` shortcuts | All domains to read/write | — | N/A | — | security-permissions/token-permissions.md | Clear |
| 10 | `concurrency` (workflow level) | Parallel run limit; max 1-5; QUEUE/IGNORE | `max`: 1-5; `exceed-action`: IGNORE/QUEUE | `enable: true`, `max: ?`, `exceed-action: ?` | Yes (workflow & job level) | writing-pipelines/workflow-file-location-structure.md | Fuzzy — default max/exceed-action not stated |
| 11 | `concurrency.preemption` | Preempt running runs by event | `enable` default true; `events` max 10 | `preemption.enable: true` | Yes | writing-pipelines/workflow-file-location-structure.md | Fuzzy — preemption event semantics unclear |
| 12 | `stages` top-level | Stage serialization; stage-level `fail_fast` | Stage order = execution order | Optional (omit = single stage) | — | writing-pipelines/configure-dependencies-order.md | Clear |
| 13 | `post` top-level | Post-processing stage; `run_always` | Default `run_always: true` | `run_always: true` | Yes | writing-pipelines/workflow-file-location-structure.md | Clear |
| 14 | Unknown field handling | Undocumented | Unknown — silently ignore vs. error | N/A | — | 未知 (no spec page addresses this) | Unknown |

### A.2 Trigger Semantics (§2)

| # | Capability | Semantics | Constraints / Boundaries | Default | Configurable? | Source | Confidence |
|---|---|---|---|---|---|---|---|
| 15 | `push` | Branch/tag push trigger | Supports `branches`, `branches-ignore`, `tags`, `tags-ignore`, `paths`, `paths-ignore` | N/A | Yes (filters) | syntax-reference/trigger-events.md §1.1 | Clear |
| 16 | `pull_request` | PR open/reopen/update/merge trigger | `types`: `[open, reopen, update, merge]`; filter by `branches` (target), `paths` | `types` default: `[open, reopen, update]` | Yes | syntax-reference/trigger-events.md §1.2 | Clear |
| 17 | `pull_request_target` | PR trigger in base context with secrets | Same `types` as `pull_request`; base-branch workflow used | `types` default: `[open, reopen, update]` | Yes | syntax-reference/trigger-events.md §1.3 | Clear |
| 18 | `issue_comment` | Issue/PR comment trigger | `types`: `[created, edited, deleted]` | Unknown | Yes | syntax-reference/trigger-events.md §1.4 | Fuzzy — default types not stated |
| 19 | `pull_request_comment` | PR-only comment trigger with regex filter | `comments` regex filter; `branches` filter | Unknown | Yes | syntax-reference/trigger-events.md §1.5 | Clear |
| 20 | `workflow_dispatch` | Manual trigger with string inputs | `inputs` only `type: string` | N/A | Yes | syntax-reference/trigger-events.md §1.6 | Clear |
| 21 | `workflow_call` | Reusable workflow invocation | Max 2-layer nesting; `inputs` (string only) + `secrets` pass-through | N/A | Yes | syntax-reference/trigger-events.md §1.8 | Clear |
| 22 | `schedule` | Cron trigger; UTC only; default branch only | Min interval 5 min; POSIX cron 5-field | N/A | Yes | syntax-reference/trigger-events.md §1.9 | Clear |
| 23 | `branches` / `branches-ignore` filter | Wildcard pattern (`**`, `*`); `!` negation | Cannot use both simultaneously | N/A | — | writing-pipelines/configure-triggers.md | Clear |
| 24 | `paths` / `paths-ignore` filter | File-change filter; `!` negation; glob (`**/*.js`) | **Match only first 300 changed files**; cannot use both simultaneously | N/A | — | writing-pipelines/configure-triggers.md | Clear — 300-file bound is explicit |
| 25 | `tags` / `tags-ignore` filter | Tag name pattern filter; `!` negation | Cannot use both simultaneously | N/A | — | writing-pipelines/configure-triggers.md | Clear |
| 26 | Multi-event on | Single workflow responds to multiple events | All events in `on:` block compose additively | N/A | — | writing-pipelines/configure-triggers.md | Clear |
| 27 | `!` negation (trigger filters) | Exclude pattern; must combine with positive patterns | Pure negation (only `!`) results in no trigger | N/A | — | writing-pipelines/configure-triggers.md | Clear |
| 28 | `pull_request` fork safety | Fork PR: ATOMGIT_TOKEN read-only, no secrets access | Hard constraint — cannot override | — | No | security-permissions/pr-mr-pipeline-security.md | Clear |
| 29 | `pull_request_target` fork safety | Fork PR: base workflow, full permissions, secrets available | Risk: checkout `head.sha` runs untrusted code with privileges | — | No | security-permissions/pr-mr-pipeline-security.md | Clear |

### A.3 Execution Model (§3)

| # | Capability | Semantics | Constraints / Boundaries | Default | Configurable? | Source | Confidence |
|---|---|---|---|---|---|---|---|
| 30 | `needs` job dependency | DAG dependency; downstream waits for upstream completion | Dependency failure → downstream skipped (unless `always`) | No `needs` → parallel execution | Yes | writing-pipelines/configure-dependencies-order.md | Clear |
| 31 | `stages` serial execution | Stage 1 completes → Stage 2 starts | Stage-level `fail_fast` controls intra/inter-stage failure propagation | Optional | Yes | writing-pipelines/configure-dependencies-order.md | Clear |
| 32 | `stages.fail_fast` | `true` = kill sibling jobs + skip subsequent stages; `false` = siblings continue, subsequent skipped | `false` still blocks subsequent stages | Unknown | Yes | core-concepts/workflow-job-step-action.md | Fuzzy — `fail_fast: false` exact behavior |
| 33 | `strategy.matrix` | Cartesian product job expansion | Up to 3 dimensions documented; `include`/`exclude` | N/A | Yes | writing-pipelines/configure-matrix-builds.md | Clear |
| 34 | `strategy.fail-fast` | Matrix-level fast failure; kills remaining matrix jobs | Distinct from `stages.fail_fast` | Unknown | Yes | writing-pipelines/configure-matrix-builds.md | Clear |
| 35 | `strategy.max-parallel` | Cap concurrent matrix jobs | Upper bound not documented | "取决于Runner可用数量" | Yes | writing-pipelines/configure-matrix-builds.md | Fuzzy |
| 36 | `if` (job level) | Conditional job execution | Supports expressions + status functions | Default `success` | Yes | writing-pipelines/configure-conditional-execution.md | Clear |
| 37 | `if` (step level) | Conditional step execution | Supports expressions + status functions | Default `success` | Yes | writing-pipelines/configure-steps.md | Clear |
| 38 | Status functions: `success`/`always`/`cancelled`/`failed` | No parentheses (GitCode syntax); judge prior step status | `success` = all prior success; `failed` = any prior failure; `cancelled` = workflow cancelled; `always` = any state | — | Yes (in `if`) | syntax-reference/expressions.md | Clear |
| 39 | `continue-on-error` (job) | Job failure does not block subsequent jobs | Subsequent `success` condition fails; use `always` | `false` | Yes | writing-pipelines/configure-jobs.md | Clear |
| 40 | `continue-on-error` (step) | Step failure does not fail job | Subsequent steps continue | `false` | Yes | writing-pipelines/configure-steps.md | Clear |
| 41 | `timeout-minutes` (job) | Job timeout; forced termination | Default 360 min (6 hours) | 360 | Yes | writing-pipelines/configure-jobs.md | Clear |
| 42 | `timeout-minutes` (step) | Step timeout | No independent default; bounded by job timeout | None | Yes | writing-pipelines/configure-steps.md | Clear |
| 43 | Step `outputs` via `ATOMGIT_OUTPUT` | Key=value → `$ATOMGIT_OUTPUT`; multi-line with heredoc delimiter | Max 1 MB per parameter | N/A | — | writing-pipelines/pass-output-between-jobs.md | Clear |
| 44 | Job `outputs` mapping | `jobs.<id>.outputs.<key>` from step outputs | Referenced via `needs.<id>.outputs.<key>` | N/A | Yes | writing-pipelines/pass-output-between-jobs.md | Clear |
| 45 | Workflow `outputs` (workflow_call) | `on.workflow_call.outputs` mapped from job outputs | — | N/A | Yes | writing-pipelines/pass-output-between-jobs.md | Clear |
| 46 | `runs-on` official runner tags | 3-segment: `{os-version},{arch},{flavor}` or `default` | Default = `[ubuntu-latest, x64, small]` | `default` | Yes | runner-management/using-hosted-runners.md | Clear |
| 47 | `runs-on` self-hosted | `type: self-hosted` + `group` + `labels` | Full-match on labels | N/A | Yes | writing-pipelines/configure-jobs.md | Clear |
| 48 | `runs-on` dynamic (matrix) | `${{ matrix.os }},${{ matrix.arch }},small` in `runs-on` | — | N/A | Yes | writing-pipelines/configure-matrix-builds.md | Clear |
| 49 | `container` for custom Docker image | `container.image` + optional `credentials` | **文档自承: 能力无法使用** (existing case TC-273) | N/A | — | runner-management/using-hosted-runners.md | Fuzzy — documented but verified non-functional |
| 50 | Cancel semantics | Manual cancel → running step terminated | Post-stage cleanup hooks uncertain | — | — | 未知 (no dedicated cancel spec page) | Unknown |

### A.4 Reuse & Supply Chain (§7)

| # | Capability | Semantics | Constraints / Boundaries | Default | Configurable? | Source | Confidence |
|---|---|---|---|---|---|---|---|
| 51 | Official action (short name) | `uses: checkout` — no owner prefix | Built-in: `checkout`, `setup-node`, `setup-java`, `setup-go`, `setup-python`, `cache`, `upload-artifact`, `download-artifact` | N/A | — | writing-pipelines/using-actions.md | Clear |
| 52 | Third-party action (full path) | `uses: owner/repo/path@ref` | `@ref` = tag, branch, or commit SHA | N/A | Yes | writing-pipelines/using-actions.md | Clear |
| 53 | Local action (relative path) | `uses: ./.gitcode/actions/<name>` | Requires `action.yml` in path | N/A | Yes | writing-pipelines/using-actions.md | Clear |
| 54 | Action ref pinning | `@v4` (tag), `@v4.1.0` (exact), `@main` (branch), `@sha` (commit) | SHA recommended for production | N/A | Yes | writing-pipelines/using-actions.md | Clear |
| 55 | Action runtime | `runs.using: node16` | Only `node16` documented (no node20/docker/composite) | N/A | — | COMPAT-NOTES.md §10 | Fuzzy |
| 56 | Reusable workflow invocation | `uses: ./.gitcode/workflows/<name>.yml` with `with:` and `secrets:` | Max 2-layer nesting | N/A | Yes | syntax-reference/trigger-events.md §1.8 | Clear |
| 57 | `with` parameter passing | Key-value to action inputs | Matches `action.yml` `inputs` definition | N/A | Yes | writing-pipelines/configure-steps.md | Clear |

### A.5 Artifact / Cache (§8)

| # | Capability | Semantics | Constraints / Boundaries | Default | Configurable? | Source | Confidence |
|---|---|---|---|---|---|---|---|
| 58 | Artifact upload | `uses: upload-artifact` with `name` + `path` (glob); multi-path | Name must be unique within workflow | N/A | Yes | writing-pipelines/upload-download-artifacts.md | Clear |
| 59 | Artifact download | `uses: download-artifact` with `name` + optional `path` | Omit `name` to download all artifacts | `path` = current directory | Yes | writing-pipelines/upload-download-artifacts.md | Clear |
| 60 | Artifact retention | "可设定保留天数" | Default retention, max retention, size limit — **not documented** | Unknown | Unknown | core-concepts/artifacts-and-cache.md | Unknown |
| 61 | Cache save/restore | `uses: cache` with `key` + `path` + optional `restore-keys` | Exact key → prefix fallback on `restore-keys` | N/A | Yes | writing-pipelines/using-dependency-cache.md | Clear |
| 62 | Cache key matching | Exact match → `restore-keys` ordered prefix match → miss | LRU eviction mentioned | N/A | — | writing-pipelines/using-dependency-cache.md | Fuzzy — eviction policy details not specified |
| 63 | Cache scope | "同仓库的所有运行" | Fork PR cache isolation not documented | N/A | — | core-concepts/artifacts-and-cache.md | Unknown |
| 64 | `hashFiles()` | SHA256 of matched file set; for cache key generation | Behavior with no matching files **not documented** | N/A | — | syntax-reference/expressions.md | Fuzzy |

### A.6 Observability (§9)

| # | Capability | Semantics | Constraints / Boundaries | Default | Configurable? | Source | Confidence |
|---|---|---|---|---|---|---|---|
| 65 | Run state machine | queued → in_progress → completed (success/failure/cancelled/skipped) | — | N/A | — | running-pipelines/view-run-results.md | Clear |
| 66 | Run detail page | Stage sidebar + Job cards + Step timeline + Post section | Staged by `stages` definition order | N/A | — | running-pipelines/view-run-results.md | Clear |
| 67 | Job log display | Timestamp-prefixed; per-step grouping; fold/collapse long output | Search by keyword; download as UTF-8 text | N/A | — | running-pipelines/view-job-logs.md | Clear |
| 68 | Secret masking in logs | `***` substitution for secrets | `echo "${{ secrets.X }}"` may **bypass** masking per doc warning | — | — | security-permissions/using-secrets.md | Clear — doc admits bypass risk |
| 69 | `::add-mask::` command | Runtime secret masking | Still supported | — | — | writing-pipelines/using-script-commands.md | Clear |
| 70 | Workflow commands: `ATOMGIT_OUTPUT` | Step output via file append | Multi-line via heredoc delimiter | N/A | — | syntax-reference/workflow-commands.md §5.1 | Clear |
| 71 | Workflow commands: `ATOMGIT_ENV` | Env var for subsequent steps | Multi-line via heredoc delimiter | N/A | — | syntax-reference/workflow-commands.md §5.2 | Clear |
| 72 | Workflow commands: `ATOMGIT_PATH` | PATH append for subsequent steps | — | N/A | — | syntax-reference/workflow-commands.md §5.3 | Clear |
| 73 | Workflow commands: `ATOMGIT_STEP_SUMMARY` | Markdown write to run summary page | — | N/A | — | syntax-reference/workflow-commands.md §5.4 | Clear |
| 74 | Re-run: all jobs | New run, all jobs re-executed, run number incremented | Max 3 retries; timeout > 6h cannot re-run; uses original commit's config | — | — | running-pipelines/rerun-failed-jobs.md | Clear |
| 75 | Re-run: failed jobs only | Only failed (+ cascade-skipped) jobs re-executed; successful cached | Same constraints as re-run all | — | — | running-pipelines/rerun-failed-jobs.md | Clear |
| 76 | Status badge | `![Build Status](https://atomgit.com/{owner}/{repo}/badges/{workflow}/pipeline.svg)` | — | N/A | — | running-pipelines/view-run-results.md | Clear |
| 77 | Commit status | Status icon on Commits page → links to run details | — | — | — | running-pipelines/view-run-results.md | Clear |
| 78 | PR Checks tab | All pipeline run results for a PR aggregated | — | — | — | running-pipelines/view-run-results.md | Clear |

### A.7 Variable System (§3 auxiliary)

| # | Capability | Semantics | Constraints / Boundaries | Default | Configurable? | Source | Confidence |
|---|---|---|---|---|---|---|---|
| 79 | `env` (3-level scope) | Workflow → Job → Step; higher scope overrides lower | Workflow env accessible by `$VAR` and `${{ env.VAR }}` | — | Yes | writing-pipelines/using-variables-secrets.md | Clear |
| 80 | `vars` | Org/project config variables | GUI-created; `ATOMGIT_` prefix disallowed | — | Yes (GUI) | writing-pipelines/using-variables-secrets.md | Clear |
| 81 | `secrets` | Encrypted secrets; log masking `***` | Fork PR: inaccessible (`pull_request` only) | — | Yes (GUI) | security-permissions/using-secrets.md | Clear |
| 82 | `inputs` | `workflow_dispatch`/`workflow_call` parameters | **Only `type: string`** | — | Yes | writing-pipelines/using-variables-secrets.md | Clear |
| 83 | System variables `ATOMGIT_*` | 27 documented system env vars | `ATOMGIT_TOKEN` scoped to run lifetime | — | No | syntax-reference/variables.md | Clear |
| 84 | Variable priority | Step env > Job env > Workflow env > vars > ATOMGIT_* | — | — | — | writing-pipelines/using-variables-secrets.md | Clear |
| 85 | `ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS` | Enable/disable deprecated commands | **Default value not documented** (existing case TC-220 found missing) | Unknown | Unknown | syntax-reference/variables.md | Fuzzy |
| 86 | `ATOMGIT_REPOSITORY_OWNER` | Repository owner | **Existing case TC-206 found not injected** | — | — | syntax-reference/variables.md | Fuzzy — documented but observed absent |

### A.8 Expressions (§1 auxiliary)

| # | Capability | Semantics | Constraints / Boundaries | Default | Configurable? | Source | Confidence |
|---|---|---|---|---|---|---|---|
| 87 | `contains(search, item)` | Substring match for strings; membership for arrays | Case-sensitive | — | — | syntax-reference/expressions.md | Clear |
| 88 | `startsWith` / `endsWith` | Prefix/suffix match | Case-sensitive | — | — | syntax-reference/expressions.md | Clear |
| 89 | `format(template, args...)` | `{0}`, `{1}` placeholders | — | — | — | syntax-reference/expressions.md | Clear |
| 90 | `substring(str, start, len)` | **GitCode-specific** (not in GitHub) | Index semantics unclear | — | — | syntax-reference/expressions.md | Fuzzy — start index: 0-based or 1-based? |
| 91 | `replace(str, old, new)` | **GitCode-specific** (not in GitHub) | — | — | — | syntax-reference/expressions.md | Clear |
| 92 | `hashFiles(paths...)` | SHA256 of matched file set | No-match behavior unknown | — | — | syntax-reference/expressions.md | Fuzzy |
| 93 | `toJson(value)` | Serialize to JSON string | What contexts are serializable unknown | — | — | syntax-reference/expressions.md | Fuzzy |
| 94 | Null/undefined handling | Expression evaluation on missing context | **Not documented** | — | — | 未知 | Unknown |

---

## Part B: Spec Gaps & Ambiguities

Items marked `Unknown` or `Fuzzy` from above, cross-referenced with impacted dimensions.

| # | Gap | Impacted Dimensions | Detail |
|---|---|---|---|---|
| G01 | **Default `permissions` when undeclared** | completeness, security | Doc says "使用仓库设置中定义的权限" — what IS that default? What domains + levels? |
| G02 | **Default `defaults.run.shell`** | completeness, compatibility | Not explicitly stated — bash? sh? System-dependent? |
| G03 | **`concurrency` defaults** | completeness, reliability | Default `max` and `exceed-action` not stated; preemption `events` semantics unclear |
| G04 | **`hashFiles()` with no matching files** | completeness | Empty hash? Error? Skip? Impacts cache key generation correctness |
| G05 | **`toJson()` serialization scope** | completeness | Which contexts produce valid JSON? `atomgit.event`? `matrix`? Documented but semantics thin |
| G06 | **Expression null/undefined handling** | completeness, compatibility | What happens when `${{ inputs.OPTIONAL }}` is not provided? Empty string? Null? Error? |
| G07 | **Cancel semantics for `post` stage** | completeness, reliability | Does `post` with `run_always: true` fire on cancel? What about `run_always: false`? |
| G08 | **Artifact retention — default, max, size limit** | completeness, reliability | "可设定保留天数" but no numbers; size quota not documented |
| G09 | **Cache eviction details** | completeness | LRU mentioned but max cache size, per-repo quota, eviction trigger not specified |
| G10 | **Fork PR cache isolation** | security, completeness | Can fork PR write cache that poisons main-branch cache? Docs silent |
| G11 | **`runs-on` matching for official runner tags** | completeness | "Full match" semantics translated from self-hosted but not separately described for official pool |
| G12 | **`stages.fail_fast` + `strategy.fail-fast` interaction** | completeness, reliability | Two `fail_fast` levels — what is the precedence/interaction when both are set? |
| G13 | **`substring()` index semantics** | completeness, compatibility | 0-based or 1-based? Not documented; critical for expression portability |
| G14 | **`container.image` capability gap** | completeness | Doc says supported but existing cases show it's non-functional (TC-273) |
| G15 | **`environment` field syntax** | completeness, usability | Doc mentions environment-level secrets but YAML binding syntax not documented (TC-010) |
| G16 | **`schedule` minimum interval enforcement** | completeness, reliability | Doc says 5 min min-interval — what happens with `*/2 * * * *`? Rejected or coerced? |
| G17 | **Action runtime beyond `node16`** | completeness, compatibility | Only `node16` documented; `node20`, `docker`, `composite` unclear |
| G18 | **`paths` 300-file partial match behavior** | completeness | If PR changes 400 files and a matching pattern hits file #1-#200, what happens to #301-#400? Are they invisible to ALL `paths` rules or just the rule that hit the cap? |
| G19 | **Multi-workflow same-trigger execution order** | completeness, reliability | Multiple `.gitcode/workflows/*.yml` with same trigger — order? Parallel? Any guarantee? |
| G20 | **`pull_request_comment` with `comments` regex + no match** | completeness | If `comments` filter yields no match, does the workflow still create a run (skipped) or no run at all? |
| G21 | **`needs` on matrix job** | completeness | Existing case TC-486/481/499 shows `needs` pointing to matrix parent job causes "任务初始化错误" — is this bug or by-design? |

---

## Part C: Missing Inputs Notice

- **`inputs/workflow-samples/`** is MISSING. Intents involving real-world YAML parsing edge cases (indentation variants, anchor/alias, multi-doc, empty file) would benefit from real samples.
- **`inputs/platform-config/`** is MISSING. Boundary-value intents that need known runner capacity limits (max concurrent runs, queue depth, artifact size quotas, cache eviction thresholds) lack platform-specific data to set precise bounds.

---

## Part D: Completeness Test Intents

> Intent format per `phase01/templates/intent.md`. Dimensions = `[completeness]`.
> Priority clues from `phase01/baseline/risk-register.md`: RISK-COMPAT-01 (P1, 默认值差异), RISK-REL-01 (P1, 并发洪泛).
> These intents verify that spec-claimed capabilities are **actually present and behaving as documented** — the core of completeness testing.

---

```
意图 ID:    INTENT-COMP-001
维度标签:   [completeness]
标题:       验证 8 种触发事件类型的实际可用性

风险点:     规格声明支持 push / pull_request / pull_request_target / issue_comment /
            pull_request_comment / workflow_dispatch / workflow_call / schedule 共 8 种事件。
            若任一事件类型未实现或行为与文档不一致，则「事件驱动」核心卖点塌方；
            现有用例中 pull_request_target 的 open 事件、schedule 整体已报告不工作（TC-461/463, S3×24+TC-391）。

预期系统行为: 每种事件类型按文档声明的语义触发 workflow 运行——
            push: 分支推送触发；pull_request: PR open/reopen/update 触发；
            pull_request_target: base 上下文触发；issue_comment: 评论创建触发；
            pull_request_comment: PR 评论（含 comments 正则过滤）触发；
            workflow_dispatch: 手动触发（含 inputs 参数注入）；
            workflow_call: 被其他 workflow 通过 uses 调用触发；
            schedule: cron 定时触发（UTC 时区，默认分支，最小 5 分钟间隔）。

Oracle 来源: GitCode规格（triggers 语法参考 §1.1-§1.9）+ 现有用例问题清单

验证要点:
  - [正向] 每种事件类型成功创建 workflow 运行记录
  - [正向] pull_request_target 使用目标分支 workflow 文件版本执行
  - [正向] workflow_dispatch 的 inputs 值正确注入 ${{ inputs.NAME }}
  - [正向] workflow_call 被调用方通过 with/secrets 传参正确接收
  - [正向] schedule 按 cron 表达式在 UTC 时区触发
  - [负向] pull_request 的 fork PR 不应读到项目 secrets

优先级线索: RISK-COMPAT-01（事件集差异高发区）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/syntax-reference/trigger-events.md;
            参照现有用例问题: TC-461/463 (pull_request_target 不触发), S3×24+TC-391 (schedule 不工作)
```

```
意图 ID:    INTENT-COMP-002
维度标签:   [completeness]
标题:       验证 trigger 过滤器: branches/paths/tags 的通配、否定与互斥规则

风险点:     文档声称 branches/branches-ignore 互斥、paths/paths-ignore 互斥、
            否定模式 `!` 必须与肯定模式组合、paths 只匹配前 300 个变更文件。
            这些规则的边界实现错误会导致 workflow 漏触发或误触发——
            漏触发 = CI 静默跳过，误触发 = 资源浪费。
            现有用例 TC-236 报告 paths 规则未触发独立 job。

预期系统行为: 
            - branches 与 branches-ignore 同时使用 → 报错
            - paths 与 paths-ignore 同时使用 → 报错
            - `branches: ['!main']` 仅否定模式 → 不触发任何 workflow
            - `branches: ['feature/**', '!feature/experimental']` → 仅 feature 分支触发，
              experimental 排除
            - `paths: ['src/**']` → 仅 src/ 下有变更时触发
            - `paths: ['!src/docs/**']` 仅否定 → 不触发
            - PR 变更 301 个文件时，第 301 个文件不参与 paths 匹配判断

Oracle 来源: GitCode规格（configure-triggers §branches / paths 过滤 + syntax-ref §1.1）

验证要点:
  - [正向] branches 与 branches-ignore 互斥时报错（不应静默选一）
  - [正向] paths 与 paths-ignore 互斥时报错
  - [正向] 仅否定模式的 branches/paths/tags → 不触发（或明确报错）
  - [正向] `**` 通配递归匹配多级目录
  - [正向] `*` 通配仅匹配单级
  - [非功能] 超过 300 个变更文件时，paths 匹配行为可预测

优先级线索: RISK-COMPAT-01（过滤语义差异高发区）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/writing-pipelines/configure-triggers.md;
            inputs/gitcode-spec/syntax-reference/trigger-events.md §1.1;
            参照现有用例 TC-236 (paths 不触发)
```

```
意图 ID:    INTENT-COMP-003
维度标签:   [completeness]
标题:       验证 job DAG: needs 依赖拓扑的正确执行与失败传播

风险点:     needs 是 workflow 编排的核心原语。依赖 job 失败时下游默认不执行；
            多依赖汇聚时必须所有上游成功才触发下游；
            `if: ${{ always }}` 应能覆盖失败传播默认行为。
            若 DAG 拓扑执行错误（如依赖未完成即启动下游、失败仍传播），
            则 pipeline 的确定性坍塌。

预期系统行为:
            - `needs: [A]` → B 在 A 成功后执行
            - `needs: [A, B]` → C 在 A 和 B 都成功后执行
            - A 失败 → 依赖 A 的 job 默认不执行（skipped）
            - 下游 job 配置 `if: ${{ always }}` → 即使上游失败也执行
            - 无 needs 的 job 并行启动

Oracle 来源: GitCode规格（configure-dependencies-order §needs + configure-conditional-execution）

验证要点:
  - [正向] 线性依赖 A→B→C 按序执行
  - [正向] 汇聚依赖 A,B→C 的 C 在两个上游均成功后执行
  - [正向] 上游 A 失败 → 下游 B 状态为 skipped
  - [正向] `if: ${{ always }}` 覆盖失败传播，下游仍执行
  - [正向] 无 needs 的 job 在 workflow 启动时并行调度
  - [非功能] DAG 拓扑深度 ≥ 5 层时执行正确（无截断）

优先级线索: RISK-COMPAT-01（执行模型差异）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/writing-pipelines/configure-dependencies-order.md;
            inputs/gitcode-spec/writing-pipelines/configure-conditional-execution.md；
            参照现有用例 TC-486/481/499 (needs 指向矩阵父 job 致"任务初始化错误")
```

```
意图 ID:    INTENT-COMP-004
维度标签:   [completeness]
标题:       验证矩阵构建: include/exclude/fail-fast/max-parallel 语义

风险点:     strategy.matrix 是 workflow 横向扩展的核心机制。
            include 未定义的变量会被注入到对应 job 实例；
            exclude 减少组合数；
            fail-fast 与 stages.fail_fast 是两个不同层面的控制；
            max-parallel 限制并行度。
            若矩阵展开错误（include 变量未注入、exclude 未生效、fail-fast 作用域错），
            测试/构建覆盖率出现盲区。

预期系统行为:
            - 2D matrix [os: A,B] × [ver: 1,2] → 4 个 job 实例
            - include 追加的额外变量（如 experimental）在对应实例的 ${{ matrix.experimental }} 可用
            - exclude 排除的组合不生成 job 实例
            - fail-fast: true → 第一个失败后取消剩余矩阵 job
            - fail-fast: false → 一个失败不影响其他
            - max-parallel: N → 同时运行不超过 N 个矩阵 job
            - runs-on 可引用 ${{ matrix.os }} 动态选择 runner

Oracle 来源: GitCode规格（configure-matrix-builds）

验证要点:
  - [正向] 1D/2D/3D 矩阵生成的 job 实例数量 = 笛卡尔积值 × exclude 调整
  - [正向] include 注入的额外变量在 job 中通过 ${{ matrix.var }} 可读
  - [正向] exclude 排除了指定组合 → 对应实例不存在
  - [正向] fail-fast: true 时第一个失败后其他 job 被取消
  - [正向] fail-fast: false 时失败不波及其他
  - [正向] max-parallel 限制生效，同时运行数不超过配置值

优先级线索: RISK-REL-01（大规模矩阵下稳定性）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/writing-pipelines/configure-matrix-builds.md
```

```
意图 ID:    INTENT-COMP-005
维度标签:   [completeness]
标题:       验证并发控制: concurrency max / exceed-action / preemption

风险点:     concurrency 是防资源耗尽的第一道防线。max 范围 1-5；
            exceed-action: IGNORE(忽略新请求) / QUEUE(排队)；
            preemption 可抢占运行中的旧 run。
            若 IGNORE 变成静默丢任务、QUEUE 无限排队饿死、preemption 误杀，
            则并发控制不仅无效反而制造新问题。

预期系统行为:
            - max: 3 且 exceed-action: QUEUE → 第 4 个触发排队，前序完成后依次调度
            - max: 1 且 exceed-action: IGNORE → 有运行中时新触发被忽略（不创建排队 run）
            - preemption.enable: true + events: [push] → 新 push 到达时抢占旧 run
            - job 级 concurrency 覆盖 workflow 级

Oracle 来源: GitCode规格（workflow-file-location-structure §concurrency + configure-jobs §concurrency）

验证要点:
  - [正向] max 限制生效：同时运行的 workflow 实例数不超过 max
  - [正向] QUEUE 策略：超额触发排队并按 FIFO 顺序执行
  - [正向] IGNORE 策略：超额触发不创建新运行
  - [正向] preemption 抢占：新事件到达时旧运行被取消
  - [正向] job 级 concurrency 优先级高于 workflow 级

优先级线索: RISK-REL-01（并发洪泛下排队/公平性）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/writing-pipelines/workflow-file-location-structure.md;
            inputs/gitcode-spec/writing-pipelines/configure-jobs.md
```

```
意图 ID:    INTENT-COMP-006
维度标签:   [completeness]
标题:       验证 artifact 跨 job 上传/下载及保留策略

风险点:     artifact 是 job 间传递构建产物的唯一内置机制。
            upload 后 download 应拿到完全一致的字节；
            同名 artifact 在同一 workflow 内应唯一；
            若 artifact 丢失、损坏、提前过期，则后续 job 无条件失败。
            文档未声明 artifact 大小上限和默认保留天数——这些都是边界。

预期系统行为:
            - upload-artifact(name=A, path=dist/) → 上传 dist/ 下的所有文件
            - download-artifact(name=A) → 恢复到指定路径，文件内容与上传一致
            - 同一 workflow 中同名 artifact 重复上传 → 报错或覆盖
            - 不指定 name 时 download-artifact 下载当前 workflow 全部 artifact
            - artifact 在 workflow 运行结束后保留不超过声明天数

Oracle 来源: GitCode规格（upload-download-artifacts + core-concepts/artifacts-and-cache）

验证要点:
  - [正向] 上传 → 下载 → 文件内容逐字节一致
  - [正向] 目录结构与 glob 模式上传正确
  - [正向] 多路径上传（dist/ + reports/ + coverage/）全部包含
  - [正向] 同名 artifact 同一 workflow → 应有明确行为（报错或覆盖）
  - [负向] download-artifact 引用不存在的 name → 应报错并停止 job
  - [非功能] artifact 保留期后可确认不再可下载

优先级线索: RISK-COMPAT-01（artifact 行为差异）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/writing-pipelines/upload-download-artifacts.md;
            inputs/gitcode-spec/core-concepts/artifacts-and-cache.md
```

```
意图 ID:    INTENT-COMP-007
维度标签:   [completeness]
标题:       验证缓存: cache key 精确/前缀匹配与跨 run 持久性

风险点:     缓存机制直接影响 CI 速度。key 精确匹配 → 直接恢复；
            restore-keys 前缀匹配 → 取最近一次前缀匹配缓存；
            全部 miss → 保存新缓存。
            若缓存 key 哈希计算错误、prefix 匹配逻辑偏差、
            或 fork PR 可污染主分支缓存，则 CI 变慢或出错。

预期系统行为:
            - key 精确命中 → 直接恢复缓存（不执行 cache step 的 post-run save）
            - 精确未命中 → 按 restore-keys 顺序前缀匹配 → 恢复最近匹配
            - 全部未命中 → 执行后保存 path 内容为新缓存
            - 缓存跨 workflow run 持久（同仓库）
            - hashFiles 有文件匹配时返回确定性的 SHA256 值

Oracle 来源: GitCode规格（using-dependency-cache）

验证要点:
  - [正向] cache key 不变时第二次运行命中缓存（run 更快或日志显示 cache hit）
  - [正向] restore-keys 前缀匹配恢复最近缓存
  - [正向] cache miss → path 内容被保存 → 下次命中
  - [正向] hashFiles 返回值在两份相同内容的文件间一致
  - [负向] 不应出现跨仓库的缓存泄露

优先级线索: RISK-COMPAT-01（缓存隔离差异）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/writing-pipelines/using-dependency-cache.md;
            inputs/gitcode-spec/core-concepts/artifacts-and-cache.md
```

```
意图 ID:    INTENT-COMP-008
维度标签:   [completeness]
标题:       验证 outputs 三级传递链: step → job → workflow

风险点:     outputs 是 job 间传递结构化数据的唯一通道。
            step 通过 $ATOMGIT_OUTPUT 写入 key=value；
            job 通过 outputs 映射暴露；
            下游 job 通过 needs.<id>.outputs.<key> 读取；
            workflow_call 场景下可进一步暴露为 workflow 级 outputs。
            三级映射链上任一环节断裂（如 job outputs 声明了但未映射 step outputs），
            下游拿不到数据但可能不报错，造成静默错误。

预期系统行为:
            - step: `echo "version=1.0.0" >> $ATOMGIT_OUTPUT` → `steps.<id>.outputs.version` 为 "1.0.0"
            - job: `outputs: { result: ${{ steps.build.outputs.result }} }` → `needs.<job>.outputs.result` 可读
            - workflow_call: `on.workflow_call.outputs` 映射到 job outputs → 调用方可读
            - 每个 output 参数 ≤ 1MB
            - 多行 output 通过 heredoc 分隔符正确传递

Oracle 来源: GitCode规格（pass-output-between-jobs + syntax-reference/workflow-commands §5.1）

验证要点:
  - [正向] step output → 同 job 后续 step 通过 steps 上下文可读
  - [正向] step output → job outputs 映射 → 下游 job 通过 needs 可读
  - [正向] workflow_call outputs → 调用方 workflow 可读
  - [正向] 多行值（含换行）通过分隔符语法正确传递
  - [负向] 引用不存在的 needs.<id>.outputs.<key> 应明确报错（不静默为空）

优先级线索: RISK-COMPAT-01（outputs 传递语义差异）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/writing-pipelines/pass-output-between-jobs.md;
            inputs/gitcode-spec/syntax-reference/workflow-commands.md §5.1
```

```
意图 ID:    INTENT-COMP-009
维度标签:   [completeness]
标题:       验证 stages 阶段机制: 串行推进、fail_fast 与 job 并行

风险点:     stages 是 GitCode Action 独有的编排机制（GitHub 无等价概念）。
            阶段间串行执行、阶段内 job 默认并行、fail_fast 控制失败传播。
            若 stage 推进逻辑错误（如提前进入下一 stage、fail_fast=false 仍阻止后续），
            则 pipeline 的执行顺序不可预测。

预期系统行为:
            - Stage 1 的所有 job 完成后 Stage 2 才开始
            - 同一 Stage 内无 needs 的 job 并行执行
            - fail_fast: true → 任一 job 失败：杀死同 stage 剩余 job + 跳过所有后续 stage
            - fail_fast: false → 失败 job 的同 stage 其他 job 继续；后续 stage 跳过
            - 同一 stage 内的 job 可通过 needs 额外约束执行顺序

Oracle 来源: GitCode规格（configure-dependencies-order §stages + core-concepts/workflow-job-step-action §Stages）

验证要点:
  - [正向] 3 个 stage 按定义顺序串行执行（Stage 1 完成 → Stage 2 → Stage 3）
  - [正向] 同一 Stage 内 3 个无 needs job 并行启动
  - [正向] fail_fast: true + 某 job 失败 → 同 stage 其他 job 终止
  - [正向] fail_fast: true + 某 job 失败 → 后续 stage 全部 skipped
  - [正向] fail_fast: false + 某 job 失败 → 同 stage 其他 job 继续执行
  - [正向] 同一 stage 内 job 通过 needs 串行化

优先级线索: RISK-COMPAT-01（stages 为 GitCode 特有机制）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/writing-pipelines/configure-dependencies-order.md;
            inputs/gitcode-spec/core-concepts/workflow-job-step-action.md
```

```
意图 ID:    INTENT-COMP-010
维度标签:   [completeness]
标题:       验证 post 后处理阶段: run_always 与时序保证

风险点:     post 是 GitCode 特有的后处理机制。文档声称默认 run_always: true，
            即无论 workflow 成功/失败都执行；设为 false 则仅成功时执行。
            若 post 阶段在 workflow 取消时不执行、在 run_always: false 时错误执行、
            或 post 中的 steps 顺序/环境变量与主流程不一致，
            则通知/清理/回写等关键收尾逻辑不可靠。

预期系统行为:
            - run_always: true（默认）→ 无论主流程成功/失败/cancelled，post 都执行
            - run_always: false → 仅主流程成功时执行 post
            - post 在主流程所有 stage 完成后执行
            - post 中的 steps 串行执行

Oracle 来源: GitCode规格（workflow-file-location-structure §post + core-concepts/workflow-job-step-action §Post）

验证要点:
  - [正向] 主流程成功 + run_always: true → post 执行
  - [正向] 主流程失败 + run_always: true → post 仍执行
  - [正向] 主流程成功 + run_always: false → post 执行
  - [正向] 主流程失败 + run_always: false → post 不执行
  - [非功能] 主流程被取消 + run_always: true 时 post 的行为可观测

优先级线索: RISK-COMPAT-01（post 为 GitCode 特有）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/writing-pipelines/workflow-file-location-structure.md;
            inputs/gitcode-spec/core-concepts/workflow-job-step-action.md
```

```
意图 ID:    INTENT-COMP-011
维度标签:   [completeness]
标题:       验证环境变量四级优先级链: step > job > workflow > vars > ATOMGIT_*

风险点:     文档声明的优先级链涉及 5 级作用域。若实现偏差——
            如 step env 未覆盖 job env、vars 与 ATOMGIT_* 重叠时未正确解析——
            则 workflow 中使用错误的环境变量值导致行为偏差，且难以排查。
            现有用例 TC-533 报告 Job env 未注入到 Shell（表达式层正常但 Bash 层 UNSET）。

预期系统行为:
            - step 级 env 覆盖同名的 job 级和 workflow 级 env
            - job 级 env 覆盖同名的 workflow 级 env
            - 表达式 `${{ env.VAR }}` 和 Bash `$VAR` 均可读取 env 变量
            - vars 在 env 未定义时生效
            - 系统 ATOMGIT_* 变量最低优先级
            - 项目级 vars 覆盖同名组织级 vars

Oracle 来源: GitCode规格（using-variables-secrets §优先级规则总览 + syntax-reference/variables §4.2）

验证要点:
  - [正向] step env 覆盖 job env（同名变量取 step 值）
  - [正向] job env 覆盖 workflow env
  - [正向] `${{ env.VAR }}` 和 `$VAR` 读取到相同值
  - [正向] 项目级 vars 覆盖同名组织级 vars
  - [正向] env > vars 优先级成立（同名时 env 优先）

优先级线索: RISK-COMPAT-01（默认值/优先级差异）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/writing-pipelines/using-variables-secrets.md;
            inputs/gitcode-spec/syntax-reference/variables.md；
            参照现有用例 TC-533 (job env 未注入 Shell)
```

```
意图 ID:    INTENT-COMP-012
维度标签:   [completeness]
标题:       验证表达式状态函数不带括号的语法: success/always/failed/cancelled

风险点:     GitCode 状态函数不带括号（`${{ success }}`），与 GitHub（`${{ success() }}`）
            语法不同。若解析器在 `if:` 中错误处理这些裸标识符
            （如要求括号、或混淆为字符串），则条件执行逻辑全线崩溃。
            现有用例 TC-317-321 报告条件执行函数问题。

预期系统行为:
            - `if: ${{ success }}` → 所有前置步骤成功时执行
            - `if: ${{ always }}` → 无条件执行
            - `if: ${{ failed }}` → 有前置步骤失败时执行
            - `if: ${{ cancelled }}` → workflow 被取消时执行
            - `if: success`（不带 `${{ }}`） → 文档未声明是否支持，应验证

Oracle 来源: GitCode规格（syntax-reference/expressions §3.3）

验证要点:
  - [正向] `${{ success }}`（不带括号）作为 `if` 条件正确求值
  - [正向] `${{ always }}` 无条件触发步骤执行
  - [正向] `${{ failed }}` 在前置步骤失败时正确触发
  - [正向] `${{ cancelled }}` 在 workflow 取消时正确触发
  - [负向] 不应接受 `${{ success() }}`（GitHub 语法）——要么报错，要么语义与 success 一致

优先级线索: RISK-COMPAT-01（表达式语法差异, 状态函数不带括号为 GitCode 特有）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/syntax-reference/expressions.md；
            COMPAT-NOTES.md §3；
            参照现有用例 TC-317-321 (条件执行函数问题)
```

```
意图 ID:    INTENT-COMP-013
维度标签:   [completeness]
标题:       验证表达式函数的边界行为: contains/startsWith/endsWith/format/hashFiles/toJson

风险点:     表达式函数是与 workflow YAML 逻辑正确性的基础。
            空字符串、null、含特殊字符的输入如何被每个函数处理——
            文档只给了 happy path 示例，边界行为完全未知。
            这些是兼容性差异高发点（与 GitHub 同名函数行为是否一致）。

预期系统行为:
            - `contains('hello world', '')` → 应返回 true（空串是任何串的子串）还是 false？需验证
            - `startsWith('', 'prefix')` → false
            - `format('{0}{1}', 'a')` 缺参数 → 明确的报错或空位
            - `hashFiles('nonexistent/**')` 无匹配文件 → 明确的返回值或报错
            - `toJson(atomgit.event)` → 合法 JSON 字符串
            - `toJson(null)` → 报错还是 `"null"`？需验证

Oracle 来源: GitCode规格（syntax-reference/expressions §3.3）

验证要点:
  - [正向] contains 对空串、单字符、多字节 UTF-8 参数的正确行为
  - [正向] startsWith/endsWith 对空串的边界行为
  - [正向] format 缺参数/多参数/非字符串参数的行为
  - [正向] hashFiles 无匹配文件时的返回值（不应为崩溃/空哈希）
  - [正向] toJson 对复杂对象、null、数组的序列化行为
  - [负向] 语法错误的表达式不应导致 workflow 静默跳过

优先级线索: RISK-COMPAT-01（表达式函数差异, contains/startsWith 边界行为待比对）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/syntax-reference/expressions.md；
            COMPAT-NOTES.md §3
```

```
意图 ID:    INTENT-COMP-014
维度标签:   [completeness]
标题:       验证上下文对象 atomgit.* 的所有文档属性实际可用

风险点:     文档列出了 atomgit 上下文的 20 个属性（atomgit.event_name 到 atomgit.api_url）。
            若任一属性返回 null/空/错误类型（而非文档声明的类型），依赖该属性的条件判断
            或变量赋值会静默出错。现有用例 TC-038 报告 atomgit.repository_owner 不可用；
            TC-206 报告 ATOMGIT_REPOSITORY_OWNER 系统变量未注入。

预期系统行为:
            - 每个 atomgit.* 属性返回文档声明的类型和值
            - atomgit.event 为完整的 event payload 对象
            - PR 事件中 atomgit.head_ref / base_ref 有值
            - push 事件中 atomgit.head_ref / base_ref 为空
            - atomgit.run_attempt 首次运行 = 1，重运行后递增

Oracle 来源: GitCode规格（syntax-reference/context §2.2）

验证要点:
  - [正向] 20 个 atomgit.* 属性在相应的触发事件下返回非空值
  - [正向] atomgit.event.pull_request.* 字段在 PR 事件下完整
  - [正向] atomgit.event_name 在每种触发事件下返回正确的字符串值
  - [正向] atomgit.run_id 在每次运行中唯一
  - [正向] atomgit.run_number 跨运行递增
  - [负向] 不应出现文档声明存在但实际返回 null/undefined 的属性

优先级线索: RISK-COMPAT-01（上下文对象差异, atomgit vs github 是核心命名差异）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/syntax-reference/context.md §2.2；
            COMPAT-NOTES.md §2；
            参照现有用例 TC-038/TC-206 (属性缺失)
```

```
意图 ID:    INTENT-COMP-015
维度标签:   [completeness]
标题:       验证 permissions 权限模型的 6 个权限域与快捷语法

风险点:     permissions 是安全基线的最小控制面。GitCode 权限域命名
            (project/pr/issue/note/repository/hook) 与 GitHub 完全不同。
            若某权限域声明的 read/write/none 未实际生效——
            如 write 仍被降级为 read——则 Token 权限大于预期。
            快捷语法 read-all/write-all/{} 的语义也需验证。

预期系统行为:
            - `permissions: { repository: read, pr: write }` → ATOMGIT_TOKEN 仅有仓库读 + PR 写权限
            - `permissions: {}` → 所有权限域为 none（最小权限）
            - `permissions: read-all` → 所有域为 read
            - `permissions: write-all` → 所有域为 write
            - 声明 `pr: none` 后尝试写 PR → 操作失败
            - 未声明 permissions → 使用仓库默认权限（需确定默认值是什么）

Oracle 来源: GitCode规格（token-permissions §permissions 字段详解）

验证要点:
  - [正向] `permissions: {}` 下 ATOMGIT_TOKEN 仅有 repository:read（最小默认）
  - [正向] 声明 `pr: write` 后可通过 API 评论 PR
  - [正向] 声明 `pr: none` 后尝试写 PR → API 调用被拒
  - [正向] read-all / write-all 快捷语法正确展开到全部域
  - [负向] `permissions` 声明了 write 但实际 Token 却被降级为 read

优先级线索: 关联 RISK-SEC-01（权限越界）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/security-permissions/token-permissions.md；
            COMPAT-NOTES.md §6
```

```
意图 ID:    INTENT-COMP-016
维度标签:   [completeness]
标题:       验证可重用工作流 workflow_call 的调用传参与 2 层嵌套限制

风险点:     workflow_call 是组织级流程标准化的基础设施。
            调用方通过 with: 传 inputs、secrets: 传 secrets；
            最大嵌套 2 层（被调用方不能再调用另一个 workflow_call）。
            若传参丢失、secrets 未透传、或 2 层限制未有效拦截，
            则标准化流水线不可用。

预期系统行为:
            - 调用方 `with: { key: value }` → 被调用方 `${{ inputs.key }}` 可读
            - 调用方 `secrets: { TOKEN: ${{ secrets.X }} }` → 被调用方可读 `${{ secrets.TOKEN }}`
            - 2 层嵌套：A → B (workflow_call) 成功；B 内定义 workflow_call → C 被拦截
            - 被调用方 outputs 可被调用方通过 `needs.<job>.outputs` 读取

Oracle 来源: GitCode规格（syntax-reference/trigger-events §1.8 + write-pipelines/configure-triggers §workflow_call）

验证要点:
  - [正向] inputs 传参正确到达被调用方
  - [正向] secrets 透传正确到达被调用方
  - [正向] 被调用方 outputs 在调用方可读
  - [正向] 2 层 OK（直接调用 → 被调用方）
  - [负向] 第 3 层（被调用方再 workflow_call）→ 明确报错而非静默跳过

优先级线索: RISK-COMPAT-01（workflow_call 嵌套限制为 GitCode 特有）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/syntax-reference/trigger-events.md §1.8；
            inputs/gitcode-spec/writing-pipelines/configure-triggers.md；
            COMPAT-NOTES.md §5
```

```
意图 ID:    INTENT-COMP-017
维度标签:   [completeness]
标题:       验证 runner 标签匹配: 官方三段式标签、default 等效、自托管全匹配

风险点:     runs-on 决定 job 在哪执行。官方三段式标签 `{os-version},{arch},{flavor}`、
            default 快捷方式、自托管全匹配规则——这些是 job 调度正确性的基础。
            若标签匹配错误（如部分匹配即调度），job 可能在错误环境中执行，
            导致构建产物架构错误或工具链不可用。

预期系统行为:
            - `runs-on: [ubuntu-latest, x64, small]` → 分配 small 规格的 x64 Ubuntu runner
            - `runs-on: default` → 等价 `[ubuntu-latest, x64, small]`
            - `runs-on: [self-hosted, linux, gpu]` → 仅分配到同时有这 3 个标签的自托管 runner
            - 无匹配 runner → job 排队或超时失败
            - `${{ matrix.os }},${{ matrix.arch }},small` 动态标签 → 正确展开

Oracle 来源: GitCode规格（runner-management/using-hosted-runners + runner-management/selecting-runner-labels）

验证要点:
  - [正向] 官方三段式标签匹配到正确规格的 runner
  - [正向] default 等价于 [ubuntu-latest, x64, small]
  - [正向] 自托管全匹配：标签子集不匹配，必须全部满足
  - [正向] 动态 runs-on（matrix 变量）正确展开并匹配
  - [负向] 无匹配 runner 时不应随机分配到其他 runner

优先级线索: RISK-COMPAT-01（runner 标签体系差异）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/runner-management/using-hosted-runners.md;
            inputs/gitcode-spec/runner-management/selecting-runner-labels.md；
            COMPAT-NOTES.md §7
```

```
意图 ID:    INTENT-COMP-018
维度标签:   [completeness]
标题:       验证 workflow 文件解析: YAML 合法性检查与错误信息可操作性

风险点:     非法的 YAML 定义（缺必填字段 on、runs-on 标签格式错误、schema 违规）
            的报错质量是可用性基线。若报错仅是 "syntax error" 而不指明位置和原因，
            用户排错成本极高。这也是从 GitHub 迁移时的第一摩擦点。

预期系统行为:
            - 缺 `on` 字段 → 明确报错 "on is required" + 文件路径
            - 缺 `runs-on` → 明确报错 + 指明哪个 job
            - YAML 语法错误（缩进/标点） → 报错 + 行列号
            - 未知字段（不在 schema 中） → 报错还是静默忽略，行为需可预测
            - `.gitcode/workflows/` 下非 .yml/.yaml 文件被忽略（不报错也不执行）

Oracle 来源: GitCode规格（workflow-file-location-structure §基本结构字段）

验证要点:
  - [正向] 合法 YAML 被正确解析并触发
  - [正向] 缺 on 字段 → 明确报错信息，包含文件路径
  - [正向] 缺 runs-on 的 job → 明确报错，包含 job 名称
  - [正向] YAML 语法错误 → 报错信息包含行号和具体错误原因
  - [正向] `.gitcode/workflows/` 下的 .json/.txt 文件被忽略
  - [非功能] 报错信息包含中文（或用户可理解的语言），而非仅英文错误码

优先级线索: 关联 RISK-USE-01（迁移报错不指明差异）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/writing-pipelines/workflow-file-location-structure.md
```

```
意图 ID:    INTENT-COMP-019
维度标签:   [completeness]
标题:       验证 workflow 命令: ATOMGIT_STEP_SUMMARY 输出到运行摘要页

风险点:     ATOMGIT_STEP_SUMMARY 允许 job 将 Markdown 内容输出到运行详情摘要——
            这是 CI 结果可视化的关键能力。若内容丢失、Markdown 渲染错误、
            或被后续步骤覆盖，则用户看不到预期的构建/测试结果摘要。

预期系统行为:
            - `echo "## Test Results" >> $ATOMGIT_STEP_SUMMARY` → 运行详情页显示 Markdown 表格
            - 多个 step 写入 → 内容累积（追加），不互相覆盖
            - Markdown 表格、标题、链接被正确渲染

Oracle 来源: GitCode规格（syntax-reference/workflow-commands §5.4 + view-run-results）

验证要点:
  - [正向] 写入 Markdown 表 → 运行详情摘要页正确渲染
  - [正向] 多个 step 各自写入 → 内容累积可见
  - [正向] 空内容写入不报错
  - [正向] 超长内容（如 100KB）正常截断或完整显示

优先级线索: 关联 RISK-USE-01（可观测性体验）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/syntax-reference/workflow-commands.md §5.4;
            inputs/gitcode-spec/running-pipelines/view-run-results.md
```

```
意图 ID:    INTENT-COMP-020
维度标签:   [completeness]
标题:       验证重运行机制: re-run all / re-run failed 的隔离性与状态保持

风险点:     重运行是 CI 高频操作。re-run failed jobs 仅重跑失败 job——
            但 stages 中因 fail_fast 跳过的 job 也应纳入重跑范围。
            重运行使用原始 commit 的配置（不读最新配置），
            且 sha/ref/event_name 保持原值。
            最大 3 次重试、超时 > 6h 不可重跑。
            若这些约束未正确实现，重运行可能误用最新配置导致结果不一致。

预期系统行为:
            - Re-run all jobs → 创建新 run，所有 job 重执行，run_number 递增
            - Re-run failed jobs → 仅失败 job + fail_fast 跳过的后续 stage job 重执行
            - 重运行使用原始 commit 的 `.gitcode/workflows/` 配置
            - 重运行后 atomgit.sha/ref/event_name 保持原值
            - 第 4 次重运行被拒绝（最大 3 次）
            - 运行时长 > 6h 的 run 无法重运行

Oracle 来源: GitCode规格（rerun-failed-jobs）

验证要点:
  - [正向] Re-run all → 所有 job 重新执行，run_number 递增
  - [正向] Re-run failed → 仅失败 job 执行，成功 job 保持 cached
  - [正向] 修改 workflow 文件后 re-run → 使用原始 commit 配置
  - [正向] Run 时长 > 360min → re-run 被拒绝
  - [负向] 超过 3 次 re-run → 被拒绝

优先级线索: RISK-REL-01（重试机制可靠性）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/running-pipelines/rerun-failed-jobs.md
```

```
意图 ID:    INTENT-COMP-021
维度标签:   [completeness]
标题:       验证 workflow 调度延迟与 schedule 最短间隔（5 分钟）约束

风险点:     文档声明 schedule 最小间隔 5 分钟、默认分支生效。
            若 cron `*/2 * * * *`（每 2 分钟）被静默接受但不执行，
            用户以为 pipeline 在跑但实际上被跳过。
            现有用例 S3×24+TC-391 报告 schedule 完全不工作。

预期系统行为:
            - cron `*/5 * * * *`（每 5 分钟）→ 每 5 分钟触发
            - cron `*/2 * * * *`（每 2 分钟）→ 被拒绝或按最小间隔 5 分钟执行
            - schedule 仅在默认分支上生效
            - UTC 时区（声明如此）
            - 存在数分钟的调度延迟（文档自承）

Oracle 来源: GitCode规格（syntax-reference/trigger-events §1.9）

验证要点:
  - [正向] 合法 cron 在默认分支上按 UTC 时区触发
  - [正向] 非默认分支的 schedule → 不触发
  - [非功能] 多次 schedule 触发之间的最小间隔 ≥ 5 分钟
  - [非功能] 调度延迟在文档声明的 "数分钟" 范围内（非数十分钟）

优先级线索: RISK-REL-01（定时触发的可靠性）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/syntax-reference/trigger-events.md §1.9；
            参照现有用例 S3×24+TC-391 (schedule 完全不工作)
```

```
意图 ID:    INTENT-COMP-022
维度标签:   [completeness]
标题:       验证 Action 引用方式: 官方短名、第三方全路径、本地相对路径

风险点:     GitCode 的官方 action 使用无 owner 短名（如 `uses: checkout`），
            第三方 action 使用 owner/repo/path@ref，本地 action 使用相对路径。
            若引用解析逻辑有误（如短名与全路径冲突、ref 解析规则不同于文档声明），
            则 job 无法 checkout 代码或使用预置 action。

预期系统行为:
            - `uses: checkout` → 使用官方 checkout action
            - `uses: setup-node` with `node-version: '20'` → 安装 Node.js 20
            - `uses: docker/build-push-action@v6` → 使用第三方 action
            - `uses: ./.gitcode/actions/my-action` → 使用仓库本地 action
            - `@main` 引用分支 → 每次使用该分支最新提交
            - `@a1b2c3d` 引用 SHA → 使用精确提交

Oracle 来源: GitCode规格（using-actions §三种引用方式）

验证要点:
  - [正向] 官方短名 `checkout` 正确拉取代码
  - [正向] 官方短名 `setup-node` 正确设置 Node 版本
  - [正向] 第三方 action 全路径引用成功获取并执行
  - [正向] 本地 action 相对路径引用成功
  - [正向] `@v4` tag 引用、`@sha` commit 引用均正确解析
  - [负向] 引用不存在的 action → 明确报错

优先级线索: RISK-COMPAT-01（action 引用格式差异）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/writing-pipelines/using-actions.md；
            COMPAT-NOTES.md §10
```

```
意图 ID:    INTENT-COMP-023
维度标签:   [completeness]
标题:       验证 continue-on-error 对 job DAG 失败传播的影响

风险点:     continue-on-error: true 允许 job/step 失败不阻断后续。
            但 `success` 状态函数在 continue-on-error 场景下的语义需精确验证：
            文档称 job 级 continue-on-error 后，下游 `if: ${{ success }}` 条件不满足，
            需改用 `if: ${{ always }}`。若实现与文档不一致，则 cleanup/log 类步骤被意外跳过。

预期系统行为:
            - step 级 continue-on-error → step 失败，后续 step 继续执行
            - job 级 continue-on-error → job 失败但不阻断后续 job
            - continue-on-error job 失败后，`${{ success }}` 在下游为 false
            - continue-on-error job 失败后，`${{ always }}` 在下游为 true
            - continue-on-error job 失败后，`needs.<id>.result` 反映真实状态

Oracle 来源: GitCode规格（configure-jobs §continue-on-error + configure-steps §continue-on-error）

验证要点:
  - [正向] step continue-on-error → step 失败后同 job 后续 step 正常执行
  - [正向] job continue-on-error → 下游 job 通过 needs 依赖时仍可执行
  - [正向] continue-on-error job 失败后 `${{ success }}` = false
  - [正向] continue-on-error job 失败后 `${{ always }}` = true
  - [正向] `needs.<job>.result` 反映 continue-on-error job 的真实 outcome

优先级线索: RISK-COMPAT-01（执行模型差异）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/writing-pipelines/configure-jobs.md;
            inputs/gitcode-spec/writing-pipelines/configure-steps.md
```

```
意图 ID:    INTENT-COMP-024
维度标签:   [completeness]
标题:       验证 timeout-minutes 超时终止与 job 状态标记

风险点:     timeout-minutes 是防无限卡死的最后手段。job 默认 360 分钟超时；
            step 无独立默认超时，受 job 超时约束。
            若超时后 job 状态标记错误（如记为 success 而非 cancelled）、
            或 step 级 timeout-minutes 不可配，则 pipeline 可能假阳性。

预期系统行为:
            - job `timeout-minutes: 5` → 运行 5 分钟后被强制终止，状态为 cancelled
            - step `timeout-minutes: 2` → 运行 2 分钟后被终止，step 标记失败
            - 未设 timeout-minutes 的 job → 默认 360 分钟后超时
            - 超时终止的 job → 日志包含明确的超时原因

Oracle 来源: GitCode规格（configure-jobs §timeout-minutes + configure-steps §timeout-minutes）

验证要点:
  - [正向] job 超时终止 → job 状态为 cancelled（非 success）
  - [正向] step 超时终止 → step 标记失败，日志含超时原因
  - [正向] 未设 timeout 的 job 不受短超时限制
  - [正向] post 阶段在 job 超时后的执行行为可观测

优先级线索: RISK-REL-01（长时运行可靠性）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/writing-pipelines/configure-jobs.md;
            inputs/gitcode-spec/writing-pipelines/configure-steps.md
```

```
意图 ID:    INTENT-COMP-025
维度标签:   [completeness]
标题:       验证 job 级 if 对矩阵展开的独立求值

风险点:     当 job 同时配置 strategy.matrix 和 job 级 `if` 时，
            条件是在矩阵展开前还是展开后求值？文档未明确说明。
            若 `if: ${{ atomgit.ref == 'refs/heads/main' }}` 在展开前求值，
            则整个矩阵被跳过；若展开后逐实例求值，则每个矩阵实例独立判断。
            这种不一致可能导致某些平台组合被意外跳过。

预期系统行为:
            job 级 `if` 在矩阵展开后对每个实例独立求值（与 GitHub 行为一致）。
            若在展开前求值，整个矩阵全或无——与 GitHub 行为显著不同。

Oracle 来源: GitHub行为（GitCode规格未覆盖此细节）

验证要点:
  - [正向] 矩阵展开后每个实例独立求值 job 级 if
  - [正向] 不同矩阵实例的 if 求值结果不同时，行为正确
  - [正向] if 中使用 ${{ matrix.var }} 可以正常工作

优先级线索: RISK-COMPAT-01（矩阵 if 语义差异）
破坏级别:   fixture
来源输入:   inputs/gitcode-spec/writing-pipelines/configure-matrix-builds.md;
            inputs/gitcode-spec/writing-pipelines/configure-conditional-execution.md
```

---

## Part E: Cross-Reference: Spec Gaps to Intent Coverage

| Gap ID | Covered by Intent | Notes |
|---|---|---|
| G01 (default permissions) | INTENT-COMP-015 | Permission model validation |
| G02 (default shell) | INTENT-COMP-018 | Schema parsing & defaults |
| G03 (concurrency defaults) | INTENT-COMP-005 | Concurrency control validation |
| G04 (hashFiles no-match) | INTENT-COMP-013 | Expression boundary behavior |
| G05 (toJson scope) | INTENT-COMP-013 | Expression boundary behavior |
| G06 (null/undefined) | INTENT-COMP-013 | Expression boundary behavior |
| G07 (cancel + post) | INTENT-COMP-010 | Post stage semantics |
| G08 (artifact retention) | INTENT-COMP-006 | Artifact lifecycle |
| G09 (cache eviction) | INTENT-COMP-007 | Cache behavior |
| G10 (fork PR cache) | *(compat-diff/security domain)* | More appropriate for security |
| G11 (official tag match) | INTENT-COMP-017 | Runner label matching |
| G12 (dual fail_fast) | INTENT-COMP-004 + INTENT-COMP-009 | Matrix + stages |
| G13 (substring index) | INTENT-COMP-013 | Expression boundary behavior |
| G14 (container image) | *(reliability domain)* | Verified non-functional per TC-273 |
| G15 (environment field) | *(usability domain)* | Doc gap, no YAML to test |
| G16 (schedule enforcement) | INTENT-COMP-021 | Schedule semantics |
| G17 (action runtime) | INTENT-COMP-022 | Action reference resolution |
| G18 (300-file bound) | INTENT-COMP-002 | Trigger filter boundary |
| G19 (multi-workflow order) | *(reliability domain)* | Execution ordering guarantee |
| G20 (comments regex no-match) | INTENT-COMP-001 | Trigger event availability |
| G21 (needs + matrix) | INTENT-COMP-004 | Matrix parent job needs |

---
*Generated by spec-analyst agent | Run: 2026-07-20-01 | Inputs: gitcode-spec/ (50 pages), existing-cases/cases.md (631 cases)*
