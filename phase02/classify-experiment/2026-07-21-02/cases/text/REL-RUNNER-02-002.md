用例 ID:   REL-RUNNER-02-002
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-013
标题:      step 填充 runner 磁盘超过 50GB 上限时，job 失败并给出磁盘空间相关错误

前置条件:
  - small runner 磁盘 50GB
  - step 执行 dd 创建大文件填满磁盘

操作步骤:
  1. 执行 `dd if=/dev/zero of=/tmp/fill bs=1M count=50000` 填充磁盘
  2. 验证 step 因磁盘满失败（exit code != 0）
  3. 验证日志含 "No space left on device" 或等价信息

预期结果:
  - step 因 ENOSPC 失败，job status = failure
  - 日志含磁盘空间不足信息
  - runner 不被永久损伤

验证点:
  - [正向] step 因磁盘满失败（exit code != 0），job = failure
  - [正向] 日志含 "No space left" 或 "disk quota exceeded"
  - [负向] job 不为 success

清理:      fixture
