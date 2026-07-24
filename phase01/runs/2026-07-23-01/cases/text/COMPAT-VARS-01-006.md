用例 ID:   COMPAT-VARS-01-006
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-022
母意图:    —
标题:      vars 在 Action 中的可用性差异

前置条件:
  - 仓库已启用 Actions
  - 若平台支持 vars，已配置 vars.ACTION_VAR=action_value

操作步骤:
  1. 创建一个 workflow，Action 的 with 参数引用 `${{ vars.ACTION_VAR }}`
  2. 触发 workflow

预期结果:
  - GitHub 行为：vars 在 Action 的 with 参数中正常求值
  - GitCode 行为：若支持 vars，应正常求值；若不支持应报错

验证点:
  - [正向] 若支持 vars，Action 的 with 参数正确接收值
  - [负向] 不通过 vars 在 Action 中被静默视为空字符串

清理:      fixture
