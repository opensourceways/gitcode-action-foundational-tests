用例 ID:   COMP-CACHE-01-002
维度标签:   [completeness, security, reliability]
维度:      completeness
优先级:    P0
溯源意图:  INTENT-COMP-016
母意图:    —
标题:      restore-keys 前缀匹配兜底生效

前置条件:
  - 之前运行已生成前缀匹配的 cache

操作步骤:
  1. 触发 workflow，精确 key 不匹配但 restore-keys 前缀匹配

预期结果:
  - restore-keys 前缀匹配成功，恢复最近同前缀缓存

验证点:
  - [正向] cache 步骤通过 restore-keys 命中

清理:      none
