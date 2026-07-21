用例 ID:   COMPAT-STAGES-SYNTAX-02-001
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-058
母意图:    —
标题:      stages 两种写法 + 缩进瑕疵——列表 - name: vs 映射 stage1: 的解析容错

前置条件:
  - workflow 使用 stages 的两种 YAML 写法

操作步骤:
  1. 使用列表写法（- name:）定义 stages
  2. 使用映射写法（stage1:）定义 stages
  3. 提交并观察解析结果

预期结果:
  - 两种写法应被等价解析
  - 缩进瑕疵应给出明确报错而非静默失败

验证点:
  - [正向] 两种写法均成功解析
  - [nonfunctional] 缩进错误报错精确到行

清理:      重置 fixture 仓库
