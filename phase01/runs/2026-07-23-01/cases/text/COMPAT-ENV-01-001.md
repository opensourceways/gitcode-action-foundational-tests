用例 ID:   COMPAT-ENV-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-017
母意图:    —
标题:      ATOMGIT_SHA 环境变量应正确返回触发提交 SHA

前置条件:
  - 仓库已启用 Actions
  - Runner 环境正常注入 ATOMGIT_* 变量

操作步骤:
  1. 在 workflow 的 run 步骤中输出 $ATOMGIT_SHA
  2. 触发 workflow 运行

预期结果:
  - $ATOMGIT_SHA 应返回当前触发事件的提交 SHA（40 位十六进制字符串）

验证点:
  - [正向] 日志中 ATOMGIT_SHA 的值不为空且为有效 SHA 格式

清理:      fixture
