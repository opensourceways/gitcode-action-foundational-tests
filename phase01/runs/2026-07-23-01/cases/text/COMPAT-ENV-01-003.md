用例 ID:   COMPAT-ENV-01-003
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-017
母意图:    —
标题:      GITHUB_ENV 环境变量不应被静默映射到 ATOMGIT_ENV

前置条件:
  - 仓库已启用 Actions
  - 测试者持有 maintainer 权限

操作步骤:
  1. 创建一个 workflow，在 run 步骤中输出 `$GITHUB_ENV` 和 `$ATOMGIT_ENV`
  2. 触发 workflow

预期结果:
  - GITHUB_ENV 不应存在或被设置为空/未定义
  - 不应将 GITHUB_ENV 静默映射为 ATOMGIT_ENV 的值

验证点:
  - [负向] GITHUB_ENV 不等于 ATOMGIT_ENV
  - [正向] GITHUB_ENV 为空或未定义

清理:      无
