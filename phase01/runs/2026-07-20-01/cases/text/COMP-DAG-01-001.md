用例 ID:   COMP-DAG-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-003
母意图:    —
标题:      验证 job DAG: needs 依赖拓扑的正确执行与失败传播

前置条件:
  - 仓库无特殊设置
  - 准备线性依赖链 A→B→C 和汇聚依赖 A,B→C

操作步骤:
  1. 配置线性依赖 A→B→C，触发 workflow
  2. 配置汇聚依赖 A,B→C 场景，A 成功 B 失败
  3. 配置下游 job 使用 `if: ${{ always }}` 覆盖失败传播
  4. 无 needs 的 job 应并行启动
  5. DAG 拓扑深度 5 层验证

预期结果:
  - 线性依赖按 A→B→C 顺序执行
  - 汇聚依赖中的 C 在 A 和 B 都成功后执行
  - A 失败后依赖 A 的 B 状态为 skipped
  - `if: ${{ always }}` 覆盖失败传播
  - 无 needs 的 job 并行启动

验证点:
  - [正向] 线性依赖串行执行正确
  - [正向] 汇聚依赖拓扑正确
  - [正向] 失败传播默认行为（上游失败→下游 skipped）
  - [正向] `if: ${{ always }}` 覆盖失败传播
  - [非功能] DAG 深度 5 层正确执行

清理:      fixture
