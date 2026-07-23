用例 ID:   COMP-PARSE-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-018
标题:      验证 workflow 文件解析: YAML 合法性检查与错误信息可操作性
前置条件:  仓库无特殊设置
操作步骤:
  1. 缺 on → 明确报错含文件路径
  2. 缺 runs-on → 明确报错含 job 名称
  3. YAML 语法错误 → 报错含行号
  4. 未知字段 → 确认行为
  5. .gitcode/workflows/ 下非 .yml/.yaml 文件被忽略
预期结果: 错误信息包含具体位置、原因、修复建议
验证点:
  - [正向] 合法 YAML 正确解析
  - [正向] 缺 on 明确报错
  - [正向] 缺 runs-on 明确报错
  - [正向] YAML 语法错误含行列号
  - [正向] 非 .yml/.yaml 文件被忽略
清理:      fixture
