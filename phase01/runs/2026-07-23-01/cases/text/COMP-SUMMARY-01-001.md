用例 ID:   COMP-SUMMARY-01-001
维度标签:   [completeness, compatibility]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-018
母意图:    —
标题:      ATOMGIT_STEP_SUMMARY Markdown 表格与标题正确渲染

前置条件:
  - workflow 向 ATOMGIT_STEP_SUMMARY 写入 Markdown

操作步骤:
  1. 触发 workflow
  2. 查看运行详情页的 summary

预期结果:
  - Markdown 表格、标题、列表在运行详情页正确渲染

验证点:
  - [正向] 详情页显示格式化的 Markdown 内容
  - [正向] 表格结构正确

清理:      none
