用例 ID:   COMPAT-BACTREF-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-012
标题:      内置 action 引用格式差异：checkout vs actions/checkout@v4

前置条件: 仓库有正常 workflow；已知 TC-310 setup-java 不存在
操作步骤:
  1. uses: checkout → 验证 checkout 支持 ref/fetch-depth/path
  2. uses: setup-node/setup-python/setup-go → 验证可用
  3. uses: cache/upload-artifact/download-artifact → 验证可用
  4. uses: actions/checkout@v4 → 验证报错
  5. checkout outputs 与 GitHub actions/checkout 一致性

预期结果: 短名正确解析；GitHub 引用格式明确报错
验证点:
  - [正向] checkout 等内置 action 短名可用
  - [负向] actions/checkout@v4 明确报错
清理:      fixture
