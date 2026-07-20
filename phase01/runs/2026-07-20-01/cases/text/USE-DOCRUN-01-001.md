用例 ID:   USE-DOCRUN-01-001
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-009
标题:      文档声明的 `runner.os` / `runner.arch` 返回值与平台实际返回值的一致性

前置条件:
  - 文档 `context.md` 声明 runner.os 返回 `Linux`/`Windows`/`macOS`
  - 文档声明 runner.arch 返回 `X64`/`ARM`/`ARM64`
  - 现有案例 TC-023 显示平台实际返回 `linux`（全小写），TC-095 显示返回 `x86_64`

操作步骤:
  1. 在 workflow 中 echo `runner.os` 的值，记录实际返回
  2. 在 workflow 中 echo `runner.arch` 的值，记录实际返回
  3. 将实际返回值与文档声明值逐字比对（大小写敏感）

预期结果:
  - 文档声明值必须与平台实际返回值完全一致（大小写、命名均一致）
  - 若平台行为不改，则文档必须更新为实际取值

验证点:
  - [正-非功能] runner.os 实际返回值与文档声明完全一致
  - [正-非功能] runner.arch 实际返回值与文档声明完全一致
  - [负向] 不应存在大小写/命名差异

清理:      fixture
