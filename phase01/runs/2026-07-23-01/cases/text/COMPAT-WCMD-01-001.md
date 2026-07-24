用例 ID:   COMPAT-WCMD-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-NEW-009
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    —
标题:      ::add-mask:: 不被支持时应静默降级而非报错

前置条件:
  - 仓库已启用 Actions
  - 测试者持有 maintainer 权限

操作步骤:
  1. 创建一个 workflow，在 run 步骤中输出 `::add-mask::MY_SECRET_VALUE`
  2. 触发 workflow

预期结果:
  - GitHub 行为：add-mask 命令生效，后续该值在日志中被脱敏
  - GitCode 行为：若不支持 add-mask，应静默降级（忽略该命令）而非报错中断 workflow
  - 差异应被记录

验证点:
  - [正向] workflow 不因 add-mask 命令而失败
  - [负向] 不通过 add-mask 导致 workflow 报错中断

清理:      无
