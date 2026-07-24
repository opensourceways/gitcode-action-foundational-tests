用例 ID:   SEC-RUN-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-020
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    —
标题:      Job 结束后 workspace 与临时文件必须被彻底清理

前置条件:
  - 仓库支持多 job workflow

操作步骤:
  1. 提交一个多 job workflow，job A 写入敏感临时文件
  2. job B 检查是否存在 job A 的残留文件

预期结果:
  - job B 绝不应读取到 job A 残留的敏感文件
  - 即使 job A 异常崩溃，清理钩子仍应执行

验证点:
  - [负向] job B 绝不应能读取到 job A 残留的敏感文件
  - [非功能] 即使 job A 异常崩溃，清理钩子仍应执行

清理:      重置 fixture 仓库
