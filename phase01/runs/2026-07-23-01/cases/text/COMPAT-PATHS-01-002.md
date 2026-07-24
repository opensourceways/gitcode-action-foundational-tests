用例 ID:   COMPAT-PATHS-01-002
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-012
参照来源:  inputs/gitcode-spec/core-concepts/trigger-events.md
母意图:    COMPAT-PATHS-01-001
标题:      paths 过滤器 301 条越界测试

前置条件:
  - 仓库已启用 Actions
  - 测试分支存在
  - 存在目标分支 main

操作步骤:
  1. 在 workflow 的 on.push.paths 中配置 301 条路径规则（超出上限）
  2. 提交并推送该 workflow
  3. 观察平台校验行为

预期结果:
  - 平台应对超出 300 条上限的 paths 给出明确的校验错误或运行时错误
  - 错误信息应指出 paths 数量超过限制

验证点:
  - [负向] 超出上限的 paths 不应被静默接受
  - [正向] 错误信息应明确指出 paths 数量限制

清理:      fixture
