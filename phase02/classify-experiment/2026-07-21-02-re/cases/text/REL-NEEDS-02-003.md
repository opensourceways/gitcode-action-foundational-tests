用例 ID:   REL-NEEDS-02-003
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-024
标题:      needs 指向 matrix 父 job 时，下游 job 正确等待所有矩阵实例完成后执行（复测 TC-486）

前置条件:
  - job A 使用 matrix 生成多个实例
  - job C needs: [A]（指向父 job，非具体实例）
  - 已知 TC-486：needs 指向 matrix 父 job 导致任务初始化错误

操作步骤:
  1. job A 的 matrix 展开为 2 个实例
  2. job C needs: [A] 等待所有实例全部完成
  3. 验证 job C 在所有 A 实例 completed 后才开始执行
  4. 验证 ${{ needs.A.result }} 可正确获取汇总状态

预期结果:
  - job C 等待所有 matrix 实例完成
  - needs 上下文可查
  - 无"任务初始化错误"

验证点:
  - [正向] job C 在所有 A 实例 completed 后才开始
  - [正向] needs 上下文正确
  - [负向] 无"任务初始化错误"（TC-486 bug）

清理:      fixture
