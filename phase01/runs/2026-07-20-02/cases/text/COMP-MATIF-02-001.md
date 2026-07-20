用例 ID:   COMP-MATIF-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-025
标题:      验证 job 级 if 对 matrix 展开的独立求值

前置条件:
  - job 同时有 strategy.matrix 和 job 级 if

操作步骤:
  1. if: ${{ atomgit.ref == 'refs/heads/main' }} + matrix
  2. 验证 if 在矩阵展开后逐实例独立求值
  3. if 中使用 ${{ matrix.var }}
  4. 不同矩阵实例 if 结果不同时行为正确

预期结果:
  - 矩阵展开后每个实例独立求值 if
  - 与 GitHub 行为一致

验证点:
  - [正向] 逐实例独立求值 if
  - [正向] matrix.var 在 if 中可用
  - [正向] 不同实例可产生不同 if 结果

清理:      fixture
