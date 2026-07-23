用例 ID:   COMP-SUMMARY-01-002
维度标签:   [completeness, compatibility]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-018
母意图:    —
标题:      summary 中不应暴露系统内部路径

前置条件:
  - workflow 向 ATOMGIT_STEP_SUMMARY 写入内容

操作步骤:
  1. 触发 workflow
  2. 检查 summary 内容

预期结果:
  - summary 中不包含 Runner 内部绝对路径等敏感信息

验证点:
  - [负向] summary 中不出现 /tmp/runner-xxx 等内部路径

清理:      none
