## 失败分诊 · COMPAT-MASK-01-002 · 通过 env 注入 secret 后输出应在日志中被脱敏

**判定结果**: FAIL
**失败断言**:
assertions (secret mask via env) — job COMPLETED，但 'Env value: ' 后为空，secret 未注入

**根因初判**: 环境问题
**责任人**: Phase 02

**证据**:

- **Job 日志全量**（共 53 行）:
```
  === JOB: Test secret masking via env (status=COMPLETED) ===
  [2026/07/23 22:04:04.780 GMT+08:00] [INFO] Job(1529972393445822464_1529972393420656647) duration check: true
  [2026/07/23 14:04:17.603 GMT+00:00] [INFO] repository dist full path is /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-3
  Getting Git version info >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:04:17.608 GMT+00:00] [INFO] run git command --> git version
  [2026/07/23 14:04:17.616 GMT+00:00] [INFO] run git command stdout --> git version 2.43.0
  
  [2026/07/23 14:04:17.618 GMT+00:00] [INFO] Deleting the contents of '/home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-3'
  initialize git repository >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:04:17.619 GMT+00:00] [INFO] run git command --> git init
  [2026/07/23 14:04:17.625 GMT+00:00] [INFO] run git command stdout --> Initialized empty Git repository in /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-3/.git/
  [2026/07/23 14:04:17.625 GMT+00:00] [INFO] run git command --> git remote add origin https://gitcode.com/ComputingActionTest/gitcode-test-3.git
  [2026/07/23 14:04:17.629 GMT+00:00] [INFO] git repository initialized at /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-3
  
  Disabling automatic garbage collection >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:04:17.630 GMT+00:00] [INFO] run git command --> git config --local gc.auto 0
  
  Setting up auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:04:17.633 GMT+00:00] [INFO] Removing SSH command configuration
  [2026/07/23 14:04:17.634 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
  [2026/07/23 14:04:17.638 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
  [2026/07/23 14:04:17.657 GMT+00:00] [INFO] Removing HTTP extra header
  [2026/07/23 14:04:17.658 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
  [2026/07/23 14:04:17.661 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
  [2026/07/23 14:04:17.681 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
  [2026/07/23 14:04:17.688 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'
  [2026/07/23 14:04:17.708 GMT+00:00] [INFO] configuring token
  [2026/07/23 14:04:17.714 GMT+00:00] [INFO] configuring token config local
  
  Start fetch git repo >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:04:17.725 GMT+00:00] [INFO] run git command --> git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --progress --depth=1 origin +refs/heads/main*:refs/remotes/origin/main* +refs/tags/main*:refs/tags/main*
  
  Checking out the ref >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:04:18.230 GMT+00:00] [INFO] run git command --> git branch --list --remote origin/main
  [2026/07/23 14:04:18.234 GMT+00:00] [INFO] run git command stdout -->   origin/main
  [2026/07/23 14:04:18.235 GMT+00:00] [INFO] run git command --> git checkout --progress --force -B main refs/remotes/origin/main
  [2026/07/23 14:04:18.240 GMT+00:00] [INFO] run git command stdout --> branch 'main' set up to track 'origin/main'.
  
  Removing auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:04:18.248 GMT+00:00] [INFO] Removing SSH command configuration
  [2026/07/23 14:04:18.248 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
  [2026/07/23 14:04:18.251 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
  [2026/07/23 14:04:18.270 GMT+00:00] [INFO] Removing HTTP extra header
  [2026/07/23 14:04:18.271 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
  [2026/07/23 14:04:18.274 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
  [2026/07/23 14:04:18.294 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
  [2026/07/23 14:04:18.316 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'
  
  
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/6d24c376-496d-4668-8190-7b44251ab3a2.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/6d24c376-496d-4668-8190-7b44251ab3a2.sh
  Env value:
```

- **预期行为**（Phase 01 文本用例 `COMPAT-MASK-01-002`，优先级 P0，维度 兼容性）:
  - 前置条件: - 仓库配置了 secret TEST_SECRET，值为已知字符串（如 my-secret-value-456）
  - 操作步骤: 1. 创建一个 workflow_dispatch 触发的 workflow
    2. 在 step 的 env 块中将 TEST_SECRET 注入为环境变量 MY_VAR
    3. 在 run 脚本中执行 `echo "$MY_VAR"`
    4. 手动触发该 workflow
    5. 查看运行日志中该 step 的输出
  - 预期结果: - 日志中 MY_VAR 的值（即 secret 的值）应被替换为 `***`
    - 即使通过 env 间接引用，脱敏机制仍应生效
    - 不应出现 my-secret-value-456 的明文
  - 验证点: - [负向] 日志中不含 TEST_SECRET 的原始明文值
    - [正向] 日志中出现 `***` 替代通过 env 注入的 secret 值
    - [正向] 环境变量在运行时可被正常读取（仅日志脱敏）

- **实际行为**:
  - Job "Test secret masking via env" status=COMPLETED
  - 'Env value: ' 为空白，secret 未通过环境变量注入

- **对照 GitCode 规格**:
  - 文本用例参照来源: `inputs/security-knowledge/issues.md; inputs/github-reference/security/`

- **环境前置条件验证**:
  - setup.secrets: `[TEST_SECRET]`
  - setup.repo_fixture: `with-secrets`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (manual)
  - Phase 01 前置条件: - 仓库配置了 secret TEST_SECRET，值为已知字符串（如 my-secret-value-456）

**置信度**: 中（job 执行成功但断言评判未通过，需进一步确认断言逻辑）

**影响**:
- **阻塞性**: 🟡非阻塞 — job 执行成功，功能正常
- **静默性**: 🟢明确报错 — 断言差异可通过 logs/assertions 定位
- **影响面**: 🟢单用例 — 仅本用例断言未通过
- **综合**: 基于上述证据，COMPAT-MASK-01-002 的失败根因初步判定为 **环境问题**（责任人: **Phase 02**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可调整断言评判规则或补充环境配置

**建议**:
- 复查断言评判器对 COMPAT-MASK-01-002 的判断逻辑
- 在 Phase 02 补充环境配置（config_probe、secret 注入、event 匹配等）
