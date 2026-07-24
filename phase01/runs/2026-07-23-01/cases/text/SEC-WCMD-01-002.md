用例 ID:   SEC-WCMD-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-029
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    —
标题:      跨运行 artifact 必须被视为不可信数据

前置条件:
  - 仓库支持 artifact 传递

操作步骤:
  1. 提交一个不可信运行（fork PR）上传 artifact
  2. 提交一个特权运行尝试下载并执行该 artifact

预期结果:
  - 特权运行不自动执行 artifact 内容
  - artifact 来源可追溯至其产出运行的信任级别

验证点:
  - [负向] 不可信来源的 artifact 绝不应被特权运行隐式信任执行
  - [正向] artifact 来源可被追溯判定

清理:      重置 fixture 仓库
