用例 ID:   COMPAT-MIGERR-01-003
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-031
母意图:    COMPAT-MIGERR-01-001
标题:      vars 上下文缺失时的报错质量

前置条件:
  - 仓库已启用 Actions
  - 测试分支存在

操作步骤:
  1. 提交包含 vars 上下文引用的 workflow
  2. 观察平台 YAML 校验或运行时的错误信息

预期结果:
  - 错误信息应明确指出 vars 上下文在 GitCode 中不受支持
  - 错误信息应给出替代写法（如使用 atomgit 上下文或环境变量）
  - 不应出现 generic 的「语法错误」而不指明原因

验证点:
  - [正向] 错误信息包含不兼容上下文名称
  - [正向] 错误信息提供可操作的修改建议或替代写法

清理:      fixture
