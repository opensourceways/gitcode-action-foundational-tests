用例 ID:   SEC-CACHE-03-004
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-054
母意图:    —
标题:      pull_request_target workflow 对默认分支缓存仅有只读访问

前置条件:
  - 存在 pull_request_target 触发的 workflow
  - 默认分支已有写入的缓存

操作步骤:
  1. pull_request_target workflow 中尝试 restore 缓存
  2. pull_request_target workflow 中尝试 save 缓存
  3. 观察 save 操作是否被拒绝

预期结果:
  - pull_request_target 下 cache restore 应正常命中
  - cache write/save 应被拒绝或写入隔离作用域

验证点:
  - [正向] pull_request_target workflow 中 restore 缓存应正常命中
  - [负向] pull_request_target workflow 中 save 缓存应被拒绝

清理:      none
