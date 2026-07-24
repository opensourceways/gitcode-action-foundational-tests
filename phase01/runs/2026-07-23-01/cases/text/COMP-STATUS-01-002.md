用例 ID:   COMP-STATUS-01-002
维度标签:   [completeness, usability]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-017
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    —
标题:      失败 step 的日志完整保留且可查看

前置条件:
  - workflow 包含会失败的 step

操作步骤:
  1. 触发 workflow
  2. 等待运行失败
  3. 通过 API 下载 job 日志

预期结果:
  - 失败 step 之前的日志完整保留
  - 失败 step 的错误输出可见

验证点:
  - [正向] 失败 step 前的输出存在于日志
  - [正向] 失败 step 的错误信息存在于日志

清理:      none
