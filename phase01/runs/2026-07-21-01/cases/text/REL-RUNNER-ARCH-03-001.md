用例 ID:   REL-RUNNER-ARCH-03-001
维度标签:   [reliability]
维度:      可靠性
优先级:    P1
溯源意图:  INTENT-REL-028
标题:      K8s runner 架构不匹配：runs-on 指定 arm64 但只有 x64 节点时的行为

前置条件:
  - K8s runner 集群仅有 x64 节点
  - workflow runs-on 指定 arm64

操作步骤:
  1. 配置 runs-on=[self-hosted, arm64, medium]
  2. 触发 workflow
  3. 观察 job 状态（queued/failed/误调度）

预期结果:
  - 无匹配 runner 时 job 状态 = queued/failed
  - 应有「no matching runner」提示
  - 不应被调度到错误架构的节点（x64）

验证点:
  - [负向] job 不应在 x64 节点上执行
  - [正向] job 在合理时间内明确报告 no matching runner

清理:      fixture
