用例 ID:   COMPAT-FLAVOR-LABEL-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-040
母意图:    —
标题:      资源规格标签差异——GitCode flavor（slim~2xlarge）与「large+ 需申请」vs GitHub 标准/大型 runner

前置条件:
  - runner 池包含 small/large 标签

操作步骤:
  1. 使用不同 flavor 标签触发 workflow
  2. 比较各 flavor 的 CPU/内存规格

预期结果:
  - small/large 等标签应能正确调度
  - 规格应与文档声明一致

验证点:
  - [正向] 各 flavor 成功调度
  - [nonfunctional] 规格与文档一致

清理:      重置 fixture 仓库
