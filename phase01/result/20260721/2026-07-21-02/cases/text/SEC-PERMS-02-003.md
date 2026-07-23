用例 ID:   SEC-PERMS-02-003
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-017
标题:      job 级 permissions 声明可覆盖 workflow 级声明

前置条件:
  - workflow 级设 repository:none，jobA 级设 repository:read
  - workflow 级设 pr:write，jobB 级设 pr:none

操作步骤:
  1. jobA 验证可 clone（overrode none → read）
  2. jobB 验证不可操作 PR（overrode write → none）

预期结果:
  - job 级覆盖生效
  - 未设的 job 继承 workflow 级
  - 不存在意外的权限放大

验证点:
  - [正向] jobA 覆盖后可以 clone
  - [负向] jobB 覆盖后不可写 PR
  - [负向] 未设 job 的权限不意外变大

清理:      fixture
