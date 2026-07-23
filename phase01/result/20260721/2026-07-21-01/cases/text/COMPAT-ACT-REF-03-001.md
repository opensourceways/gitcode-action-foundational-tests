用例 ID:   COMPAT-ACT-REF-03-001
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-050
标题:      Action 引用格式差异：uses: checkout vs uses: actions/checkout@v4

前置条件:
  - workflow 中使用不同格式的 uses 引用

操作步骤:
  1. 使用 GitCode 短名格式 uses: checkout
  2. 使用 GitHub 格式 uses: actions/checkout@v4
  3. 使用 GitCode 完整格式 uses: official_checkout
  4. 对比三种写法是否都能成功 checkout

预期结果:
  - uses: checkout（GitCode 短名）应成功执行
  - uses: actions/checkout@v4（GitHub 格式）应明确报错「action not found」
  - 报错应指引用户替换为 GitCode 短名

验证点:
  - [正向] GitCode 短名 checkout 正常执行
  - [正向] GitHub 格式明确报错（非静默失败）
  - [正向] 报错含可操作替换指引

清理:      fixture
