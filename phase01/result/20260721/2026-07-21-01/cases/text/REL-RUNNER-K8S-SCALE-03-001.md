用例 ID:   REL-RUNNER-K8S-SCALE-03-001
维度标签:   [reliability]
维度:      可靠性
优先级:    P1
溯源意图:  INTENT-REL-017
标题:      K8s runner 弹性伸缩：从 min=1 触发到 max=5 扩展后正确回收

前置条件:
  - K8s runner 配置 min=1, max=5
  - 并发触发 5 个 job

操作步骤:
  1. 确认初始 Pod 数量 = 1
  2. 同时触发 5 个并发 job
  3. 观察 Pod 是否扩展到 5
  4. 所有 job 完成后等待 5min 观察 Pod 是否缩回 1

预期结果:
  - 5 个并发 job 触发后 Pod 扩展至 5
  - 所有 job 完成后空闲 5min，Pod 缩回 min=1
  - 无 Pod 在空闲后长期残留

验证点:
  - [正向] Pod 在 3min 内扩展至 5
  - [正向] job 完成后 Pod 在 5min 内缩回 1
  - [负向] 无 Pod 残留

清理:      fixture
