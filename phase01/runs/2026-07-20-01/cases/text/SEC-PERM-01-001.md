用例 ID:   SEC-PERM-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-015
母意图:    —
标题:      permissions: {}（空对象）使 ATOMGIT_TOKEN 持有最小默认权限

前置条件:
  - 仓库无特殊 permissions 设置
  - workflow 声明 `permissions: {}`（空对象）
  - 准备测试写操作：git push、PR API 调用、Webhook 管理

操作步骤:
  1. 提交 workflow，声明 `permissions: {}`（空对象）
  2. 在 job 中依次尝试：(a) git clone → (b) git push → (c) 通过 API 创建 PR 评论 → (d) 通过 API 创建 Issue
  3. 记录各操作的成功/失败状态
  4. 对比：同一仓库使用 `permissions: write-all` 的 workflow 中对应操作的行为

预期结果:
  - `permissions: {}` 下 git clone 正常成功（repository:read）
  - `permissions: {}` 下 git push 被拒绝（repository:write 未授予）
  - `permissions: {}` 下 PR 写操作被拒绝（返回 403）
  - `permissions: {}` 下 Issue 创建被拒绝
  - `permissions: {}` 下 Webhook 管理被拒绝
  - ATOMGIT_TOKEN 仅拥有 repository:read 最小默认权限

验证点:
  - [正向] git clone 正常成功（repository:read 生效）
  - [负向] git push 被拒绝（返回非零退出码或 403）
  - [负向] 通过 API 操作 PR 返回 403
  - [负向] 通过 API 创建 Issue 返回 403
  - [负向] Token 权限不大于 repository:read

清理:      fixture
