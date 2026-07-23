用例 ID:   USE-TYPE-01-001
维度标签:   ['usability', 'compatibility']
维度:      usability/compatibility
优先级:    P1
溯源意图:  INTENT-USE-009
母意图:    —
标题:      使用 GitCode types 命名时正常触发

前置条件:
  - 仓库存在 PR

操作步骤:
  1. 配置 on: pull_request: types: [open, update, reopen]

预期结果:
  PR 事件正常触发 workflow

验证点:
  - [正向] PR 创建或更新时触发运行
  - [正向] 运行成功或至少进入执行态

清理:      无

