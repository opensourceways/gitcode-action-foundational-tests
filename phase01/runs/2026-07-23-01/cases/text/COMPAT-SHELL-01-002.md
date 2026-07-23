```
用例 ID:   COMPAT-SHELL-01-002
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-001
母意图:    —
标题:      默认工作目录隐式行为差异 - 未显式声明时是否为仓库根目录

前置条件:
  - 仓库已启用 GitCode Action
  - 仓库根目录下存在若干文件或子目录

操作步骤:
  1. 提交一个 workflow，其中 step 不声明 working-directory
  2. 在该 step 中输出当前工作目录，并列出当前目录内容
  3. 手动触发该 workflow

预期结果:
  - 系统在未显式声明 working-directory 时，默认将工作目录置为仓库根目录
  - 可观察到仓库根目录下的文件列表

验证点:
  - [正向] 当前工作目录路径与仓库根目录一致
  - [正向] 可访问到仓库根目录下的文件

清理:      重置 fixture 仓库
```
