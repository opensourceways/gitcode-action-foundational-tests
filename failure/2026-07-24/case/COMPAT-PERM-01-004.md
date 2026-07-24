## 失败分诊 · COMPAT-PERM-01-004 · permissions 命名差异——GitCode repository 权限项正常生效

**判定结果**: FAIL
**失败断言**:
assertions (repository permission) — job COMPLETED，REPOSITORY_PERM_OK 正确输出

**根因初判**: 标记不匹配
**责任人**: Phase 01

**证据**:

- **Job 日志全量**（共 53 行）:
```
  === JOB: Verify repository permission works (status=COMPLETED) ===
  [2026/07/23 22:04:26.369 GMT+08:00] [INFO] Job(1529972484109897728_1529972484084731911) duration check: true
  [2026/07/23 14:04:37.887 GMT+00:00] [INFO] repository dist full path is /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-4
  Getting Git version info >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:04:37.892 GMT+00:00] [INFO] run git command --> git version
  [2026/07/23 14:04:37.899 GMT+00:00] [INFO] run git command stdout --> git version 2.43.0
  
  [2026/07/23 14:04:37.901 GMT+00:00] [INFO] Deleting the contents of '/home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-4'
  initialize git repository >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:04:37.902 GMT+00:00] [INFO] run git command --> git init
  [2026/07/23 14:04:37.908 GMT+00:00] [INFO] run git command stdout --> Initialized empty Git repository in /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-4/.git/
  [2026/07/23 14:04:37.908 GMT+00:00] [INFO] run git command --> git remote add origin https://gitcode.com/ComputingActionTest/gitcode-test-4.git
  [2026/07/23 14:04:37.912 GMT+00:00] [INFO] git repository initialized at /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-4
  
  Disabling automatic garbage collection >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:04:37.912 GMT+00:00] [INFO] run git command --> git config --local gc.auto 0
  
  Setting up auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:04:37.916 GMT+00:00] [INFO] Removing SSH command configuration
  [2026/07/23 14:04:37.916 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
  [2026/07/23 14:04:37.920 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
  [2026/07/23 14:04:37.939 GMT+00:00] [INFO] Removing HTTP extra header
  [2026/07/23 14:04:37.939 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
  [2026/07/23 14:04:37.942 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
  [2026/07/23 14:04:37.961 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
  [2026/07/23 14:04:37.969 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'
  [2026/07/23 14:04:37.987 GMT+00:00] [INFO] configuring token
  [2026/07/23 14:04:37.993 GMT+00:00] [INFO] configuring token config local
  
  Start fetch git repo >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:04:38.003 GMT+00:00] [INFO] run git command --> git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --progress --depth=1 origin +refs/heads/main*:refs/remotes/origin/main* +refs/tags/main*:refs/tags/main*
  
  Checking out the ref >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:04:38.530 GMT+00:00] [INFO] run git command --> git branch --list --remote origin/main
  [2026/07/23 14:04:38.533 GMT+00:00] [INFO] run git command stdout -->   origin/main
  [2026/07/23 14:04:38.534 GMT+00:00] [INFO] run git command --> git checkout --progress --force -B main refs/remotes/origin/main
  [2026/07/23 14:04:38.539 GMT+00:00] [INFO] run git command stdout --> branch 'main' set up to track 'origin/main'.
  
  Removing auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:04:38.548 GMT+00:00] [INFO] Removing SSH command configuration
  [2026/07/23 14:04:38.548 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
  [2026/07/23 14:04:38.551 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
  [2026/07/23 14:04:38.570 GMT+00:00] [INFO] Removing HTTP extra header
  [2026/07/23 14:04:38.571 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
  [2026/07/23 14:04:38.574 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
  [2026/07/23 14:04:38.594 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
  [2026/07/23 14:04:38.618 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'
  
  
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/a4891b7f-e216-4587-91dd-acfb9c9bfd8d.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/a4891b7f-e216-4587-91dd-acfb9c9bfd8d.sh
  REPOSITORY_PERM_OK
```

- **预期行为**（Phase 01 文本用例 `COMPAT-PERM-01-004`，优先级 P0，维度 兼容性）:
  - 前置条件: - 仓库支持 permissions 字段解析
    - 平台已配置 repository 权限域
  - 操作步骤: 1. 在工作流中声明 `permissions: { repository: read }`
    2. 在工作流步骤中执行 clone 或读取仓库内容的操作
    3. 验证权限正常生效，工作流可完成仓库读取
  - 预期结果: - `repository: read` 被平台正确解析并生效
    - 工作流可正常执行 clone 和读取仓库内容
    - GitCode 风格的权限命名与平台语义一致
  - 验证点: - [正向] workflow 解析阶段无报错
    - [正向] 工作流成功执行仓库读取操作
    - [正向] repository 权限项语义与 GitCode 平台预期一致

- **实际行为**:
  - Job "Verify repository permission works" status=COMPLETED

- **对照 GitCode 规格**:
  - 文本用例参照来源: `inputs/security-knowledge/issues.md; inputs/github-reference/security/`

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (manual)
  - Phase 01 前置条件: - 仓库支持 permissions 字段解析
    - 平台已配置 repository 权限域

**置信度**: 中（job 执行成功但断言评判未通过，需进一步确认断言逻辑）

**影响**:
- **阻塞性**: 🟡非阻塞 — job 执行成功，功能正常
- **静默性**: 🟢明确报错 — 断言差异可通过 logs/assertions 定位
- **影响面**: 🟢单用例 — 仅本用例断言未通过
- **综合**: 基于上述证据，COMPAT-PERM-01-004 的失败根因初步判定为 **标记不匹配**（责任人: **Phase 01**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可调整断言评判规则或补充环境配置

**建议**:
- 复查断言评判器对 COMPAT-PERM-01-004 的判断逻辑
- 相关用例: COMPAT-PERM-01-001
