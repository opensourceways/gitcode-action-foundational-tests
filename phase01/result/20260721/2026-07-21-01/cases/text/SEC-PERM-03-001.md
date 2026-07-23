用例 ID:   SEC-PERM-03-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-015
母意图:    —
标题:      permissions: {} 空对象使 ATOMGIT_TOKEN 持有最小默认权限

前置条件:
  - 仓库配置了默认权限为 repository:read
  - workflow 中声明 permissions: {}

操作步骤:
  1. 在 workflow 中声明 `permissions: {}`（空对象）
  2. 通过 ATOMGIT_TOKEN 尝试 git push（写操作）
  3. 通过 ATOMGIT_TOKEN 尝试 API 操作 PR（写操作）

预期结果: permissions: {} 时仅具 repository:read；git push 被拒绝；API 写操作返回 403

验证点:
  - [负向] git push 返回非零退出码或 Permission denied
  - [负向] API 写操作 PR 返回 403
  - [正向] git clone 正常完成

清理: fixture
