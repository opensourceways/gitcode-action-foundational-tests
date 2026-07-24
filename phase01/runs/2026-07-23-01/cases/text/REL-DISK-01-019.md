用例 ID:   REL-DISK-01-019
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-019
参照来源:  inputs/gitcode-spec/runner-management/selecting-runner-labels.md; inputs/platform-config/instance-config.md
母意图:    —
标题:      Runner 磁盘越界——small runner 写入 51 GB 应失败并报磁盘满

前置条件:
  - 仓库具备 small runner 使用权限

操作步骤:
  1. 触发 runs-on=[ubuntu-latest,x64,small] 的 workflow，job 尝试写入 51 GB 文件

预期结果:
  - job 状态=failure
  - 日志含 No space left on device 或平台等价错误

验证点:
  - [正向] job 状态=failure
  - [正向] 日志含磁盘满错误
  - [负向] 不应静默卡死

清理:      重置 fixture 仓库
