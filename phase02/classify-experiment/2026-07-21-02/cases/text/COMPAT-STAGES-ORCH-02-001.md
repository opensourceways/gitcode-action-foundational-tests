用例 ID:   COMPAT-STAGES-ORCH-02-001
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-057
母意图:    —
标题:      stages 编排层——GitHub 扁平 jobs 迁移到 GitCode 是否需引入 stages 及默认行为

前置条件:
  - workflow 使用 stages 结构

操作步骤:
  1. 定义包含多个 stage 的 workflow
  2. 观察 stage 间串行执行与默认行为

预期结果:
  - stage 应按顺序串行执行
  - 默认行为应与文档一致

验证点:
  - [正向] stage 按顺序执行
  - [nonfunctional] 默认行为可预测

清理:      重置 fixture 仓库
