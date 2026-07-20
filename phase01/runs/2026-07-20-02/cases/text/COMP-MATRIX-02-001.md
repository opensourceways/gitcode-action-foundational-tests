用例 ID:   COMP-MATRIX-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-004
标题:      验证矩阵构建 include/exclude/fail-fast/max-parallel 语义

前置条件:
  - 配置 2D matrix os=[ubuntu,windows] × node=[18,20,22]

操作步骤:
  1. 基础组合应生成 6 个实例
  2. include 追加额外组合和变量（experimental）
  3. exclude 排除指定组合
  4. fail-fast: true → 第一个失败取消其余
  5. max-parallel: 2 → 同时运行 <= 2
  6. runs-on 动态引用 ${{ matrix.os }}

预期结果:
  - 实例数 = 笛卡尔积 + include - exclude
  - include 注入额外变量在对应实例可用
  - fail-fast 和 max-parallel 正确生效

验证点:
  - [正向] 实例数正确（6 + 1 include - 1 exclude = 6）
  - [正向] include 变量可用
  - [正向] exclude 不产生实例
  - [正向] fail-fast 取消剩余实例 <= 30s
  - [正向] max-parallel 限制生效

清理:      fixture
