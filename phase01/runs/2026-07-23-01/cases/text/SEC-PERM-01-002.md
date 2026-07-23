用例 ID:   SEC-PERM-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-016
母意图:    SEC-PERM-01-001
标题:      permissions 声明 read 时写操作被平台拒绝

前置条件:
  - 仓库配置了 permissions: repository: read

操作步骤:
  1. 提交一个 workflow，job 级声明 repository: read
  2. 触发 workflow 并执行 push 操作

预期结果:
  - push 操作返回 403 权限拒绝
  - token 的 effective scope 与声明一致

验证点:
  - [负向] 写操作绝不应在 read-only 声明下成功
  - [正向] 返回明确的权限拒绝错误

清理:      重置 fixture 仓库
