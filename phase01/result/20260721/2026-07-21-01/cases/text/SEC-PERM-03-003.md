用例 ID:   SEC-PERM-03-003
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-017
母意图:    —
标题:      job 级 permissions 声明可覆盖 workflow 级声明

前置条件:
  - 存在 push 触发的 workflow

操作步骤:
  1. workflow 级声明 permissions: repository: none
  2. 特定 job 级声明 permissions: repository: read
  3. 验证该 job 可 clone 代码但 workflow 级权限受限

预期结果:
  - job 级 permissions 覆盖 workflow 级的同名权限域
  - job 未声明时继承 workflow 级权限
  - 权限放大有文档说明

验证点:
  - [正向] workflow 级设 repository:none，job 级设 repository:read，job 应能 clone
  - [负向] workflow 级设 pr:write，job 级不声明，job 应继承 pr:write

清理:      none
