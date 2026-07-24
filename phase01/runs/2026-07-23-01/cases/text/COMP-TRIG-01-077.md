用例 ID:   COMP-TRIG-01-077
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-469~470
母意图:    —
标题:      pull_request_comment 事件关键字段与过滤验证

前置条件:
  - 仓库已启用 AtomGit Action
  - 存在 PR

操作步骤:
  1. 配置 pull_request_comment 触发并定义 types
  2. 在 PR 下创建评论验证触发

预期结果:
  - pull_request_comment 事件触发 workflow，types 允许 created / edited / deleted，atomgit.event.comment 和 pull_request 字段可访问

验证点:
  - [正向] PR 评论创建时触发
  - [正向] event.comment.body 非空
  - [正向] event.pull_request.number 非空

清理:      重置 fixture 仓库
