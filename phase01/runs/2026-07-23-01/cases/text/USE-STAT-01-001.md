用例 ID:   USE-STAT-01-001
维度标签:   ['usability', 'compatibility']
维度:      usability/compatibility
优先级:    P1
溯源意图:  INTENT-USE-004
母意图:    —
标题:      使用 always() 带括号时若被接受则正常执行

前置条件:
  - workflow 文件合法

操作步骤:
  1. 在 step 中使用 if: ${{ always() }}

预期结果:
  该 step 无论上游成败均执行

验证点:
  - [正向] step 日志出现执行记录
  - [正向] 运行成功完成

清理:      无

