用例 ID:   REL-PATHS-01-015
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-015
母意图:    —
标题:      paths 匹配越界值——第 301 个变更文件不参与 paths 匹配判断

前置条件:
  - 仓库已配置 on.push.paths 的 workflow

操作步骤:
  1. push 变更 301 个文件，仅第 301 个匹配 paths 规则

预期结果:
  - workflow 不触发

验证点:
  - [正向] workflow 不触发
  - [负向] 第 301 个文件不应触发 workflow

清理:      无需特殊清理
