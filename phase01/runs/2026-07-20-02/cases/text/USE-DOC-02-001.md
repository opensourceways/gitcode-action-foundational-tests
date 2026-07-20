用例 ID:   USE-DOC-02-001
维度标签:   [usability]
维度:      易用性
优先级:    P2
溯源意图:  INTENT-USE-009
标题:      文档声明的 runner.os/runner.arch 返回值与平台实际返回值的一致性
incorporates: TC-094/095 (runner.os=linux, runner.arch=x86_64)

前置条件:
  - 输出 runner.os / runner.arch 与文档比对

操作步骤:
  1. echo runner.os → 与文档声明比对
  2. echo runner.arch → 与文档声明比对

预期结果:
  - 实际返回值与文档一致（或文档更新为实际值）

验证点:
  - [正向] runner.os 与文档一致
  - [正向] runner.arch 与文档一致
  - [负向] 不存在大小写/命名差异

清理:      fixture
