用例 ID:   COMPAT-MIGERR-01-001
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-031
母意图:    —
标题:      迁移报错质量：不兼容语法报错应指明 GitCode 差异

前置条件:
  - 仓库已启用 Actions
  - 测试分支存在

操作步骤:
  1. 提交包含 GitHub 专属语法的 workflow（如 `permissions: contents: read`、`runs-on: ubuntu-latest` 单标签、`github.*` 上下文）
  2. 观察平台 YAML 校验或运行时的错误信息

预期结果:
  - 错误信息应明确指出具体的不兼容项
  - 错误信息应给出 GitCode 的替代写法或文档链接
  - 不应出现 generic 的「语法错误」而不指明原因

验证点:
  - [正向] 错误信息包含不兼容字段/语法名称
  - [正向] 错误信息提供可操作的修改建议或替代写法

清理:      fixture
