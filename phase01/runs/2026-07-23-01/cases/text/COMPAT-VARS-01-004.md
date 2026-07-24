用例 ID:   COMPAT-VARS-01-004
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-022
参照来源:  inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md
母意图:    —
标题:      vars 与 env 同名时的优先级差异

前置条件:
  - 仓库已启用 Actions
  - 若平台支持 vars，已配置 vars.MY_VAR=var_value
  - workflow 中定义 env.MY_VAR=env_value

操作步骤:
  1. 在 workflow 中同时定义 env.MY_VAR 和引用 ${{ vars.MY_VAR }}
  2. 在 run 步骤中输出 $MY_VAR 和 ${{ vars.MY_VAR }}
  3. 触发 workflow

预期结果:
  - GitHub 行为：env 优先级高于 vars，$MY_VAR 返回 env_value
  - GitCode 行为：若支持 vars，应遵循相同优先级链

验证点:
  - [正向] 若支持 vars，env 优先级高于 vars
  - [正向] shell 环境变量 $MY_VAR 返回 env_value

清理:      fixture
