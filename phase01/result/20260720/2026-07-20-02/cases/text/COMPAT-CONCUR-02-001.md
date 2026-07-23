用例 ID:   COMPAT-CONCUR-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-015
标题:      concurrency 并发模型差异：验证 GitCode enable/max/exceed-action 模型与 GitHub group/cancel-in-progress 对应关系

前置条件:
  - 配置 concurrency: { enable: true, max: N, exceed-action: QUEUE/CANCEL/IGNORE }

操作步骤:
  1. 测试 max=1, QUEUE：同时触发多个 run，仅 1 个执行其余排队
  2. 测试 max=3, CANCEL：触发 5 个 run，超额的被取消
  3. 测试排队的 run 在前一个完成后自动开始
  4. 测试 concurrency max=0 或负数的边界行为
  5. 对比 GitHub 的 group + cancel-in-progress 模型

预期结果:
  - QUEUE 下超出 max 的 run 排队执行（不取消）
  - CANCEL 下超出 max 的 run 被取消
  - 排队 run 自动开始
  - 非法值应报错

验证点:
  - [正向] max=1 QUEUE 下同时触发多个 run 仅 1 个执行
  - [正向] max=3 CANCEL 下触发 5 个 run，2 个被取消
  - [正向] 排队 run 自动开始
  - [负向] max=0/负数不应静默通过

清理:      fixture
