用例 ID:   SEC-FORKENV-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-001
母意图:    —
标题:      fork PR 中通过环境变量间接访问 secret 应被阻止

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - 存在一个来自 fork 的 PR

操作步骤:
  1. 以外部 fork 贡献者身份，提交一个试图将 DEPLOY_TOKEN 通过 env 注入到 step 中的 workflow
  2. 在 fork PR 场景下触发该 workflow
  3. 观察 workflow 执行结果与日志

预期结果:
  - 系统阻止 fork PR 通过 env 字段间接访问 DEPLOY_TOKEN，或 workflow 拿不到该值
  - 运行日志中不出现 DEPLOY_TOKEN 明文
  - env 注入行为被隔离或忽略

验证点:
  - [负向] 日志不含 DEPLOY_TOKEN 明文
  - [负向] fork 身份无法通过 env 间接获取 secret
  - [正向] workflow 被阻止或 secret 值为空

清理:      重置 fixture 仓库
