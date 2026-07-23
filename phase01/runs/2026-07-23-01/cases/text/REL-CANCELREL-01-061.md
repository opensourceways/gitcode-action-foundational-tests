用例 ID:   REL-CANCELREL-01-061
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-061
母意图:    —
标题:      取消操作可靠性——queued/running/post 各阶段取消状态正确过渡

前置条件:
  - 仓库具备取消操作权限

操作步骤:
  1. 实验 a: 触发后立即取消(queued 阶段)
  2. 实验 b: running 30s 后取消(running 阶段)
  3. 实验 c: 主 step 完成后 post 执行中取消(post 阶段)

预期结果:
  - queued 取消→终态 cancelled 无 runner 分配
  - running 取消→终态 cancelled 且 cleanup 执行
  - post 取消→主结论不变 post 被终止

验证点:
  - [正向] 各阶段取消终态稳定
  - [非功能] 取消到终态稳定时间≤60s
  - [负向] queued 取消后不应错标 success/failure

清理:      重置 fixture 仓库
