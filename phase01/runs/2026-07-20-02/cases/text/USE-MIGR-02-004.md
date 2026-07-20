用例 ID:   USE-MIGR-02-004
维度标签:   [usability, compatibility]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-017
标题:      uses: actions/checkout@v4 等 GitHub 风格内置 action 引用在 GitCode 下的行为与报错

前置条件:
  - 在 workflow 中使用 GitHub 风格的 owner/repo@ref 引用内置 action

操作步骤:
  1. 配置 `uses: actions/checkout@v4` → 观察报错内容和 step 状态
  2. 配置 `uses: actions/setup-node@v4` → 同上
  3. 配置 `uses: actions/cache@v4` → 同上
  4. 验证错误消息是否提示 GitCode 等价短名写法

预期结果:
  - GitHub 风格引用被识别并报错
  - 错误消息提示用短名替代（如 `checkout`, `setup-node`）

验证点:
  - [正向] actions/checkout@v4 被报错
  - [正向] 错误消息提示短名替代

可理解性判据: eval: llm_assisted
清理:      fixture
