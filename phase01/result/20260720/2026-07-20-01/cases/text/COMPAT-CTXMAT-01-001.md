用例 ID:   COMPAT-CTXMAT-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-025
标题:      上下文可用性矩阵：各上下文在各作用域可用性

前置条件: 仓库 workflow 跨作用域使用各上下文
操作步骤:
  1. env 上下文 → 验证 workflow/job/step/if 各级可用
  2. secrets 上下文 → 验证 run 可用、if 不可用（与 GitHub 一致）
  3. runner 上下文 → 验证 job/step 可用、workflow 级不可用
  4. job 上下文 → 验证仅在 job/step 级可用

预期结果: 各上下文可用性与 GitHub 矩阵对齐
验证点:
  - [正向] env 各作用域可用
  - [负向] secrets 在 if 中不可用
  - [正向] runner 作用域符合预期
清理:      fixture
