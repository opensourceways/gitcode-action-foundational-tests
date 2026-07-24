用例 ID:   COMPAT-MATRIX-01-004
维度标签:   [compatibility]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-NEW-007
参照来源:  inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md
母意图:    —
标题:      matrix include 无基础变量不被支持时的差异

前置条件:
  - 仓库已启用 Actions
  - 测试者持有 maintainer 权限

操作步骤:
  1. 创建一个 workflow，配置 `strategy.matrix.include`，其中 include 项不依赖基础变量
  2. 提交并触发 workflow

预期结果:
  - GitHub 行为：include 无基础变量时应正常添加到矩阵实例中
  - GitCode 行为：可能不支持该模式
  - 应明确记录差异

验证点:
  - [正向] 系统接受或拒绝 include 配置时给出明确提示
  - [负向] 不通过 include 配置被静默忽略

清理:      无
