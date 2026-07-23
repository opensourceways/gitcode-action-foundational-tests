用例 ID:   COMP-POST-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-010
标题:      验证 post 后处理阶段: run_always 与时序保证
前置条件:  仓库无特殊设置
操作步骤:
  1. 配置 post 阶段 run_always:true，主流程成功→验证 post 执行
  2. 主流程失败→验证 run_always:true 时 post 仍执行
  3. 配置 run_always:false，主流程成功→post 执行
  4. run_always:false + 主流程失败→post 不执行
预期结果: post.run_always:true 时无论成败都执行；false 时仅成功执行
验证点:
  - [正向] 主流程成功 + run_always:true → post 执行
  - [正向] 主流程失败 + run_always:true → post 仍执行
  - [正向] 主流程失败 + run_always:false → post 不执行
  - [非功能] 主流程取消 + run_always:true 时 post 行为可观测
清理:      fixture
