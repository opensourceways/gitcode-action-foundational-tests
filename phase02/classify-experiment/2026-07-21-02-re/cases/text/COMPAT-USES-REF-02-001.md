用例 ID:   COMPAT-USES-REF-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-044
母意图:    —
标题:      uses action 引用方式差异——GitHub owner/repo@ref marketplace vs GitCode 官方短名 + 本地

前置条件:
  - workflow 使用 GitHub 式 uses: owner/repo@v1 引用

操作步骤:
  1. 在 workflow 中使用 GitHub 式 owner/repo@ref 引用 action
  2. 再使用 GitCode 官方短名引用同一 action
  3. 比较两者的行为

预期结果:
  - GitCode 短名应成功解析
  - GitHub 式引用应给出明确的格式错误或迁移提示

验证点:
  - [正向] 官方短名运行成功
  - [nonfunctional] GitHub 式引用报错可理解

清理:      重置 fixture 仓库
