用例 ID:   USE-STATE-01-001
维度标签:   [usability]
维度:      易用性
优先级:    P2
溯源意图:  INTENT-USE-011
标题:      运行状态机的完整性与可观察性

前置条件:
  - 准备不同类型 workflow：标准 push、concurrency 排队、fail_fast 场景

操作步骤:
  1. 触发一个需排队的 workflow（配置 concurrency queue），观察 queued 状态及排队信息
  2. 手动取消一个正在运行的 workflow，观察 cancelled 状态及取消原因
  3. 配置 fail_fast 场景（A → B 且 A 失败），观察被跳过的 job 是否有跳过原因说明

预期结果:
  - Actions 标签页显示清晰状态：queued / in_progress / success / failure / cancelled / skipped
  - queued 状态应显示排队位置或预计等待信息
  - cancelled 状态应显示取消原因（手动取消 vs 被抢占 vs fail_fast 级联）
  - skipped job 应有可见的跳过原因

验证点:
  - [正-非功能] queued 状态可见 + 排队信息展示（可截图判定）
  - [正-非功能] cancelled 状态含取消原因文本（如 "cancelled by user @username"）
  - [正-非功能] skipped job 有跳过原因说明（如 "skipped: upstream job failed"）
  - [非功能] 原因文本是否足够具体（LLM 辅助评判 0=仅状态标签, 1=有原因但笼统, 2=具体可操作）

清理:      fixture
