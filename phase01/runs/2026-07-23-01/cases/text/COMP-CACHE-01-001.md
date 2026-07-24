用例 ID:   COMP-CACHE-01-001
维度标签:   [completeness, security, reliability]
维度:      completeness
优先级:    P0
溯源意图:  INTENT-COMP-016
参照来源:  inputs/gitcode-spec/core-concepts/artifacts-and-cache.md
母意图:    —
标题:      cache hit 时恢复缓存内容正确

前置条件:
  - 之前运行已生成匹配的 cache

操作步骤:
  1. 触发 workflow，使用 cache 插件
  2. 观察 cache 是否命中

预期结果:
  - cache 命中并正确恢复内容

验证点:
  - [正向] cache 步骤状态为 success
  - [正向] 恢复后的文件内容与之前一致

清理:      none
