用例 ID:   COMPAT-VARS-01-003
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-022
母意图:    —
标题:      vars 项目级覆盖组织级的优先级差异

前置条件:
  - 仓库已启用 Actions
  - 若平台支持 vars，已配置组织级 ORG_VAR=org_value 和项目级 ORG_VAR=proj_value

操作步骤:
  1. 在 workflow 中输出 ${{ vars.ORG_VAR }}
  2. 触发 workflow

预期结果:
  - GitHub 行为：项目级 vars 覆盖组织级 vars，返回 proj_value
  - GitCode 行为：若支持 vars，应遵循相同优先级；若不支持应报错

验证点:
  - [正向] 若支持 vars，项目级值覆盖组织级值
  - [负向] 不通过组织级值错误地覆盖项目级值

清理:      fixture
