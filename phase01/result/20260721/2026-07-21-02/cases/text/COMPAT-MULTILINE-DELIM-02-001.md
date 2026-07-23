用例 ID:   COMPAT-MULTILINE-DELIM-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-035
母意图:    —
标题:      多行值 delimiter 协议与「不可覆盖默认变量」约束一致性

前置条件:
  - workflow 向 ATOMGIT_ENV 写入多行值

操作步骤:
  1. 使用 delimiter 语法向 ATOMGIT_ENV 写入多行值
  2. 在后续 step 中读取该变量
  3. 测试默认变量是否可被覆盖

预期结果:
  - 多行值应正确传递
  - 默认变量（如 PATH）不应被 workflow 意外覆盖

验证点:
  - [正向] 多行值在后续 step 中完整可读
  - [负向] 默认变量未被静默覆盖

清理:      重置 fixture 仓库
