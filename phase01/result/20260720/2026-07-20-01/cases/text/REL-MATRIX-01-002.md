用例 ID:   REL-MATRIX-01-002
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-006
标题:      matrix include 追加 3 组合，exclude 1 组合，总数正确

前置条件: 基础矩阵 2×2=4，include 3，exclude 1 → 预期 6
操作步骤:
  1. 配置 matrix 含 include/exclude
  2. 触发 workflow
  3. 验证总 job 数 = 6
  4. 验证 include 中额外变量仅其对应实例可见

预期结果: 6 实例；include 变量仅对 include 实例可见；被 exclude 的组合无实例
验证点:
  - [正向] 总 job 数 = 6
  - [正向] include 额外变量作用域正确
  - [负向] 被 exclude 组合无 job
清理:      none
