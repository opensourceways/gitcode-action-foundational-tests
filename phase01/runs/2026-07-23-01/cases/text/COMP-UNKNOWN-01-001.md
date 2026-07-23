用例 ID:   COMP-UNKNOWN-01-001
维度标签:   [completeness, compatibility]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-002
母意图:    —
标题:      包含未知顶层字段的 workflow 触发 YAML 校验失败

前置条件:
  - 仓库具备提交 workflow 的权限

操作步骤:
  1. 提交包含未知顶层字段（如 unknown_field: true）的 workflow
  2. 尝试触发该 workflow

预期结果:
  - 平台在校验阶段报错，拒绝执行该 workflow
  - 错误信息应指明不支持的字段名或行号

验证点:
  - [正向] workflow 提交后触发校验失败
  - [非功能] 错误信息包含字段名及不支持语义

清理:      none
