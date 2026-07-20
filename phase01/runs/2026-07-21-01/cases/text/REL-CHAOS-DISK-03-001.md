用例 ID:   REL-CHAOS-DISK-03-001
维度标签:   [reliability]
维度:      可靠性
优先级:    P1
溯源意图:  INTENT-REL-014
标题:      job 执行中磁盘写满后 step 应失败并有明确日志

前置条件:
  - step 执行 dd 填满磁盘后触发后续写操作

操作步骤:
  1. step 执行 dd 生成大文件填满 /tmp 磁盘空间
  2. 后续 step 尝试写入文件
  3. 观察 failure 状态和日志内容

预期结果:
  - 磁盘满时 step 失败，Run = failure
  - 日志含磁盘满错误（'No space left on device' / ENOSPC）
  - job 不永久 hang 在写入操作

验证点:
  - [正向] Run = failure
  - [正向] 日志含 'No space left on device' 或等价信息
  - [负向] job 不永久 hang

清理:      fixture
