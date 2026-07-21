用例 ID:   COMPAT-ACTION-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-012
标题:      验证内置 action 引用格式差异 checkout vs actions/checkout@v4
incorporates: TC-310 (setup-java 不存在)

前置条件:
  - 使用 GitCode 短名和 GitHub 全路径引用

操作步骤:
  1. uses: checkout → 正确 checkout 代码
  2. uses: setup-node/setup-python/setup-go → 可用
  3. uses: cache/upload-artifact/download-artifact → 可用
  4. uses: actions/checkout@v4（GitHub 格式）→ 验证报错
  5. 各内置 action 的 outputs 与 GitHub 对齐

预期结果:
  - GitCode 短名正确执行
  - GitHub 全路径格式明确报错
  - setup-java 应存在

验证点:
  - [正向] checkout setup-node 可用
  - [正向] 参数和 outputs 对齐
  - [负向] actions/checkout@v4 报错

清理:      fixture
