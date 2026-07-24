用例 ID:   COMP-TRIG-01-073
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-061~083
母意图:    —
标题:      pull_request 事件关键字段与 types 验证

前置条件:
  - 仓库已启用 AtomGit Action
  - 存在可触发 PR 的条件

操作步骤:
  1. 配置 pull_request 触发并定义 types 和 branches
  2. 创建或更新 PR 验证触发

预期结果:
  - pull_request 事件触发 workflow，types 过滤生效，branches 过滤目标分支，atomgit.event.pull_request 各字段可访问

验证点:
  - [正向] PR 创建时触发 workflow
  - [正向] event.pull_request.number 非空
  - [正向] types 仅匹配指定类型

清理:      重置 fixture 仓库
