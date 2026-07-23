用例 ID:   COMP-CACHE-01-003
维度标签:   [completeness, security, reliability]
维度:      completeness
优先级:    P0
溯源意图:  INTENT-COMP-016
母意图:    —
标题:      fork PR 不应覆盖或污染主分支 cache

前置条件:
  - 主分支已存在 cache
  - 存在一个来自 fork 的 PR

操作步骤:
  1. fork PR 触发 workflow 并写入 cache
  2. 主分支再次触发 workflow 读取同一 cache key

预期结果:
  - 主分支 cache 未被 fork PR 覆盖
  - 主分支读取到的仍是原有 cache 内容

验证点:
  - [负向] fork PR 不应覆盖主分支 cache
  - [正向] 主分支 cache 内容保持不变

清理:      重置 fixture 仓库
