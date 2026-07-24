用例 ID:   COMP-ATOMGIT-01-048
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-048~060
参照来源:  inputs/existing-cases/cases.md
母意图:    —
标题:      atomgit 事件相关属性可访问性

前置条件:
  - 仓库已启用 AtomGit Action
  - workflow 配置为 push 触发

操作步骤:
  1. 在 push 触发的 workflow 中引用 atomgit.event 下各字段
  2. 运行 workflow 并检查日志

预期结果:
  - push 事件下 atomgit.event.ref / before / after / commits / base_ref / created / deleted 等字段可正常访问并输出非空或合理值

验证点:
  - [正向] event.ref 与 atomgit.ref 一致
  - [正向] event.before 和 event.after 为 40 位 SHA
  - [正向] event.commits 数组可访问

清理:      重置 fixture 仓库
