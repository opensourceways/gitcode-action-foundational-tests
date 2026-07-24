用例 ID:   COMP-RUNNER-01-002
维度标签:   [completeness, compatibility]
维度:      completeness
优先级:    P1
溯源意图:  INTENT-COMP-010
参照来源:  inputs/gitcode-spec/runner-management/selecting-runner-labels.md; inputs/platform-config/instance-config.md
母意图:    —
标题:      runs-on default 等效 ubuntu-latest x64 small

前置条件:
  - 平台支持 default 快捷标签

操作步骤:
  1. 配置 runs-on: default
  2. 触发 workflow

预期结果:
  - job 被调度到 small 规格 Runner
  - 运行成功

验证点:
  - [正向] 运行状态为 success
  - [正向] Runner 规格与 small（2核8G）一致

清理:      none
