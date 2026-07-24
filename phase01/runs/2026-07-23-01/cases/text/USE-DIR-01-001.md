用例 ID:   USE-DIR-01-001
维度标签:   ['usability']
维度:      usability
优先级:    P1
溯源意图:  INTENT-USE-001
参照来源:  inputs/gitcode-spec/core-concepts/trigger-events.md
母意图:    —
标题:      workflow 放置于 .gitcode/workflows/ 下可正常触发

前置条件:
  - 仓库已初始化
  - .gitcode/workflows/ 目录存在

操作步骤:
  1. 在 .gitcode/workflows/ 下提交一个合法的 workflow 文件
  2. 推送代码触发 push 事件

预期结果:
  workflow 被正常识别并触发运行

验证点:
  - [正向] 运行记录列表中出现该 workflow 的运行
  - [正向] 运行状态为成功或至少进入执行态

清理:      无

