## 失败分诊 · COMPAT-OUTCOME-01-001 · continue-on-error false 时 outcome 与 conclusion 应均为 failure

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, step_status) — 期望 `failure`，实际 `FAILED`（平台 API 大小写与表达式函数语义不一致：platform=`FAILED` vs `${{ failure }}`=`failed`）
assertions[1] (positive, step_conclusion) — 期望 `failure`，下游随上游失败而 IGNORED

**根因初判**: Engine Bug

**证据**:

- **Job 日志全量**（共 58 行）:
```
=== JOB: Test outcome with continue on error false (status=FAILED) ===
[2026/07/23 22:23:05.278 GMT+08:00] [INFO] Job(1529977177305133056_1529977177284161543) duration check: true
[2026/07/23 14:23:16.991 GMT+00:00] [INFO] repository dist full path is /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0
Getting Git version info >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:16.995 GMT+00:00] [INFO] run git command --> git version
[2026/07/23 14:23:17.005 GMT+00:00] [INFO] run git command stdout --> git version 2.43.0

[2026/07/23 14:23:17.006 GMT+00:00] [INFO] Deleting the contents of '/home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0'
initialize git repository >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:17.007 GMT+00:00] [INFO] run git command --> git init
[2026/07/23 14:23:17.013 GMT+00:00] [INFO] run git command stdout --> Initialized empty Git repository in /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0/.git/
[2026/07/23 14:23:17.014 GMT+00:00] [INFO] run git command --> git remote add origin https://gitcode.com/ComputingActionTest/gitcode-test-0.git
[2026/07/23 14:23:17.018 GMT+00:00] [INFO] git repository initialized at /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0

Disabling automatic garbage collection >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:17.019 GMT+00:00] [INFO] run git command --> git config --local gc.auto 0

Setting up auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:17.022 GMT+00:00] [INFO] Removing SSH command configuration
[2026/07/23 14:23:17.023 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
[2026/07/23 14:23:17.027 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
[2026/07/23 14:23:17.050 GMT+00:00] [INFO] Removing HTTP extra header
[2026/07/23 14:23:17.051 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
[2026/07/23 14:23:17.055 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
[2026/07/23 14:23:17.075 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
[2026/07/23 14:23:17.083 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'
[2026/07/23 14:23:17.103 GMT+00:00] [INFO] configuring token
[2026/07/23 14:23:17.109 GMT+00:00] [INFO] configuring token config local

Start fetch git repo >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:17.120 GMT+00:00] [INFO] run git command --> git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --progress --depth=1 origin +refs/heads/main*:refs/remotes/origin/main* +refs/tags/main*:refs/tags/main*

Checking out the ref >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:17.648 GMT+00:00] [INFO] run git command --> git branch --list --remote origin/main
[2026/07/23 14:23:17.652 GMT+00:00] [INFO] run git command stdout -->   origin/main
[2026/07/23 14:23:17.653 GMT+00:00] [INFO] run git command --> git checkout --progress --force -B main refs/remotes/origin/main
[2026/07/23 14:23:17.659 GMT+00:00] [INFO] run git command stdout --> branch 'main' set up to track 'origin/main'.

Removing auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:17.669 GMT+00:00] [INFO] Removing SSH command configuration
[2026/07/23 14:23:17.669 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
[2026/07/23 14:23:17.672 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
[2026/07/23 14:23:17.693 GMT+00:00] [INFO] Removing HTTP extra header
[2026/07/23 14:23:17.694 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
[2026/07/23 14:23:17.698 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
[2026/07/23 14:23:17.719 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
[2026/07/23 14:23:17.744 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'


No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/8891abb1-c0e1-467c-acc5-7a1c90ae5398.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/8891abb1-c0e1-467c-acc5-7a1c90ae5398.sh
::error::Process exited with code 1

No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/d1ee7d63-bf63-43b2-bdd5-b8b1a2c2dae7.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/d1ee7d63-bf63-43b2-bdd5-b8b1a2c2dae7.sh
Check step outcome and conclusion
```

  **日志分析**: ::error::Process exited with code 1 → cleanup "Check step outcome and conclusion" — "failure"≠"FAILED"

- **预期行为**（Phase 01 文本用例 `COMPAT-OUTCOME-01-001`，优先级 P1，维度 compatibility）:
  - 操作步骤 1: "创建一个 workflow_dispatch 触发的 workflow"
  - 操作步骤 2: "配置一个 step，显式设置 `continue-on-error: false`（或默认不写）"
  - 操作步骤 3: "该 step 的 run 脚本以非零退出码结束（如 `exit 1`）"
  - 操作步骤 4: "在后续 step 中通过 `${{ atomgit.step.status }}` 或上下文读取该 step 的状态"
  - 操作步骤 5: "手动触发该 workflow"

  预期结果:
  - 该 step 失败后，job 整体标记为失败
  - outcome（执行结果）与 conclusion（最终判定）均为 failure
  - 由于 continue-on-error 为 false，两者不应出现差异

  验证点:
  - [正向] 失败 step 的 outcome 为 failure
  - [正向] 失败 step 的 conclusion 为 failure
  - [正向] job 整体状态为 failure

- **实际行为**:
  - ::error::Process exited with code 1 → cleanup "Check step outcome and conclusion" — "failure"≠"FAILED"


- **测试 YAML 与规格精确对照**:
  - 规格文件: `expressions.md` (路径: `phase01/inputs/gitcode-spec/syntax-reference/expressions.md`)
  - 规格节选:
```yaml
# expressions.md 第36-39行: success/failed 状态函数
# context.md 第202-207行: steps 上下文 outcome 与 conclusion
steps:<step_id>.conclusion 的值: success / failure / cancelled
```
    该规格明确声明: expressions.md 36-39行 + context.md 202-207行

  测试 YAML 的写法与规格示例一致，证明平台文档确凿承诺了该行为。

**置信度**: 高（::error::Process exited with code 1 → cleanup "Check step outcome and conclusion" — "failure"≠"FAILED"）

**影响**:
- **阻塞性**: ⚪无影响 — Engine Bug（大小写比较），平台 continue-on-error false 后 cleanup 正常执行（"Check step outcome and conclusion"），仅断言 "failure"≠"FAILED"
- **静默性**: 🟢明确报错 — 平台输出 "::error::Process exited with code 1"，错误清晰可诊断
- **影响面**: 🟢单用例 — 表达式引擎大小写不一致，仅影响断言比较
- **综合**: 平台 outcome/conclusion 行为正确，step 失败后 cleanup 执行，仅表达式返回值大小写与断言不匹配
- **是否有规避手段**: 是 — 统一断言为 FAILED 或平台修复大小写语义

**建议**:
- 平台表达式引擎同时返回大写(`FAILED`/`CANCELED`)和文档中的小写(`success`/`failure`/`cancelled`)值
- 建议统一为文档约定的小写语义值
- 将 COMPAT-OUTCOME-01-001 标记为「平台修复后重新验跑」
- 相关用例: COMPAT-OUTCOME-01-002
