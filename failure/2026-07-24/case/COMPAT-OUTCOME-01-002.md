## 失败分诊 · COMPAT-OUTCOME-01-002 · continue-on-error true 时 outcome 应为 failure 而 conclusion 应为 success

**判定结果**: FAIL
**失败断言**:
assertions (outcome/conclusion, continue-on-error) — job COMPLETED，'Check step outcome and conclusion' 正确，断言值不匹配

**根因初判**: 标记不匹配
**责任人**: Phase 01

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

- **预期行为**（Phase 01 文本用例 `COMPAT-OUTCOME-01-002`，优先级 P1，维度 兼容性）:
  - 前置条件: - 仓库已启用 workflow
  - 操作步骤: 1. 创建一个 workflow_dispatch 触发的 workflow
    2. 配置一个 step，显式设置 `continue-on-error: true`
    3. 该 step 的 run 脚本以非零退出码结束（如 `exit 1`）
    4. 在后续 step 中读取该 step 的 outcome 和 conclusion
    5. 手动触发该 workflow
  - 预期结果: - 该 step 的 outcome 为 failure（实际执行失败）
    - 该 step 的 conclusion 为 success（因 continue-on-error 被覆盖为成功）
    - job 整体继续执行后续 step，不应被中断
    - 语义与 GitHub Actions 一致
  - 验证点: - [正向] 失败 step 的 outcome 为 failure
    - [正向] 失败 step 的 conclusion 为 success
    - [正向] 后续 step 正常执行
    - [正向] job 最终状态为 success（若无其他失败）

- **实际行为**:
  - Job "Test outcome with continue on error true" status=COMPLETED

- **对照 GitCode 规格** `phase01/inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md`:
  - 规格摘要:
    ```
# Variables, Secrets, Context and Expressions
AtomGit Action provides a four-level variable system using `env`, `vars`, `secrets`, and `inputs`, enabling flexible workflow configuration through context (primarily `atomgit`) and expressions (`${{ expression }}`).
## Four-Level Variable System
| Type | Suitable For | Sensitive | Reference Method |
|------|-------------|-----------|-------------------|
| `env` | Temporary variables within workflow | No | `$VAR_NAME` or `${{ env.VAR }}` |
| `vars` | Repository/organization-level regular variables | No | `${{ vars.VAR }}` |
| `secrets` | Passwords,
    ```
  - 测试 YAML 工作流模式与此规格承诺一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (manual)
  - Phase 01 前置条件: - 仓库已启用 workflow

**置信度**: 中（job 执行成功但断言评判未通过，需进一步确认断言逻辑）

**影响**:
- **阻塞性**: 🟡非阻塞 — job 执行成功，功能正常
- **静默性**: 🟢明确报错 — 断言差异可通过 logs/assertions 定位
- **影响面**: 🟢单用例 — 仅本用例断言未通过
- **综合**: 基于上述证据，COMPAT-OUTCOME-01-002 的失败根因初步判定为 **标记不匹配**（责任人: **Phase 01**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可调整断言评判规则或补充环境配置

**建议**:
- 复查断言评判器对 COMPAT-OUTCOME-01-002 的判断逻辑
- 相关用例: COMPAT-OUTCOME-01-001
