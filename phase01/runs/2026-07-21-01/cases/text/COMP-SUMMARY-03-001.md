用例 ID:   COMP-SUMMARY-03-001
维度标签:   [completeness, usability]
维度:      完备性
优先级:    P2
溯源意图:  INTENT-COMP-025
标题:      ATOMGIT_STEP_SUMMARY 的 Markdown 渲染与上传——表格/标题/代码块格式支持

前置条件:
  - step 中写入 ATOMGIT_STEP_SUMMARY 含 Markdown 内容

操作步骤:
  1. step 写入 Markdown 标题（## Test Results）
  2. 写入 Markdown 表格（|Status|Count|）
  3. 写入代码块（```bash ... ```）
  4. 多 step 追加内容验证 append 语义
  5. step 完成后验证内容不可改

预期结果:
  - 运行详情页 Summary 区域完整渲染 Markdown
  - 表格、标题、代码块正确显示
  - 多 step 追加内容合并显示

验证点:
  - [正向] Summary 区域可见渲染后的 Markdown
  - [正向] 表格/标题/代码块正确渲染
  - [正向] 多 step 追加内容合并

清理:      none
