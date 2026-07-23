用例 ID:   COMPAT-EXPRFN-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-004
标题:      验证 GitCode 独有 substring/replace 函数，缺失 join/fromJSON 时报错

前置条件:
  - 使用 GitCode 独有函数和 GitHub 独有函数

操作步骤:
  1. substring(str, start, len) 正确截取
  2. replace(str, old, new) 正确替换
  3. 使用 join() → 应报错
  4. 使用 fromJSON() → 应报错
  5. 使用 case() → 应报错

预期结果:
  - GitCode 独有函数 behavior 与文档一致
  - GitHub 独有函数不应静默返回空

验证点:
  - [正向] substring 正确截取
  - [正向] replace 正确替换
  - [负向] join/fromJSON/case 明确报错

清理:      fixture
