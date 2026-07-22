用例 ID:   USE-ERR-MSG-02-006
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-005
标题:      表达式括号语法差异（failure() vs failed）的错误信息可诊断性

前置条件:
  - 在 workflow 中使用 GitHub 风格的带括号状态函数语法

操作步骤:
  1. 配置 `if: ${{ failure() }}`（带括号）→ 验证报错信息
  2. 配置 `if: ${{ always() }}`（带括号）→ 同上
  3. 配置 `if: ${{ success() }}`（带括号）→ 同上
  4. 验证错误消息是否提示「GitCode 不需要括号」

预期结果:
  - 表达式语法错误有报错
  - 消息暗示应使用 `failed`/`always`/`success` 替代

验证点:
  - [正向] failure() 语法被报错
  - [正向] 消息含表达式位置
  - [非功能] 消息是否让 GitHub 迁移者意识到「不需要括号」

可理解性判据: eval: llm_assisted
清理:      fixture
