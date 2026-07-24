用例 ID:   COMP-EXPR-01-055
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-186
母意图:    —
标题:      hashFiles 函数边界行为

前置条件:
  - 仓库已启用 AtomGit Action
  - 仓库根目录存在 package.json

操作步骤:
  1. 在 env 或 run 中使用 hashFiles 计算单文件和多文件哈希
  2. 验证输出为 64 位十六进制字符串

预期结果:
  - hashFiles 返回 64 位十六进制 SHA256 值，多文件时组合计算

验证点:
  - [正向] 单文件 hashFiles 输出 64 位 hex
  - [正向] 多文件 hashFiles 输出 64 位 hex
  - [正向] 不匹配路径返回空或固定值

清理:      重置 fixture 仓库
