用例 ID:   SEC-SUPPLY-01-003
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-015
母意图:    —
标题:      第三方 Action 来源应具备信任边界（typosquatting 限制）

前置条件:
  - 仓库可引用外部 Action

操作步骤:
  1. 提交一个 workflow，引用一个与官方 Action 名称高度相似的 Action
  2. 触发 workflow

预期结果:
  - 系统不应静默解析 typosquatting 名称为合法来源
  - 首次使用未审核 Action 时应触发警告或需审批

验证点:
  - [负向] 与官方 action 名称高度相似的恶意 Action 绝不应被静默解析为合法来源
  - [非功能] 首次使用未审核 Action 时应留下审计记录

清理:      重置 fixture 仓库
