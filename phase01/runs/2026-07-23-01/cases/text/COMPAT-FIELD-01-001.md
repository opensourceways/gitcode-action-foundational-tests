用例 ID:   COMPAT-FIELD-01-001
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-021
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    —
标题:      含 run-name 字段的 workflow 应被报错或警告

前置条件:
  - 仓库已启用 Actions

操作步骤:
  1. 在 workflow 根级别添加 run-name 字段
  2. 提交并推送该 workflow
  3. 观察平台解析行为

预期结果:
  - 平台应在解析或保存阶段给出明确报错或警告
  - 不应被静默接受且运行名显示为文件路径

验证点:
  - [负向] 不应被静默接受
  - [非功能] 报错信息应指明 run-name 字段不支持

清理:      fixture
