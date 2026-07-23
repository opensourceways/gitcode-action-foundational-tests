用例 ID:   SEC-PERM-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-016
母意图:    —
标题:      显式声明的 permissions 必须在 job 级实际生效并限制 ATOMGIT_TOKEN

前置条件:
  - 仓库配置了 permissions 声明

操作步骤:
  1. 提交一个 workflow，在 job 级显式声明 repository: read
  2. 触发 workflow 并尝试执行写操作

预期结果:
  - 声明 read 时读操作成功
  - 声明 read 时写操作返回 403 或失败

验证点:
  - [正向] 声明 read 时读操作（clone、API 读取）成功
  - [负向] 声明 read 时写操作（push、评论、修改 PR）返回 403 或失败

清理:      重置 fixture 仓库
