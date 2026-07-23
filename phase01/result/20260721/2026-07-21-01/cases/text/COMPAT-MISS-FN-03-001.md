用例 ID:   COMPAT-MISS-FN-03-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-012
标题:      fromJSON/join/case 缺失函数：验证 GitCode 对不支持函数是报错还是静默失败

前置条件:
  - 使用标准 fixture 仓库

操作步骤:
  1. 在表达式中使用 fromJSON('["a","b"]') 尝试将 JSON 字符串转数组
  2. 使用 join(array, ',') 尝试合并数组元素
  3. 使用 case(condition, true_val, false_val) 尝试条件分支
  4. 观察每种用法是解析报错、运行时失败、还是静默返回空值

预期结果:
  - 不支持函数应在解析阶段明确报错（如「unknown function: fromJSON」）
  - 不应静默返回空值（导致后续逻辑在空数据上运行）
  - 若某函数实际支持但未文档化，应记录实际行为供差异清单使用

验证点:
  - [正向] fromJSON/join/case 使用时应产生明确错误
  - [负向] 不应静默返回空字符串/空数组
  - [正向] 报错消息应含函数名，便于用户定位

清理:      fixture
