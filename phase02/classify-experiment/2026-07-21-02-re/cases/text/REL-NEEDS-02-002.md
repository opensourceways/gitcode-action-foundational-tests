用例 ID:   REL-NEEDS-02-002
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-024
标题:      needs 指向 matrix 父 job 时下游等待所有实例完成后执行

前置条件:
  - jobA 使用 matrix os=[ubuntu, windows] 2 实例
  - jobB needs: [A]

操作步骤:
  1. jobB 在所有 matrix 实例 completed 后才开始
  2. B 可访问 needs.<A>.result 获知汇总状态
  3. 验证无"任务初始化错误"

预期结果:
  - 下游等全部实例完成
  - 无初始化错误

验证点:
  - [正向] B 等待全部实例
  - [正向] needs 上下文正确
  - [负向] 无初始化错误（TC-486 修复确认）

清理:      fixture
