用例 ID:   SEC-DEFPERM-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-036
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    —
标题:      ATOMGIT_TOKEN 默认权限范围与 job 级覆盖必须正确生效

前置条件:
  - 仓库未声明或声明了部分 permissions

操作步骤:
  1. 提交一个 workflow，顶层声明 repository: read，job 级覆盖为 repository: write
  2. 触发 workflow 并验证实际权限

预期结果:
  - 顶层声明被各 job 继承
  - job 级声明覆盖顶层

验证点:
  - [正向] 顶层声明被各 job 继承；job 级声明覆盖顶层
  - [非功能] 权限范围与覆盖关系可被观测判定

清理:      重置 fixture 仓库
