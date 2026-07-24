用例 ID:   USE-PERM-01-002
维度标签:   ['usability', 'compatibility']
维度:      usability/compatibility
优先级:    P1
溯源意图:  INTENT-USE-005
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    —
标题:      使用 GitHub 权限域命名时报错应给出 GitCode 对照表

前置条件:
  - workflow 文件位于 .gitcode/workflows/

操作步骤:
  1. 在 workflow 中使用 permissions: contents: read

预期结果:
  YAML 校验报错，提示 GitCode 支持的权限域列表，并指出命名差异

验证点:
  - [负向] 不应静默忽略未知权限域
  - [非功能] 报错中应列出 GitCode 可用权限域列表

清理:      无

