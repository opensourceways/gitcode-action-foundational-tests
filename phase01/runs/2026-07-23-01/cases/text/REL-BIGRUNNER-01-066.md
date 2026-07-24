用例 ID:   REL-BIGRUNNER-01-066
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-066
参照来源:  inputs/gitcode-spec/runner-management/selecting-runner-labels.md; inputs/platform-config/instance-config.md
母意图:    —
标题:      大规格资源调度稳定性——xlarge/2xlarge 反复编译成功率

前置条件:
  - 仓库具备 xlarge/2xlarge runner 使用权限

操作步骤:
  1. 对 xlarge 和 2xlarge 各触发 10 次编译型 job

预期结果:
  - 成功率≥90%
  - 失败归因 100% 明确
  - 无 flaky

验证点:
  - [正向] 成功率≥90%
  - [正向] 失败归因明确
  - [负向] 不应出现同一规格今天成功明天失败

清理:      无需特殊清理
