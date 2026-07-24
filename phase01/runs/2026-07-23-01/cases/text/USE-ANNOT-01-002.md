用例 ID:   USE-ANNOT-01-002
维度标签:   ['usability']
维度:      usability
优先级:    P1
溯源意图:  INTENT-USE-021
参照来源:  inputs/gitcode-spec/syntax-reference/workflow-commands.md
母意图:    —
标题:      ::error:: 生成的 PR annotation 具备文件路径、行号与可点击跳转

前置条件:
  - PR 存在
  - workflow 由 PR 事件触发

操作步骤:
  1. 在 PR 触发的工作流中输出 ::error file=...,line=...::message
  2. 检查 PR 页面的 annotation 展示

预期结果:
  若支持 annotation，则 PR 页面显示包含文件路径、行号、错误信息的红色/黄色标注，且可点击跳转

验证点:
  - [非功能] annotation 是否包含准确的文件路径、行号、错误信息
  - [非功能] annotation 颜色是否符合语义（error 红色、warning 黄色）

清理:      无

