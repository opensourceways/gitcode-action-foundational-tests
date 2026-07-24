用例 ID:   COMP-PRTARGET-01-001
维度标签:   [completeness, security]
维度:      completeness
优先级:    P0
溯源意图:  INTENT-COMP-014
参照来源:  inputs/gitcode-spec/core-concepts/trigger-events.md
母意图:    —
标题:      pull_request_target 默认使用 base 分支 workflow 版本

前置条件:
  - 存在一个来自 fork 的 PR
  - base 分支 workflow 与 fork 分支 workflow 内容不同

操作步骤:
  1. fork 贡献者修改 workflow 文件
  2. 触发 pull_request_target

预期结果:
  - 执行的 workflow 版本来自 base 分支
  - fork 修改的 workflow 不影响执行逻辑

验证点:
  - [正向] 执行的 step 内容与 base 分支 workflow 一致
  - [负向] 不应执行 fork 分支修改后的 workflow 逻辑

清理:      重置 fixture 仓库
