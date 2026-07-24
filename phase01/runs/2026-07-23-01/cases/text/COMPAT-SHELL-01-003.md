用例 ID:   COMPAT-SHELL-01-003
维度标签:   [compatibility]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-001
母意图:    —
标题:      Windows runner 默认 shell 差异

前置条件:
  - 仓库已启用 Actions
  - 存在 Windows Runner

操作步骤:
  1. 创建一个 workflow，runs-on 使用 Windows Runner，不声明 shell
  2. 执行 `echo %OS%` 命令
  3. 触发 workflow

预期结果:
  - GitHub 行为：Windows runner 默认 shell 为 pwsh/powershell
  - GitCode 行为：默认 shell 可能不同
  - 应明确记录差异

验证点:
  - [正向] 默认 shell 正确执行 Windows 命令
  - [正向] 若默认 shell 不是 powershell，系统应给出明确说明

清理:      无
