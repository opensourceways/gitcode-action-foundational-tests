用例 ID:   SEC-SUPPLY-03-001
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-018
母意图:    —
标题:      第三方 action 引用未 pin 到 commit SHA 时有平台警告

前置条件:
  - 存在 push 触发的 workflow

操作步骤:
  1. 使用 uses: action@main（浮动引用）触发 workflow
  2. 对比使用 uses: action@<commit SHA>（pin 引用）
  3. 观察平台是否产生 lint 安全警告

预期结果:
  - 平台应对浮动引用提供可见警告机制
  - SHA-pinned 引用应被接受且正常运行
  - tag 被覆盖指向新 commit 后，SHA-pinned 引用不受影响

验证点:
  - [正向] uses: action@<commit SHA> 应被接受并正常运行
  - [负向] uses: action@main 平台是否产生安全警告
  - [负向] tag 变动后 SHA-pinned 引用不应受影响

清理:      none
