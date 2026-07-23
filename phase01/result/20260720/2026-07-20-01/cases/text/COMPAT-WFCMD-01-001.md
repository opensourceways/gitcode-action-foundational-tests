用例 ID:   COMPAT-WFCMD-01-001
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-024
标题:      workflow 命令对标可用性

前置条件: 仓库 workflow 使用 ::group:: 等 workflow 命令
操作步骤:
  1. ::group::Build ... ::endgroup:: → 验证日志折叠
  2. ::error file=app.js,line=1:: → 验证创建注解
  3. ::warning:: → 验证创建 warning 注解
  4. ::debug:: → 在 ACTIONS_STEP_DEBUG=true 时验证可见
预期结果: 若支持则功能正常；不支持不应导致 step 失败
验证点:
  - [正向] ::group:: 日志折叠效果
  - [正向] ::error::/::warning:: 创建注解
  - [负向] 不支持时不导致 step 失败
清理:      fixture
