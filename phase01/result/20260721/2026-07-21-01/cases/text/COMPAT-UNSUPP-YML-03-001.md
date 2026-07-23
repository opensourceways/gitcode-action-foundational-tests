用例 ID:   COMPAT-UNSUPP-YML-03-001
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-041
标题:      不支持 YAML 字段（run-name/environment/runs.using:node20）的降级方式

前置条件:
  - 在 GitCode workflow 中使用 GitHub 特有字段

操作步骤:
  1. 添加 run-name: "Deploy to ${{ inputs.env }}" 字段
  2. 添加 environment: production 字段
  3. 使用 runs.using: node20 创建自定义 action
  4. 观察各字段是报错还是静默忽略

预期结果:
  - 不支持的字段应在解析阶段报错（最安全）
  - 不应静默忽略（用户以为生效实际没有）
  - 报错信息应指出具体不支持字段名

验证点:
  - [正向] run-name 使用时应明确报错或文档标注不支持
  - [正向] environment 已知报 unknown property（TC-010）
  - [负向] 不应静默接受导致用户误判功能生效

清理:      fixture
