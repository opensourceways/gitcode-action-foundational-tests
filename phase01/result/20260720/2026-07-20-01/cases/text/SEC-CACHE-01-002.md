用例 ID:   SEC-CACHE-01-002
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-020
标题:      跨事件类型 cache 隔离：fork PR 写入的 cache 不应被内部 push 命中

前置条件:
  - 仓库有 push 触发和 pull_request 触发的两个 workflow
  - push workflow 使用 cache 读写
  - fork PR 的 pull_request workflow 也可操作 cache

操作步骤:
  1. 内部 push 触发 workflow 写入 cache key = cross-event-test
  2. 再次 push 触发 workflow → 验证可命中步骤 1 的 cache（同分支同事件）
  3. fork PR 触发 pull_request workflow → 尝试写入同 key cache
  4. 内部 push 再次触发 → 验证不命中 fork PR 写入的 cache

预期结果:
  - 同分支 push→push 之间 cache 正常命中
  - fork PR 写入的 cache 不对 push 事件可见
  - fork PR 不能覆盖 push 已存在的 cache 条目

验证点:
  - [正向] 第二次 push 命中第一次 push 写入的 cache
  - [负向] fork PR 写入的 cache 不被 push 命中
  - [负向] fork PR 不能覆盖 push 的 cache 条目

清理:      fixture
