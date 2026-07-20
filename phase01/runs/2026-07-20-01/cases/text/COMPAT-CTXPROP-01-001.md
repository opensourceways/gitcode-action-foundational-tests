用例 ID:   COMPAT-CTXPROP-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-001
标题:      atomgit 上下文对象属性完整性：验证 atomgit.* 核心属性集是否对齐 github.*
前置条件:  仓库无特殊设置；准备 push 和 PR 触发事件
操作步骤:
  1. 在 push 事件中枚举全部 20 个 atomgit.* 文档属性
  2. 对 GitHub 有但 atomgit 未文档化的属性（如 action_path/actor_id），测试访问行为
  3. 验证未文档化属性的返回值（空 vs null vs 报错）
预期结果:
  - 已文档化属性返回非空合法值
  - 未文档化属性应有可判定行为（报错 > 空值 > 静默返回 null）
验证点:
  - [正向] 已文档化 atomgit.* 属性返回正确格式值
  - [负向] 未文档化的属性不应静默返回非预期值导致逻辑分支错误
清理:      fixture
