用例 ID:   COMPAT-ENVIRON-01-002
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-023
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    —
标题:      environment 字段绑定 secrets 的行为差异

前置条件:
  - 仓库已启用 Actions
  - 测试者持有 maintainer 权限

操作步骤:
  1. 创建一个 workflow，job 声明 `environment: prod` 并引用环境 secret
  2. 提交并触发 workflow

预期结果:
  - GitHub 行为：environment 字段绑定环境，环境 secrets 经审批后可用
  - GitCode 行为：environment 字段不被识别，环境 secrets 不可用
  - 应明确报错或警告，不应静默忽略

验证点:
  - [负向] 不通过 environment 字段被静默忽略
  - [正向] 系统对 environment 字段给出明确报错或警告

清理:      无
