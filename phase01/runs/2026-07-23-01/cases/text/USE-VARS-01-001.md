用例 ID:   USE-VARS-01-001
维度标签:   ['usability']
维度:      usability
优先级:    P1
溯源意图:  INTENT-USE-014
母意图:    —
标题:      vars 上下文在文档与样本中的声明必须一致

前置条件:
  - 文档与样本版本为 2026-07-20 抓取版本

操作步骤:
  1. 比对 syntax-reference/context.md 与 workflow-samples 注释对 vars 的支持声明

预期结果:
  两者声明一致：要么均支持，要么均不支持

验证点:
  - [正向] 若支持，文档示例可运行且样本注释已移除已知不支持
  - [负向] 若不支持，文档中不应出现 vars 使用示例

清理:      无

