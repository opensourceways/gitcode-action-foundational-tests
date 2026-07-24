用例 ID:   REL-RERUN-01-012
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-012
参照来源:  inputs/gitcode-spec/running-pipelines/view-job-logs.md; inputs/gitcode-spec/running-pipelines/view-run-results.md
母意图:    —
标题:      rerun 越界值——尝试第 4 次重新运行应被系统拒绝

前置条件:
  - 已完成 3 次 rerun 的运行记录存在

操作步骤:
  1. 尝试第 4 次 rerun

预期结果:
  - 第 4 次 rerun 被拒绝
  - 系统给出明确错误提示

验证点:
  - [正向] 第 4 次 rerun 按钮不可用或点击后报错
  - [正向] 错误信息含最多 3 次或类似提示

清理:      无需特殊清理
