## 失败分诊 · COMPAT-ACTION-01-001 · checkout 短名等价性——ref 参数支持

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 `completed_success`，实际 `COMPLETED`（平台 API 返回大写枚举值，与合约期望的小写语义值不匹配）

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（共 53 行）:
```
=== JOB: Verify checkout ref parameter (status=COMPLETED) ===
[2026/07/23 22:16:32.689 GMT+08:00] [INFO] Job(1529975526330863616_1529975526309892103) duration check: true
[2026/07/23 14:16:44.151 GMT+00:00] [INFO] repository dist full path is /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0
Getting Git version info >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:16:44.156 GMT+00:00] [INFO] run git command --> git version
[2026/07/23 14:16:44.164 GMT+00:00] [INFO] run git command stdout --> git version 2.43.0

[2026/07/23 14:16:44.165 GMT+00:00] [INFO] Deleting the contents of '/home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0'
initialize git repository >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:16:44.166 GMT+00:00] [INFO] run git command --> git init
[2026/07/23 14:16:44.172 GMT+00:00] [INFO] run git command stdout --> Initialized empty Git repository in /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0/.git/
[2026/07/23 14:16:44.173 GMT+00:00] [INFO] run git command --> git remote add origin https://gitcode.com/ComputingActionTest/gitcode-test-0.git
[2026/07/23 14:16:44.176 GMT+00:00] [INFO] git repository initialized at /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0

Disabling automatic garbage collection >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:16:44.177 GMT+00:00] [INFO] run git command --> git config --local gc.auto 0

Setting up auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:16:44.181 GMT+00:00] [INFO] Removing SSH command configuration
[2026/07/23 14:16:44.181 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
[2026/07/23 14:16:44.185 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
[2026/07/23 14:16:44.206 GMT+00:00] [INFO] Removing HTTP extra header
[2026/07/23 14:16:44.207 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
[2026/07/23 14:16:44.211 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
[2026/07/23 14:16:44.231 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
[2026/07/23 14:16:44.238 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'
[2026/07/23 14:16:44.257 GMT+00:00] [INFO] configuring token
[2026/07/23 14:16:44.263 GMT+00:00] [INFO] configuring token config local

Start fetch git repo >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:16:44.274 GMT+00:00] [INFO] run git command --> git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --progress --depth=1 origin +refs/heads/main*:refs/remotes/origin/main* +refs/tags/main*:refs/tags/main*

Checking out the ref >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:16:44.751 GMT+00:00] [INFO] run git command --> git branch --list --remote origin/main
[2026/07/23 14:16:44.755 GMT+00:00] [INFO] run git command stdout -->   origin/main
[2026/07/23 14:16:44.756 GMT+00:00] [INFO] run git command --> git checkout --progress --force -B main refs/remotes/origin/main
[2026/07/23 14:16:44.763 GMT+00:00] [INFO] run git command stdout --> branch 'main' set up to track 'origin/main'.

Removing auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:16:44.773 GMT+00:00] [INFO] Removing SSH command configuration
[2026/07/23 14:16:44.773 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
[2026/07/23 14:16:44.776 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
[2026/07/23 14:16:44.795 GMT+00:00] [INFO] Removing HTTP extra header
[2026/07/23 14:16:44.796 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
[2026/07/23 14:16:44.799 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
[2026/07/23 14:16:44.818 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
[2026/07/23 14:16:44.842 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'


No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/20aa2fa8-ac2f-4c83-814f-cb3aa2519e7b.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/20aa2fa8-ac2f-4c83-814f-cb3aa2519e7b.sh
CHECKOUT_REF_OK
```

  **日志分析**: "CHECKOUT_REF_OK" — checkout ref 短名正常, run=COMPLETED

- **预期行为**（Phase 01 文本用例 `COMPAT-ACTION-01-001`，优先级 P1，维度 compatibility）:
  - 操作步骤 1: "在工作流中使用 `uses: checkout` 并传入 `ref: main` 参数"
  - 操作步骤 2: "触发工作流，观察 checkout 行为"
  - 操作步骤 3: "再传入 `ref: feature-branch` 参数重复触发"

  预期结果:
  - `uses: checkout` 配合 ref 参数可正确检出指定分支
  - 裸插件名写法与 GitHub 全名写法在行为上等价
  - 检出后的工作目录包含指定分支代码

  验证点:
  - [正向] checkout 步骤成功完成，无报错
  - [正向] 检出后的代码与指定分支一致
  - [负向] 不应因使用裸插件名而解析失败

- **实际行为**:
  - "CHECKOUT_REF_OK" — checkout ref 短名正常, run=COMPLETED


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

**置信度**: 高（"CHECKOUT_REF_OK" — checkout ref 短名正常, run=COMPLETED）

**建议**:
- 修复 `compile_asserts.py` 中的 run_status 词汇映射：`COMPLETED→success, FAILED→failure, CANCELED→canceled`
- 将 COMPAT-ACTION-01-001 标记为「用例断言修复后应重新验跑」
- 相关用例: COMPAT-ACTION-01-002
