用例 ID:   COMPAT-MATFF-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-029
标题:      matrix fail-fast 双层语义：strategy.fail-fast vs stages.fail_fast 的区分与交互

前置条件:
  - workflow 同时使用 stages.fail_fast 和 strategy.fail-fast
  - 矩阵中有多个实例

操作步骤:
  1. 测试 strategy.fail-fast: true → 矩阵内任一 job 失败取消其余
  2. 测试 strategy.fail-fast: false → 矩阵内一 job 失败其余继续
  3. 测试 stages.fail_fast: true → 当前阶段 job 失败跳过后续 stage
  4. 测试两者同时为 true 时的交互行为

预期结果:
  - strategy.fail-fast 和 stages.fail_fast 行为独立且可预测
  - 两者语义不混淆

验证点:
  - [正向] strategy.fail-fast: true → 其余矩阵 job 被取消
  - [正向] strategy.fail-fast: false → 其余 job 继续
  - [正向] stages.fail_fast: true → 后续 stage 跳过
  - [正向] 两者同时为 true → 行为可预测

清理:      fixture
