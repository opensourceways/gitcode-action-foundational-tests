用例 ID:   SEC-TYPO-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-015
母意图:    —
标题:      第三方 Action 应具备信任边界（typosquatting 限制）

前置条件:
  - 仓库存在 workflow 引用第三方 Action
  - 插件市场中存在与知名 Action 拼写相似但未审核的 Action

操作步骤:
  1. 提交一个 workflow，引用一个拼写与官方 Action 高度相似但未进入信任列表的第三方 Action（如 chekcout 替代 checkout）
  2. 触发该 workflow
  3. 观察系统对该引用的处理行为

预期结果:
  - 系统阻止执行未审核或拼写混淆的第三方 Action
  - 运行日志中明确提示 Action 来源不可信或被拒绝
  - 不会下载或执行 typosquatting Action 的代码

验证点:
  - [负向] workflow 未成功执行被混淆的第三方 Action
  - [负向] 系统未下载或运行未审核 Action 的代码
  - [正向] 系统返回明确的信任边界拒绝信息

清理:      重置 fixture 仓库
