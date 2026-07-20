用例 ID:   REL-RUNNER-K8S-POD-03-001
维度标签:   [reliability]
维度:      可靠性
优先级:    P1
溯源意图:  INTENT-REL-018
标题:      K8s runner Pod 被意外删除后调度器感知失败并标记 Run failure

前置条件:
  - K8s runner job 执行中

操作步骤:
  1. 启动长时间运行的 job（sleep 300s）
  2. 执行 kubectl delete pod <runner-pod>
  3. 观察 Run 状态变化和调度器感知时间

预期结果:
  - Pod 被删除后 5min 内 Run 状态变为 failure
  - Run 日志中反映 Pod 意外终止
  - Run 不永久停留在 in_progress

验证点:
  - [正向] Pod 删除后 5min 内 Run failure
  - [负向] Run 不永久停留在 in_progress

清理:      full_instance
