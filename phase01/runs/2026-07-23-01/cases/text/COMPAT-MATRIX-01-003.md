用例 ID:   COMPAT-MATRIX-01-003
维度标签:   [compatibility]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-NEW-007
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    —
标题:      matrix 三维展开不被支持时的差异

前置条件:
  - 仓库已启用 Actions
  - 测试者持有 maintainer 权限

操作步骤:
  1. 创建一个 workflow，配置三维 matrix（如 os × node × browser）
  2. 提交并触发 workflow

预期结果:
  - GitHub 行为：三维 matrix 应正常展开为多个 job 实例
  - GitCode 行为：可能不支持三维展开
  - 应明确记录差异

验证点:
  - [正向] 系统对三维 matrix 给出明确响应（接受或拒绝）
  - [负向] 不通过静默忽略导致 matrix 配置失效

清理:      无
