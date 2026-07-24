用例 ID:   COMPAT-WCMD-01-003
维度标签:   [compatibility]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-NEW-009
参照来源:  inputs/gitcode-spec/syntax-reference/workflow-commands.md
母意图:    —
标题:      ::stop-commands:: 不被支持时应静默降级而非报错

前置条件:
  - 仓库已启用 Actions
  - 测试者持有 maintainer 权限

操作步骤:
  1. 创建一个 workflow，在 run 步骤中使用 `::stop-commands::` 和 `::` 恢复
  2. 触发 workflow

预期结果:
  - GitHub 行为：stop-commands 生效，后续 workflow 命令被忽略
  - GitCode 行为：若不支持 stop-commands，应静默降级而非报错

验证点:
  - [正向] workflow 不因 stop-commands 而失败
  - [负向] 不通过 stop-commands 导致 workflow 报错中断

清理:      无
