```
用例 ID:   COMPAT-SHELL-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-001
母意图:    —
标题:      默认 shell 隐式行为差异 - 未显式声明时是否为 bash

前置条件:
  - 仓库已启用 GitCode Action
  - 存在一个可手动触发的 workflow 入口

操作步骤:
  1. 提交一个 workflow，其中 step 不声明 shell 字段
  2. 在该 step 中输出当前进程使用的 shell 名称
  3. 手动触发该 workflow

预期结果:
  - 系统在未显式声明 shell 时，默认使用 bash 执行命令
  - 运行日志中可观察到 bash 或 /bin/bash

验证点:
  - [正向] 日志包含 bash 字样
  - [正向] 命令按 bash 语法解析执行（如 here-string、数组等可用）

清理:      重置 fixture 仓库
```
