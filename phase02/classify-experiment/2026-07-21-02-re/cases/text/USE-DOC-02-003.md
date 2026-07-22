用例 ID:   USE-DOC-02-003
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-009
标题:      文档声明的 runner.os / runner.arch 返回值与平台实际返回值的一致性

前置条件:
  - 文档声明 runner.os 返回 Linux/Windows/macOS
  - 文档声明 runner.arch 返回 X64/ARM/ARM64
  - 已知 TC-023/TC-095：实际返回 linux（全小写）、x86_64（非 X64）

操作步骤:
  1. 在 workflow 中 echo runner.os 和 runner.arch 值
  2. 与文档声明值逐字比对

预期结果:
  - 实际返回值与文档声明一致
  - 或不一致则文档必须更新为实际取值

验证点:
  - [正向] runner.os 返回值与文档一致
  - [正向] runner.arch 返回值与文档一致
  - [负向] 不应存在大小写/命名差异

可理解性判据: 确定性判定
清理:      fixture
