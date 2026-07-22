用例 ID:   SEC-INJECT-02-005
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-014
标题:      不可信输入注入到 ATOMGIT_ENV/ATOMGIT_OUTPUT 文件不导致环境变量污染

前置条件:
  - workflow 将 PR 标题（不可信输入）写入 ATOMGIT_ENV 文件
  - 后续 step 读取该环境变量

操作步骤:
  1. 将含换行符的不可信值写入 ATOMGIT_ENV
  2. 后续 step echo 该环境变量，检查是否被注入了额外变量
  3. 将含特殊字符的值写入 ATOMGIT_OUTPUT，后续 step 检查

预期结果:
  - 写入/读取协议不被不可信输入破坏
  - 无额外的环境变量被注入
  - 读取值 = 原始写入值

验证点:
  - [负向] 不含额外注入的环境变量
  - [正向] 后续 step echo 值与原始值一致
  - [负向] 多行值不导致多行注入

清理:      fixture
