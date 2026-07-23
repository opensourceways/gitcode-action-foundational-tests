用例 ID:   COMPAT-TOKEN-01-001
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-020
母意图:    —
标题:      ATOMGIT_TOKEN 应正确返回有效令牌

前置条件:
  - 仓库已启用 Actions
  - 仓库设置中已启用 TOKEN

操作步骤:
  1. 在 workflow 中通过 ${{ secrets.ATOMGIT_TOKEN }} 引用令牌
  2. 使用该令牌发起一次只读 API 调用
  3. 触发 workflow 运行

预期结果:
  - ATOMGIT_TOKEN 应不为空且能完成认证
  - 日志中令牌值应被脱敏为 ***

验证点:
  - [正向] API 调用返回 200，表明 TOKEN 有效
  - [负向] 日志中不应出现 TOKEN 明文

清理:      fixture
