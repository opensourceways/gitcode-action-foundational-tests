用例 ID:   USE-MIGDOC-01-001
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-019
标题:      从 GitHub Actions 迁移到 GitCode Action 的官方迁移指南的完整性与可操作性

前置条件:
  - COMPAT-NOTES.md 列出了全部已知差异点（11 大类约 30+ 条）

操作步骤:
  1. 搜索 GitCode 官方文档中是否存在 "Migrate from GitHub Actions" / "从 GitHub 迁移" 等关键词的页面
  2. 逐条核对迁移指南是否覆盖以下 7 个阻断性差异点：
     (a) 上下文命名（github.* → atomgit.*）
     (b) permissions 命名（contents → project, pull-requests → pr）
     (c) runs-on 格式（ubuntu-latest → 三段式标签）
     (d) pull_request.types 命名（opened → open, synchronize → update）
     (e) 表达式状态函数语法（success() → success）
     (f) workflow_dispatch.inputs 类型限制（仅 string）
     (g) 内置 action 引用方式（actions/checkout@v4 → checkout）
  3. 验证每个差异点是否配有：差异说明 + GitHub 写法 + GitCode 写法 + 报错现象

预期结果:
  - 存在一份从 GitHub Actions 迁移到 GitCode Action 的官方指南
  - 至少覆盖上述 7 个阻断性差异点
  - 每个差异点的改写示例可直接复制使用

验证点:
  - [正-非功能] 迁移指南存在（可确定性搜索）
  - [正-非功能] 覆盖 ≥ 5 个阻断性差异点
  - [非功能] 指南操作性评估：代码示例可复制、说明具体（0=不可操作, 1=部分可操作, 2=完整可操作）

清理:      none
