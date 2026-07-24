用例 ID:   COMPAT-MATRIX-01-005
维度标签:   [compatibility]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-NEW-007
母意图:    —
标题:      matrix exclude 全排除不被支持时的差异

前置条件:
  - 仓库已启用 Actions
  - 测试者持有 maintainer 权限

操作步骤:
  1. 创建一个 workflow，配置 `strategy.matrix.exclude` 排除所有组合
  2. 提交并触发 workflow

预期结果:
  - GitHub 行为：exclude 全排除时应报矩阵为空错误或生成 0 个实例
  - GitCode 行为：可能不支持 exclude 全排除
  - 应明确记录差异

验证点:
  - [正向] 系统对空矩阵给出明确报错
  - [负向] 不通过 exclude 被静默忽略导致所有实例仍生成

清理:      无
