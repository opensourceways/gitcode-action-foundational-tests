用例 ID:   USE-BADGE-01-001
维度标签:   ['usability']
维度:      usability
优先级:    P1
溯源意图:  INTENT-USE-019
母意图:    —
标题:      workflow 运行完成后状态徽标及时回写且语义清晰

前置条件:
  - PR 存在且关联了 workflow

操作步骤:
  1. 触发 workflow 运行
  2. 完成后检查 Commits 页面与 PR Checks 标签页

预期结果:
  状态徽标在 30 秒内刷新，成功/失败/跳过图标语义清晰、颜色可辨

验证点:
  - [正向] Commits 页面出现对应状态徽标
  - [正向] PR Checks 标签页汇总运行结果
  - [非功能] 从运行完成到徽标刷新延迟小于 30 秒

清理:      无

