用例 ID:   SEC-TAMPER-03-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-029
母意图:    —
标题:      fork PR 的 workflow 不应能修改目标仓库的 workflow 文件

前置条件:
  - 目标仓库有 .gitcode/workflows/protected.yml
  - fork PR workflow 尝试通过 git push 和 API 修改此文件

操作步骤:
  1. fork PR workflow 中尝试 `git push` 修改 workflow YAML
  2. fork PR workflow 中尝试 API 上传 workflow 文件
  3. 验证修改是否成功

预期结果: fork PR run 不可直接修改目标仓库 workflow 定义；操作被拒绝

验证点:
  - [负向] git push 修改 workflow 文件应返回 Permission denied
  - [负向] API 上传 workflow 文件应返回 403
  - [正向] 内部 push 修改 workflow 应正常（对照）

清理: fixture
