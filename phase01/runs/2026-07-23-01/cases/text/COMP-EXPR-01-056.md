用例 ID:   COMP-EXPR-01-056
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-187
母意图:    —
标题:      toJson 函数边界行为

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 在 run 中使用 toJson 序列化 atomgit.event 和 env 上下文
  2. 验证输出为合法 JSON 字符串

预期结果:
  - toJson 将对象序列化为合法 JSON 字符串，字符串含转义

验证点:
  - [正向] toJson(atomgit.event) 输出以 { 开头
  - [正向] toJson(env) 输出合法 JSON
  - [正向] 嵌套对象可被正确序列化

清理:      重置 fixture 仓库
