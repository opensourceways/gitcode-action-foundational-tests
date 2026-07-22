用例 ID:   COMPAT-CACHE-EQUIV-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-048
母意图:    —
标题:      cache action 差异——key/restore-keys 语义、fork 隔离、跨 run 命中与 GitHub 等价性

前置条件:
  - runner 支持 cache

操作步骤:
  1. 使用 cache action 保存与恢复缓存
  2. 测试 restore-keys 的前缀匹配语义
  3. 验证 fork 隔离

预期结果:
  - key 精确匹配与 restore-keys 前缀匹配应生效
  - fork PR 不应污染主分支缓存

验证点:
  - [正向] cache 保存与恢复成功
  - [负向] fork PR 不命中主分支缓存

清理:      重置 fixture 仓库
