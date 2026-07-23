用例 ID:   COMP-SUMMARY-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-019
标题:      验证 ATOMGIT_STEP_SUMMARY 输出 Markdown 到运行摘要页

前置条件:
  - 仓库有正常的 workflow 配置

操作步骤:
  1. 在 step 中 echo "## Test Results" >> $ATOMGIT_STEP_SUMMARY
  2. 写入 Markdown 表格（含表头、数据行）
  3. 多个 step 各自写入不同内容到 SUMMARY
  4. 写入空内容到 SUMMARY
  5. 查看运行详情摘要页的渲染效果

预期结果:
  - Markdown 表格在摘要页正确渲染
  - 多个 step 写入的内容累积显示（追加，不互相覆盖）
  - 空内容写入不报错
  - 超长内容（如 100KB）正常截断或完整显示

验证点:
  - [正向] Markdown 表正确渲染
  - [正向] 多个 step 写入内容累积可见
  - [正向] 空内容写入不报错
  - [非功能] 超长内容处理合理

清理:      fixture
