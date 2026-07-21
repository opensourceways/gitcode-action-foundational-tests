用例 ID:   COMPAT-ACTION-INPUTS-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-051
母意图:    —
标题:      action inputs 环境变量注入差异——INPUT_<NAME> 命名转换与 required 校验

前置条件:
  - 存在一个带 inputs 定义的自定义 action

操作步骤:
  1. 在 workflow 中调用该 action 并传入参数
  2. 在 action 的 run 脚本中读取 INPUT_* 环境变量

预期结果:
  - inputs 应正确映射为 INPUT_* 环境变量
  - required 缺失时应报错

验证点:
  - [正向] INPUT_TEST_PARAM 值为传入值
  - [nonfunctional] required 缺失报错可理解

清理:      重置 fixture 仓库
