用例 ID:   USE-MIGR-02-003
维度标签:   [usability, compatibility, security]
维度:      易用性
优先级:    P0
溯源意图:  INTENT-USE-016
标题:      permissions 使用 GitHub 命名体系时应报错而不可静默忽略

前置条件:
  - 配置 permissions: { contents: read, pull-requests: write }（GitHub 命名）

操作步骤:
  1. permissions: { contents: read } → 验证报错/warning
  2. permissions: { pull-requests: write } → 验证报错/warning
  3. 若静默忽略 → 验证实际权限可能仍为默认值

预期结果:
  - 不识别的权限项应报错
  - 决不可静默忽略
  - 给出 GitCode 可用权限项列表

验证点:
  - [正向] 不识别权限项报错/warning
  - [负向] 绝不可静默忽略
  - [负向] 不导致安全隐患

清理:      fixture
