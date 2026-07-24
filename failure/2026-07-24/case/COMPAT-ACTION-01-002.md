## 失败分诊 · COMPAT-ACTION-01-002 · checkout 短名等价性——path 参数支持

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 `completed_success`，实际 `COMPLETED`（平台 API 返回大写枚举值，与合约期望的小写语义值不匹配）

**根因初判**: 标记不匹配

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

  **日志分析**: "CHECKOUT_PATH_OK" — checkout path 正常, run=COMPLETED

- **预期行为**（Phase 01 文本用例 `COMPAT-ACTION-01-002`，优先级 P1，维度 compatibility）:
  - 操作步骤 1: "在工作流中使用 `uses: checkout` 并传入 `path: subdir/checkout-path` 参数"
  - 操作步骤 2: "触发工作流，观察 checkout 行为"
  - 操作步骤 3: "在后续步骤中验证代码是否被检出到指定子目录"

  预期结果:
  - `uses: checkout` 配合 path 参数可将代码检出到指定子目录
  - 裸插件名写法与 GitHub 全名写法在行为上等价
  - 后续步骤可在指定子目录中访问仓库文件

  验证点:
  - [正向] checkout 步骤成功完成，无报错
  - [正向] 指定子目录下存在仓库文件
  - [负向] 不应因使用裸插件名而解析失败
  - [负向] 不应将代码检出到默认工作目录以外的意外位置

- **实际行为**:
  - "CHECKOUT_PATH_OK" — checkout path 正常, run=COMPLETED


- **测试 YAML 与规格精确对照**:
  - 规格文件: `using-actions.md` (路径: `phase01/inputs/gitcode-spec/writing-pipelines/using-actions.md`)
  - 规格节选:
```yaml
steps:
  - uses: checkout
# 裸插件名等价于全名写法
```
    该规格明确声明: 使用 actions 插件的基本语法

  测试 YAML 的写法与规格示例一致，证明平台文档确凿承诺了该行为。

**置信度**: 高（"CHECKOUT_PATH_OK" — checkout path 正常, run=COMPLETED）

**影响**:
- **阻塞性**: ⚪无影响 — 平台 checkout 短名 path 参数正常（CHECKOUT_PATH_OK），断言标记 COMPLETED≠success
- **静默性**: 🟢明确报错 — 平台正常 checkout 到指定路径，仅测试断言词汇不一致
- **影响面**: 🟢单用例 — 仅本用例断言标记需修复
- **综合**: checkout 裸插件名 path 参数功能完全正常，仅断言词汇不匹配
- **是否有规避手段**: 是 — 修复 run_status 词汇映射

**建议**:
- 修复 `compile_asserts.py` 中的 run_status 词汇映射：`COMPLETED→success, FAILED→failure, CANCELED→canceled`
- 将 COMPAT-ACTION-01-002 标记为「用例断言修复后应重新验跑」
- 相关用例: COMPAT-ACTION-01-001
