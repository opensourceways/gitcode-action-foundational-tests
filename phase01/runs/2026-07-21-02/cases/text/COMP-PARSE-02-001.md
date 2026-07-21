用例 ID:   COMP-PARSE-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-018
标题:      验证 workflow 文件 YAML 合法性检查与错误信息

前置条件:
  - 提交各种 YAML 配置错误的工作流文件

操作步骤:
  1. 缺 on 字段 → 明确报错 + 文件路径
  2. 缺 runs-on → 明确报错 + job 名称
  3. YAML 语法错误（缩进/标点） → 报错 + 行列号
  4. 未知字段 → 报错还是静默忽略
  5. .gitcode/workflows/ 下非 .yml/.yaml 文件被忽略

预期结果:
  - 报错信息包含文件路径和行号
  - 非 yml/yaml 文件被忽略
  - 未知字段行为一致

验证点:
  - [正向] 缺 on → 明确报错
  - [正向] 缺 runs-on → 明确报错
  - [正向] 语法错误有行号
  - [非功能] 报错信息可理解

清理:      fixture
