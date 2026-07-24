用例 ID:   REL-DISK-01-018
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-018
参照来源:  inputs/gitcode-spec/runner-management/selecting-runner-labels.md; inputs/platform-config/instance-config.md
母意图:    —
标题:      Runner 磁盘边界——small runner 写入 49 GB 应成功

前置条件:
  - 仓库具备 small runner 使用权限

操作步骤:
  1. 触发 runs-on=[ubuntu-latest,x64,small] 的 workflow，job 顺序写入 49 GB 文件

预期结果:
  - job 状态=success
  - df 显示剩余约 1 GB
  - 文件完整性校验通过

验证点:
  - [正向] job 状态=success
  - [负向] 不应在 49 GB 时报磁盘满

清理:      重置 fixture 仓库
