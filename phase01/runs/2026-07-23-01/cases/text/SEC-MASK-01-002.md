用例 ID:   SEC-MASK-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-004
参照来源:  inputs/security-knowledge/issues.md; inputs/github-reference/security/
母意图:    SEC-MASK-01-001
标题:      Secret 值在 step summary 和错误堆栈中必须被脱敏

前置条件:
  - 仓库配置了 secret API_KEY

操作步骤:
  1. 提交一个 workflow，将 secrets.API_KEY 写入 ATOMGIT_STEP_SUMMARY
  2. 触发 workflow 并查看 step summary 与日志

预期结果:
  - step summary 中 API_KEY 的原值被替换为 ***
  - 若步骤失败产生堆栈，堆栈中亦不应出现原值

验证点:
  - [负向] step summary 不含 API_KEY 原值
  - [负向] 错误堆栈不含 API_KEY 原值

清理:      重置 fixture 仓库
