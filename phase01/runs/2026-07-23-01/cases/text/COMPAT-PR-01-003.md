用例 ID:   COMPAT-PR-01-003
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-NEW-003
母意图:    —
标题:      PR types 配置后匹配类型不触发与 GitHub 行为差异

前置条件:
  - 仓库已启用 Actions
  - 存在至少一个已配置的 workflow，on 包含 pull_request.types
  - 测试者持有 maintainer 权限

操作步骤:
  1. 配置 workflow 触发器为 `pull_request.types: [open, reopen, update]`
  2. 创建一个满足 types 条件的 PR（如更新提交）
  3. 观察是否触发对应 workflow 运行

预期结果:
  - GitHub 行为：匹配 types 的 PR 事件应触发独立 Job
  - GitCode 实际：满足 types 条件的 PR 变更没有对应 workflow 运行（已知问题）
  - 差异应被记录，且平台若修复后应重新验证

验证点:
  - [负向] 不通过假阴性（PR 更新后没有对应 workflow 运行）
  - [正向] 若平台已修复，PR 更新后应触发 workflow 运行

清理:      无
