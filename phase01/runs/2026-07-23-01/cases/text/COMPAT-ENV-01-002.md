用例 ID:   COMPAT-ENV-01-002
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-017
参照来源:  inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md
母意图:    COMPAT-ENV-01-001
标题:      GITHUB_SHA 环境变量在 GitCode 中应为空或未定义

前置条件:
  - 仓库已启用 Actions

操作步骤:
  1. 在 workflow 的 run 步骤中输出 $GITHUB_SHA
  2. 触发 workflow 运行

预期结果:
  - $GITHUB_SHA 应为空字符串或未定义
  - 不应被错误映射到 ATOMGIT_SHA

验证点:
  - [负向] GITHUB_SHA 不应被静默映射为 ATOMGIT_SHA
  - [非功能] 运行日志中应能区分 GITHUB_SHA 为空

清理:      fixture
