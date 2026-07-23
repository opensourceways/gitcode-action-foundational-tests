用例 ID:   COMPAT-EXPRFN-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-004
标题:      表达式函数集差异：GitCode 独有函数 + GitHub 缺失函数行为

前置条件:
  - 仓库有正常 workflow 配置
  - 了解 GitCode 有 substring/replace，GitHub 有 join/fromJSON/case

操作步骤:
  1. 使用 substring(str, start, len) → 验证正确截取
  2. 使用 replace(str, old, new) → 验证正确替换
  3. 使用 join()（GitHub 函数）→ 验证报错而非静默
  4. 使用 fromJSON()（GitHub 函数）→ 同上
  5. 使用 case()（GitHub 函数）→ 同上

预期结果:
  - substring/replace 按文档正确执行
  - join/fromJSON/case 有明确报错（不应静默通过）
  - 不出现 GitHub 函数在 GitCode 中被不同语义执行

验证点:
  - [正向] substring 正确截取子串
  - [正向] replace 正确替换
  - [负向] join/fromJSON/case 应报错
  - [负向] 不出现语义不同的静默执行

清理:      fixture
