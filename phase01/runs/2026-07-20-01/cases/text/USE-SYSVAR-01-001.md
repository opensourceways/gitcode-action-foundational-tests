用例 ID:   USE-SYSVAR-01-001
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-012
标题:      日志中 `ATOMGIT_*` 系统变量的注入完整性

前置条件:
  - 文档 `view-job-logs.md` 列出 8 个 ATOMGIT_* 系统变量
  - 现有案例 TC-206 报告 ATOMGIT_REPOSITORY_OWNER 未注入

操作步骤:
  1. 在 workflow 中逐个 echo 全部 8 个 ATOMGIT_* 变量：
     ATOMGIT_REPOSITORY, ATOMGIT_EVENT_NAME, ATOMGIT_REF, ATOMGIT_SHA,
     ATOMGIT_ACTOR, ATOMGIT_TOKEN, ATOMGIT_RUN_ID, ATOMGIT_RUN_NUMBER
  2. 验证每个变量的值非空且内容合理
  3. 特别验证 ATOMGIT_REPOSITORY 包含正确 owner/repo 格式
  4. 验证 ATOMGIT_ACTOR 值匹配当前触发用户

预期结果:
  - 全部 8 个 ATOMGIT_* 变量在 Runner 环境中有效注入
  - 每个变量的值非空且含义正确

验证点:
  - [正-非功能] 8 个变量全部非空（可 shell 脚本断言）
  - [正-非功能] ATOMGIT_REPOSITORY 格式为 owner/repo
  - [正-非功能] ATOMGIT_ACTOR 匹配触发用户

清理:      fixture
