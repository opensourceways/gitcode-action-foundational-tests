用例 ID:   USE-SUMMARY-02-001
维度标签:   [usability]
维度:      易用性
优先级:    P2
溯源意图:  INTENT-USE-026
标题:      Step Summary（ATOMGIT_STEP_SUMMARY）写入后是否在运行详情页可见、超长内容是否截断及提示

前置条件:
  - 工作流可在 push 事件下触发
  - 运行详情页支持展示 Step Summary

操作步骤:
  1. 触发工作流，在 step 中通过 ATOMGIT_STEP_SUMMARY 写入正常长度的 Markdown 内容（含表格、标题）
  2. 观测运行详情页是否出现独立 Summary 区块，内容是否正确渲染
  3. 再触发一次工作流，写入超长 Markdown 内容，观测是否被截断及是否有截断提示

预期结果:
  - 正常长度的 Markdown summary 在运行详情页有独立 Summary 区块，支持基本 Markdown 渲染
  - 若内容超长被截断，应在截断处给出提示（如「内容已截断」）
  - 多 job 时 summary 聚合顺序符合声明

验证点:
  - [正向] 运行详情页存在 summary 区块且内容非空；Markdown 表格有边框/标题有样式
  - [负向] 不应出现「写入了但详情页完全不可见」或「Markdown 被当纯文本原样展示」
  - [非功能] 超长 summary 若被截断，截断提示应包含「截断」「超过」「省略」等关键字之一
  - [非功能] summary 区块的醒目程度与导航便利性（主观判据）

清理:      fixture
