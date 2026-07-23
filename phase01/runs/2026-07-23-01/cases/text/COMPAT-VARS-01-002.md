用例 ID:   COMPAT-VARS-01-002
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-022
母意图:    COMPAT-VARS-01-001
标题:      vars 上下文若不支持应报错而非静默为空

前置条件:
  - 仓库已启用 Actions

操作步骤:
  1. 在 workflow 的 run 步骤中输出 ${{ vars.UNKNOWN_VAR }}
  2. 触发 workflow 运行

预期结果:
  - 若 vars 不支持，应在解析或运行时给出明确报错
  - 不应静默求值为空字符串

验证点:
  - [负向] 不应静默求值为空
  - [非功能] 报错信息应说明 vars 上下文不支持

清理:      fixture
