用例 ID:   USE-ANNOT-01-001
维度标签:   ['usability']
维度:      usability
优先级:    P1
溯源意图:  INTENT-USE-021
母意图:    —
标题:      workflow 命令 ::error:: 与 ::warning:: 在日志中保留原文

前置条件:
  - workflow 在 GitCode Runner 上执行

操作步骤:
  1. 在 run 步骤中输出 ::error:: 和 ::warning:: 命令

预期结果:
  日志中保留原始命令文本，不静默吞掉

验证点:
  - [正向] 日志中包含 ::error:: 原始文本
  - [正向] 日志中包含 ::warning:: 原始文本

清理:      无

