用例 ID:   USE-DEBUG-02-001
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-010
标题:      日志中 ::group::/::endgroup:: workflow 命令的实际支持情况

前置条件:
  - step 中使用 ::group::/::endgroup:: 日志命令

操作步骤:
  1. echo "::group::My Group" → 检查日志折叠效果
  2. echo "::endgroup::" → 检查分组结束
  3. echo "::error file=app.js,line=10::Something wrong" → 检查注解
  4. echo "::warning::Some warning" → 检查 warning 注解
  5. 不支持时不应导致 step 非零退出

预期结果:
  - 若支持：日志有可视化折叠/注解效果
  - 若不支持：不应导致 step 失败

验证点:
  - [正向] 折叠/注解效果存在或原样输出但不失败
  - [负向] 不支持时 step 不失败

清理:      fixture
