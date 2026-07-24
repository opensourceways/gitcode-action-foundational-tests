用例 ID:   USE-PERM-01-001
维度标签:   ['usability', 'compatibility']
维度:      usability/compatibility
优先级:    P1
溯源意图:  INTENT-USE-005
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    —
标题:      使用 GitCode 权限域命名时正常生效

前置条件:
  - 仓库已配置权限

操作步骤:
  1. 在 workflow 中使用 permissions: repository: read

预期结果:
  权限声明被正确解析，运行成功

验证点:
  - [正向] 运行成功完成
  - [正向] 权限声明未导致校验失败

清理:      无

