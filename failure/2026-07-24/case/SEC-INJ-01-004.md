## 失败分诊 · SEC-INJ-01-004 · 不可信 commit message 不可直接插进 run 脚本导致命令注入

**判定结果**: FAIL
**失败断言**:
  - 负向 `run_logs` `must_not_contain: "injected_command_executed"` — **PASS**: 未出现注入执行
  - 正向 `run_status` `equals: "success"` — **PASS**: job status=COMPLETED

**根因初判**: 测试 YAML 与规格行为不匹配（commit message 为空，未实际注入 shell 元字符）
**责任人**: Phase 01

**证据**:

- **Job 日志全量**:
  ```
  === JOB: Test commit message injection (status=COMPLETED) ===
  [2026/07/23 22:06:29.162 GMT+08:00] [INFO] Job(1529972999023501312_1529972998989946887) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/8941f2f4-2522-4a0c-8792-efd010805730.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/8941f2f4-2522-4a0c-8792-efd010805730.sh
  Message is 
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 存在一条 commit message 含反引号或分号的 push
  - 操作步骤: 1. 提交一个由 push 触发的 workflow，在 run 中引用 commit message；2. 推送一条含 shell 元字符的 commit
  - 预期结果: commit message 中的 shell 元字符不应被解释为命令执行

- **实际行为**:
  - 日志输出 "Message is " 后为空，说明 push 事件的 commit message 为空
  - 测试环境的 push 未携带包含 shell 元字符（反引号、分号）的 commit message
  - Job 正常完成但未实际执行注入测试
  - **失败传导链**: push trigger 未提供包含元字符的 commit message → `${{ atomgit.event.commits[0].message }}` 求值为空 → 无注入输入 → 断言无法验证注入防护效果

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `commit-inj` 的 `Inline commit message`:
    ```yaml
    on:
      push:
        branches: [main]
    jobs:
      commit-inj:
        name: Test commit message injection
        runs-on: [dedicate-hosted, x64, large]
        steps:
          - name: Inline commit message
            run: |
              echo "Message is ${{ atomgit.event.commits[0].message }}"
    ```
  - **GitCode 规格** `core-concepts/variables-secrets-context-expressions.md` 第 25-30 行:
    ```
    ## Context
    AtomGit Action supports 12 contexts, with the core context being **`atomgit`**:
    | `atomgit` | Core workflow run information | `atomgit.sha`, `atomgit.ref`, `atomgit.event_name` |
    ```
  - **逐项映射**:
    - `${{ atomgit.event.commits[0].message }}`: 测试 YAML 引用 commit message 作为执行输入 — 此即为注入风险点
    - 规格中上下文 `atomgit` 提供运行时信息，`atomgit.event_name` 可获取事件类型
    - 测试 YAML 的防护写法是将 commit message 作为 echo 字符串输出，不执行 — 若平台转义正确，应仅显示字符串
    - **关键问题**: 测试环境 push 触发时未注入包含 shell 元字符的 test commit，导致实际测试输入为空

- **环境前置条件验证**: push 触发正常但 commit message 为空，前置条件（含 shell 元字符的 commit message）未满足

**置信度**: 中（push 触发成功但 commit message 为空，无法判定平台的注入防护是否生效）

**影响**:
- **阻塞性**: 中 — 测试未覆盖注入场景，无法验证平台的安全性
- **静默性**: 高 — 若平台存在注入漏洞，当前测试不会发现
- **影响面**: 高 — commit message 注入是常见的 CI/CD 攻击向量
- **综合**: push 事件触发的 workflow 中 commit message 为空，测试无法验证注入防护效果；需修改测试前置条件确保注入包含 shell 元字符的 commit message
- **是否有规避手段**: 是 — 在测试 fixture 中显式推送包含反引号/分号的 commit

**建议**:
- Phase 01: 重新设计测试流程：(1) setup 阶段先推送一条包含 `; whoami` 或 `` `id` `` 的 commit；(2) 确保 commit message 非空且包含 shell 元字符
- Phase 02: 测试 YAML 的 trigger 参数中增加 test commit message 注入逻辑
