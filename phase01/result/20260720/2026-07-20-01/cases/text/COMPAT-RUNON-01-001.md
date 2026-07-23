用例 ID:   COMPAT-RUNON-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-010
标题:      runs-on 标签格式差异：三段式标签 vs 单标签

前置条件: 仓库有正常 workflow
操作步骤:
  1. runs-on: default → 验证分配到托管 runner
  2. runs-on: ubuntu-latest（GitHub 格式）→ 验证明确报错
  3. 对比 runner 上下文值与文档声明的一致性
预期结果: GitCode 三段式正确匹配；GitHub 格式有明确报错
验证点:
  - [正向] default 标签正确分配 runner
  - [负向] ubuntu-latest 有明确报错
清理:      fixture
