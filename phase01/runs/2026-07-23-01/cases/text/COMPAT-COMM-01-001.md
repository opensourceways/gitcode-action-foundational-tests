用例 ID:   COMPAT-COMM-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-NEW-004
母意图:    —
标题:      issue_comment types 命名差异 - GitCode 合法 types 应被接受

前置条件:
  - 仓库已启用 Actions
  - 测试者持有 maintainer 权限

操作步骤:
  1. 创建一个 workflow，on 配置为 `issue_comment.types: [created, edited]`（GitCode 风格命名）
  2. 提交并触发 issue_comment 事件

预期结果:
  - GitCode 合法 types（created/edited/deleted）应被接受并正常触发
  - 不应因命名差异导致 workflow 被拒绝

验证点:
  - [正向] GitCode 风格 types 命名被接受
  - [负向] 不通过因命名差异导致的误报错误

清理:      无
