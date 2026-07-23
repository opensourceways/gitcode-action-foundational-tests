用例 ID:   SEC-ENV-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-027
母意图:    —
标题:      环境级 secret 必须经审批后才能被 workflow 访问

前置条件:
  - 仓库配置了环境级 secret PROD_TOKEN
  - 环境审批规则已启用

操作步骤:
  1. 提交一个引用环境级 secret 的 workflow
  2. 在审批前触发 workflow
  3. 审批后再次触发 workflow

预期结果:
  - 审批前 workflow 无法读取到环境 secret 的值
  - 审批后 secret 可被正常引用，job 成功执行

验证点:
  - [正向] 审批后 secret 可被正常引用，job 成功执行
  - [负向] 审批前 workflow 绝不应读取到环境 secret 的值

清理:      重置 fixture 仓库
