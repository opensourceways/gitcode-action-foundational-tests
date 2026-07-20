用例 ID:   SEC-CONFIG-01-002
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-034
标题:      PAT 权限模型文档声明：permissions 仅控制 ATOMGIT_TOKEN，不约束手动注入的 token

前置条件:
  - 仓库有 workflow 使用手动创建的 PAT（个人访问令牌）
  - 同时有 workflow 使用 ATOMGIT_TOKEN

操作步骤:
  1. 在 workflow 中同时使用 ATOMGIT_TOKEN 和手动注入的 MANUAL_PAT
  2. 声明 permissions: {repository: none}
  3. 使用 ATOMGIT_TOKEN 调用 API → 预期被权限限制
  4. 使用 MANUAL_PAT 调用相同 API → 验证是否同样受限
  5. 查阅文档：是否明确声明 permissions 不约束手动 token

预期结果:
  - ATOMGIT_TOKEN 受 permissions 约束 → API 调用被限
  - 手动 PAT 不受 permissions 约束 → API 调用成功（若 PAT 有权限）
  - 文档明确声明此差异
  - 不应让用户误以为 permissions 约束所有 token

验证点:
  - [正向] ATOMGIT_TOKEN 受 permissions 约束 → API 调用被限
  - [正向] 手动 PAT 不受 permissions 约束 → 可正常使用
  - [非功能] 文档是否明确声明 permissions 仅控制 ATOMGIT_TOKEN

清理:      fixture
