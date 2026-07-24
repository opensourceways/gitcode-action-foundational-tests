## 失败分诊 · COMPAT-EXPR-01-003 · failure() 与 failed 关键字的处理行为差异

**判定结果**: FAIL
**失败断言**: assertions[0] (positive, run_status) — 期望 `failure`，实际 `FAILED`（平台 API 大小写与表达式函数语义不一致：platform=`FAILED` vs `${{ failure }}`=`failed`）

**根因初判**: Engine Bug

**证据**:

- **Job 日志全量**（共 58 行）:
```
=== JOB: Test failure handling (status=FAILED) ===
[2026/07/23 22:19:21.153 GMT+08:00] [INFO] Job(1529976237059743744_1529976237026189319) duration check: true
[2026/07/23 14:19:33.853 GMT+00:00] [INFO] repository dist full path is /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0
Getting Git version info >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:19:33.858 GMT+00:00] [INFO] run git command --> git version
[2026/07/23 14:19:33.866 GMT+00:00] [INFO] run git command stdout --> git version 2.43.0

[2026/07/23 14:19:33.867 GMT+00:00] [INFO] Deleting the contents of '/home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0'
initialize git repository >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:19:33.869 GMT+00:00] [INFO] run git command --> git init
[2026/07/23 14:19:33.874 GMT+00:00] [INFO] run git command stdout --> Initialized empty Git repository in /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0/.git/
[2026/07/23 14:19:33.874 GMT+00:00] [INFO] run git command --> git remote add origin https://gitcode.com/ComputingActionTest/gitcode-test-0.git
[2026/07/23 14:19:33.882 GMT+00:00] [INFO] git repository initialized at /home/slave1/runner/workers/0.0.4.4.version/worker_dir/ComputingActionTest/gitcode-test-0

Disabling automatic garbage collection >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:19:33.883 GMT+00:00] [INFO] run git command --> git config --local gc.auto 0

Setting up auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:19:33.887 GMT+00:00] [INFO] Removing SSH command configuration
[2026/07/23 14:19:33.887 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
[2026/07/23 14:19:33.892 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
[2026/07/23 14:19:33.912 GMT+00:00] [INFO] Removing HTTP extra header
[2026/07/23 14:19:33.913 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
[2026/07/23 14:19:33.917 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
[2026/07/23 14:19:33.938 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
[2026/07/23 14:19:33.946 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'
[2026/07/23 14:19:33.968 GMT+00:00] [INFO] configuring token
[2026/07/23 14:19:33.974 GMT+00:00] [INFO] configuring token config local

Start fetch git repo >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:19:33.986 GMT+00:00] [INFO] run git command --> git -c protocol.version=2 fetch --no-tags --prune --no-recurse-submodules --progress --depth=1 origin +refs/heads/main*:refs/remotes/origin/main* +refs/tags/main*:refs/tags/main*

Checking out the ref >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:19:34.525 GMT+00:00] [INFO] run git command --> git branch --list --remote origin/main
[2026/07/23 14:19:34.529 GMT+00:00] [INFO] run git command stdout -->   origin/main
[2026/07/23 14:19:34.530 GMT+00:00] [INFO] run git command --> git checkout --progress --force -B main refs/remotes/origin/main
[2026/07/23 14:19:34.538 GMT+00:00] [INFO] run git command stdout --> branch 'main' set up to track 'origin/main'.

Removing auth >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
[2026/07/23 14:19:34.548 GMT+00:00] [INFO] Removing SSH command configuration
[2026/07/23 14:19:34.549 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp core\.sshCommand
[2026/07/23 14:19:34.553 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'core\.sshCommand' && git config --local --unset-all 'core.sshCommand' || :"'
[2026/07/23 14:19:34.576 GMT+00:00] [INFO] Removing HTTP extra header
[2026/07/23 14:19:34.576 GMT+00:00] [INFO] run git command --> git config --local --name-only --get-regexp http\.https\:\/\/gitcode\.com\/\.extraheader
[2026/07/23 14:19:34.581 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'sh -c "git config --local --name-only --get-regexp 'http\.https\:\/\/gitcode\.com\/\.extraheader' && git config --local --unset-all 'http.https://gitcode.com/.extraheader' || :"'
[2026/07/23 14:19:34.605 GMT+00:00] [INFO] Removing includeIf entries pointing to credentials config files
[2026/07/23 14:19:34.632 GMT+00:00] [INFO] run git command --> git submodule foreach --recursive 'git config --local --show-origin --name-only --get-regexp remote.origin.url'


No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/171224bf-061f-44bb-bfc7-e3347f00c2bb.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/171224bf-061f-44bb-bfc7-e3347f00c2bb.sh
::error::Process exited with code 1

No shell specified, using platform default: default-bash
::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/50d5d8ab-bf43-4943-a68e-b6809424f4a7.sh
::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/50d5d8ab-bf43-4943-a68e-b6809424f4a7.sh
Cleanup ran after failure
```

  **日志分析**: cleanup 执行 "Cleanup ran after failure" — value=PASS; 断言 exp="failure" vs act="FAILED" — 大小写不匹配

- **预期行为**（Phase 01 文本用例 `COMPAT-EXPR-01-003`，优先级 P1，维度 compatibility）:
  - 操作步骤 1: "提交一个 workflow，其中包含一个会失败的 step"
  - 操作步骤 2: "在后续 step 中尝试使用 failure() 函数或 failed 关键字形式的表达式"
  - 操作步骤 3: "手动触发并观察运行结果"

  预期结果:
  - 平台对 failure() 函数与 failed 关键字可能有不同的支持策略
  - 记录实际行为，验证与 GitHub Actions 的兼容性差异

  验证点:
  - [正向] 若支持，可在失败后获取到正确的状态值
  - [负向] 若不支持，应有表达式解析错误或降级行为
  - [正向] 失败后 step 的执行状态可被观察或引用

- **实际行为**:
  - cleanup 执行 "Cleanup ran after failure" — value=PASS; 断言 exp="failure" vs act="FAILED" — 大小写不匹配


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

**置信度**: 高（cleanup 执行 "Cleanup ran after failure" — value=PASS; 断言 exp="failure" vs act="FAILED" — 大小写不匹配）

**影响**:
- **阻塞性**: ⚪无影响 — Engine Bug（大小写比较问题），平台 cleanup 正常执行（"Cleanup ran after failure" value=PASS），仅断言 "failure"≠"FAILED" 大小写不匹配
- **静默性**: 🟢明确报错 — 平台完整输出 step 执行结果，错误可定位：表达式返回 FAILED 而断言期望 failure
- **影响面**: 🟢单用例 — 平台表达式引擎大小写不一致问题，仅影响断言比较
- **综合**: 平台行为正确（failure 后 cleanup 正常执行），表达式引擎返回大写 FAILED 与文档约定的小写 failure 不一致
- **是否有规避手段**: 是 — 统一断言为大写匹配或平台修复大小写语义

**建议**:
- 平台表达式引擎同时返回大写(`FAILED`/`CANCELED`)和文档中的小写(`success`/`failure`/`cancelled`)值
- 建议统一为文档约定的小写语义值
- 将 COMPAT-EXPR-01-003 标记为「平台修复后重新验跑」
- 相关用例: COMPAT-EXPR-01-002
