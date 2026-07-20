用例 ID:   COMP-DAG-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-003
标题:      验证 job DAG needs 依赖拓扑的正确执行与失败传播
incorporates: TC-486/481/499 (needs 指向 matrix 父 job 初始化错误)

前置条件:
  - 配置线性依赖 A→B→C、fan-in 汇聚 A,B→C

操作步骤:
  1. 线性依赖 A→B→C 验证按序执行
  2. A 失败 → B/C 状态为 skipped
  3. A,B 汇聚到 C，A 失败 → C skipped
  4. `if: ${{ always }}` 覆盖失败传播，下游仍执行
  5. 无 needs 的 job 并行启动
  6. 5 层深度 DAG 执行正确

预期结果:
  - 依赖拓扑按 needs 声明的 DAG 执行
  - 失败传播正确：上游失败 → 下游 skipped
  - always() 覆盖默认传播

验证点:
  - [正向] 线性和汇聚拓扑正确
  - [正向] 失败传播语义正确
  - [正向] DAG 深度 >= 5 元截断
  - [负向] needs 指向 matrix 父 job 不产生"任务初始化错误"

清理:      fixture
