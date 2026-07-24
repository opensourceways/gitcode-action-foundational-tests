用例 ID:   COMPAT-TOKEN-01-002
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-020
参照来源:  inputs/gitcode-spec/
母意图:    COMPAT-TOKEN-01-001
标题:      GITHUB_TOKEN 在 GitCode 中应为空且不应被静默映射

前置条件:
  - 仓库已启用 Actions

操作步骤:
  1. 在 workflow 中通过 ${{ secrets.GITHUB_TOKEN }} 引用令牌
  2. 尝试使用该令牌发起 API 调用
  3. 触发 workflow 运行

预期结果:
  - secrets.GITHUB_TOKEN 应为空或未定义
  - 不应被静默映射到 ATOMGIT_TOKEN

验证点:
  - [负向] GITHUB_TOKEN 不应被静默映射为 ATOMGIT_TOKEN
  - [非功能] 报错信息应提示使用 ATOMGIT_TOKEN 替代

清理:      fixture
