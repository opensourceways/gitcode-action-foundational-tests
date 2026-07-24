用例 ID:   COMPAT-COMM-01-002
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-NEW-004
母意图:    —
标题:      issue_comment types:created 不支持时应给出降级指引

前置条件:
  - 仓库已启用 Actions
  - 测试者持有 maintainer 权限

操作步骤:
  1. 创建一个 workflow，on 配置为 `issue_comment.types: [created]`
  2. 提交并触发 issue_comment 事件
  3. 观察系统行为

预期结果:
  - 若 types:created 不被支持，系统应明确报错或给出替代 types 列表
  - 不应静默忽略 types 配置导致所有 issue_comment 事件都触发

验证点:
  - [负向] 不通过静默忽略（types 配置失效）
  - [正向] 报错信息包含可接受的 types 列表

清理:      无
