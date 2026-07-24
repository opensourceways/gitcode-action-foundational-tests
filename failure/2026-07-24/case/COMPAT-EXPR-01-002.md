## 失败分诊 · COMPAT-EXPR-01-002 · success() 函数的处理行为差异

**判定结果**: FAIL
**失败断言**:
assertions (needs/success) — 两个 job 均 COMPLETED，'Job B ran after Job A success' 正确输出

**根因初判**: 标记不匹配
**责任人**: Phase 01

**证据**:

- **Job 日志全量**（共 108 行）:
```
  === JOB: Job A that succeeds (status=COMPLETED) ===
  [2026/07/23 22:19:11.534 GMT+08:00] [INFO] Job(1529976192327618560_1529976192302452743) duration check: true
  [2026/07/23 14:19:23.648 GMT+00:00] [INFO] repository dist full path is /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0
  Getting Git version info >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:19:23.651 GMT+00:00] [INFO] run git command --> git version
  [2026/07/23 14:19:23.657 GMT+00:00] [INFO] run git command stdout --> git version 2.43.0
  
  [2026/07/23 14:19:23.658 GMT+00:00] [INFO] Deleting the contents of '/home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0'
  initialize git repository >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:19:23.659 GMT+00:00] [INFO] run git command --> git init
  [2026/07/23 14:19:23.662 GMT+00:00] [INFO] run git command stdout --> Initialized empty Git repository in /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0/.git/
  [2026/07/23 14:19:23.663 GMT+00:00] [INFO] run git command --> git remote add origin https://gitcode.com/ComputingActionTest/gitcode-test-0.git
  [2026/07/23 14:19:23.665 GMT+00:00] [INFO] git repository initialized at /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0
  
  Disabling automatic garbage collection >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:19:23.666 GMT+00:00] [INFO] run git command --> git config --local gc.auto 0
  
  Setting up auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:19:23.668 GMT+00:00] [INFO] Removing SSH command configuration
  [2026/07/23 14:19:23.669 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
  [2026/07/23 14:19:23.672 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
  [2026/07/23 14:19:23.687 GMT+00:00] [INFO] Removing HTTP extra header
  [2026/07/23 14:19:23.687 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
  [2026/07/23 14:19:23.690 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
  [2026/07/23 14:19:23.704 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
  [2026/07/23 14:19:23.710 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'
  [2026/07/23 14:19:23.724 GMT+00:00] [INFO] configuring token
  [2026/07/23 14:19:23.728 GMT+00:00] [INFO] configuring token config local
  
  Start fetch git repo >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:19:23.736 GMT+00:00] [INFO] run git command --> git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --progress --depth=1 origin +refs/heads/main*:refs/remotes/origin/main* +refs/tags/main*:refs/tags/main*
  
  Checking out the ref >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:19:24.217 GMT+00:00] [INFO] run git command --> git branch --list --remote origin/main
  [2026/07/23 14:19:24.219 GMT+00:00] [INFO] run git command stdout -->   origin/main
  [2026/07/23 14:19:24.219 GMT+00:00] [INFO] run git command --> git checkout --progress --force -B main refs/remotes/origin/main
  [2026/07/23 14:19:24.224 GMT+00:00] [INFO] run git command stdout --> branch 'main' set up to track 'origin/main'.
  
  Removing auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:19:24.230 GMT+00:00] [INFO] Removing SSH command configuration
  [2026/07/23 14:19:24.230 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
  [2026/07/23 14:19:24.232 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
  [2026/07/23 14:19:24.247 GMT+00:00] [INFO] Removing HTTP extra header
  [2026/07/23 14:19:24.247 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
  [2026/07/23 14:19:24.250 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
  [2026/07/23 14:19:24.265 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
  [2026/07/23 14:19:24.282 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'
  
  
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/34b9134b-ea3c-434d-afeb-e2704cbc035c.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/34b9134b-ea3c-434d-afeb-e2704cbc035c.sh
  Job A done
  
  
  === JOB: Job B depends on A (status=COMPLETED) ===
  [2026/07/23 22:19:26.695 GMT+08:00] [INFO] Job(1529976192327618560_1529976192302452745) duration check: true
  [2026/07/23 14:19:38.132 GMT+00:00] [INFO] repository dist full path is /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0
  Getting Git version info >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:19:38.137 GMT+00:00] [INFO] run git command --> git version
  [2026/07/23 14:19:38.145 GMT+00:00] [INFO] run git command stdout --> git version 2.43.0
  
  [2026/07/23 14:19:38.146 GMT+00:00] [INFO] Deleting the contents of '/home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0'
  initialize git repository >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:19:38.147 GMT+00:00] [INFO] run git command --> git init
  [2026/07/23 14:19:38.153 GMT+00:00] [INFO] run git command stdout --> Initialized empty Git repository in /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0/.git/
  [2026/07/23 14:19:38.154 GMT+00:00] [INFO] run git command --> git remote add origin https://gitcode.com/ComputingActionTest/gitcode-test-0.git
  [2026/07/23 14:19:38.157 GMT+00:00] [INFO] git repository initialized at /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0
  
  Disabling automatic garbage collection >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:19:38.158 GMT+00:00] [INFO] run git command --> git config --local gc.auto 0
  
  Setting up auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:19:38.162 GMT+00:00] [INFO] Removing SSH command configuration
  [2026/07/23 14:19:38.163 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
  [2026/07/23 14:19:38.167 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
  [2026/07/23 14:19:38.187 GMT+00:00] [INFO] Removing HTTP extra header
  [2026/07/23 14:19:38.187 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
  [2026/07/23 14:19:38.191 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
  [2026/07/23 14:19:38.210 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
  [2026/07/23 14:19:38.217 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'
  [2026/07/23 14:19:38.236 GMT+00:00] [INFO] configuring token
  [2026/07/23 14:19:38.241 GMT+00:00] [INFO] configuring token config local
  
  Start fetch git repo >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:19:38.251 GMT+00:00] [INFO] run git command --> git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --progress --depth=1 origin +refs/heads/main*:refs/remotes/origin/main* +refs/tags/main*:refs/tags/main*
  
  Checking out the ref >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:19:38.909 GMT+00:00] [INFO] run git command --> git branch --list --remote origin/main
  [2026/07/23 14:19:38.912 GMT+00:00] [INFO] run git command stdout -->   origin/main
  [2026/07/23 14:19:38.913 GMT+00:00] [INFO] run git command --> git checkout --progress --force -B main refs/remotes/origin/main
  [2026/07/23 14:19:38.920 GMT+00:00] [INFO] run git command stdout --> branch 'main' set up to track 'origin/main'.
  
  Removing auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:19:38.928 GMT+00:00] [INFO] Removing SSH command configuration
  [2026/07/23 14:19:38.928 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
  [2026/07/23 14:19:38.931 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
  [2026/07/23 14:19:38.950 GMT+00:00] [INFO] Removing HTTP extra header
  [2026/07/23 14:19:38.950 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
  [2026/07/23 14:19:38.953 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
  [2026/07/23 14:19:38.974 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
  [2026/07/23 14:19:38.997 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'
  
  
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/a3a62746-96da-443f-849e-8ca346e32d9f.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/a3a62746-96da-443f-849e-8ca346e32d9f.sh
  Job B ran after Job A success
```

- **预期行为**（Phase 01 文本用例 `COMPAT-EXPR-01-002`，优先级 P1，维度 兼容性）:
  - 前置条件: - 仓库已启用 GitCode Action
  - 操作步骤: 1. 提交一个 workflow，在 step 中尝试使用 success() 函数形式的表达式
    2. 对比平台对 success() 与 bare success 的解析差异
    3. 手动触发并观察运行结果
  - 预期结果: - 平台可能对 success() 函数与 bare success 关键字有不同的支持策略
    - 记录并验证实际行为与 GitHub Actions 的兼容性差异
  - 验证点: - [正向] 若支持，表达式返回布尔结果
    - [负向] 若不支持，应有表达式解析错误或降级行为

- **实际行为**:
  - Job "Job A that succeeds" status=COMPLETED
  - Job "Job B depends on A" status=COMPLETED

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
  - Phase 01 前置条件: - 仓库已启用 GitCode Action

**置信度**: 中（job 执行成功但断言评判未通过，需进一步确认断言逻辑）

**影响**:
- **阻塞性**: 🟡非阻塞 — job 执行成功，功能正常
- **静默性**: 🟢明确报错 — 断言差异可通过 logs/assertions 定位
- **影响面**: 🟢单用例 — 仅本用例断言未通过
- **综合**: 基于上述证据，COMPAT-EXPR-01-002 的失败根因初步判定为 **标记不匹配**（责任人: **Phase 01**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可调整断言评判规则或补充环境配置

**建议**:
- 复查断言评判器对 COMPAT-EXPR-01-002 的判断逻辑
- 相关用例: COMPAT-EXPR-01-003
