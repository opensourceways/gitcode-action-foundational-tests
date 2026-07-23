用例 ID:   USE-UNKN-01-001
维度标签:   ['usability', 'compatibility']
维度:      usability/compatibility
优先级:    P1
溯源意图:  INTENT-USE-023
母意图:    —
标题:      未知字段如 run-name 不应被静默忽略而应给出警告或错误

前置条件:
  - workflow 文件位于 .gitcode/workflows/

操作步骤:
  1. 在 workflow 中使用 GitHub 特有的 run-name 字段

预期结果:
  系统在校验阶段给出警告或错误，指明字段不支持

验证点:
  - [负向] 不应静默忽略未知字段
  - [非功能] 报错中是否包含字段名、文件路径、不支持字样

清理:      无

