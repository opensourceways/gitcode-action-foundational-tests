用例 ID:   REL-RUNNER-RBT-03-001
维度标签:   [reliability]
维度:      可靠性
优先级:    P1
溯源意图:  INTENT-REL-016
标题:      自托管 runner 重启后自动恢复注册（「重启免注册」承诺验证）

前置条件:
  - 自托管 runner 在线并可接受 job

操作步骤:
  1. 确认 runner 在线状态
  2. 重启 runner 主机
  3. 等待 5min 后检查 runner 状态是否恢复在线
  4. 触发新 workflow 验证可调度到该 runner

预期结果:
  - 主机重启后 5min 内 runner 状态恢复在线
  - 恢复后新 workflow 可调度到该 runner 并成功执行
  - 符合 GitCode 文档「重启免注册」承诺

验证点:
  - [正向] 重启后 5min 内 runner 恢复在线
  - [正向] 恢复后可接受新 job 并执行成功
  - [负向] 无需人工重新注册

清理:      fixture
