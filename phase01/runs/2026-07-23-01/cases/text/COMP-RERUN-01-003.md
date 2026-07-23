用例 ID:   COMP-RERUN-01-003
维度标签:   [completeness, reliability]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-009
母意图:    —
标题:      超过 6 小时的运行不可 rerun

前置条件:
  - 存在一条完成时间超过 6 小时的运行

操作步骤:
  1. 尝试对超 6h 的运行执行 rerun

预期结果:
  - 系统拒绝 rerun

验证点:
  - [负向] 超 6h 的运行的 rerun 不应成功

清理:      none
