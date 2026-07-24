用例 ID:   USE-YAML-01-001
维度标签:   ['usability']
维度:      usability
优先级:    P1
溯源意图:  INTENT-USE-022
参照来源:  inputs/gitcode-spec/; inputs/business-context/README.md
母意图:    —
标题:      缺少必填字段 on 时报错应指出具体字段名与位置

前置条件:
  - workflow 文件位于 .gitcode/workflows/

操作步骤:
  1. 提交一个缺少 on 字段的 workflow

预期结果:
  报错包含文件名、出错行号、缺少字段名，最好给出正确写法示例

验证点:
  - [负向] 不应仅报泛化 YAML parse error
  - [非功能] 报错中是否同时包含字段名与所在行号

清理:      无

