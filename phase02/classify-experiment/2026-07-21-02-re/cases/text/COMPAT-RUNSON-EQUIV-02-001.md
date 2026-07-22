用例 ID:   COMPAT-RUNSON-EQUIV-02-001
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-037
母意图:    —
标题:      runs-on 多种写法等价性——数组 [..] vs 花括号 {..} vs default vs 键值 arch=arm

前置条件:
  - runner 池包含对应标签

操作步骤:
  1. 分别使用数组、花括号、default、键值四种写法定义 runs-on
  2. 触发 workflow 并观察调度结果

预期结果:
  - 等价写法应调度到同一 runner 或同规格 runner
  - 不支持的写法应给出明确报错

验证点:
  - [正向] 等价写法运行成功
  - [nonfunctional] 报错信息可理解

清理:      重置 fixture 仓库
