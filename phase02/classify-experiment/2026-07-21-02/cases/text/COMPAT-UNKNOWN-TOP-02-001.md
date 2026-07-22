用例 ID:   COMPAT-UNKNOWN-TOP-02-001
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-041
母意图:    —
标题:      未知/不支持顶层字段的处理——报错 vs 静默忽略（GitHub 有 run-name 等 GitCode 无）

前置条件:
  - workflow 包含 GitCode 未声明的顶层字段

操作步骤:
  1. 在 workflow 中添加 run-name、concurrency.cancel-in-progress 等 GitHub 专有字段
  2. 提交并观察解析行为

预期结果:
  - 不应静默忽略导致用户误以为功能可用
  - 应给出明确的「不支持字段」报错或警告

验证点:
  - [负向] 不静默成功运行
  - [nonfunctional] 报错精确到字段名与行号

清理:      重置 fixture 仓库
