## 失败分诊 · SEC-INJ-01-004 · 不可信 commit message 不可直接插进 run 脚本导致命令注入

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, run_logs) — must_not_contain "injected_command_executed"，实际未出现（PASS）；assertions[1] (positive, run_status) — 期望 run_status equals "success"，实际 run_status=COMPLETED，词汇不匹配

**根因初判**: 用例问题

**证据**:

- **Job 日志全量**（仅 6 行）:
  ```
  === JOB: Test commit message injection (status=COMPLETED) ===
  [2026/07/23 22:06:29.162 GMT+08:00] [INFO] Job(1529972999023501312_1529972998989946887) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/8941f2f4-2522-4a0c-8792-efd010805730.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/8941f2f4-2522-4a0c-8792-efd010805730.sh
  Message is 
  ```
  日志仅输出 `Message is `（后无内容），表明 `atomgit.event.commits[0].message` 在 push 触发下被解析为空字符串。commit message 内容从未被注入脚本中，因此"命令注入"测试本身未能执行——不存在 shell 元字符被解释的场景。Job run_status 为 COMPLETED，断言期望小写 "success" 词汇不匹配。

- **预期行为**（Phase 01 文本用例 `SEC-INJ-01-004`，优先级 P0，维度 security）:
  - 操作步骤 1: "提交一个由 push 触发的 workflow，在 run 中引用 commit message"
  - 操作步骤 2: "推送一条含 shell 元字符的 commit"
  - 预期结果: "commit message 中的 shell 元字符不应被解释为命令执行；安全写法（中间环境变量）应正常生效"
  - 验证点: "[负向] 含反引号或分号的 commit message 绝不应被解释为命令执行"

- **实际行为**:
  - commit message 被平台解析为空字符串，`echo "Message is "` 输出空白
  - 命令注入攻击面未被实际测试到——无 shell 元字符出现在脚本中
  - 同时 run_status "COMPLETED" ≠ 断言期望的 "success" 是典型的 标记不匹配

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `commit-inj` job 的 `Inline commit message` 步骤:
    ```yaml
    - name: Inline commit message
      run: |
        echo "Message is ${{ atomgit.event.commits[0].message }}"
    ```
  - 这对应 GitCode 规格 `writing-pipelines/configure-conditional-execution.md` 第 42-60 行的 `if` 表达式语法（表达式求值机制），以及 第 9-12 行的前提条件:
    ```
    前提条件:
    - 理解 atomgit 上下文。
    - 理解表达式语法 ${{ }}。
    ```
    规格文档第 12 行承诺了 `atomgit` 上下文的存在，但未明确 `atomgit.event.commits[0].message` 在 push 事件下的具体行为。实际平台返回空 commit message 是上下文解析行为与测试假设不一致。
  - 同时对应规格 `syntax-reference/context.md`（未在本次读取中完整获取，但从命名可推断其定义了 atomgit 上下文字段），`atomgit.event` 应携带事件级别上下文数据。

**置信度**: 中（commit message 为空导致注入测试未实际执行是确凿事实，同时 COMPLETED≠"success" 的 标记不匹配 叠加导致 FAIL）

**影响**:
- **阻塞性**: ⚪无影响 — 测试失败原因是指令注入攻击面未被实际触发（commit message 为空）而非真实安全漏洞；平台在 push 事件下 commit message 为空不是安全缺陷
- **静默性**: 🟢明确报错 — run_status COMPLETED 与断言关键词 "success" 不匹配是可观测的断言失败，非隐藏行为
- **影响面**: 🟢单用例 — 仅影响 SEC-INJ-01-004 的命令注入测试，不涉及其他用例或维度
- **综合**: commit message 上下文传递为空字符串导致注入测试未执行，叠加 COMPLETED ≠ "success" 的标记不匹配，无安全风险
- **是否有规避手段**: 是 — 确保 push 事件的 commit message 正确传递到 atomgit.event 上下文；run_status 断言使用 must_not_equal "FAILED"

**建议**:
- 前置条件需确保 push 的 commit message 正确传递到 workflow 上下文（而非空字符串）
- run_status 断言应使用语义映射（COMPLETED→"success"）或使用 `must_not_equal: "FAILED"`
- 相关用例: SEC-INJ-01-001, SEC-INJ-01-002, SEC-INJ-01-003
