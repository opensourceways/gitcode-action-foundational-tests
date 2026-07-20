用例 ID:   USE-SUMMARY-03-001
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-041
标题:      Step Summary 的 Markdown 渲染与链接有效性——历史 #56/#73

前置条件:
  - step 中写入 ATOMGIT_STEP_SUMMARY 含 Markdown 表格和外部链接

操作步骤:
  1. step 写入 echo "## Test Results" >> $ATOMGIT_STEP_SUMMARY
  2. 写入 Markdown 表格（|Status|Count|）
  3. 写入外部链接 [external](https://example.com)
  4. 验证运行详情页 Summary 区域渲染结果

预期结果:
  - Summary 区域完整渲染 Markdown 内容（表格/标题等）
  - 外部链接可直接访问，不被注入无关域名
  - Summary 内容不被截断或丢失

验证点:
  - [正向] Summary 区域可见渲染后的 Markdown
  - [正向] 表格正确渲染
  - [正向] 链接不被注入中间页/无关域名

清理:      none
