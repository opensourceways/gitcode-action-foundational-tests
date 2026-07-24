用例 ID:   SEC-NET-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-023
参照来源:  inputs/gitcode-spec/runner-management/selecting-runner-labels.md; inputs/platform-config/instance-config.md
母意图:    —
标题:      Runner 网络出站必须受控，防止 SSRF 与内网跳板

前置条件:
  - 仓库配置了自托管或官方 runner

操作步骤:
  1. 提交一个 workflow，尝试访问内部元数据端点或内网地址
  2. 触发 workflow 并查看网络访问结果

预期结果:
  - 访问尝试返回超时或连接拒绝
  - 运行日志中无外发成功记录

验证点:
  - [负向] Runner 绝不应能访问内网元数据端点或内部服务
  - [非功能] 访问尝试应返回超时或连接拒绝，不应产生可识别的内部服务响应

清理:      重置 full_instance
