用例 ID:   REL-MANY-STEPS-02-001
维度标签:   [reliability]
维度:      稳定性
优先级:    P2
溯源意图:  INTENT-REL-031
母意图:    —
标题:      超多 step 的单 job 稳定性（接近 16 step 上限）

前置条件:
  - runner 资源正常

操作步骤:
  1. 创建一个包含 15 个 step 的 job
  2. 每个 step 执行简单命令
  3. 观察运行是否成功完成

预期结果:
  - 15 个 step 应全部成功执行
  - 总耗时应在合理范围内

验证点:
  - [正向] 所有 15 个 step 状态为 success
  - [nonfunctional] 总耗时 < 300 秒

清理:      重置 fixture 仓库
