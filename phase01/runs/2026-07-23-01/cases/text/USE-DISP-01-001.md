用例 ID:   USE-DISP-01-001
维度标签:   ['usability', 'completeness']
维度:      usability/completeness
优先级:    P1
溯源意图:  INTENT-USE-030
参照来源:  inputs/gitcode-spec/core-concepts/trigger-events.md
母意图:    —
标题:      workflow_dispatch 必填参数未提供时应给出明确校验错误

前置条件:
  - workflow 配置了一个 required: true 且无 default 的 input

操作步骤:
  1. 手动触发 workflow 但不提供该必填参数

预期结果:
  系统拒绝触发并提示缺少必填参数

验证点:
  - [负向] 不应在缺少必填参数时触发运行
  - [非功能] 报错中是否指出具体缺少的字段名

清理:      无

