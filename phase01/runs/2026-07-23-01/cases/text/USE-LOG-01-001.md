用例 ID:   USE-LOG-01-001
维度标签:   ['usability']
维度:      usability
优先级:    P1
溯源意图:  INTENT-USE-017
母意图:    —
标题:      多 step 日志按时间线组织且边界清晰

前置条件:
  - workflow 含多个 steps

操作步骤:
  1. 触发一个含 5 个以上 steps 的 workflow
  2. 在日志面板查看组织方式

预期结果:
  step 按定义顺序排列，含时间戳前缀，长输出可折叠

验证点:
  - [正向] 日志面板中 step 按定义顺序排列，step 名称与 workflow 中 name 一致
  - [非功能] 用户能在 3 秒内定位到失败 step

清理:      无

