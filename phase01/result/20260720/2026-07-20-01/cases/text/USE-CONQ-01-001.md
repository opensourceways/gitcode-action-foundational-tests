用例 ID:   USE-CONQ-01-001
维度标签:   [usability]
维度:      易用性
优先级:    P2
溯源意图:  INTENT-USE-023
标题:      `concurrency` 排队时用户的等待信息可见性

前置条件:
  - 配置 `concurrency: { enable: true, max: 1, exceed-action: QUEUE }`

操作步骤:
  1. 配置 concurrency 队列（max=1, QUEUE 模式）
  2. 连续快速触发 3 个 push
  3. 观察 Actions 列表页中第 2、3 个 run 的排队信息展示
  4. 观察排队 run 的详情页中是否展示排队位置（如 "3rd in queue"）
  5. 验证排队信息在 Actions 列表页即可见（无需点进详情）

预期结果:
  - Actions 列表页和详情页均应显示排队状态（queued）
  - 排队信息应包含排队位置（如 "2nd in queue"）
  - 理想情况下包含预计开始时间

验证点:
  - [正-非功能] queued 状态在列表页可见（可截图判定）
  - [正-非功能] 排队序号展示（如 "2nd in queue"）
  - [非功能] 排队信息是否足以让用户判断「该等还是该取消」（LLM 辅助评判）

清理:      fixture
