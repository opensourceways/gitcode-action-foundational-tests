用例 ID:   SEC-QUOTA-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-033
母意图:    —
标题:      大 artifact 应受配额与边界限制

前置条件:
  - 仓库配置了 artifact 上传大小限制（如单文件 500MB、总大小 2GB）
  - workflow 具备上传 artifact 的权限

操作步骤:
  1. 提交一个 workflow，生成一个超过平台 artifact 大小配额的大文件
  2. 在 workflow 中使用 upload-artifact 上传该大文件
  3. 观察上传结果与系统响应

预期结果:
  - 系统拒绝上传超出配额的 artifact，或在上传达到上限后截断/报错
  - 运行日志中明确提示大小超出限制
  - 超大 artifact 不会导致 runner 磁盘耗尽或平台服务异常

验证点:
  - [负向] 超出配额的 artifact 未被成功完整上传
  - [负向] 上传过程未导致 runner 磁盘耗尽或平台服务异常
  - [正向] 系统返回明确的大小超限错误信息

清理:      重置 fixture 仓库
