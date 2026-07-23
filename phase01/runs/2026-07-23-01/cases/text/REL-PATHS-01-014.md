用例 ID:   REL-PATHS-01-014
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-014
母意图:    —
标题:      paths 匹配边界值——变更恰好 300 个文件时 paths 过滤应生效

前置条件:
  - 仓库已配置 on.push.paths 的 workflow

操作步骤:
  1. push 变更恰好 300 个文件，其中 1 个匹配 paths 规则

预期结果:
  - workflow 被正确触发

验证点:
  - [正向] workflow 运行被创建
  - [负向] 不应因文件数=300 而判定异常

清理:      无需特殊清理
