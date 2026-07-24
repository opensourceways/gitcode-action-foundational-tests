用例 ID:   USE-NEST-01-002
维度标签:   ['usability']
维度:      usability
优先级:    P1
溯源意图:  INTENT-USE-026
参照来源:  inputs/gitcode-spec/core-concepts/trigger-events.md
母意图:    —
标题:      workflow_call 嵌套 2 层时应正常执行

前置条件:
  - 仓库存在 2 层嵌套的 reusable workflow

操作步骤:
  1. 主 workflow 调用 A，A 调用 B

预期结果:
  运行成功完成，无嵌套层数报错

验证点:
  - [正向] 运行成功完成
  - [负向] 不应报嵌套超限错误

清理:      无

