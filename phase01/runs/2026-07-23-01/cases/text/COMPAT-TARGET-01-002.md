# 用例归档

用例 ID:   COMPAT-TARGET-01-002
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-032
母意图:    —
标题:      pull_request_target 在 fork 场景下应保持 secret 隔离

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - 存在一个来自外部 fork 的 PR

操作步骤:
  1. 配置一个以 `pull_request_target` 触发的 workflow
  2. 该 workflow 在 job 中尝试读取 secrets.DEPLOY_TOKEN 并输出到日志
  3. 提交一个 fork PR 并触发该 workflow
  4. 观察 workflow 执行结果和日志输出

预期结果:
  - pull_request_target 允许访问仓库 secrets（语义与 GitHub 一致）
  - 但 secrets 在日志中应被脱敏为 `***`
  - 系统不应因 fork 来源而阻止 pull_request_target 访问 secrets（这是该事件的设计行为）
  - 对比组：同一 fork PR 以普通 `pull_request` 触发时不应能访问 secrets

验证点:
  - [负向] 日志中不应出现 DEPLOY_TOKEN 明文
  - [正向] pull_request_target 场景下 workflow 能成功引用 secrets.DEPLOY_TOKEN
  - [正向] 普通 pull_request 场景下 fork PR 无法访问 secrets

清理:      重置 fixture 仓库
