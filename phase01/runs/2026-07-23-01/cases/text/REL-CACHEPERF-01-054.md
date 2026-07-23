用例 ID:   REL-CACHEPERF-01-054
维度标签:   [reliability]
维度:      稳定性
优先级:    P2
溯源意图:  INTENT-REL-054
母意图:    —
标题:      缓存加速比——cache 命中 vs 未命中构建耗时对比

前置条件:
  - 仓库具备 cache 使用权限

操作步骤:
  1. 第一轮无 cache 记录安装耗时 T1
  2. 第二轮 cache 命中记录耗时 T2

预期结果:
  - T2 ≤ 0.5 × T1
  - restore 耗时≤30s

验证点:
  - [正向] 加速比≥2x
  - [负向] cache 命中后不应仍执行完整安装

清理:      重置 fixture 仓库
