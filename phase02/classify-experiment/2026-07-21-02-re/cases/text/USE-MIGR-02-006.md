用例 ID:   USE-MIGR-02-006
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-019
标题:      迁移清单文档的完整性与可操作性：从 GitHub 迁移到 GitCode 的官方指南

前置条件:
  - 搜索 GitCode 官方文档中是否存在 "Migrate from GitHub Actions" / "从 GitHub 迁移" 引导页

操作步骤:
  1. 搜索是否存在迁移指南页面
  2. 逐条核对覆盖了哪些阻断性差异点：
     - 上下文命名（github.* → atomgit.*）
     - permissions 命名（contents → repository）
     - runs-on 格式（单标签 → 三段式）
     - PR types 命名（opened → open）
     - 表达式语法（success() → success）
     - inputs 类型限制（仅 string）
     - 内置 action 引用（actions/checkout@v4 → checkout）
  3. 评估每个差异点的改写示例是否可直接复制

预期结果:
  - 存在迁移指南页面
  - 覆盖全部 7 个阻断性差异点
  - 每个差异点有 GitHub vs GitCode 对比示例

验证点:
  - [正向] 迁移指南存在
  - [正向] 覆盖核心差异点
  - [非功能] 示例可直接复制使用

可理解性判据: eval: llm_assisted
清理:      fixture
