用例 ID:   SEC-PERM-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-016
母意图:    —
标题:      未声明 permissions 时 ATOMGIT_TOKEN 使用仓库设置中的默认权限

前置条件:
  - 仓库设置中默认 permissions 可配置为不同级别（read / write）
  - 准备两个 workflow：一个不声明 permissions，另一个显式声明 `permissions: { repository: write }`

操作步骤:
  1. 将仓库默认 permissions 设为 repository:read
  2. 提交不声明 permissions 的 workflow，尝试 git push 和 git clone
  3. 将仓库默认 permissions 改为 repository:write
  4. 提交同样不声明 permissions 的 workflow，尝试 git push
  5. 对比两次运行结果

预期结果:
  - 仓库默认 permissions 为 read 时：未声明 permissions 的 workflow 可 clone 但不可 push
  - 仓库默认 permissions 为 write 时：未声明 permissions 的 workflow 可 push
  - 行为与仓库设置中的默认值一致（不是平台硬编码的固定值）
  - 未声明 permissions 不等于 permissions: {}（最小权限）

验证点:
  - [正向] 仓库默认 read 时，不声明 permissions → 可 clone 不可 push
  - [正向] 仓库默认 write 时，不声明 permissions → 可 push
  - [负向] 未声明 permissions 时的 Token 权限不应被意外放大（超过仓库默认值）
  - [负向] 未声明 permissions 时的 Token 权限不应被意外缩小（低于仓库默认值）

清理:      fixture
