用例 ID:   SEC-SUPPLY-02-001
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-018
标题:      第三方 action 引用未 pin 到 commit SHA 时有平台警告

前置条件:
  - workflow 使用 `uses: owner/repo@main`（浮动分支）
  - workflow 使用 `uses: owner/repo@<commit-sha>`（SHA pinned）

操作步骤:
  1. 提交浮动引用 workflow，观察平台警告
  2. 提交 SHA pinned workflow，验证正常执行
  3. 修改 tag 指向新 commit，验证浮动引用是否自动更新

预期结果:
  - 浮动引用有可见警告机制
  - SHA-pinned 引用不受 tag 改写影响

验证点:
  - [正向] SHA-pinned 引用正常执行
  - [负向] 浮动引用触发 lint/安全警告
  - [负向] tag 改写后引用该 tag 的 workflow 可能拉取新代码

清理:      fixture
