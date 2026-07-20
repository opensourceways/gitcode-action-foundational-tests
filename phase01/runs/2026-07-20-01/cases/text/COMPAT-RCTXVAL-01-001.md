用例 ID:   COMPAT-RCTXVAL-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-011
标题:      runner 上下文字段值格式差异：os 大小写 / arch 命名

前置条件: 仓库有正常 workflow；TC-094 runner.os 返回 linux
操作步骤:
  1. echo runner.os → 记录实际返回值并对比文档
  2. echo runner.arch → 记录实际返回值并对比文档
  3. echo runner.temp / runner.tool_cache → 验证路径可用
预期结果: 返回值格式一致或差异明确文档化
验证点:
  - [正向] runner.os 格式一致
  - [正向] runner.arch 格式一致
  - [正向] runner.temp/tool_cache 路径可用
清理:      fixture
