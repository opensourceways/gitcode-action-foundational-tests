用例 ID:   COMPAT-OUTPUT-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-NEW-006
母意图:    —
标题:      跨 Job 引用未声明 output 时返回空值的差异

前置条件:
  - 仓库已启用 Actions
  - 测试者持有 maintainer 权限

操作步骤:
  1. 创建 workflow，job A 声明 outputs，job B 通过 needs 引用 job A 的 outputs
  2. job B 引用一个 job A 未声明的 output 键
  3. 触发 workflow

预期结果:
  - GitHub 行为：引用未声明的 output 返回空字符串
  - GitCode 行为：可能返回空字符串或报错
  - 应明确记录差异

验证点:
  - [正向] 跨 Job 引用未声明 output 时不导致 workflow 崩溃
  - [正向] 返回值与 GitHub 行为一致（空字符串）

清理:      无
