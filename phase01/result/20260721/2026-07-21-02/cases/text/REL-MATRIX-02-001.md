用例 ID:   REL-MATRIX-02-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-005
标题:      二维矩阵生成 16 个 job 实例时全部正确展开并独立执行

前置条件:
  - 4(os) × 4(node) = 16 实例 matrix
  - max-parallel=8

操作步骤:
  1. 验证 16 个 job 全部生成
  2. 每个 job 的 matrix 上下文值正确注入
  3. runs-on 动态解析正确
  4. 无"任务初始化错误"（TC-486 问题确认）

预期结果:
  - 16 实例全部生成
  - matrix 变量值正确
  - job 日志独立无交叉

验证点:
  - [正向] 16 个 job 全部可枚举
  - [正向] matrix 变量值正确
  - [负向] 无初始化错误
  - [非功能] 日志独立无交叉

清理:      fixture
