用例 ID:   USE-PATH-01-001
维度标签:   ['usability', 'compatibility']
维度:      usability/compatibility
优先级:    P1
溯源意图:  INTENT-USE-015
参照来源:  inputs/gitcode-spec/core-concepts/trigger-events.md
母意图:    —
标题:      paths 300 文件上限在文档与行为中一致且明示

前置条件:
  - 文档版本为 2026-07-20 抓取版本

操作步骤:
  1. 检查 configure-triggers.md 中 paths 说明
  2. 触发一次变更文件数超过 300 的 push

预期结果:
  文档在显眼位置标注 300 文件上限；超出时调试日志有提示

验证点:
  - [非功能] 文档 paths 章节顶部或注意块中是否有 300 文件上限提示
  - [非功能] 超出上限时调试日志是否提示 paths 过滤超出文件上限

清理:      无

