用例 ID:   COMP-CONTEXT-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-014
标题:      验证上下文对象 atomgit.* 的所有文档属性实际可用
incorporates: TC-028~047 (atomgit 核心属性)

前置条件:
  - 各触发事件下读取 atomgit.* 属性

操作步骤:
  1. 验证 20 个 atomgit.* 属性在对应事件下返回非空值
  2. atomgit.event 为完整 event payload 对象
  3. PR 事件下 head_ref/base_ref 有值
  4. atomgit.event_name 在各触发事件下返回正确字符串
  5. atomgit.run_id 唯一、run_number 递增

预期结果:
  - 所有文档声明属性返回文档声明的类型和值
  - event_name 取值与触发事件一致

验证点:
  - [正向] 20 个属性非空且类型正确
  - [正向] run_id 唯一、run_number 递增
  - [负向] 无属性返回 null/undefined/错误类型

清理:      fixture
