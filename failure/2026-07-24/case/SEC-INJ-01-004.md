## 失败分诊 · SEC-INJ-01-004 · 不可信 commit message 不可直接插进 run 脚本导致命令注入

**判定结果**: FAIL
**失败断言**: 
- negative, run_logs, must_not_contain "injected_command_executed" — 通过（无注入）
- positive, run_status, equals "success" — job 状态 COMPLETED（未 FAIL），符合

**根因初判**: 环境问题
**责任人**: Phase 02

**证据**:

- **Job 日志全量** (6 行):
  ```
  === JOB: Test commit message injection (status=COMPLETED) ===
  [2026/07/23 22:06:29.162 GMT+08:00] [INFO] Job(1529972999023501312_1529972998989946887) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/8941f2f4-2522-4a0c-8792-efd010805730.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/8941f2f4-2522-4a0c-8792-efd010805730.sh
  Message is 
  ```

- **预期行为** (Phase 01 文本用例 SEC-INJ-01-004, 优先级 P0, 维度 security):
  - 前置条件: 存在一条 commit message 含反引号或分号的 push
  - 操作步骤 1: 提交一个由 push 触发的 workflow，在 run 中引用 commit message
  - 操作步骤 2: 推送一条含 shell 元字符的 commit
  - 预期结果: commit message 中的 shell 元字符不应被解释为命令执行；安全写法（中间环境变量）应正常生效

- **实际行为**:
  - `echo "Message is ${{ atomgit.event.commits[0].message }}"` 输出 `Message is ` (空)
  - `atomgit.event.commits[0].message` 展开为空字符串
  - push 事件未携带含 shell 元字符的 commit message（可能使用了空 commit 或普通 commit）
  - 无法验证注入保护机制，但命令注入本身未发生

- **对照 GitCode 规格** `security-permissions/using-secrets.md`:
  - 第 66 行: "Secret 值在日志中自动替换为 ***" (同类安全机制)
  - 未找到 commit message 注入防护的显式规格，属于 knowledge base 来自的安全要求

- **环境前置条件验证**: YAML `setup.repo_fixture: default`, 无 secrets, trigger as `untrusted_contributor`。确认 commit message 为空 —— push 事件的触发上下文未提供含恶意字符的 commit。

**置信度**: 中 (commit message 为空，测试预期输入未满足)

**影响**:
- **阻塞性**: 🟡非阻塞 — 测试覆盖了代码路径但缺少有效测试输入
- **静默性**: 🟡可察觉 — 日志显示 "Message is " 暗示输入为空，但未报错
- **影响面**: 🟢单用例 — 其他注入用例可能也不受影响
- **综合**: push 触发事件未提供含反引号/分号的 commit message，测试断言可部分通过但未验证注入保护
- **是否有规避手段**: 是

**建议**:
- 测试 YAML 确保 push trigger 携带含 `;` 或 `` ` `` 的 commit message (如 `test;cat /etc/passwd`)
- 添加 config_probe 步骤打印 commit message 原值以确认输入有效性
- 或切换为 workflow_dispatch + inputs 方式可控注入攻击向量
