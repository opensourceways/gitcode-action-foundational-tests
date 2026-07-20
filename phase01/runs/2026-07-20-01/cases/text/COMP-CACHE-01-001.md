用例 ID:   COMP-CACHE-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-007
标题:      验证缓存: cache key 精确/前缀匹配与跨 run 持久性
前置条件:  仓库支持 cache action
操作步骤:
  1. 首次 run 使用 cache key=test-cache-001，验证 miss → 保存
  2. 二次 run 使用相同 key，验证命中（hit）
  3. 使用 restore-keys 前缀匹配，验证回退命中
  4. 验证 hashFiles 确定性
预期结果:
  - key 精确命中 → cache hit
  - restore-keys 前缀匹配按序回退
  - hashFiles 相同内容文件返回一致值
  - 缓存跨 run 持久
验证点:
  - [正向] cache key 不变时命中
  - [正向] restore-keys 前缀匹配恢复最近缓存
  - [负向] 不应出现跨仓库的缓存泄露
清理:      fixture
