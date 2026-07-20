用例 ID:   COMPAT-IN-TYPE-03-001
维度标签:   [compatibility, reliability]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-016
标题:      inputs 字符串 "3.10" 隐式转换为数字 3.1 的回归验证——历史 #75

前置条件:
  - 定义 workflow_dispatch 含 string 类型 inputs.version
  - 默认值设为 "3.10"

操作步骤:
  1. 定义 workflow_dispatch.inputs.version: type=string, default="3.10"
  2. 手动触发 workflow，在 step 中打印 inputs.version
  3. 同样测试 "3.0", "1.20", "1e5", "true", "false", "null", "0xff"
  4. 用 inputs.version == '3.10' 做字符串比较验证类型一致性

预期结果:
  - "3.10" 严格输出为 "3.10"（不应变成 3.1）
  - "3.0" 不应去掉末尾零变成 3
  - "1e5" 不应解析为科学计数法 100000
  - "true"/"false"/"null" 应保持字符串原样

验证点:
  - [正向] 所有易转字符串输出与输入完全一致
  - [负向] "3.10" 不应等于 3.1
  - [正向] inputs.version == '3.10' 字符串比较为 true

清理:      fixture
