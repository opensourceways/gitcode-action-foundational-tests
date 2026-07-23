用例 ID:   SEC-MASK-03-006
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-028
母意图:    —
标题:      fork PR 下 ::add-mask:: 命令注册新 mask 不应影响主分支 job

前置条件:
  - 仓库配置了 secret TEST_SECRET
  - 存在 fork 仓库可提交 PR

操作步骤:
  1. fork PR 的 workflow 中通过 ::add-mask:: 注册大量干扰值
  2. fork PR job 完成后，在主分支触发内部 push workflow
  3. 验证内部 job 不受 fork PR mask 影响

预期结果:
  - fork PR job 注册的 mask 值不影响后续内部 job
  - 后续内部 job 的 mask 表应独立

验证点:
  - [负向] fork PR job 注册的 mask 值在后续内部 job 中不生效
  - [负向] fork PR job 注册大量 mask 不影响后续 job 正常日志

清理:      fixture
