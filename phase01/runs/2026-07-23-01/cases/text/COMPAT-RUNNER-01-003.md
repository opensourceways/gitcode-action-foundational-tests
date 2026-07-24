用例 ID:   COMPAT-RUNNER-01-003
维度标签:   [compatibility]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-NEW-008
母意图:    —
标题:      self-hosted 标签不被支持时应明确报错

前置条件:
  - 仓库已启用 Actions
  - 测试者持有 maintainer 权限

操作步骤:
  1. 创建一个 workflow，runs-on 使用 `[self-hosted, linux]`
  2. 提交并触发 workflow

预期结果:
  - GitHub 行为：self-hosted 标签匹配到自托管 Runner
  - GitCode 行为：self-hosted 标签可能不被支持
  - 应明确报错而非无限排队

验证点:
  - [正向] 系统对不支持的 self-hosted 标签给出明确报错
  - [负向] 不通过 job 无限排队且无提示

清理:      无
