用例 ID:   USE-RUN-01-002
维度标签:   ['usability', 'compatibility']
维度:      usability/compatibility
优先级:    P1
溯源意图:  INTENT-USE-006
参照来源:  inputs/gitcode-spec/runner-management/selecting-runner-labels.md; inputs/platform-config/instance-config.md
母意图:    —
标题:      使用单标签 ubuntu-latest 时报错应给出三段式格式指引

前置条件:
  - workflow 文件位于 .gitcode/workflows/

操作步骤:
  1. 在 job 中写 runs-on: [ubuntu-latest]

预期结果:
  系统在校验或调度阶段报错，给出三段式标签格式示例或可用标签列表

验证点:
  - [负向] 不应无限 queued 且无提示
  - [非功能] 报错中应包含三段式或 default 等关键词

清理:      无

