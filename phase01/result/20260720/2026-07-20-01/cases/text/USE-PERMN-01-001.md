用例 ID:   USE-PERMN-01-001
维度标签:   [usability, compatibility, security]
维度:      易用性
优先级:    P0
溯源意图:  INTENT-USE-016
母意图:    —
标题:      permissions 使用 GitHub 命名体系时的错误信息质量与不应静默忽略

前置条件:
  - 仓库无特殊 permissions 设置
  - 准备多个 workflow，使用 GitHub 权限命名体系（contents/pull-requests/issues/actions/packages/deployments）
  - 同时也准备使用 GitCode 权限命名的对照组

操作步骤:
  1. 提交 workflow A，使用 `permissions: { contents: read }`（GitHub 命名）
  2. 提交 workflow B，使用 `permissions: { pull-requests: write }`（GitHub 命名）
  3. 提交 workflow C，使用 `permissions: { contents: read, packages: write }`（多条 GitHub 命名混合）
  4. 观察每种情况下：(a) workflow 解析是否报错？(b) 错误信息是否指出不识别的权限项名称？(c) 若静默忽略，是否至少给出 warning？
  5. 若静默忽略，验证实际 Token 权限是否仍是默认值（而非用户意图的权限范围）

预期结果:
  - 使用 GitHub 权限命名（如 contents/pull-requests）时，平台应报错或产生 warning
  - 不应静默忽略不识别的权限项——静默忽略会导致用户以为限制了权限但实际未生效
  - 若报错，消息应包含：(1) 不识别的权限项名称，(2) GitCode 可用权限项列表（project/pr/issue/note/repository/hook）
  - 若只产生 warning（不阻断），warning 应足够显眼让用户注意到权限未按预期生效

验证点:
  - [负向] 使用 `contents: read` 时不应静默忽略——应报错或产生 warning
  - [负向] 使用 `pull-requests: write` 时不应静默忽略
  - [负向] 混合使用多条 GitHub 命名权限时不应静默忽略
  - [正向] 若报错，消息应指出不识别项名称及合法值列表
  - [负向] 不应出现：静默忽略后 Token 权限与用户预期不一致

清理:      fixture
