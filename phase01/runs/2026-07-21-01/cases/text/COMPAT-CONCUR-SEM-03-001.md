用例 ID:   COMPAT-CONCUR-SEM-03-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-072
标题:      concurrency 字段命名与语义差异：GitCode enable/max/exceed-action vs GitHub group/cancel-in-progress

前置条件:
  - workflow 配置 GitCode 风格的 concurrency

操作步骤:
  1. 配置 concurrency.enable=true, max=1, exceed-action=QUEUE
  2. 快速连续触发 3 次 push
  3. 观察第 2/3 次触发的排队/取代行为
  4. 对比 GitHub 的 group + cancel-in-progress 语义

预期结果:
  - exceed-action=QUEUE：后续触发排队，前序完成后依次执行
  - exceed-action=IGNORE：后续触发被丢弃
  - 与 GitHub 的 group/cancel-in-progress 模型语义对应关系明确
  - 迁移指南应提供 GitHub→GitCode concurrency 映射表

验证点:
  - [正向] QUEUE 模式正确排队并依次执行
  - [正向] IGNORE 模式正确丢弃后续触发
  - [正向] 文档提供 GitHub→GitCode concurrency 迁移对照

清理:      fixture
