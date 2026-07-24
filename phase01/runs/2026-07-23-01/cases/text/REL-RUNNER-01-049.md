用例 ID:   REL-RUNNER-01-049
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-049
参照来源:  inputs/gitcode-spec/runner-management/selecting-runner-labels.md; inputs/platform-config/instance-config.md
母意图:    —
标题:      Runner 规格真实性——small/medium/large 实际 CPU/内存/磁盘 vs 声明值

前置条件:
  - 仓库具备多种 flavor runner 使用权限

操作步骤:
  1. 对 small/medium/large 各触发探针 job，读取 /proc/cpuinfo、free -m、df

预期结果:
  - 每种 flavor 实际资源不低于声明值的 90%
  - 各探针在 5 分钟内完成调度

验证点:
  - [正向] CPU/内存/磁盘最小比率≥0.9
  - [负向] 实际资源不应显著低于声明
  - [非功能] queued→running ≤5min

清理:      无需特殊清理
