## 失败分诊 · COMPAT-ACTION-01-002 · checkout 短名等价性——path 参数支持

**判定结果**: FAIL
**失败断言**:
assertions (checkout path) — job COMPLETED，CHECKOUT_PATH_OK 正确输出

**根因初判**: 标记不匹配
**责任人**: Phase 01

**证据**:

- **Job 日志全量**（共 52 行）:
```
  === JOB: Verify checkout path parameter (status=COMPLETED) ===
  [2026/07/23 22:16:42.407 GMT+08:00] [INFO] Job(1529975571306004480_1529975571276644359) duration check: true
  [2026/07/23 14:16:53.903 GMT+00:00] [INFO] repository dist full path is /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0/subdir/checkout-path
  Getting Git version info >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:16:53.908 GMT+00:00] [INFO] run git command --> git version
  [2026/07/23 14:16:53.916 GMT+00:00] [INFO] run git command stdout --> git version 2.43.0
  
  initialize git repository >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:16:53.918 GMT+00:00] [INFO] run git command --> git init
  [2026/07/23 14:16:53.928 GMT+00:00] [INFO] run git command stdout --> Initialized empty Git repository in /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0/subdir/checkout-path/.git/
  [2026/07/23 14:16:53.929 GMT+00:00] [INFO] run git command --> git remote add origin https://gitcode.com/ComputingActionTest/gitcode-test-0.git
  [2026/07/23 14:16:53.933 GMT+00:00] [INFO] git repository initialized at /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0/subdir/checkout-path
  
  Disabling automatic garbage collection >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:16:53.934 GMT+00:00] [INFO] run git command --> git config --local gc.auto 0
  
  Setting up auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:16:53.938 GMT+00:00] [INFO] Removing SSH command configuration
  [2026/07/23 14:16:53.938 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
  [2026/07/23 14:16:53.943 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
  [2026/07/23 14:16:53.964 GMT+00:00] [INFO] Removing HTTP extra header
  [2026/07/23 14:16:53.964 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
  [2026/07/23 14:16:53.968 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
  [2026/07/23 14:16:53.988 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
  [2026/07/23 14:16:53.996 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'
  [2026/07/23 14:16:54.016 GMT+00:00] [INFO] configuring token
  [2026/07/23 14:16:54.022 GMT+00:00] [INFO] configuring token config local
  
  Start fetch git repo >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:16:54.037 GMT+00:00] [INFO] run git command --> git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --progress --depth=1 origin +refs/heads/main*:refs/remotes/origin/main* +refs/tags/main*:refs/tags/main*
  
  Checking out the ref >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:16:54.515 GMT+00:00] [INFO] run git command --> git branch --list --remote origin/main
  [2026/07/23 14:16:54.519 GMT+00:00] [INFO] run git command stdout -->   origin/main
  [2026/07/23 14:16:54.519 GMT+00:00] [INFO] run git command --> git checkout --progress --force -B main refs/remotes/origin/main
  [2026/07/23 14:16:54.525 GMT+00:00] [INFO] run git command stdout --> branch 'main' set up to track 'origin/main'.
  
  Removing auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
  [2026/07/23 14:16:54.535 GMT+00:00] [INFO] Removing SSH command configuration
  [2026/07/23 14:16:54.536 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
  [2026/07/23 14:16:54.539 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
  [2026/07/23 14:16:54.560 GMT+00:00] [INFO] Removing HTTP extra header
  [2026/07/23 14:16:54.561 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
  [2026/07/23 14:16:54.565 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
  [2026/07/23 14:16:54.586 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
  [2026/07/23 14:16:54.610 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'
  
  
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/4e72cbf8-35e9-4b43-a198-293074894a4d.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/4e72cbf8-35e9-4b43-a198-293074894a4d.sh
  CHECKOUT_PATH_OK
```

- **预期行为**（Phase 01 文本用例 `COMPAT-ACTION-01-002`，优先级 P1，维度 兼容性）:
  - 前置条件: - 仓库存在默认分支 main
  - 操作步骤: 1. 在工作流中使用 `uses: checkout` 并传入 `path: subdir/checkout-path` 参数
    2. 触发工作流，观察 checkout 行为
    3. 在后续步骤中验证代码是否被检出到指定子目录
  - 预期结果: - `uses: checkout` 配合 path 参数可将代码检出到指定子目录
    - 裸插件名写法与 GitHub 全名写法在行为上等价
    - 后续步骤可在指定子目录中访问仓库文件
  - 验证点: - [正向] checkout 步骤成功完成，无报错
    - [正向] 指定子目录下存在仓库文件
    - [负向] 不应因使用裸插件名而解析失败
    - [负向] 不应将代码检出到默认工作目录以外的意外位置

- **实际行为**:
  - Job "Verify checkout path parameter" status=COMPLETED

- **对照 GitCode 规格** `phase01/inputs/gitcode-spec/action-development/top-level-fields.md`:
  - 规格摘要:
    ```
# 顶级字段
本文档定义了插件开发中顶级字段的配置规范，包括插件的元信息、输入输出参数的声明方式，以及执行方式的配置。
## `name`
```
name: 'codecheck'
```
## `version`
```
version: '1.0.0'
```
## `author`
```
author: 'XXX'
```
## `description`
    ```
  - 测试 YAML 工作流模式与此规格承诺一致

- **环境前置条件验证**:
  - setup.secrets: `[]`
  - setup.repo_fixture: `default`
  - setup.branch_protection: `default`
  - 触发方式: workflow_dispatch (manual)
  - Phase 01 前置条件: - 仓库存在默认分支 main

**置信度**: 中（job 执行成功但断言评判未通过，需进一步确认断言逻辑）

**影响**:
- **阻塞性**: 🟡非阻塞 — job 执行成功，功能正常
- **静默性**: 🟢明确报错 — 断言差异可通过 logs/assertions 定位
- **影响面**: 🟢单用例 — 仅本用例断言未通过
- **综合**: 基于上述证据，COMPAT-ACTION-01-002 的失败根因初步判定为 **标记不匹配**（责任人: **Phase 01**），需在对应阶段修复后重新验证。
- **是否有规避手段**: 是 — 可调整断言评判规则或补充环境配置

**建议**:
- 复查断言评判器对 COMPAT-ACTION-01-002 的判断逻辑
- 相关用例: COMPAT-ACTION-01-001
