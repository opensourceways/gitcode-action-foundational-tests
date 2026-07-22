用例 ID:   COMPAT-SYSENV-MAP-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-032
母意图:    —
标题:      系统环境变量映射差异——GITHUB_* 全集 → ATOMGIT_* 及缺失变量

前置条件:
  - workflow 引用 GITHUB_ENV/GITHUB_OUTPUT 等 GitHub 式变量名

操作步骤:
  1. 在 workflow 中同时输出 GITHUB_ENV 与 ATOMGIT_ENV 的值
  2. 比较两者是否存在及内容一致性

预期结果:
  - ATOMGIT_* 变量应存在且内容正确
  - GITHUB_* 变量名应被映射或给出迁移提示

验证点:
  - [正向] ATOMGIT_ENV 非空
  - [负向] 无静默空值陷阱
  - [nonfunctional] 若 GITHUB_ENV 不被支持，报错应可理解

清理:      重置 fixture 仓库
