用例 ID:   COMP-BOUND-01-085
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-475~512
母意图:    —
标题:      cron 表达式格式与位置边界验证

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 配置 schedule 的 cron 使用各种合法符号
  2. 验证平台接受合法 cron

预期结果:
  - cron 五段式格式正确，支持 * 任意值 , 列表 - 范围 / 步长，分钟/小时/日/月/星期位置正确

验证点:
  - [正向] 含 * 的 cron 通过校验
  - [正向] 含 , 的 cron 通过校验
  - [正向] 含 - 和 / 的 cron 通过校验

清理:      重置 fixture 仓库
