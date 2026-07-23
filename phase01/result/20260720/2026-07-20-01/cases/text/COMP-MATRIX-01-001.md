用例 ID:   COMP-MATRIX-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-004
母意图:    —
标题:      验证矩阵构建: include/exclude/fail-fast/max-parallel 语义

前置条件:  仓库无特殊设置；准备 matrix 测试 workflow

操作步骤:
  1. 配置 2D matrix os=[ubuntu, windows] × node=[18, 20]，验证 4 实例
  2. 配置 include 追加额外变量 experimental
  3. 配置 exclude 排除特定组合
  4. 验证 fail-fast: true 时首个失败取消其余 job
  5. 验证 max-parallel 限制

预期结果:
  - 矩阵实例数 = 笛卡尔积 × exclude 调整
  - include 注入额外变量可通过 ${{ matrix.var }} 读取
  - fail-fast 正确取消未完成 job
  - max-parallel 限制生效

验证点:
  - [正向] 矩阵展开实例数正确
  - [正向] include/exclude 语义正确
  - [正向] fail-fast 取消传播正确
  - [正向] max-parallel 并发限制生效

清理:      fixture
