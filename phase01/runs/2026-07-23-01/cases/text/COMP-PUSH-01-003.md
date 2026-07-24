用例 ID:   COMP-PUSH-01-003
维度标签:   [completeness]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-003
参照来源:  inputs/gitcode-spec/core-concepts/trigger-events.md
母意图:    —
标题:      paths 过滤匹配前 300 个变更文件行为符合预期

前置条件:
  - workflow 配置 paths: [src/**]

操作步骤:
  1. 推送仅修改 docs/ 下文件的 commit
  2. 观察 workflow 是否触发

预期结果:
  - 因 docs/ 不匹配 src/**，workflow 不应触发

验证点:
  - [负向] 运行列表中不存在该 push 触发的运行

清理:      none
