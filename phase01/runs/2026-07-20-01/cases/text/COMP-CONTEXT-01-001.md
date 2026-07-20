用例 ID:   COMP-CONTEXT-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-014
标题:      验证上下文对象 atomgit.* 的所有文档属性实际可用
前置条件:  仓库无特殊设置；准备 push 和 PR 两种触发事件
操作步骤:
  1. push 事件中枚举 20 个 atomgit.* 属性
  2. PR 事件中同样枚举
  3. 验证 atomgit.event 完整 payload
  4. 验证 atomgit.run_attempt 首次=1，重运行后递增
预期结果: 每个 atomgit.* 属性返回文档声明类型和值；属性不应返回 null/undefined
验证点:
  - [正向] 20 个属性在对应事件下返回非空值
  - [正向] atomgit.event 在 PR 事件下字段完整
  - [正向] atomgit.run_id 唯一，run_number 递增
  - [负向] 不存在文档声明但实际返回 null/undefined 的属性
清理:      fixture
