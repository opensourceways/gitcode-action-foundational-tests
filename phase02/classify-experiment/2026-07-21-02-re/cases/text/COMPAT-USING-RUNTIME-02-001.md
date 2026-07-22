用例 ID:   COMPAT-USING-RUNTIME-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-043
母意图:    —
标题:      action runs.using 运行时差异——GitHub node20/docker/composite vs GitCode 仅 node16

前置条件:
  - 存在 using: node20 或 docker 的 action 定义

操作步骤:
  1. 在 workflow 中引用 using: node20 的 action
  2. 观察运行是否成功或给出降级提示

预期结果:
  - 不支持的 using 类型不应静默失败
  - 应给出明确的运行时不支持报错

验证点:
  - [负向] 不静默挂起
  - [nonfunctional] 报错指明支持的 using 类型

清理:      重置 fixture 仓库
