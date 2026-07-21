用例 ID:   COMPAT-CONCUR-MODEL-02-001
维度标签:   [compatibility, reliability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-042
母意图:    —
标题:      concurrency 模型差异——GitHub group+cancel-in-progress vs GitCode enable+max+exceed-action+preemption

前置条件:
  - runner 资源正常

操作步骤:
  1. 使用 GitHub 式 concurrency 语法（group+cancel-in-progress）定义 workflow
  2. 观察平台是否兼容或给出迁移提示

预期结果:
  - GitHub 式语法不应被静默忽略
  - 若不兼容，报错应指向 GitCode 的正确语法

验证点:
  - [负向] 不静默忽略并发控制
  - [nonfunctional] 报错包含可操作的迁移建议

清理:      重置 fixture 仓库
