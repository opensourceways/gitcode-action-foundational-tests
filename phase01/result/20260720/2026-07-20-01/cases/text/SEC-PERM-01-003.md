用例 ID:   SEC-PERM-01-003
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-017
标题:      job 级 permissions 声明可覆盖 workflow 级声明
前置条件:  仓库无特殊设置
操作步骤:
  1. workflow 级设 repository:none，job 级设 repository:read → job 应能 clone
  2. workflow 级设 pr:write，job 级设 pr:none → job 不应能操作 PR
  3. workflow 级设 repository:read，job 级不声明 → job 权限不应变为 write
预期结果: job 级覆盖生效，未设则继承 workflow 级，不存在意外权限放大
验证点:
  - [正向] job 级 repository:read 覆盖 workflow 级 repository:none → 可 clone
  - [负向] job 级 pr:none 覆盖 workflow 级 pr:write → 不可操作 PR
  - [负向] 未声明 job 级 permissions 时不出现权限放大
清理:      fixture
