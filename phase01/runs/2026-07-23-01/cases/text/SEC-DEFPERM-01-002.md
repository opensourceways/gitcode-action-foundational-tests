用例 ID:   SEC-DEFPERM-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-036
母意图:    SEC-DEFPERM-01-001
标题:      job 级覆盖后权限正确收窄

前置条件:
  - 仓库声明了顶层 permissions: repository: write

操作步骤:
  1. 提交一个 workflow，顶层声明 repository: write，job 级覆盖为 repository: read
  2. 触发 workflow 并验证 job 实际权限

预期结果:
  - job 级收窄后不应仍保留顶层的更大权限
  - token 实际权限应与 job 级声明一致

验证点:
  - [负向] job 级收窄后不应仍保留顶层的更大权限
  - [正向] 各权限域实测与有效声明一致，越权写被拒

清理:      重置 fixture 仓库
