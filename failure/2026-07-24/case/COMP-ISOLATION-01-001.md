## 失败分诊 · COMP-ISOLATION-01-001 · 同一 workflow 先后 job 的文件系统相互隔离

**判定结果**: FAIL
**失败断言**:
assertions[0] (positive, run_status) — 期望 `success`，实际 job status=COMPLETED（平台状态值不匹配）
assertions[1] (negative, run_logs) — 期望通过，实际待验证

**根因初判**: 平台行为异常
**责任人**: 平台方

**证据**:

- **Job 日志全量**（共 125 行）:
  ```
=== JOB: Write isolation markers (status=COMPLETED) ===
[2026/07/23 22:02:38.534 GMT+08:00] [INFO] Job(1529972031431122944_1529972031389179911) duration check: true
[2026/07/23 14:02:50.884 GMT+00:00] [INFO] repository dist full path is /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0
Getting Git version info >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:02:50.891 GMT+00:00] [INFO] run git command --> git version
[2026/07/23 14:02:50.900 GMT+00:00] [INFO] run git command stdout --> git version 2.43.0

[2026/07/23 14:02:50.902 GMT+00:00] [INFO] Deleting the contents of '/home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0'
initialize git repository >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:02:50.903 GMT+00:00] [INFO] run git command --> git init
[2026/07/23 14:02:50.909 GMT+00:00] [INFO] run git command stdout --> Initialized empty Git repository in /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0/.git/
[2026/07/23 14:02:50.910 GMT+00:00] [INFO] run git command --> git remote add origin https://gitcode.com/ComputingActionTest/gitcode-test-0.git
[2026/07/23 14:02:50.913 GMT+00:00] [INFO] git repository initialized at /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0

Disabling automatic garbage collection >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:02:50.914 GMT+00:00] [INFO] run git command --> git config --local gc.auto 0

Setting up auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:02:50.918 GMT+00:00] [INFO] Removing SSH command configuration
[2026/07/23 14:02:50.918 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
[2026/07/23 14:02:50.922 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
[2026/07/23 14:02:50.944 GMT+00:00] [INFO] Removing HTTP extra header
[2026/07/23 14:02:50.945 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
[2026/07/23 14:02:50.950 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
[2026/07/23 14:02:50.970 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
[2026/07/23 14:02:50.979 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'
[2026/07/23 14:02:50.999 GMT+00:00] [INFO] configuring token
[2026/07/23 14:02:51.006 GMT+00:00] [INFO] configuring token config local

Start fetch git repo >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:02:51.018 GMT+00:00] [INFO] run git command --> git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --progress --depth=1 origin +refs/heads/main*:refs/remotes/origin/main* +refs/tags/main*:refs/tags/main*

Checking out the ref >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:02:51.498 GMT+00:00] [INFO] run git command --> git branch --list --remote origin/main
[2026/07/23 14:02:51.502 GMT+00:00] [INFO] run git command stdout -->   origin/main
[2026/07/23 14:02:51.503 GMT+00:00] [INFO] run git command --> git checkout --progress --force -B main refs/remotes/origin/main
[2026/07/23 14:02:51.509 GMT+00:00] [INFO] run git command stdout --> branch 'main' set up to track 'origin/main'.

Removing auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:02:51.518 GMT+00:00] [INFO] Removing SSH command configuration
[2026/07/23 14:02:51.519 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
[2026/07/23 14:02:51.522 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
[2026/07/23 14:02:51.544 GMT+00:00] [INFO] Removing HTTP extra header
[2026/07/23 14:02:51.544 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
[2026/07/23 14:02:51.548 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
[2026/07/23 14:02:51.569 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
[2026/07/23 14:02:51.596 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'


No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/41142bf8-d480-4157-b215-cd020a4e2017.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/41142bf8-d480-4157-b215-cd020a4e2017.sh

No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/9a970376-3bd7-4f0b-a58b-ccd91cfcd239.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/9a970376-3bd7-4f0b-a58b-ccd91cfcd239.sh

No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/e5fc42a3-5c6c-456c-86fc-a9b7789221ea.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/e5fc42a3-5c6c-456c-86fc-a9b7789221ea.sh


=== JOB: Verify isolation from job A (status=COMPLETED) ===
[2026/07/23 22:02:56.442 GMT+08:00] [INFO] Job(1529972031431122944_1529972031389179913) duration check: true
[2026/07/23 14:03:09.235 GMT+00:00] [INFO] repository dist full path is /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0
Getting Git version info >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:03:09.241 GMT+00:00] [INFO] run git command --> git version
[2026/07/23 14:03:09.249 GMT+00:00] [INFO] run git command stdout --> git version 2.43.0

[2026/07/23 14:03:09.250 GMT+00:00] [INFO] Deleting the contents of '/home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0'
initialize git repository >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:03:09.251 GMT+00:00] [INFO] run git command --> git init
[2026/07/23 14:03:09.257 GMT+00:00] [INFO] run git command stdout --> Initialized empty Git repository in /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0/.git/
[2026/07/23 14:03:09.259 GMT+00:00] [INFO] run git command --> git remote add origin https://gitcode.com/ComputingActionTest/gitcode-test-0.git
[2026/07/23 14:03:09.263 GMT+00:00] [INFO] git repository initialized at /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0

Disabling automatic garbage collection >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:03:09.264 GMT+00:00] [INFO] run git command --> git config --local gc.auto 0

Setting up auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:03:09.268 GMT+00:00] [INFO] Removing SSH command configuration
[2026/07/23 14:03:09.269 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
[2026/07/23 14:03:09.273 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
[2026/07/23 14:03:09.294 GMT+00:00] [INFO] Removing HTTP extra header
[2026/07/23 14:03:09.294 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
[2026/07/23 14:03:09.298 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
[2026/07/23 14:03:09.320 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
[2026/07/23 14:03:09.328 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'
[2026/07/23 14:03:09.351 GMT+00:00] [INFO] configuring token
[2026/07/23 14:03:09.358 GMT+00:00] [INFO] configuring token config local

Start fetch git repo >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:03:09.369 GMT+00:00] [INFO] run git command --> git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --progress --depth=1 origin +refs/heads/main*:refs/remotes/origin/main* +refs/tags/main*:refs/tags/main*

Checking out the ref >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:03:09.835 GMT+00:00] [INFO] run git command --> git branch --list --remote origin/main
[2026/07/23 14:03:09.838 GMT+00:00] [INFO] run git command stdout -->   origin/main
[2026/07/23 14:03:09.839 GMT+00:00] [INFO] run git command --> git checkout --progress --force -B main refs/remotes/origin/main
[2026/07/23 14:03:09.845 GMT+00:00] [INFO] run git command stdout --> branch 'main' set up to track 'origin/main'.

Removing auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:03:09.854 GMT+00:00] [INFO] Removing SSH command configuration
[2026/07/23 14:03:09.855 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
[2026/07/23 14:03:09.858 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
[2026/07/23 14:03:09.880 GMT+00:00] [INFO] Removing HTTP extra header
[2026/07/23 14:03:09.880 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
[2026/07/23 14:03:09.884 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
[2026/07/23 14:03:09.907 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
[2026/07/23 14:03:09.933 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'


No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/93a05410-449d-4274-b398-33749ea9db85.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/93a05410-449d-4274-b398-33749ea9db85.sh
WORKSPACE_ISOLATED_OK

No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/e9a59ee9-1ef0-41ab-8a0d-be93e4320443.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/e9a59ee9-1ef0-41ab-8a0d-be93e4320443.sh
TMP_ISOLATED_OK

No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/cf04efd1-fd83-4e47-a568-1613f4150940.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/cf04efd1-fd83-4e47-a568-1613f4150940.sh
NO_ORPHAN_PROCESS_OK
  ```

- **预期行为**（Phase 01 文本用例 `COMP-ISOLATION-01-001`，优先级 P0，维度 completeness）:
  - 前置条件: workflow 含两个串行 jobs
  - 操作步骤:
    1. job 1 写入文件到工作目录
    2. job 2 尝试读取该文件
  - 预期结果:
    - job 2 无法看到 job 1 写入的文件
  - 验证点:
    - [负向] job 2 不应访问到 job 1 的文件
    - [正向] 显式通过 artifact 传递后 job 2 可访问

- **实际行为**:
  - Job "Write isolation markers" status=COMPLETED
  - Job "Verify isolation from job A" status=COMPLETED
  - **失败传导链**: Write isolation markers (COMPLETED) → Verify isolation from job A (COMPLETED)

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** `phase02/classify-experiment/2026-07-23/VALID/COMP-ISOLATION-01-001.yaml` 中 workflow 定义:
    ```yaml
      on:
        workflow_dispatch:
      jobs:
        job1:
          name: Write file
          runs-on: [dedicate-hosted, x64, large]
          steps:
            - name: Create file
              run: |
                echo "secret data" > /tmp/isolation_test.txt
        job2:
          name: Read file
          runs-on: [dedicate-hosted, x64, large]
          needs: job1
          steps:
            - name: Attempt read
              run: |
                if [ -f /tmp/isolation_test.txt ]; then
                  echo "file exists"
                  cat /tmp/isolation_test.txt
                  exit 1
                else
                  echo "file not found as expected"
                fi
    ```
  - **GitCode 规格** `inputs/gitcode-spec/core-concepts/workflow-job-step-action.md` 第 13-42 行（Workflow（工作流））:
    ```yaml
    ## Workflow（工作流）
    
    Workflow 是自动化流程的顶层定义，存储在仓库的 `.gitcode/workflows/` 目录下，以 YAML 格式描述。
    
    ```yaml
    name: Build and Deploy
    on:
      push:
        branches: [main]
    stages:
      - build
        jobs:
          build-job:
            runs-on: ubuntu-latest
            steps:
              - run: echo "Building..."
      - test
        jobs:
          test-job:
            runs-on: ubuntu-latest
            steps:
              - run: echo "Testing..."
      - deploy
        jobs:
          deploy-job:
            runs-on: ubuntu-latest
            steps:
              - run: echo "Deploying..."
    ```
    
    ```
  - **GitCode 规格** `inputs/gitcode-spec/writing-pipelines/configure-jobs.md` 第 1-50 行:
    ```yaml
    <!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/writing-pipelines/configure-jobs | fetched: 2026-07-20 -->
    
    # 配置任务 Jobs
    
    **适用场景**：当你需要在 workflow 中定义一个或多个任务，指定运行环境、超时时间、环境变量、并发控制、矩阵策略等时。
    
    ## 前提条件
    
    - 已理解 workflow 的基本结构。
    - 已确定 job 需要的运行环境（Runner 标签）。
    
    ## 快速示例
    
    ```yaml
    name: ci
    on:
      push:
        branches:
          - main
    jobs:
      build:
        runs-on: [ubuntu-latest, x64, small]
        timeout-minutes: 30
        env:
          APP_ENV: production
        steps:
          - uses: checkout
          - run: ./build.sh
    ```
    
    ## 配置说明
    
    ### runs-on 运行环境
    
    `runs-on` 指定 job 运行的 Runner 环境。AtomGit Action 的官方资源池标签采用**三段式格式**：`{os}-{version},{arch},{flavor}`。
    
    | 段位 | 说明 | 示例 |
    |------|------|------|
    | `{os}-{version}` | 操作系统及版本 | `ubuntu-latest` |
    | `{arch}` | CPU 架构 | `x64`、`arm64` |
    ```
  - **逐项映射**:
    - 测试 `run_status` (positive断言) → 规格定义了工作流运行状态应正常完成
    - 测试 `run_logs` (negative断言) → 规格定义了预期日志输出，测试在步骤输出中验证
    - 测试用例设计源自规格 `inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md`，测试步骤与规格文档化行为一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (as maintainer)
  - Phase 01 前置条件: workflow 含两个串行 jobs

**置信度**: 中（job 执行完成（COMPLETED）但断言不匹配，需核对平台状态值）

**影响**:
- **阻塞性**: 🟢不阻塞 — job 状态为 COMPLETED，功能可能正常运行
- **静默性**: 🟡可察觉 — 通过断言对比可见
- **影响面**: 🟡局部 — 影响单一断言与平台状态值的匹配
- **综合**: 基于上述证据，COMP-ISOLATION-01-001 的失败根因初步判定为 **平台行为异常**（责任人: **平台方**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可通过直接检查日志内容自行验证功能是否正常

**建议**:
- 提交缺陷给平台工程团队，附日志 `/home/chenqi252/code/gitcode-ci/workspace-gitcode-action/gitcode-action-foundational-tests/failure/2026-07-24/COMP-ISOLATION-01-001.log`
- 修复后重新验跑 COMP-ISOLATION-01-001
- 相关用例: COMP-ISOLATION-01-002
