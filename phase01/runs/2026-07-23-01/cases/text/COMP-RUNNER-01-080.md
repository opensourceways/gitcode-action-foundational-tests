用例 ID:   COMP-RUNNER-01-080
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-096~098
母意图:    —
标题:      runner 上下文属性可访问性验证

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 在 step 中引用 runner.name / runner.temp / runner.tool_cache / runner.os / runner.arch
  2. 验证输出非空且格式正确

预期结果:
  - runner 上下文各属性可正常访问，runner.os 为 Linux / Windows / macOS，runner.arch 为 X64 / ARM / ARM64

验证点:
  - [正向] runner.name / temp / tool_cache 非空
  - [正向] runner.os 为预定义值之一
  - [正向] runner.arch 为预定义值之一

清理:      重置 fixture 仓库
