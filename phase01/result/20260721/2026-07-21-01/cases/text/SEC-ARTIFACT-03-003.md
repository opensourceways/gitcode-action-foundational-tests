用例 ID:   SEC-ARTIFACT-03-003
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-043
母意图:    —
标题:      workflow_run 不应对篡改触发事件类型的攻击免疫

前置条件:
  - 存在 workflow_run 触发的工作流

操作步骤:
  1. 验证 workflow_run 的 types 过滤是否严格生效
  2. 尝试用不匹配的触发事件触发特权 workflow
  3. 观察是否被正确拦截

预期结果:
  - workflow_run 的 types 过滤应严格匹配
  - 不匹配的事件类型不应触发特权 workflow

验证点:
  - [负向] 攻击者修改非特权 workflow 以发出非预期事件类型，特权 workflow 不应被触发
  - [负向] workflow_run 的 types 过滤配置应严格匹配

清理:      none
