用例 ID:   COMP-CACHE-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-007
标题:      验证缓存 cache key 精确/前缀匹配与跨 run 持久性

前置条件:
  - 配置 cache step with key + restore-keys

操作步骤:
  1. 第一次 run: 写入 cache（miss → save）
  2. 第二次 run: 同 key 应命中（exact hit → restore）
  3. 修改部分 key → 前缀匹配到 restore-keys
  4. hashFiles 返回确定性 SHA256

预期结果:
  - cache 命中/未命中/回退行为正确
  - hashFiles 对相同内容返回相同哈希
  - 缓存跨 run 持久

验证点:
  - [正向] cache key 不变时第二次命中
  - [正向] restore-keys 前缀匹配恢复
  - [正向] cache miss → 保存 → 下次命中
  - [负向] 无跨仓库缓存泄露

清理:      fixture
