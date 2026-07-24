用例 ID:   REL-ARTCONC-01-063
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-063
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    —
标题:      制品并发写一致性——多 job 同时 upload-artifact 同名 artifact

前置条件:
  - 仓库具备 artifact 使用权限

操作步骤:
  1. matrix 3 实例并行，每实例生成不同内容文件并同时 upload-artifact 到同名 artifact

预期结果:
  - 下载内容确定，绝非混合态
  - 内容完整无损

验证点:
  - [正向] 下载内容确定
  - [负向] 不应出现 ABA/BAB 等混合态

清理:      重置 fixture 仓库
