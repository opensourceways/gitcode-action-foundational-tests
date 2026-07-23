用例 ID:   COMP-RERUN-01-002
维度标签:   [completeness, reliability]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-009
母意图:    —
标题:      第 4 次 rerun 应被系统拒绝

前置条件:
  - 某条运行已 rerun 3 次

操作步骤:
  1. 尝试第 4 次 rerun

预期结果:
  - 系统拒绝第 4 次 rerun
  - 返回明确提示说明已达最大重试次数

验证点:
  - [负向] 第 4 次 rerun 不应创建新运行
  - [非功能] 报错信息应说明最多 3 次限制

清理:      none
