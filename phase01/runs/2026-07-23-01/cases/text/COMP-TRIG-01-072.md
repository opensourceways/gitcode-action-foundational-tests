用例 ID:   COMP-TRIG-01-072
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-223~233
母意图:    —
标题:      push 事件关键字段与过滤验证

前置条件:
  - 仓库已启用 AtomGit Action
  - 存在 main 分支

操作步骤:
  1. 配置 push 触发并定义 branches / paths / tags 过滤
  2. 推送代码验证触发和字段

预期结果:
  - push 事件触发 workflow，atomgit.event.ref / before / after / commits 字段可访问，branches 过滤仅匹配分支触发

验证点:
  - [正向] push 到 main 触发 workflow
  - [正向] event.before 和 event.after 非空
  - [正向] branches 过滤生效

清理:      重置 fixture 仓库
