用例 ID:   REL-CACHE-ISOLATE-03-001
维度标签:   [reliability]
维度:      可靠性
优先级:    P1
溯源意图:  INTENT-REL-055
标题:      cache key 隔离：job-A 的 cache 不污染 job-B（不同 key）

前置条件:
  - job-A cache key=cache-A
  - job-B cache key=cache-B（不同）

操作步骤:
  1. job-A 写入缓存（key=cache-A, 内容=cache-data-a）
  2. job-B 使用不同 key=cache-B 尝试恢复缓存
  3. 验证 job-B 是否错误命中 job-A 的缓存

预期结果:
  - job-B 不应 hit job-A 的 cache（key 不同）
  - job-B 日志显示 cache miss
  - 不同 key 的缓存完全隔离

验证点:
  - [负向] job-B 不应 hit cache-A
  - [正向] job-B 日志显示 cache miss

清理:      fixture
