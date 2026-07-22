用例 ID:   USE-QUEUE-02-001
维度标签:   [usability]
维度:      易用性
优先级:    P2
溯源意图:  INTENT-USE-023
标题:      concurrency 排队时用户的等待信息可见性

前置条件:
  - 配置 concurrency: { enable: true, max: 1, exceed-action: QUEUE }
  - 连续触发 3 个 push

操作步骤:
  1. 连续触发 3 次 push
  2. 观察第 2/3 个 run 的排队信息展示
  3. 验证 Actions 列表页是否可见排队状态

预期结果:
  - 排队状态展示（queued）
  - 排队位置可见（如 "3rd in queue"）
  - 若有预计开始时间更佳

验证点:
  - [正向] queued 状态展示
  - [正向] 排队序号展示
  - [非功能] 信息足以让用户判断是等还是取消

可理解性判据: eval: llm_assisted
清理:      fixture
