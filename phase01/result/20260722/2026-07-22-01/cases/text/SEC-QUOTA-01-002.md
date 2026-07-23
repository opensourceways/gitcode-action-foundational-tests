用例 ID:   SEC-QUOTA-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-033
母意图:    —
标题:      大 cache 应受配额与边界限制

前置条件:
  - 仓库配置了 cache 存储大小限制
  - workflow 具备使用 cache 的权限

操作步骤:
  1. 提交一个 workflow，生成一个超过平台 cache 大小配额的大目录
  2. 在 workflow 中使用 cache Action 保存该大目录
  3. 观察保存结果与系统响应

预期结果:
  - 系统拒绝保存超出配额的 cache，或在达到上限后报错/截断
  - 运行日志中明确提示 cache 大小超出限制
  - 超大 cache 不会导致 runner 磁盘耗尽或平台服务异常

验证点:
  - [负向] 超出配额的 cache 未被成功完整保存
  - [负向] cache 保存过程未导致 runner 磁盘耗尽或平台服务异常
  - [正向] 系统返回明确的 cache 大小超限错误信息

清理:      重置 fixture 仓库
