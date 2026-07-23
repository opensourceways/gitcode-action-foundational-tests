用例 ID:   USE-YAML-01-002
维度标签:   ['usability']
维度:      usability
优先级:    P1
溯源意图:  INTENT-USE-022
母意图:    —
标题:      YAML 缩进错误时报错应指出具体行号与列号

前置条件:
  - workflow 文件位于 .gitcode/workflows/

操作步骤:
  1. 提交一个 steps 缩进错误的 workflow

预期结果:
  报错包含具体的行号、列号，指出缩进错误位置

验证点:
  - [负向] 不应仅报泛化 YAML parse error
  - [非功能] 报错中是否包含行号与列号

清理:      无

