用例 ID:   SEC-SUPPLY-01-004
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-032
标题:      reusable workflow 调用方传入的 secrets 不被被调用方泄露到日志

前置条件:
  - 定义被调用方 reusable workflow（callee）
  - 调用方 workflow（caller）通过 secrets: inherit 传入 Secret
  - callee 中故意 echo 传入的 Secret

操作步骤:
  1. 定义 callee workflow，接收 secrets 参数并在 run 中 echo
  2. caller 通过 workflow_call 调用 callee，传入 Secret SHARED_TOKEN
  3. 触发 caller，检查 callee 的 job 日志
  4. 验证传入的 Secret 在 callee 日志中被脱敏
  5. base64 编码传入 Secret 后输出 → 验证不泄露原始值

预期结果:
  - 跨 workflow 传入的 Secret 在接收方日志中脱敏（显示 ***）
  - base64 编码后的 secret 也不泄露原始值
  - 脱敏行为与被调用方自身的 Secret 一致

验证点:
  - [负向] callee 日志中 echo 传入 Secret → 显示 ***（非明文）
  - [负向] base64 编码输出传入 Secret → 不泄露
  - [正向] Secret 脱敏与自身 Secret 行为一致

清理:      fixture
