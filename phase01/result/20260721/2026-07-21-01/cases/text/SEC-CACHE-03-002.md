用例 ID:   SEC-CACHE-03-002
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-020
母意图:    —
标题:      同一 workflow 多次运行之间的 cache 不应跨不同事件类型互相污染

前置条件:
  - 存在 push 和 pull_request 两种触发的 workflow
  - workflow 均使用相同 cache key 模式

操作步骤:
  1. push 事件触发 workflow 写入 cache
  2. 同一分支 pull_request 事件触发 workflow 尝试读取同 key cache
  3. 观察是否命中

预期结果:
  - 不同事件类型的 cache 应隔离
  - fork PR 写入的 cache 内部 push 不应命中

验证点:
  - [正向] 同分支两次 push：第一次写入 cache，第二次恢复应命中
  - [负向] fork PR 写入的 cache，内部 push 不应命中

清理:      none
