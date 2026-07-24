用例 ID:   COMP-PERMS-01-001
维度标签:   [completeness, security]
维度:      completeness
优先级:    P0
溯源意图:  INTENT-COMP-013
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    —
标题:      permissions 空对象时 ATOMGIT_TOKEN 仅 repository read

前置条件:
  - 仓库具备写权限测试条件

操作步骤:
  1. 配置 permissions: {}
  2. 尝试使用 ATOMGIT_TOKEN 推送代码

预期结果:
  - 写操作因权限不足失败
  - TOKEN 仅拥有 repository:read 权限

验证点:
  - [正向] permissions: {} 下无法执行写操作
  - [负向] 推送代码应返回 403

清理:      none
