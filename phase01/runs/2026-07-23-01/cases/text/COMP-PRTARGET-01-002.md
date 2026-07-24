用例 ID:   COMP-PRTARGET-01-002
维度标签:   [completeness, security]
维度:      completeness
优先级:    P0
溯源意图:  INTENT-COMP-014
参照来源:  inputs/gitcode-spec/action-development/top-level-fields.md
母意图:    —
标题:      显式 checkout head.sha 后执行不可信代码的风险可控

前置条件:
  - 存在一个来自 fork 的 PR

操作步骤:
  1. 在 pull_request_target workflow 中显式 checkout head.sha
  2. 执行 head.sha 中的脚本

预期结果:
  - 平台允许此行为（设计如此）
  - 但 workflow 文件版本仍来自 base 分支

验证点:
  - [正向] checkout head.sha 成功
  - [正向] workflow 文件仍为 base 分支版本

清理:      重置 fixture 仓库
