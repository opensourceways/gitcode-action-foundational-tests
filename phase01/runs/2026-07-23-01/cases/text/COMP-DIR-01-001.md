用例 ID:   COMP-DIR-01-001
维度标签:   [completeness]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-001
参照来源:  inputs/gitcode-spec/core-concepts/trigger-events.md
母意图:    —
标题:      .gitcode/workflows/ 下的 YAML 被正确识别并触发

前置条件:
  - 仓库已启用 AtomGit Action
  - 仓库 .gitcode/workflows/ 目录下存在 ci.yml

操作步骤:
  1. 向默认分支推送代码变更
  2. 观察 Actions 标签页是否出现新运行

预期结果:
  - .gitcode/workflows/ci.yml 被识别为 workflow
  - push 事件触发该 workflow 执行
  - 运行状态最终变为 completed/success

验证点:
  - [正向] 运行记录存在且 file_path 为 .gitcode/workflows/ci.yml
  - [正向] 运行状态成功完成

清理:      none
