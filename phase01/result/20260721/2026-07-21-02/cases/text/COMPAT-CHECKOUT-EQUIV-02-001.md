用例 ID:   COMPAT-CHECKOUT-EQUIV-02-001
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-047
母意图:    —
标题:      checkout action 差异——GitCode uses: checkout 参数集与 GitHub actions/checkout@v4 等价性

前置条件:
  - 仓库存在分支与 PR

操作步骤:
  1. 使用 GitCode checkout action 并传入 fetch-depth、ref 等参数
  2. 比较检出结果与 GitHub 行为的等价性

预期结果:
  - 常用参数（fetch-depth、ref）应生效
  - 检出结果应与 GitHub 行为一致

验证点:
  - [正向] fetch-depth=0 成功获取完整历史
  - [正向] ref 参数正确检出指定分支

清理:      重置 fixture 仓库
