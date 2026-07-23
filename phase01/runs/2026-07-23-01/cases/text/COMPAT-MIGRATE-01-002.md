# 用例归档

用例 ID:   COMPAT-MIGRATE-01-002
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-031
母意图:    —
标题:      GitHub 风格 run-name 语法迁移报错应给出可操作指引

前置条件:
  - 仓库已启用 workflow
  - 测试者持有 maintainer 权限

操作步骤:
  1. 在仓库中创建一个包含 GitHub 风格 `run-name` 字段的 workflow 文件
  2. 该字段值使用 GitHub 表达式语法，如 `run-name: "Build by ${{ github.actor }}"`
  3. 尝试通过 API 或 UI 提交/校验该 workflow

预期结果:
  - 系统拒绝该 workflow（GitCode 不支持 `run-name` 字段）
  - 报错信息应明确指出 `run-name` 不被支持，并建议使用 `name` 字段替代
  - 若表达式中使用 `github.actor`，报错应提示改用 `atomgit.actor`

验证点:
  - [负向] 不通过无指引的原始报错
  - [正向] 报错信息包含 `run-name` 不支持及替代方案
  - [正向] 若含 `github.*` 上下文，报错提示改用 `atomgit.*`

清理:      重置 fixture 仓库
