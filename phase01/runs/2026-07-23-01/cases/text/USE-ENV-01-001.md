用例 ID:   USE-ENV-01-001
维度标签:   ['usability', 'compatibility']
维度:      usability/compatibility
优先级:    P1
溯源意图:  INTENT-USE-003
母意图:    —
标题:      使用 ATOMGIT_SHA 环境变量时正常取值

前置条件:
  - workflow 在 GitCode Runner 上执行

操作步骤:
  1. 在 run 步骤中输出 $ATOMGIT_SHA

预期结果:
  环境变量正常输出当前 commit SHA

验证点:
  - [正向] 日志中出现非空的 SHA 值
  - [正向] 运行成功完成

清理:      无

