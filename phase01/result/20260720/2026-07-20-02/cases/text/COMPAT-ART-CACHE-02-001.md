用例 ID:   COMPAT-ART-CACHE-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-031
标题:      验证内置 upload-artifact/download-artifact 等价性及 cache 作用域隔离

前置条件:
  - 使用 GitCode 内置 artifact/cache action

操作步骤:
  1. upload-artifact → download-artifact 跨 job 正确传递
  2. cache 命中/未命中/回退行为与 GitHub actions/cache 一致
  3. fork PR 写缓存不应污染主分支缓存
  4. artifact 保留期到期后不可下载

预期结果:
  - artifact 正确传递
  - cache 行为与 GitHub 一致
  - fork PR 缓存隔离

验证点:
  - [正向] artifact 跨 job 传递正确
  - [正向] cache hit/miss/restore 行为正确
  - [负向] fork PR 缓存不与主分支共享

清理:      fixture
