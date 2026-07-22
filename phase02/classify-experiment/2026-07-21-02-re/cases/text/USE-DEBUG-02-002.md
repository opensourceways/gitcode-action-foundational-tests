用例 ID:   USE-DEBUG-02-002
维度标签:   [usability]
维度:      易用性
优先级:    P2
溯源意图:  INTENT-USE-011
标题:      运行状态机的完整性与可观察性：queued/cancelled/skipped 状态的展示

前置条件:
  - 多种触发场景：concurrency 排队、手动取消、fail_fast 跳过

操作步骤:
  1. concurrency 排队时观察 queued 状态是否展示及排队位置
  2. 手动取消正在运行的 workflow，观察 cancelled 状态及取消原因
  3. fail_fast 场景下观察被跳过 job 是否有 skipped 原因说明

预期结果:
  - queued 状态展示且含排队信息
  - cancelled 含取消原因
  - skipped 含跳过原因

验证点:
  - [正向] queued 状态可见
  - [正向] cancelled 含原因
  - [正向] skipped 含原因说明

可理解性判据: eval: llm_assisted
清理:      fixture
