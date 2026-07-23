用例 ID:   COMPAT-WFDIR-01-001
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-013
标题:      工作流文件目录差异：.gitcode/workflows/ vs .github/workflows/

前置条件: 仓库有 workflow 文件
操作步骤:
  1. 在 .gitcode/workflows/ci.yml 创建 → 验证被识别触发
  2. 在 .gitcode/workflows/ci.yaml 创建 → 验证也被识别
  3. 在 .gitcode/workflows/readme.md → 验证被忽略
  4. 在 .github/workflows/ci.yml 创建 → 验证不被识别
  5. 两目录同时存在 → 验证 GitHub 目录的 workflow 不执行
预期结果: .gitcode/workflows/ 下 .yml/.yaml 被识别；.github/workflows/ 下不识别
验证点:
  - [正向] .gitcode/workflows/*.yml/.yaml 正确识别
  - [正向] 非 yml/yaml 文件被忽略
  - [负向] .github/workflows/ 下文件不被识别
清理:      fixture
