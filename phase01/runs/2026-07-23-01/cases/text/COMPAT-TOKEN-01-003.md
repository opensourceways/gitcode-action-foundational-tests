用例 ID:   COMPAT-TOKEN-01-003
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-020
参照来源:  inputs/gitcode-spec/
母意图:    —
标题:      GITHUB_TOKEN 不应被静默映射为 ATOMGIT_TOKEN

前置条件:
  - 仓库已启用 Actions
  - 测试者持有 maintainer 权限

操作步骤:
  1. 创建一个 workflow，在 run 步骤中输出 `$GITHUB_TOKEN` 和 `$ATOMGIT_TOKEN`
  2. 触发 workflow

预期结果:
  - GITHUB_TOKEN 不应存在或被设置为空/未定义
  - 不应将 GITHUB_TOKEN 静默映射为 ATOMGIT_TOKEN 的值
  - 引用 ${{ secrets.GITHUB_TOKEN }} 应返回空或报错

验证点:
  - [负向] GITHUB_TOKEN 不等于 ATOMGIT_TOKEN
  - [正向] GITHUB_TOKEN 为空或未定义
  - [负向] 不通过静默映射导致用户误用 GITHUB_TOKEN

清理:      无
