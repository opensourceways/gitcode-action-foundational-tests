用例 ID:   COMPAT-YAML-ERROR-02-001
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-060
母意图:    —
标题:      非法 YAML / schema 校验报错质量——错在第几行、可操作提示与 GitHub 对齐

前置条件:
  - workflow 包含故意的 YAML 语法错误

操作步骤:
  1. 提交包含缩进错误、缺少必填字段的 workflow
  2. 观察平台报错信息

预期结果:
  - 报错应指出具体行号
  - 提示应包含可操作的修改建议

验证点:
  - [nonfunctional] 报错精确到行号
  - [nonfunctional] 提示包含修复建议

清理:      重置 fixture 仓库
