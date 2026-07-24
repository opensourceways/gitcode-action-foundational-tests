## 失败分诊 · COMPAT-PERM-01-004 · permissions 命名差异——GitCode repository 权限项正常生效

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 `completed_success`，实际 `COMPLETED`（平台 API 返回大写枚举值，与合约期望的小写语义值不匹配）

**根因初判**: 标记不匹配

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

  **日志分析**: "REPOSITORY_PERM_OK" — permissions 正常, run=COMPLETED

- **预期行为**（Phase 01 文本用例 `COMPAT-PERM-01-004`，优先级 P1，维度 compatibility）:
  - 操作步骤 1: "在工作流中声明 `permissions: { repository: read }`"
  - 操作步骤 2: "在工作流步骤中执行 clone 或读取仓库内容的操作"
  - 操作步骤 3: "验证权限正常生效，工作流可完成仓库读取"

  预期结果:
  - `repository: read` 被平台正确解析并生效
  - 工作流可正常执行 clone 和读取仓库内容
  - GitCode 风格的权限命名与平台语义一致

  验证点:
  - [正向] workflow 解析阶段无报错
  - [正向] 工作流成功执行仓库读取操作
  - [正向] repository 权限项语义与 GitCode 平台预期一致

- **实际行为**:
  - "REPOSITORY_PERM_OK" — permissions 正常, run=COMPLETED


- **测试 YAML 与规格精确对照**:
  - 规格文件: `token-permissions.md` (路径: `phase01/inputs/gitcode-spec/security-permissions/token-permissions.md`)
  - 规格节选:
```yaml
permissions:
  repository: read
  pr: write
  issue: none
```
    该规格明确声明: 26-35行的 permissions 字段详解

  测试 YAML 的写法与规格示例一致，证明平台文档确凿承诺了该行为。

**置信度**: 高（"REPOSITORY_PERM_OK" — permissions 正常, run=COMPLETED）

**建议**:
- 修复 `compile_asserts.py` 中的 run_status 词汇映射：`COMPLETED→success, FAILED→failure, CANCELED→canceled`
- 将 COMPAT-PERM-01-004 标记为「用例断言修复后应重新验跑」
- 相关用例: COMPAT-PERM-01-001
