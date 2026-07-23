用例 ID:   SEC-ENVAPPR-01-001
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-022
标题:      环境（environment）级 Secret 受审批规则保护

前置条件:
  - 仓库配置 environment prod，设置审批人
  - environment prod 绑定环境级 Secret PROD_TOKEN
  - workflow 中 job 声明 environment: prod

操作步骤:
  1. 触发 workflow，job 声明 environment: prod
  2. 观察 job 状态：审批前应处于 queued/waiting 状态
  3. 验证 job 未开始执行、未读取 PROD_TOKEN
  4. 审批人审批通过后观察 job 开始执行
  5. job 中 echo PROD_TOKEN → 验证可读取且日志脱敏

预期结果:
  - 未审批时 job 处于等待状态，不执行任何 step
  - 审批通过后 job 开始执行，可读取环境级 Secret
  - 若平台当前不支持 environment 字段（TC-010 已知问题），记为 blocked
  - Secret 在日志中被脱敏

验证点:
  - [正向] 审批通过后 job 执行 → 可读取环境级 Secret
  - [负向] 未审批前 job 不执行
  - [负向] 若 environment 字段不可用 → blocked 状态

清理:      fixture
