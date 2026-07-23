用例 ID:   REL-LOAD-PARALLEL-03-001
维度标签:   [reliability]
维度:      可靠性
优先级:    P1
溯源意图:  INTENT-REL-043
标题:      单 workflow 含 10 个独立 job 全部正确并行分发

前置条件:
  - 10 个独立 job（无 needs），runs-on=[ubuntu-latest, x64, small]

操作步骤:
  1. 定义 10 个独立 job（各 sleep 10s）
  2. 触发 workflow
  3. 观察所有 job 的排队/执行时间线

预期结果:
  - 所有 10 个 job 最终 success
  - 任意 job 排队时间 ≤5min（runner 充足时）
  - 完成时间接近（无明显饥饿）

验证点:
  - [正向] 10 个 job 全部 success
  - [正向] 完成时间差异 < 30s
  - [非功能] 无明显 job 饥饿

清理:      none
