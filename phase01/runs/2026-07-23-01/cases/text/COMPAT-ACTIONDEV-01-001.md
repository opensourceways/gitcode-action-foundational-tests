用例 ID:   COMPAT-ACTIONDEV-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-NEW-010
参照来源:  inputs/gitcode-spec/action-development/top-level-fields.md
母意图:    —
标题:      action.yml 元数据校验与 GitHub 差异

前置条件:
  - 仓库已启用 Actions
  - 测试者持有 maintainer 权限

操作步骤:
  1. 创建一个 Action 仓库，包含 action.yml，使用 GitHub 风格元数据（如 `branding` 字段）
  2. 在 workflow 中引用该 Action
  3. 提交并触发 workflow

预期结果:
  - GitCode 对 action.yml 的校验规则可能与 GitHub 不同
  - 不支持的字段应被静默忽略或给出警告，不应导致 Action 无法引用

验证点:
  - [正向] 不支持的 action.yml 字段不导致 workflow 失败
  - [正向] 系统给出明确提示说明不支持的字段

清理:      重置 fixture 仓库
