用例 ID:   COMPAT-VARS-01-005
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-022
参照来源:  inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md
母意图:    —
标题:      vars 在条件表达式 if 中的可用性差异

前置条件:
  - 仓库已启用 Actions
  - 若平台支持 vars，已配置 vars.ENABLE_FEATURE=true

操作步骤:
  1. 创建一个 workflow，step 的 if 条件使用 `${{ vars.ENABLE_FEATURE == 'true' }}`
  2. 触发 workflow

预期结果:
  - GitHub 行为：vars 在 if 条件中正常求值
  - GitCode 行为：若支持 vars，应正常求值；若不支持应报错

验证点:
  - [正向] 若支持 vars，if 条件正确求值并控制步骤执行
  - [负向] 不通过 vars 在 if 中被静默视为空字符串

清理:      fixture
