用例 ID:   COMPAT-PATHS-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-012
参照来源:  inputs/gitcode-spec/core-concepts/trigger-events.md
母意图:    —
标题:      paths 过滤器 300 条边界测试

前置条件:
  - 仓库已启用 Actions
  - 测试分支存在
  - 存在目标分支 main

操作步骤:
  1. 在 workflow 的 on.push.paths 中配置恰好 300 条路径规则
  2. 提交并推送该 workflow
  3. 观察平台校验与触发行为

预期结果:
  - workflow 应被平台接受，不报错
  - 匹配路径的 push 事件应正常触发 workflow

验证点:
  - [正向] workflow 校验通过
  - [正向] 匹配路径的 push 能正常触发

清理:      fixture
