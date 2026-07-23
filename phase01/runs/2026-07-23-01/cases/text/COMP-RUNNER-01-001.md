用例 ID:   COMP-RUNNER-01-001
维度标签:   [completeness, compatibility]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-010
母意图:    —
标题:      三段式标签正确调度到对应规格 Runner

前置条件:
  - 平台存在对应三段式标签的 Runner

操作步骤:
  1. 配置 runs-on: [ubuntu-latest, x64, small]
  2. 触发 workflow

预期结果:
  - job 被调度到符合标签的 Runner
  - 运行成功

验证点:
  - [正向] 运行状态为 success
  - [正向] job 的 Runner 标签与声明一致

清理:      none
