用例 ID:   SEC-ENV-REVIEW-02-001
维度标签:   [security, usability]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-030
母意图:    —
标题:      环境保护规则（reviewers/wait timer）未审批时环境 Secret 不可访问

前置条件:
  - 仓库配置了 environment "production" 与对应 reviewers
  - 环境配置了环境级 secret ENV_SECRET

操作步骤:
  1. 触发一个指向 production 环境的 workflow
  2. 在审批通过前观察 workflow 状态
  3. 审批通过后再次观察

预期结果:
  - 未审批时 job 应处于等待状态，且不可访问 ENV_SECRET
  - 审批通过后 job 才能继续并读取到 ENV_SECRET

验证点:
  - [负向] 未审批时 job 不读取到 ENV_SECRET
  - [正向] 审批后 job 成功执行

清理:      重置 fixture 仓库
