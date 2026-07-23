用例 ID:   COMPAT-CONCMOD-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-015
标题:      concurrency 并发控制模型差异

前置条件: 仓库 workflow 配置 concurrency
操作步骤:
  1. concurrency enable:true max:1 exceed-action:QUEUE → 验证只 1 个执行其余排队
  2. concurrency max:3 exceed-action:CANCEL → 触发 5 个 run 验证 2 个被取消
  3. 排队的 run 在前一个完成后自动开始
  4. concurrency max:0 边界 → 验证报错

预期结果: GitCode concurrency 模型正确限制并行数；QUEUE/CANCEL 语义正确
验证点:
  - [正向] QUEUE 排队语义正确
  - [正向] CANCEL 取消语义正确
  - [负向] max:0 边界有报错
清理:      fixture
