用例 ID:   COMPAT-RUNSON-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-027
参照来源:  inputs/gitcode-spec/runner-management/selecting-runner-labels.md; inputs/platform-config/instance-config.md
母意图:    —
标题:      runs-on 标签体系——三段式数组正常匹配

前置条件:
  - 平台存在匹配 [dedicate-hosted, x64, large] 标签的 Runner

操作步骤:
  1. 在工作流中声明 `runs-on: [dedicate-hosted, x64, large]`
  2. 触发工作流，观察 Runner 调度行为
  3. 确认 job 被分配到满足所有标签的 Runner 上执行

预期结果:
  - 三段式数组格式被平台正确解析
  - job 成功调度到同时满足三个标签的 Runner
  - 工作流正常执行，无标签匹配错误

验证点:
  - [正向] 工作流成功启动并执行
  - [正向] 日志中显示 Runner 标签与声明一致
  - [负向] 不应因数组格式而被平台拒绝解析

清理:      fixture
