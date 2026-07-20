用例 ID:   COMPAT-SYSENV-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-002
标题:      系统环境变量命名约定：ATOMGIT_* 环境变量注入完整性

前置条件:
  - 仓库有正常 workflow 配置
  - 已知 TC-206 发现 ATOMGIT_REPOSITORY_OWNER 未注入

操作步骤:
  1. 在 step 中 echo 所有文档列出的 ATOMGIT_* 变量
  2. 验证 ATOMGIT_OUTPUT/ATOMGIT_ENV/ATOMGIT_PATH/ATOMGIT_STEP_SUMMARY 文件路径存在可写
  3. 验证 ATOMGIT_TOKEN 作为环境变量可用
  4. 尝试使用 $GITHUB_TOKEN / $GITHUB_OUTPUT → 验证返回 UNSET 或报错
  5. 检查文档中是否残留 GITHUB_* 引用

预期结果:
  - 所有文档声明的 ATOMGIT_* 变量在 Runner shell 中可用且值正确
  - ATOMGIT_OUTPUT 等文件路径存在且可写
  - $GITHUB_TOKEN 等 GitHub 命名不应静默返回空值（应 UNSET 或报错）
  - 文档不应残留 GITHUB_* 引用（除非在对比章节）

验证点:
  - [正向] ATOMGIT_* 变量全部注入且值正确
  - [正向] ATOMGIT_OUTPUT/ENV/PATH/STEP_SUMMARY 文件可用
  - [负向] $GITHUB_TOKEN 等不静默返回空

清理:      fixture
