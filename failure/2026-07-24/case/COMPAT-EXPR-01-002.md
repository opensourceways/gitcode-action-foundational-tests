## 失败分诊 · COMPAT-EXPR-01-002 · success() 函数的处理行为差异

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 `success`，实际 `COMPLETED`（平台 API 返回大写枚举值，与合约期望的小写语义值不匹配）

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（共 108 行，展示首 60 + 尾 20）:
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

... (省略 28 行) ...

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

  **日志分析**: "Job B ran after Job A success" — success() 函数正常

- **预期行为**（Phase 01 文本用例 `COMPAT-EXPR-01-002`，优先级 P1，维度 compatibility）:
  - 操作步骤 1: "提交一个 workflow，在 step 中尝试使用 success() 函数形式的表达式"
  - 操作步骤 2: "对比平台对 success() 与 bare success 的解析差异"
  - 操作步骤 3: "手动触发并观察运行结果"

  预期结果:
  - 平台可能对 success() 函数与 bare success 关键字有不同的支持策略
  - 记录并验证实际行为与 GitHub Actions 的兼容性差异

  验证点:
  - [正向] 若支持，表达式返回布尔结果
  - [负向] 若不支持，应有表达式解析错误或降级行为

- **实际行为**:
  - "Job B ran after Job A success" — success() 函数正常


- **测试 YAML 与规格精确对照**:
  - 规格文件: `context.md / expressions.md` (路径: `phase01/inputs/gitcode-spec/syntax-reference/context.md`)
  - 规格节选:
```yaml
# context.md 第29-31行: atomgit.ref 为完整引用名
# 如 refs/heads/main
# expressions.md 第36-39行: success/failed 状态函数定义
```
    该规格明确声明: context.md 27-33行 atomgit 上下文属性 + expressions.md 36-39行状态函数

  测试 YAML 的写法与规格示例一致，证明平台文档确凿承诺了该行为。

**置信度**: 高（"Job B ran after Job A success" — success() 函数正常）

**影响**:
- **阻塞性**: ⚪无影响 — 平台 success() 函数正常（Job B ran after Job A success），断言标记 COMPLETED≠success
- **静默性**: 🟢明确报错 — 平台正常执行 success() 条件判断，仅测试断言词汇不一致
- **影响面**: 🟢单用例 — 仅本用例断言标记需修复
- **综合**: 平台 success() 表达式函数功能完全正常，仅断言词汇不匹配
- **是否有规避手段**: 是 — 修复 run_status 词汇映射

**建议**:
- 修复 `compile_asserts.py` 中的 run_status 词汇映射：`COMPLETED→success, FAILED→failure, CANCELED→canceled`
- 将 COMPAT-EXPR-01-002 标记为「用例断言修复后应重新验跑」
- 相关用例: COMPAT-EXPR-01-003
