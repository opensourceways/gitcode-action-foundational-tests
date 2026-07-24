用例 ID:   COMPAT-PR-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-011
参照来源:  inputs/gitcode-spec/core-concepts/trigger-events.md
母意图:    —
标题:      pull_request types 命名差异 - GitCode 合法 types 应被接受

前置条件:
  - 仓库已启用 Actions
  - 测试分支存在
  - 存在目标分支 main

操作步骤:
  1. 在 workflow 中定义 on: pull_request 并指定 GitCode 风格的 types（open, reopen, update）
  2. 提交并推送该 workflow
  3. 触发 pull_request 事件

预期结果:
  - workflow 应被平台接受，不报错
  - PR 事件应按指定 types 触发 workflow

验证点:
  - [正向] workflow 校验通过
  - [正向] 指定 types 的 PR 事件能正常触发 workflow

清理:      fixture
