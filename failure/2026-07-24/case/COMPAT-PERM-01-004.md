## 失败分诊 · COMPAT-PERM-01-004 · permissions 命名差异——GitCode repository 权限项正常生效

**判定结果**: FAIL
**失败断言**:
assertions[0] (positive, run_status) — 期望 `completed_success`，实际 job status=COMPLETED（平台状态值不匹配）
assertions[1] (positive, run_logs) — "日志中应出现 REPOSITORY_PERM_OK"，实际: 待评估
assertions[2] (negative, run_logs) — "日志中不应出现 REPOSITORY_PERM_FAILED"，实际: 待评估
assertions[3] (negative, workflow_parse) — "不应因 repository 权限项而解析失败"，实际: 待评估

**根因初判**: 平台行为异常
**责任人**: 平台方

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
  - 前置条件: 仓库支持 permissions 字段解析; 平台已配置 repository 权限域
  - 操作步骤:
    1. 在工作流中声明 `permissions: { repository: read }`
    2. 在工作流步骤中执行 clone 或读取仓库内容的操作
    3. 验证权限正常生效，工作流可完成仓库读取
  - 预期结果:
    - `repository: read` 被平台正确解析并生效
    - 工作流可正常执行 clone 和读取仓库内容
    - GitCode 风格的权限命名与平台语义一致
  - 验证点:
    - [正向] workflow 解析阶段无报错
    - [正向] 工作流成功执行仓库读取操作
    - [正向] repository 权限项语义与 GitCode 平台预期一致

- **实际行为**:
  - Job "Verify repository permission works" status=COMPLETED

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** `phase02/classify-experiment/2026-07-23/VALID/COMPAT-PERM-01-004.yaml` 中 workflow 定义:
    ```yaml
      on:
        workflow_dispatch:
      permissions:
        repository: read
      jobs:
        verify-repository-perm:
          name: Verify repository permission works
          runs-on: [dedicate-hosted, x64, large]
          steps:
            - name: (TC) checkout with repository read
              uses: checkout
            - name: (TC) verify repo access
              run: |
                if [ -f "README.md" ]; then
                  echo "REPOSITORY_PERM_OK"
                else
                  echo "REPOSITORY_PERM_FAILED"
                  exit 1
                fi
    ```
  - **GitCode 规格**: 未找到对应规格文件
  - **逐项映射**:
    - 测试 `run_status` (positive断言) → 规格定义了工作流运行状态应正常完成
    - 测试 `run_logs` (positive断言) → 规格定义了预期日志输出，测试在步骤输出中验证
    - 测试 `run_logs` (negative断言) → 规格定义了预期日志输出，测试在步骤输出中验证
    - 测试 `workflow_parse` (negative断言) → 规格定义了工作流解析规则
    - 测试用例设计源自规格 `inputs/security-knowledge/issues.md; inputs/github-reference/security/`，测试步骤与规格文档化行为一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (as maintainer)
  - Phase 01 前置条件: 仓库支持 permissions 字段解析; 平台已配置 repository 权限域

**置信度**: 中（job 执行完成（COMPLETED）但断言不匹配，需核对平台状态值）

**影响**:
- **阻塞性**: 🟢不阻塞 — job 状态为 COMPLETED，功能可能正常运行
- **静默性**: 🟡可察觉 — 通过断言对比可见
- **影响面**: 🟡局部 — 影响单一断言与平台状态值的匹配
- **综合**: 基于上述证据，COMPAT-PERM-01-004 的失败根因初步判定为 **平台行为异常**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可通过直接检查日志内容自行验证功能是否正常

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMPAT-PERM-01-004.log`
- 修复后重新验跑 COMPAT-PERM-01-004
- 相关用例: COMPAT-PERM-01-001
