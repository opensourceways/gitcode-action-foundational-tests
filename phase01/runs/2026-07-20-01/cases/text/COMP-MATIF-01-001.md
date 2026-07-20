用例 ID:   COMP-MATIF-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-025
标题:      验证 job 级 if 对矩阵展开的独立求值

前置条件:
  - 仓库有 matrix job 配置
  - job 同时配置 strategy.matrix 和 job 级 if

操作步骤:
  1. 配置 java 矩阵 job，job 级 if 条件为 ${{ matrix.java-version != '21' }}
  2. 矩阵产生 java-version=[17, 21] 两个实例
  3. 观察 java-version=21 的实例是否被跳过
  4. 验证 if 使用 ${{ matrix.var }} 正常工作
  5. 对比：if 在展开前 vs 展开后求值的行为差异

预期结果:
  - job 级 if 在矩阵展开后对每个实例独立求值
  - 不同矩阵实例的 if 求值结果不同时，行为正确
  - if 中使用 ${{ matrix.var }} 可以正常工作
  - java-version=21 的实例被跳过
  - java-version=17 的实例正常执行

验证点:
  - [正向] 每个矩阵实例独立求值 job 级 if
  - [正向] if 中使用 ${{ matrix.var }} 正常工作
  - [正向] 矩阵实例正确被跳过或执行

清理:      fixture
