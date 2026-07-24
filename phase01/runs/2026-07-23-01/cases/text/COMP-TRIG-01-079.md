用例 ID:   COMP-TRIG-01-079
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-234~560
母意图:    —
标题:      触发事件 types 取值与过滤边界验证

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 配置 pull_request 和 merge_requests 的 types
  2. 验证允许值和非法值处理

预期结果:
  - pull_request types 允许 merge / open / reopen / update，merge_requests types 允许 close / merge / open / reopen / update，非法 types 被平台拒绝

验证点:
  - [正向] 合法 types 通过校验
  - [负向] 非法 types 被平台拒绝
  - [正向] 默认 types 在未指定时生效

清理:      重置 fixture 仓库
