用例 ID:   COMPAT-CONTEXT-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-001
标题:      验证 atomgit.* 核心属性集对齐 github.* 语义完整性
incorporates: TC-028~047 (atomgit 上下文属性), TC-038 (repository_owner 不可用)

前置条件:
  - 使用 atomgit.* 上下文在 if/run: 等各级别

操作步骤:
  1. 逐一验证已文档化的 atomgit.* 属性（event_name/sha/ref/ref_name/ref_type/event/workspace/action/token/repository/repository_owner/repositoryUrl/run_id/run_number/run_attempt/workflow/head_ref/base_ref/server_url/api_url）
  2. 对 GitHub 有但 atomgit 未文档化的属性（github.action_path 等），验证访问行为
  3. 确认 atomgit.repository_owner 实际可用（TC-038 问题修复确认）

预期结果:
  - 已文档化属性返回正确格式的值
  - 未文档化属性访问有可判定的行为
  - 非静默空值

验证点:
  - [正向] 已文档化属性在相应触发事件下返回非空值
  - [正向] event_name 返回正确的触发事件字符串
  - [负向] 无文档声明存在但返回 null 的属性

清理:      fixture
