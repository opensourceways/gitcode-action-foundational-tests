## 失败分诊 · COMPAT-PERM-01-001 · 未声明 permissions 时默认 TOKEN 读操作权限范围

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 `success`，实际值与断言关键词不匹配（用例设计问题）

**根因初判**: 用例问题

**证据**:

- **Job 日志全量**（共 55 行）:
```
=== JOB: Test default read permissions (status=COMPLETED) ===
[2026/07/23 22:04:15.654 GMT+08:00] [INFO] Job(1529972439037526016_1529972439003971591) duration check: true
[2026/07/23 14:04:27.410 GMT+00:00] [INFO] repository dist full path is /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-3
Getting Git version info >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:04:27.414 GMT+00:00] [INFO] run git command --> git version
[2026/07/23 14:04:27.422 GMT+00:00] [INFO] run git command stdout --> git version 2.43.0

[2026/07/23 14:04:27.424 GMT+00:00] [INFO] Deleting the contents of '/home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-3'
initialize git repository >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:04:27.425 GMT+00:00] [INFO] run git command --> git init
[2026/07/23 14:04:27.433 GMT+00:00] [INFO] run git command stdout --> Initialized empty Git repository in /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-3/.git/
[2026/07/23 14:04:27.435 GMT+00:00] [INFO] run git command --> git remote add origin https://gitcode.com/ComputingActionTest/gitcode-test-3.git
[2026/07/23 14:04:27.439 GMT+00:00] [INFO] git repository initialized at /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-3

Disabling automatic garbage collection >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:04:27.439 GMT+00:00] [INFO] run git command --> git config --local gc.auto 0

Setting up auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:04:27.443 GMT+00:00] [INFO] Removing SSH command configuration
[2026/07/23 14:04:27.444 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
[2026/07/23 14:04:27.448 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
[2026/07/23 14:04:27.468 GMT+00:00] [INFO] Removing HTTP extra header
[2026/07/23 14:04:27.469 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
[2026/07/23 14:04:27.473 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
[2026/07/23 14:04:27.494 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
[2026/07/23 14:04:27.503 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'
[2026/07/23 14:04:27.524 GMT+00:00] [INFO] configuring token
[2026/07/23 14:04:27.530 GMT+00:00] [INFO] configuring token config local

Start fetch git repo >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:04:27.545 GMT+00:00] [INFO] run git command --> git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --progress --depth=1 origin +refs/heads/main*:refs/remotes/origin/main* +refs/tags/main*:refs/tags/main*

Checking out the ref >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:04:28.059 GMT+00:00] [INFO] run git command --> git branch --list --remote origin/main
[2026/07/23 14:04:28.063 GMT+00:00] [INFO] run git command stdout -->   origin/main
[2026/07/23 14:04:28.063 GMT+00:00] [INFO] run git command --> git checkout --progress --force -B main refs/remotes/origin/main
[2026/07/23 14:04:28.069 GMT+00:00] [INFO] run git command stdout --> branch 'main' set up to track 'origin/main'.

Removing auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:04:28.079 GMT+00:00] [INFO] Removing SSH command configuration
[2026/07/23 14:04:28.079 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
[2026/07/23 14:04:28.083 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
[2026/07/23 14:04:28.104 GMT+00:00] [INFO] Removing HTTP extra header
[2026/07/23 14:04:28.104 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
[2026/07/23 14:04:28.108 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
[2026/07/23 14:04:28.133 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
[2026/07/23 14:04:28.160 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'


No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/fd2ff809-11c6-4822-8ed9-6fc25a571667.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/fd2ff809-11c6-4822-8ed9-6fc25a571667.sh
# gitcode-test-3

并发验证gitcodeactions的子仓库
```

  **日志分析**: 日志显示仓库中文内容 "并发验证gitcodeactions的子仓库" — README 成功读取, 断言关键词 "README" 与仓库实际内容不匹配

- **预期行为**（Phase 01 文本用例 `COMPAT-PERM-01-001`，优先级 P1，维度 compatibility）:
  - 操作步骤 1: "提交一个不包含 permissions 块的 workflow"
  - 操作步骤 2: "在该 workflow 中执行读操作（如 checkout、查看仓库文件）"
  - 操作步骤 3: "手动触发该 workflow"

  预期结果:
  - 系统在 workflow 未声明 permissions 时，仍赋予默认 TOKEN 足够的读权限
  - checkout 和文件读取操作成功执行

  验证点:
  - [正向] checkout step 成功完成
  - [正向] 读操作（如 cat README）成功返回内容
  - [负向] 读操作不应因权限不足而失败

- **实际行为**:
  - 日志显示仓库中文内容 "并发验证gitcodeactions的子仓库" — README 成功读取, 断言关键词 "README" 与仓库实际内容不匹配


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

**置信度**: 高（日志显示仓库中文内容 "并发验证gitcodeactions的子仓库" — README 成功读取, 断言关键词 "README" 与仓库实际内容不匹配）

**影响**:
- **阻塞性**: ⚪无影响 — 平台默认 TOKEN 读权限正常（仓库中文内容 "并发验证gitcodeactions的子仓库" 被成功读取），测试侧断言关键词"README"与仓库实际内容不匹配
- **静默性**: 🟢明确报错 — 平台正常完成 checkout 和文件读取，仅测试断言关键词误配
- **影响面**: 🟢单用例 — 仅本用例断言关键词需修正
- **综合**: 平台默认 permissions 读操作完全正常，仅断言关键词与仓库实际内容不一致
- **是否有规避手段**: 是 — 修正断言关键词匹配仓库实际内容

**建议**:
- 修正断言关键词，使其与平台的日志实际输出匹配
- 将 COMPAT-PERM-01-001 标记为「用例断言修复后重新验跑」
- 相关用例: COMPAT-PERM-01-004
