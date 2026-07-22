用例 ID:   SEC-SUPPLY-02-002
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-019
标题:      fork PR 不应能写入或污染主分支的依赖缓存

前置条件:
  - 仓库存在 cache key "node-modules-main"
  - fork PR workflow 使用 cache action 写入同一 key

操作步骤:
  1. fork PR workflow 写入 cache key
  2. 随后主分支 push workflow 读取同 key
  3. 检查是否命中 fork PR 写入的缓存

预期结果:
  - 主分支不命中 fork PR 写入的缓存
  - fork PR 写入的缓存与主分支缓存隔离

验证点:
  - [负向] 主分支 cache restore 不命中 fork PR 写入的条目
  - [负向] fork PR 不可覆盖主分支已有缓存

清理:      fixture
