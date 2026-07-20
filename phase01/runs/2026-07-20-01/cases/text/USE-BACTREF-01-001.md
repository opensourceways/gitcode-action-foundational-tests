用例 ID:   USE-BACTREF-01-001
维度标签:   [usability, compatibility]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-017
标题:      `uses: actions/checkout@v4` 等带 owner+版本的内置 action 引用在 GitCode 下的行为与报错

前置条件:
  - GitCode 内置 action 使用无 owner 短名（如 `checkout`、`setup-node`、`cache`）

操作步骤:
  1. 配置 `uses: actions/checkout@v4`（GitHub 风格），触发 push
  2. 配置 `uses: actions/setup-node@v4`，触发 push
  3. 配置 `uses: actions/cache@v4`，触发 push
  4. 观察每次的报错内容：是 "action not found" 还是尝试拉取 actions/checkout 仓库超时？
  5. 验证错误消息是否提示 GitCode 等价短名写法

预期结果:
  - 平台应明确报错（不应无限等待拉取不存在的 actions/* 仓库）
  - 若对应 GitCode 内置 action，错误消息应提示改用短名（如 `use 'checkout' instead of 'actions/checkout@v4'`）

验证点:
  - [正-非功能] actions/checkout@v4 报错且是明确错误（非超时）
  - [正-非功能] actions/setup-node@v4 报错同上
  - [正-非功能] actions/cache@v4 报错同上
  - [非功能] 消息是否提示短名替代（0=仅报不识别, 1=提示需改但未给正确写法, 2=直接给正确写法）

清理:      fixture
