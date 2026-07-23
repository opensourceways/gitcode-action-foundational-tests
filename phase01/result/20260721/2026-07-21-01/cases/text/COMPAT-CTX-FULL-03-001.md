用例 ID:   COMPAT-CTX-FULL-03-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-021
标题:      atomgit 上下文字段完备性：验证缺失字段（actor/workflow_ref/ref_protected 等）行为

前置条件:
  - 使用标准 fixture 仓库
  - push 事件触发以获取完整上下文

操作步骤:
  1. 输出 atomgit.actor 和 atomgit.actor_id（触发者审计信息）
  2. 输出 atomgit.workflow_ref 和 atomgit.workflow_sha
  3. 输出 atomgit.ref_protected（分支保护状态）
  4. 输出 atomgit.triggering_actor（重试触发者）
  5. 对每个字段记录返回值、空值或报错

预期结果:
  - 支持的字段返回有效值且符合语义
  - 不支持的字段返回空字符串（需文档标注）
  - 文档应提供 github 与 atomgit 上下文字段完整映射表

验证点:
  - [正向] 每个上下文引用均可解析（不触发 workflow 解析失败）
  - [正向] 缺失字段应被文档记录为已知差异
  - [正向] 现有字段值格式符合文档声明

清理:      fixture
