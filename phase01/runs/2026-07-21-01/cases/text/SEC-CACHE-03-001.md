用例 ID:   SEC-CACHE-03-001
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-019
母意图:    —
标题:      fork PR 不应能写入或污染主分支的依赖缓存

前置条件:
  - 存在 fork 仓库可提交 PR
  - 主分支已有人工写入的缓存

操作步骤:
  1. fork PR workflow 中尝试写入 cache 条目
  2. 主分支 push workflow 尝试读取同 key 的 cache
  3. 观察主分支是否命中 fork PR 写入的缓存

预期结果:
  - fork PR workflow 写入的缓存不应被主分支命中
  - 主分支已有缓存不被 fork PR 覆盖

验证点:
  - [负向] fork PR 写入 cache key，主分支 push 读取同 key 不应命中
  - [负向] fork PR 不应覆盖主分支已有缓存条目

清理:      fixture
