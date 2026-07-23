用例 ID:   COMPAT-CTX-AVAIL-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-025
标题:      上下文可用性矩阵：验证 atomgit/env/secrets/runner/matrix 在各作用域的可用性

前置条件:
  - 在不同作用域（workflow/job/step/if）访问各上下文

操作步骤:
  1. 测试 env 上下文在 workflow/job/step/if 各级别可用
  2. 测试 secrets 上下文在 run: 中可用，在 if: 中不可用
  3. 测试 runner 上下文在 job/step 可用，在 workflow 级别不可用
  4. 测试 job 上下文仅在 job/step 级别可用
  5. 对比 GitHub 上下文可用性矩阵

预期结果:
  - 各上下文可用性与 GitHub 对齐
  - secrets 不可在 if: 条件中直接使用
  - runner 上下文不可在 workflow 级别使用

验证点:
  - [正向] env 上下文在各作用域可用
  - [正向] secrets 在 run: 中可用
  - [负向] secrets 在 if: 中不可用
  - [正向] runner 在 job/step 可用
  - [负向] runner 在 workflow 级别不可用

清理:      fixture
