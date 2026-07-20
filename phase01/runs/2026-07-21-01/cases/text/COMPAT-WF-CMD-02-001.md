用例 ID:   COMPAT-WF-CMD-02-001
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-024
标题:      验证 workflow 命令 ::group::/::error::/::warning::/::add-mask:: 对标可用性
incorporates: TC-239~253 (workflow commands)

前置条件:
  - step 中使用 stdout workflow 命令

操作步骤:
  1. echo '::group::Build' ... echo '::endgroup::' → 验证日志折叠
  2. echo '::error file=app.js,line=1::Missing semicolon' → 验证注解
  3. echo '::warning::Deprecated API' → 验证 warning 注解
  4. echo '::add-mask::$SECRET' → 验证脱敏
  5. echo '::debug::verbose info' 配合 ACTIONS_STEP_DEBUG=true

预期结果:
  - group/endgroup 正确折叠日志
  - error/warning 创建注解
  - add-mask 脱敏生效

验证点:
  - [正向] group/endgroup 可视化折叠
  - [正向] error/warning 生成注解
  - [正向] add-mask 脱敏后续日志

清理:      fixture
