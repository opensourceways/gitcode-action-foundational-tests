用例 ID:   COMPAT-STAGES-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-017
标题:      stages 阶段机制：验证阶段间串行语义 + fail_fast 正确性

前置条件:
  - 多 stage workflow：build → test → deploy
  - 每个 stage 内含多个 job

操作步骤:
  1. 验证 3 个 stage 按 build → test → deploy 顺序串行执行
  2. 验证 stage 内多个 job 并行执行
  3. 测试 fail_fast: true 时 build 阶段失败 → test/deploy 不执行
  4. 测试 fail_fast: false 时 build 失败 → test/deploy 继续
  5. 测试 stages + needs 同时存在时的交互行为（needs 在阶段内生效还是跨阶段）
  6. 已知 TC-486/481/499：needs 指向 matrix 父 job 导致初始化错误

预期结果:
  - stages 按声明顺序串行执行
  - fail_fast 行为与文档一致
  - stages + needs 交互语义可预测

验证点:
  - [正向] build → test → deploy 顺序执行
  - [正向] stage 内 job 并行
  - [正向] fail_fast: true → 后续 stage 跳过
  - [负向] stages + needs 不应有未文档化的交互行为

清理:      fixture
