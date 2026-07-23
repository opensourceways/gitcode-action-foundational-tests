用例 ID:   SEC-SUMMARY-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-004
母意图:    —
标题:      secret 在 step summary 中应被脱敏

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - workflow 在仓库默认分支上存在

操作步骤:
  1. 提交一个 workflow，在 run 步骤中将 DEPLOY_TOKEN 写入 step summary（如通过 $ATOMGIT_STEP_SUMMARY 或平台等效机制）
  2. 触发该 workflow
  3. 查看 step summary 输出与运行日志

预期结果:
  - 系统对 step summary 中的 DEPLOY_TOKEN 进行脱敏，显示为掩码（如 ***）
  - step summary 中不出现 DEPLOY_TOKEN 明文
  - 运行日志中同样不出现 DEPLOY_TOKEN 明文

验证点:
  - [负向] step summary 不含 DEPLOY_TOKEN 明文
  - [负向] 日志不含 DEPLOY_TOKEN 明文
  - [正向] step summary 正常生成，secret 位置显示为掩码

清理:      重置 fixture 仓库
