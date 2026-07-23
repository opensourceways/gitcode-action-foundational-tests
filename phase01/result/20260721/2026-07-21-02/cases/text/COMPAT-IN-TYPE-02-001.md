用例 ID:   COMPAT-IN-TYPE-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-016
标题:      inputs 类型限制：验证非 string 类型（boolean/number/choice）的拒绝行为

前置条件:
  - workflow_dispatch 或 workflow_call 中定义了非 string 类型的 inputs
  - 对比 GitHub 支持的 boolean/number/choice/environment 类型

操作步骤:
  1. 测试 workflow_dispatch inputs 使用 type: boolean → 应报错
  2. 测试 type: number → 应报错
  3. 测试 type: choice → 应报错
  4. 测试 type: string 正常通过
  5. 验证错误信息是否指明「GitCode 仅支持 string 类型」

预期结果:
  - 非 string 类型 inputs 明确报错（非静默当 string）
  - type: string 正常
  - 错误信息应指明 GitCode 仅支持 string

验证点:
  - [正向] type: string 的 inputs 正确传递和默认值
  - [负向] type: boolean 不应静默当 string 处理
  - [负向] type: number / choice / environment 同理应报错
  - [负向] 错误信息指明仅支持 string 类型

清理:      fixture
