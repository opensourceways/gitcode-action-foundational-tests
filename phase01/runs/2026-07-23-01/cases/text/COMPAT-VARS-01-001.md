用例 ID:   COMPAT-VARS-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-022
母意图:    —
标题:      vars 上下文若支持应正确返回值

前置条件:
  - 仓库已启用 Actions
  - 若平台支持 vars，已配置测试变量 TEST_VAR

操作步骤:
  1. 在 workflow 的 run 步骤中输出 ${{ vars.TEST_VAR }}
  2. 触发 workflow 运行

预期结果:
  - 若 vars 支持，应正确返回 TEST_VAR 的配置值
  - 日志中应显示该值

验证点:
  - [正向] vars.TEST_VAR 返回配置值

清理:      fixture
