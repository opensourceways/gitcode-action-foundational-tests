用例 ID:   COMP-ISOLATION-01-001
维度标签:   [completeness, reliability, security]
维度:      completeness
优先级:    P0
溯源意图:  INTENT-COMP-011
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    —
标题:      同一 workflow 先后 job 的文件系统相互隔离

前置条件:
  - workflow 含两个串行 jobs

操作步骤:
  1. job 1 写入文件到工作目录
  2. job 2 尝试读取该文件

预期结果:
  - job 2 无法看到 job 1 写入的文件

验证点:
  - [负向] job 2 不应访问到 job 1 的文件
  - [正向] 显式通过 artifact 传递后 job 2 可访问

清理:      none
