用例 ID:   SEC-ENV-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-027
母意图:    SEC-ENV-01-001
标题:      环境级 secret 审批前 workflow 不可读取

前置条件:
  - 仓库配置了环境级 secret PROD_TOKEN
  - 环境审批规则已启用，尚未审批

操作步骤:
  1. 提交一个引用环境级 secret 的 workflow
  2. 在审批前触发 workflow

预期结果:
  - workflow job 无法读取到环境 secret 的值
  - job 应处于挂起或失败状态

验证点:
  - [负向] 审批前 job 绝不应读取到环境 secret 的值
  - [正向] job 状态为挂起或权限拒绝

清理:      重置 fixture 仓库
