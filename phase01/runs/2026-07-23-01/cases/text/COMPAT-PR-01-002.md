用例 ID:   COMPAT-PR-01-002
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-011
参照来源:  inputs/gitcode-spec/core-concepts/trigger-events.md
母意图:    COMPAT-PR-01-001
标题:      pull_request types 命名差异 - GitHub 风格 types 应报错

前置条件:
  - 仓库已启用 Actions
  - 测试分支存在
  - 存在目标分支 main

操作步骤:
  1. 在 workflow 中定义 on: pull_request 并指定 GitHub 风格的 types（opened, closed, reopened）
  2. 提交并推送该 workflow
  3. 观察平台校验行为

预期结果:
  - 平台应对不支持的 GitHub 风格 types 给出明确的校验错误
  - 错误信息应提示正确的 GitCode types 名称

验证点:
  - [负向] GitHub 风格 types 不应被静默接受
  - [正向] 错误信息应明确指出类型名称不兼容并给出正确写法

清理:      fixture
