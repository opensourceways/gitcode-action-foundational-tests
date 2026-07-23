用例 ID:   SEC-PERMS-02-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-015
标题:      permissions: {}（空对象）使 ATOMGIT_TOKEN 持有最小默认权限

前置条件:
  - workflow 声明 permissions: {}

操作步骤:
  1. permissions: {} 下尝试 git push 到目标仓库
  2. 尝试通过 API 操作 PR（创建评论、合并）
  3. 验证 git clone 是否正常

预期结果:
  - 空 permissions = 最小权限：repository:read 可 clone
  - 所有写操作被拒绝

验证点:
  - [负向] git push 被拒绝
  - [负向] API 操作 PR 返回 403
  - [正向] git clone 正常成功

清理:      fixture
