用例 ID:   COMP-ATOMGIT-01-047
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-017~057
母意图:    —
标题:      atomgit 核心上下文属性可访问性

前置条件:
  - 仓库已启用 AtomGit Action
  - workflow 使用 workflow_dispatch 触发

操作步骤:
  1. 在 workflow 的 step 中通过表达式引用 atomgit 核心属性
  2. 运行 workflow 并检查日志输出

预期结果:
  - atomgit.sha / ref / ref_name / ref_type / event_name / repository / run_number / run_attempt / workflow / server_url / api_url / workspace / actor / repositoryUrl / base_ref 均可正常访问并输出非空值

验证点:
  - [正向] 各核心属性输出不为空
  - [正向] atomgit.sha 长度为 40
  - [正向] atomgit.ref 包含 refs/ 前缀
  - [正向] atomgit.ref_name 不含 refs/ 前缀

清理:      重置 fixture 仓库
