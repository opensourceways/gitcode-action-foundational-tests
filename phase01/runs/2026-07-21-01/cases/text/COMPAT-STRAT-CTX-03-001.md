用例 ID:   COMPAT-STRAT-CTX-03-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-023
标题:      strategy 上下文字段支持：验证 job-total / max-parallel 是否可用

前置条件:
  - 使用 matrix 策略展开多个 job 实例

操作步骤:
  1. 定义 matrix 展开 4 个实例（2×2）
  2. 在每个实例中输出 strategy.job-index 和 strategy.job-total
  3. 输出 strategy.max-parallel
  4. 用 if: ${{ strategy.job-index == strategy.job-total - 1 }} 实现「最后一个汇总」

预期结果:
  - strategy.job-index 正确反映 0-based 序号
  - strategy.job-total 应返回总实例数（4），若未实现返回空值需标注
  - strategy.max-parallel 应返回实际并行数，若未实现需文档标注

验证点:
  - [正向] job-index 在 [0,1,2,3] 范围内
  - [正向] job-total = 4 或文档标注未实现
  - [负向] 缺失字段不应导致 job 解析失败

清理:      fixture
