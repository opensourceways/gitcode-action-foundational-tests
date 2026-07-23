用例 ID:   COMP-ISOLATION-01-004
维度标签:   [completeness]
维度:      功能完备性
优先级:    P0
溯源意图:  INTENT-COMP-011
母意图:    COMP-ISOLATION-01-001
标题:      Runner 跨 run 的 tmp 目录隔离验证

前置条件:
  - 仓库已启用 Actions
  - 使用平台托管 Runner

操作步骤:
  1. 触发一个 push workflow，第一步检查 /tmp 下是否存在历史标记文件
  2. 在 workflow 末尾在 /tmp 写入隔离标记文件

预期结果:
  - 首次运行时，/tmp 下不应存在上轮遗留的标记文件
  - 若平台复用 Runner 且未清理 /tmp，标记可能残留

验证点:
  - [正向] 日志显示 TMP_ISOLATED
  - [负向] 日志不含 TMP_RESIDUE_FOUND

清理:      fixture
