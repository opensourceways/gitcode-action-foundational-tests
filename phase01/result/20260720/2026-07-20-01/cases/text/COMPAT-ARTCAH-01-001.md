用例 ID:   COMPAT-ARTCAH-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-031
标题:      内置 artifact/cache 等价性 + 作用域隔离

前置条件: 仓库使用 upload-artifact/download-artifact 和 cache
操作步骤:
  1. upload-artifact → download-artifact 跨 job 传递
  2. cache key 精确匹配命中
  3. fork PR 写缓存 → 验证主分支不命中
  4. artifact 保留期验证

预期结果: artifact/cache 行为与 GitHub 一致；fork PR cache 隔离
验证点:
  - [正向] artifact 跨 job 传递
  - [正向] cache 命中正确
  - [负向] fork PR cache 与主分支隔离
清理:      fixture
