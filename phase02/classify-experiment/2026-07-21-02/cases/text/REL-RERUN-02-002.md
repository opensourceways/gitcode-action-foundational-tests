用例 ID:   REL-RERUN-02-002
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-026
标题:      同一 Run 重新运行超过 3 次时，第 4 次重新运行被拒绝

前置条件:
  - 一个注定失败的 workflow Run
  - 文档声明最大重试次数 = 3

操作步骤:
  1. 触发一个会产生 failure 的 run
  2. 连续触发 4 次 Re-run failed jobs
  3. 验证第 1-3 次 Re-run 正常执行
  4. 验证第 4 次被拒绝

预期结果:
  - 前 3 次 Re-run 均正常
  - 第 4 次被拒绝（UI 禁用/API 返回错误）

验证点:
  - [正向] 第 1-3 次 Re-run 正常执行
  - [正向] 第 4 次 Re-run 被拒绝
  - [负向] 第 4 次不被实际执行

清理:      fixture
