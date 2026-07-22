用例 ID:   REL-FAULT-01-005
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-033
母意图:    —
标题:      故障注入——runner 磁盘接近满时写入操作应失败并报磁盘满

前置条件:
  - 仓库已启用 Actions
  - runner 磁盘可被填充至接近满状态

操作步骤:
  1. 创建 workflow，包含生成大文件或多次写入磁盘的操作
  2. 预先将 runner 磁盘填充至接近满（如剩余 < 50 MB）
  3. 触发 workflow 运行
  4. 观察写入步骤的失败行为与错误信息

预期结果:
  - 当磁盘空间不足时，写入操作步骤失败
  - 错误信息明确提示磁盘空间不足（如 no space left on device、disk full）
  - 系统不崩溃，后续步骤可按配置继续或跳过

验证点:
  - [正向] 写入步骤状态为 FAILED
  - [正向] 日志中包含磁盘满相关关键词
  - [负向] runner 进程不因磁盘满而崩溃或不可恢复

清理:      重置 full_instance
