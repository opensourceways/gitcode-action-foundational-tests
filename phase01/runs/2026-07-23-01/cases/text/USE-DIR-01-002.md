用例 ID:   USE-DIR-01-002
维度标签:   ['usability']
维度:      usability
优先级:    P1
溯源意图:  INTENT-USE-001
参照来源:  inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md
母意图:    —
标题:      .github/workflows/ 下 workflow 未被识别时应给出目录差异提示

前置条件:
  - 仓库同时存在 .github/workflows/ 和 .gitcode/workflows/
  - 前者含 workflow 后者为空

操作步骤:
  1. 将 workflow 文件误放到 .github/workflows/ 目录
  2. 推送代码触发 push 事件

预期结果:
  系统在某处（运行页面、日志或校验信息）提示 .gitcode/workflows/ 为正确目录，而非静默忽略

验证点:
  - [负向] 不应无任何提示地忽略 .github/workflows/ 下的文件
  - [非功能] 提示信息中应包含 .gitcode/workflows 字样

清理:      无

