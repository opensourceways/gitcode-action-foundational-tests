用例 ID:   COMPAT-STAGE-FIELDS-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-059
母意图:    —
标题:      GitCode 特有 stage 字段——select/pre/fail-fast 无 GitHub 对应的语义确认

前置条件:
  - workflow 使用 stage 的 select、pre、fail-fast 字段

操作步骤:
  1. 定义包含 select、pre、fail-fast 的 stage
  2. 触发并观察各字段的行为

预期结果:
  - select 应按条件选择执行 job
  - pre 应在 stage 前执行
  - fail-fast 应控制失败传播

验证点:
  - [正向] select 条件生效
  - [正向] pre step 在 stage job 前执行
  - [正向] fail-fast 控制失败传播

清理:      重置 fixture 仓库
