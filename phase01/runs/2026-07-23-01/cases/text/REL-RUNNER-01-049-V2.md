用例 ID:   REL-RUNNER-01-049-V2
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-049
母意图:    —
标题:      Runner 规格真实性——xlarge/2xlarge 实际 CPU/内存/磁盘 vs 声明值

前置条件:
  - 仓库具备大规格 runner 使用权限

操作步骤:
  1. 对 xlarge/2xlarge 各触发探针 job，读取系统资源

预期结果:
  - 每种 flavor 实际资源不低于声明值的 90%
  - 失败时归因清晰

验证点:
  - [正向] CPU/内存/磁盘最小比率≥0.9
  - [负向] 不应因架构不匹配而随机失败

清理:      无需特殊清理
