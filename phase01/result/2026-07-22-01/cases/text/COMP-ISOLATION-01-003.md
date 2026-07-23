用例 ID:   COMP-ISOLATION-01-003
维度标签:   [completeness]
维度:      功能完备性
优先级:    P0
溯源意图:  INTENT-COMP-011
母意图:    COMP-ISOLATION-01-001
标题:      Runner 环境变量在跨 run 时不应残留

前置条件:
  - 仓库已启用 Actions
  - 使用平台托管 Runner

操作步骤:
  1. 触发一个 push workflow，第一步检查环境变量中是否存在上轮运行遗留的标记
  2. 在 workflow 末尾通过 ATOMGIT_ENV 写入一个标记变量

预期结果:
  - 首次运行时，环境变量中不应存在上轮标记
  - 若平台复用 Runner 且未清理环境变量，标记可能残留

验证点:
  - [正向] 日志显示 ENV_CLEAN: no previous marker
  - [负向] 日志不含 ENV_RESIDUE_FOUND

清理:      重置 fixture 仓库
