用例 ID:   COMPAT-UNSUPP-IN-03-001
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-040
标题:      不支持 workflow_dispatch inputs 类型（boolean/choice/number）时的降级行为

前置条件:
  - 定义 workflow_dispatch 含非 string 类型 inputs

操作步骤:
  1. 定义 type: boolean 的 input（如 dry_run）
  2. 定义 type: choice 的 input（含 options 列表）
  3. 定义 type: number 的 input
  4. 触发 workflow，观察每种类型的行为

预期结果:
  - 非 string 类型应在 YAML 解析/保存阶段明确报错
  - 报错应指出「仅支持 string 类型」
  - 不应静默降级为 string（用户传入 true 变成字符串 'true'）

验证点:
  - [正向] type: boolean 应在保存时报错
  - [正向] type: choice 应在保存时报错
  - [负向] 不应静默接受并降级为 string（实际行为不同）

清理:      fixture
