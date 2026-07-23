用例 ID:   COMPAT-FFAIL-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-029
标题:      matrix fail-fast 双层语义

前置条件: 仓库 matrix job 配置 strategy.fail-fast 和 stages.fail_fast
操作步骤:
  1. strategy.fail-fast:true → 矩阵 1/3 失败其余被取消
  2. strategy.fail-fast:false → 矩阵 1/3 失败其余继续
  3. stages.fail_fast:true → 阶段内 job 失败后续阶段跳过
  4. 两者同时为 true → 验证行为可预测

预期结果: strategy.fail-fast 和 stages.fail_fast 各自独立生效
验证点:
  - [正向] strategy.fail-fast 取消语义正确
  - [正向] stages.fail_fast 跳过语义正确
清理:      fixture
