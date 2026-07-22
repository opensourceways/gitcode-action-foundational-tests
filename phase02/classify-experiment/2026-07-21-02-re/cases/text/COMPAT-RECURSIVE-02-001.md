用例 ID:   COMPAT-RECURSIVE-02-001
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-056
母意图:    —
标题:      recursive run 防护一致性——GitCode token 触发的运行是否防递归

前置条件:
  - workflow 使用 API token 触发另一个 workflow

操作步骤:
  1. 在 workflow 中使用 curl + token 触发同一仓库的另一个 workflow
  2. 观察是否产生无限递归

预期结果:
  - 平台应检测到递归并阻止
  - 不应消耗无限配额

验证点:
  - [负向] 不产生无限递归 run
  - [正向] 首次触发后递归被拦截

清理:      重置 fixture 仓库
