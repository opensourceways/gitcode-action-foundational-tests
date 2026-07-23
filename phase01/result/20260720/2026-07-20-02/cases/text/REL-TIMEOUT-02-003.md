用例 ID:   REL-TIMEOUT-02-003
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-011
标题:      timeout-minutes=0 或负数的非法值被配置校验拒绝

前置条件:
  - workflow 中某 job 设置 timeout-minutes: 0

操作步骤:
  1. 提交含 timeout-minutes: 0 的 workflow 文件
  2. 验证系统拒绝该 workflow
  3. 测试 timeout-minutes: -1 同样被拒

预期结果:
  - 系统拒绝 timeout-minutes <= 0
  - 无 job 以非法 timeout 被调度执行

验证点:
  - [正向] timeout-minutes: 0 被拒绝
  - [负向] 无 job 以 timeout=0 被实际调度

清理:      fixture
