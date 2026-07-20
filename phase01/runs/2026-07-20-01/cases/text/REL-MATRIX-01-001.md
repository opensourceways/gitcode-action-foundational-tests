用例 ID:   REL-MATRIX-01-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-005
标题:      二维矩阵生成 16 job 实例全部正确展开独立执行

前置条件: 矩阵 4(os)×4(node)=16，max-parallel=8
操作步骤:
  1. 触发 matrix workflow
  2. 验证 16 个 job 全部生成
  3. 验证每个 ${{ matrix.os }} 和 ${{ matrix.node }} 值正确

预期结果: 16 实例全部生成；上下文值注入正确；无"任务初始化错误"
验证点:
  - [正向] 16 job 全部可见
  - [正向] matrix 上下文值正确
  - [负向] 无初始化错误
清理:      none
