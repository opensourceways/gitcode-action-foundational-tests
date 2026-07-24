用例 ID:   SEC-CACHE-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-018
参照来源:  inputs/gitcode-spec/core-concepts/artifacts-and-cache.md
母意图:    SEC-CACHE-01-001
标题:      主仓 cache restore 对 fork cache miss

前置条件:
  - fork PR 已写入 cache

操作步骤:
  1. 在主仓触发 workflow，使用与 fork PR 相同的 cache key 尝试 restore
  2. 查看 restore 结果

预期结果:
  - cache restore 结果为 miss
  - 日志中显示未找到对应缓存

验证点:
  - [负向] 主仓绝不应命中 fork PR 的缓存
  - [正向] cache restore 返回 miss

清理:      重置 fixture 仓库
