用例 ID:   REL-CHILDSTATE-01-064-V2
维度标签:   [reliability]
维度:      稳定性
优先级:    P0
溯源意图:  INTENT-REL-064
参照来源:  inputs/gitcode-spec/core-concepts/trigger-events.md
母意图:    —
标题:      子任务状态传播——workflow_call 未拉起时父 workflow 不应假阳性完成

前置条件:
  - fixture 仓库引用不存在的子 workflow

操作步骤:
  1. 触发父 workflow，其通过 workflow_call 引用不存在的子 workflow

预期结果:
  - 父 workflow 明确标记 failure
  - 下游默认 job 被 skip

验证点:
  - [正向] 父 workflow 状态=failure
  - [正向] 下游 job 被 skip
  - [负向] 父 workflow 不应显示 success

清理:      重置 fixture 仓库
