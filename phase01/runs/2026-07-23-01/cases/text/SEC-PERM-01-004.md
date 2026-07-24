用例 ID:   SEC-PERM-01-004
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-017
参照来源:  inputs/gitcode-spec/running-pipelines/view-job-logs.md; inputs/gitcode-spec/running-pipelines/view-run-results.md
母意图:    SEC-PERM-01-003
标题:      默认状态下写操作被 403 拒绝

前置条件:
  - 仓库未声明 permissions

操作步骤:
  1. 提交一个未声明 permissions 的 workflow，尝试 push
  2. 触发 workflow

预期结果:
  - push 操作返回权限拒绝
  - 默认权限不包含未声明的写域

验证点:
  - [负向] 默认状态下写操作绝不应成功
  - [正向] 权限拒绝信息明确

清理:      重置 fixture 仓库
