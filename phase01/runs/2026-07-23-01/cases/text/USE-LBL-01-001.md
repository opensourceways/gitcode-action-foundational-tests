用例 ID:   USE-LBL-01-001
维度标签:   ['usability']
维度:      usability
优先级:    P1
溯源意图:  INTENT-USE-025
参照来源:  inputs/gitcode-spec/runner-management/selecting-runner-labels.md; inputs/platform-config/instance-config.md
母意图:    —
标题:      runs-on 标签完全不匹配时应给出明确失败原因与可用标签列表

前置条件:
  - 仓库无匹配该标签组合的 runner

操作步骤:
  1. 使用完全不存在的标签组合如 [nonexistent-os, x64, small]

预期结果:
  系统在合理超时后失败，报错包含用户指定的标签和可用 runner 类型列表

验证点:
  - [负向] 不应无限 queued 且无提示
  - [非功能] 错误信息中是否包含用户指定的标签文本

清理:      无

