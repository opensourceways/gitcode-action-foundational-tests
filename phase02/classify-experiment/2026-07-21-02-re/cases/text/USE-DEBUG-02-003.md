用例 ID:   USE-DEBUG-02-003
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-012
标题:      日志中 ATOMGIT_* 系统变量的注入完整性

前置条件:
  - 文档列出 8 个 ATOMGIT_* 系统变量
  - 已知 TC-206：ATOMGIT_REPOSITORY_OWNER 未注入

操作步骤:
  1. 在 step 中 echo 所有 8 个 ATOMGIT_* 变量
  2. 验证每个变量非空且值正确
  3. 特别验证 ATOMGIT_REPOSITORY 格式（owner/repo）和 ATOMGIT_ACTOR 匹配触发用户

预期结果:
  - 全部 8 个变量非空、值正确
  - 变量注入无遗漏

验证点:
  - [正向] 全部 8 个变量非空且值合理
  - [正向] ATOMGIT_REPOSITORY 格式正确
  - [正向] ATOMGIT_ACTOR 匹配触发用户

清理:      fixture
