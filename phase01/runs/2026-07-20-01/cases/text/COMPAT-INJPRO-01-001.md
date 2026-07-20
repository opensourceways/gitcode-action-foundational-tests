用例 ID:   COMPAT-INJPRO-01-001
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-026
标题:      不可信输入注入防护对标

前置条件: 仓库 workflow 使用不可信上下文输入
操作步骤:
  1. PR 标题含 shell 元字符通过 ${{ }} 嵌入 run: → 验证行为
  2. secrets 在 if: 条件中 → 验证不可用
  3. 不可信输入尝试注入 :: workflow 命令 → 验证不被执行
预期结果: 注入防护不弱于 GitHub；secrets 在 if 中不可用
验证点:
  - [负向] 不可信输入不被解释为命令
  - [负向] secrets 在 if 中不可用
清理:      fixture
