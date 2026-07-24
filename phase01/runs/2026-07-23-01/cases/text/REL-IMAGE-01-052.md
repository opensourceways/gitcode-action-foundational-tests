用例 ID:   REL-IMAGE-01-052
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-052
参照来源:  inputs/gitcode-spec/runner-management/selecting-runner-labels.md; inputs/platform-config/instance-config.md
母意图:    —
标题:      镜像拉取性能——500MB 自定义 container 环境准备耗时基准

前置条件:
  - 仓库具备 container 使用权限

操作步骤:
  1. 触发使用 ~500MB 镜像的 container job，测量拉取耗时

预期结果:
  - 500MB 镜像在 2min 内完成拉取并启动
  - 失败时有明确归因

验证点:
  - [正向] 拉取≤2min
  - [负向] 不应 pending 10min 后无解释失败

清理:      无需特殊清理
