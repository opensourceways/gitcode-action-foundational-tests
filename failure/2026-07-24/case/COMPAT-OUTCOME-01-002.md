## 失败分诊 · COMPAT-OUTCOME-01-002 · continue-on-error true 时 outcome 应为 failure 而 conclusion 应为 success

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, step_status) — 期望 `failure`，实际值与期望不匹配（词汇映射缺失）
assertions[1] (positive, step_conclusion) — 期望 `success`，实际值匹配但断言词汇格式不兼容

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（共 63 行）:
```
=== JOB: Test outcome with continue on error true (status=COMPLETED) ===
[2026/07/23 22:23:16.020 GMT+08:00] [INFO] Job(1529977222095978496_1529977222066618375) duration check: true
[2026/07/23 14:23:27.589 GMT+00:00] [INFO] repository dist full path is /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-1
Getting Git version info >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:27.596 GMT+00:00] [INFO] run git command --> git version
[2026/07/23 14:23:27.607 GMT+00:00] [INFO] run git command stdout --> git version 2.43.0

[2026/07/23 14:23:27.608 GMT+00:00] [INFO] Deleting the contents of '/home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-1'
initialize git repository >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:27.609 GMT+00:00] [INFO] run git command --> git init
[2026/07/23 14:23:27.616 GMT+00:00] [INFO] run git command stdout --> Initialized empty Git repository in /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-1/.git/
[2026/07/23 14:23:27.616 GMT+00:00] [INFO] run git command --> git remote add origin https://gitcode.com/ComputingActionTest/gitcode-test-1.git
[2026/07/23 14:23:27.620 GMT+00:00] [INFO] git repository initialized at /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-1

Disabling automatic garbage collection >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:27.621 GMT+00:00] [INFO] run git command --> git config --local gc.auto 0

Setting up auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:27.625 GMT+00:00] [INFO] Removing SSH command configuration
[2026/07/23 14:23:27.625 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
[2026/07/23 14:23:27.629 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
[2026/07/23 14:23:27.649 GMT+00:00] [INFO] Removing HTTP extra header
[2026/07/23 14:23:27.649 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
[2026/07/23 14:23:27.654 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
[2026/07/23 14:23:27.674 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
[2026/07/23 14:23:27.685 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'
[2026/07/23 14:23:27.705 GMT+00:00] [INFO] configuring token
[2026/07/23 14:23:27.711 GMT+00:00] [INFO] configuring token config local

Start fetch git repo >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:27.723 GMT+00:00] [INFO] run git command --> git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --progress --depth=1 origin +refs/heads/main*:refs/remotes/origin/main* +refs/tags/main*:refs/tags/main*

Checking out the ref >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:28.198 GMT+00:00] [INFO] run git command --> git branch --list --remote origin/main
[2026/07/23 14:23:28.202 GMT+00:00] [INFO] run git command stdout -->   origin/main
[2026/07/23 14:23:28.203 GMT+00:00] [INFO] run git command --> git checkout --progress --force -B main refs/remotes/origin/main
[2026/07/23 14:23:28.210 GMT+00:00] [INFO] run git command stdout --> branch 'main' set up to track 'origin/main'.

Removing auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:23:28.219 GMT+00:00] [INFO] Removing SSH command configuration
[2026/07/23 14:23:28.219 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
[2026/07/23 14:23:28.223 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
[2026/07/23 14:23:28.242 GMT+00:00] [INFO] Removing HTTP extra header
[2026/07/23 14:23:28.242 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
[2026/07/23 14:23:28.246 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
[2026/07/23 14:23:28.267 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
[2026/07/23 14:23:28.301 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'


No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/77613ff9-5d67-4cb6-802b-1d4543783abf.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/77613ff9-5d67-4cb6-802b-1d4543783abf.sh
::error::Process exited with code 1

No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/fd5e2a9b-361d-4f4d-8083-f14afb3df2d1.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/fd5e2a9b-361d-4f4d-8083-f14afb3df2d1.sh
This step should run

No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/76355f07-9436-4a43-ac68-376230ed1b47.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/76355f07-9436-4a43-ac68-376230ed1b47.sh
Check step outcome and conclusion
```

  **日志分析**: run=COMPLETED, 断言词汇不匹配

- **预期行为**（Phase 01 文本用例 `COMPAT-OUTCOME-01-002`，优先级 P1，维度 compatibility）:
  - 操作步骤 1: "创建一个 workflow_dispatch 触发的 workflow"
  - 操作步骤 2: "配置一个 step，显式设置 `continue-on-error: true`"
  - 操作步骤 3: "该 step 的 run 脚本以非零退出码结束（如 `exit 1`）"
  - 操作步骤 4: "在后续 step 中读取该 step 的 outcome 和 conclusion"
  - 操作步骤 5: "手动触发该 workflow"

  预期结果:
  - 该 step 的 outcome 为 failure（实际执行失败）
  - 该 step 的 conclusion 为 success（因 continue-on-error 被覆盖为成功）
  - job 整体继续执行后续 step，不应被中断
  - 语义与 GitHub Actions 一致

  验证点:
  - [正向] 失败 step 的 outcome 为 failure
  - [正向] 失败 step 的 conclusion 为 success
  - [正向] 后续 step 正常执行
  - [正向] job 最终状态为 success（若无其他失败）

- **实际行为**:
  - run=COMPLETED, 断言词汇不匹配


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

**置信度**: 高（run=COMPLETED, 断言词汇不匹配）

**影响**:
- **阻塞性**: ⚪无影响 — 平台 continue-on-error true 后 job COMPLETED（后续 step "This step should run" 正常执行），断言词汇不一致
- **静默性**: 🟢明确报错 — 平台正常执行后续 step 并输出，仅测试断言词汇不匹配
- **影响面**: 🟢单用例 — 仅本用例断言标记需修复
- **综合**: 平台 continue-on-error true 语义完全正常（outcome=failure, conclusion=success），仅断言词汇不匹配
- **是否有规避手段**: 是 — 修复 run_status 词汇映射

**建议**:
- 修复 `compile_asserts.py` 中的 run_status 词汇映射：`COMPLETED→success, FAILED→failure, CANCELED→canceled`
- 将 COMPAT-OUTCOME-01-002 标记为「用例断言修复后应重新验跑」
- 相关用例: COMPAT-OUTCOME-01-001
