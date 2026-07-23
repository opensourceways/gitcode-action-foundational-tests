用例 ID:   USE-NEST-01-001
维度标签:   ['usability']
维度:      usability
优先级:    P1
溯源意图:  INTENT-USE-026
母意图:    —
标题:      workflow_call 嵌套 3 层时报错应明确提示上限为 2 层

前置条件:
  - 仓库存在 3 层嵌套的 reusable workflow

操作步骤:
  1. 主 workflow 调用 A，A 调用 B，B 调用 C

预期结果:
  系统在校验或调度阶段报错，明确说明 workflow_call 嵌套层数超过 GitCode 上限 2 层

验证点:
  - [负向] 不应静默失败或卡死
  - [非功能] 报错中是否包含 workflow_call、嵌套、2 层、上限等关键词

清理:      无

