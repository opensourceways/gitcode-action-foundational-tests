用例 ID:   COMP-TRIG-01-076
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-075~083
母意图:    —
标题:      issue_comment 事件关键字段与 types 验证

前置条件:
  - 仓库已启用 AtomGit Action
  - 存在 Issue

操作步骤:
  1. 配置 issue_comment 触发并定义 types
  2. 创建评论验证触发和字段

预期结果:
  - issue_comment 事件触发 workflow，types 允许 created / edited / deleted，atomgit.event.comment 和 issue 字段可访问

验证点:
  - [正向] issue 评论创建时触发
  - [正向] event.comment.id 非空
  - [正向] event.issue.number 非空

清理:      重置 fixture 仓库
