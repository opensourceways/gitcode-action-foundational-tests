用例 ID:   SEC-NET-03-001
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-048
母意图:    —
标题:      Runner 网络隔离——出站控制与 SSRF 防护

前置条件:
  - 存在 push 触发的 workflow

操作步骤:
  1. workflow 中 curl 访问内部 metadata 服务
  2. workflow 中 curl 访问 GitCode 内部 API
  3. 观察是否被阻止

预期结果:
  - Runner 不应能访问平台内部非公开服务
  - 内部地址 curl 应返回 timeout/connection refused/403

验证点:
  - [负向] workflow 中 curl 访问 169.254.169.254 应被阻止
  - [负向] workflow 中 curl 访问 GitCode 内部 API 应被阻止
  - [正向] workflow 可正常访问外部合法服务

清理:      none
