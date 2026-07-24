# 用例归档

用例 ID:   COMPAT-TARGET-01-001
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-032
参照来源:  inputs/gitcode-spec/core-concepts/trigger-events.md
母意图:    —
标题:      pull_request_target 默认 checkout 应为 base 分支而非 head 分支

前置条件:
  - 仓库存在 base 分支（如 main）与 fork PR
  - fork PR 的 head 分支包含与 base 分支不同的文件内容

操作步骤:
  1. 配置一个以 `pull_request_target` 触发的 workflow
  2. 该 workflow 使用 checkout 插件检出代码
  3. 在 job 中输出当前检出的 commit SHA 和 base SHA
  4. 提交一个 fork PR 并触发该 workflow

预期结果:
  - 检出的代码对应 base 分支（目标分支）的最新 commit，而非 fork PR 的 head commit
  - 日志中显示的 SHA 与 base 分支 SHA 一致
  - 系统不应默认执行不可信的 fork head 代码

验证点:
  - [负向] 日志中显示的 SHA 不应等于 fork PR head SHA
  - [正向] 日志中显示的 SHA 等于 base 分支 SHA
  - [正向] workflow 能访问仓库 secrets（pull_request_target 的特权语义）

清理:      重置 fixture 仓库
