用例 ID:   COMPAT-POST-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-018
标题:      post 后处理阶段：run_always 行为

前置条件: 仓库 workflow 配置 post 阶段
操作步骤:
  1. run_always:true → workflow 失败后 post 仍执行
  2. run_always:false → workflow 失败后 post 不执行
  3. post 中发送通知/上传 artifact → 验证可用

预期结果: run_always:true 始终执行 post；false 时仅在成功时执行
验证点:
  - [正向] run_always:true → 失败后执行
  - [正向] run_always:false → 失败后不执行
清理:      fixture
