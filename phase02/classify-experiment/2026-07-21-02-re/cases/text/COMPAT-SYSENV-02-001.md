用例 ID:   COMPAT-SYSENV-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-002
标题:      验证 ATOMGIT_* 系统环境变量注入完整性
incorporates: TC-196~220 (ATOMGIT_* 变量), TC-206 (REPOSITORY_OWNER 未注入), TC-533 (Job env 不注入 Shell)

前置条件:
  - 在 step 中输出所有 ATOMGIT_* 系统变量

操作步骤:
  1. echo 所有文档声明的 ATOMGIT_* 变量
  2. 验证 ATOMGIT_TOKEN 在 shell 中可用
  3. 验证 ATOMGIT_REPOSITORY_OWNER 实际注入（TC-206）
  4. 验证 $GITHUB_TOKEN 等 GitHub 前缀命名是否可用

预期结果:
  - 所有文档声明的 ATOMGIT_* 变量在 shell 中有值
  - GitHub 前缀命名不可用或明确报错

验证点:
  - [正向] ATOMGIT_* 变量非空且格式正确
  - [负向] $GITHUB_TOKEN/GITHUB_OUTPUT 等不静默空值
  - [负向] ATOMGIT_REPOSITORY_OWNER 应非空

清理:      fixture
