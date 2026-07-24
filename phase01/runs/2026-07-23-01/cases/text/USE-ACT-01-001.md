用例 ID:   USE-ACT-01-001
维度标签:   ['usability', 'compatibility']
维度:      usability/compatibility
优先级:    P1
溯源意图:  INTENT-USE-007
参照来源:  inputs/gitcode-spec/action-development/top-level-fields.md
母意图:    —
标题:      使用裸插件名 checkout 时正常拉取官方 Action

前置条件:
  - GitCode 官方插件市场可用

操作步骤:
  1. 在 step 中写 uses: checkout

预期结果:
  官方 Action 被正确拉取并执行

验证点:
  - [正向] checkout step 成功执行
  - [正向] 运行成功完成

清理:      无

