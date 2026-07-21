用例 ID:   COMPAT-RUN-CTX-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-011
标题:      验证 runner.os/arch 返回值格式与文档/一致性问题
incorporates: TC-094/095 (runner.os=linux, runner.arch=x86_64), TC-137/138 (FAIL)

前置条件:
  - 输出 runner.os / runner.arch / runner.name / runner.temp / runner.tool_cache

操作步骤:
  1. echo runner.os → 比对文档
  2. echo runner.arch → 比对文档
  3. echo runner.name / runner.temp / runner.tool_cache
  4. 多次运行验证一致性

预期结果:
  - 返回值与文档声明一致（或文档更新为实际值）
  - 多次运行格式一致

验证点:
  - [正向] runner.os 返回 linux/Linux 且文档一致
  - [正向] runner.arch 返回 x86_64/X64 且文档一致
  - [负向] 不在不同 run 中返回不同格式

清理:      fixture
