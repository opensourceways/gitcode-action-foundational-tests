# 用例归档

用例 ID:   COMPAT-MIGRATE-01-001
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-031
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    —
标题:      GitHub 风格 permissions 块迁移报错应给出可操作指引

前置条件:
  - 仓库已启用 workflow
  - 测试者持有 maintainer 权限

操作步骤:
  1. 在仓库中创建一个包含 GitHub 风格 `permissions` 字段的 workflow 文件
  2. 该 `permissions` 块使用 `contents: read` 和 `pull-requests: write` 等 GitHub 命名
  3. 尝试通过 API 或 UI 提交/校验该 workflow

预期结果:
  - 系统拒绝该 workflow（GitCode 不支持 `permissions` 块）
  - 报错信息应明确指出 `permissions` 字段不被支持，并建议删除该块
  - 报错不应仅给出模糊的 "unknown property"

验证点:
  - [负向] 不通过无指引的原始报错（如仅报 YAML 解析错误）
  - [正向] 报错信息包含 `permissions` 关键字及可操作建议
  - [正向] 报错指向正确行号或字段名

清理:      重置 fixture 仓库
