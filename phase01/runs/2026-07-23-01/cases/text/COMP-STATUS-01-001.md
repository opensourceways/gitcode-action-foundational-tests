用例 ID:   COMP-STATUS-01-001
维度标签:   [completeness, usability]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-017
参照来源:  inputs/gitcode-spec/running-pipelines/view-job-logs.md; inputs/gitcode-spec/running-pipelines/view-run-results.md
母意图:    —
标题:      运行状态机 queued 到 completed 转换正确

前置条件:
  - workflow 可正常触发

操作步骤:
  1. 触发 workflow
  2. 轮询 API 观察状态转换

预期结果:
  - 状态依次为 queued -> in_progress -> completed(success)

验证点:
  - [正向] 状态转换序列符合预期
  - [正向] 最终状态为 completed/success

清理:      none
