用例 ID:   SEC-NET-03-002
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-049
母意图:    —
标题:      Self-hosted runner 在内网部署时的网络跳板风险

前置条件:
  - 存在 self-hosted runner

操作步骤:
  1. 在 self-hosted runner 上执行 curl 内网服务
  2. 验证 fork PR 代码是否可访问内网
  3. 检查平台文档是否声明风险

预期结果:
  - fork PR 代码不应能访问 runner 所在内网服务
  - 平台文档应明确警告 self-hosted runner 的内网风险

验证点:
  - [负向] 公开仓库的 self-hosted runner 上，fork PR 不应能访问内网服务
  - [正向] 平台文档是否明确声明 self-hosted runner 的内网安全风险

清理:      none
