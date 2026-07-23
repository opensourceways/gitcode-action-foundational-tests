用例 ID:   COMPAT-INPTYPE-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-016
标题:      workflow_dispatch inputs 类型限制：仅 string

前置条件: 仓库 workflow 使用 workflow_dispatch inputs
操作步骤:
  1. type: string → 验证正确传递和默认值
  2. type: boolean → 验证报错（GitCode 仅支持 string）
  3. type: number → 验证报错
  4. type: choice → 验证报错

预期结果: 非 string 类型明确报错；string 类型正确工作
验证点:
  - [正向] type:string 正确工作
  - [负向] type:boolean/number/choice 应报错
清理:      fixture
