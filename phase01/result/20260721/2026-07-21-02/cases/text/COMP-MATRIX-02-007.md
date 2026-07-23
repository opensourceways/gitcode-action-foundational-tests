用例 ID:   COMP-MATRIX-02-007
维度标签:   [completeness, compatibility]
维度:      完备性
优先级:    P1
溯源意图:  INTENT-COMP-012
标题:      验证 matrix 动态 runs-on——不同组合是否调度到对应 Runner 标签

前置条件:
  - 工作流中定义了含 os 维度的矩阵，且 runs-on 引用了 matrix 变量
  - 平台存在与矩阵 os 值对应的 Runner 标签

操作步骤:
  1. 触发含动态 runs-on 的矩阵工作流
  2. 观测各矩阵实例是否被调度到与 matrix 变量求值结果匹配的 Runner
  3. 构造 runs-on 指向不存在 Runner 标签的组合，验证平台行为
  4. 检查不同实例间是否存在环境串扰

预期结果:
  - 矩阵各实例的 runs-on 经求值后，调度到与求值结果匹配的 Runner
  - 无匹配 Runner 时给出明确、可理解的调度失败报错，不无限排队或静默跳过
  - 调度结果与矩阵实例一一对应，无串扰

验证点:
  - [正向] 矩阵含有效 os 值时，各实例分别调度到对应 Runner 并成功执行
  - [正向] include 追加的全新组合含有效 os 值时，该实例也能正确调度
  - [负向] 矩阵某组合 runs-on 求值后指向不存在的 Runner 标签，不应无限排队，应在合理时限内给出调度失败报错
  - [负向] 不同实例不应被调度到同一 Runner 后互相覆盖环境
  - [非功能] 调度失败时错误信息应指明「无匹配 Runner」而非泛化失败

清理:      fixture
