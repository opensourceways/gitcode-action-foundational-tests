用例 ID:   COMPAT-VAR-02-003
维度标签:   [compatibility, reliability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-064
母意图:    —
标题:      缺失系统变量引用行为与注入时机验证

前置条件:
  - 仓库已启用 workflow 触发
  - Runner 环境已就绪

操作步骤:
  1. 在 step run 第一行立即读取系统变量 $RUNNER_OS 与 $ATOMGIT_SHA
  2. 同一 step 中 echo 未定义变量 $RUNNER_NONEXISTENT
  3. 同一 step 中尝试 export RUNNER_OS=Fake 后再读取 $RUNNER_OS
  4. 观测输出与 step 运行状态

预期结果:
  - 脚本第一行即可读到 RUNNER_OS 与 ATOMGIT_SHA 的非空正确值（验证启动前注入）
  - echo 未定义变量不报错、不导致 step 失败（输出空行或空串）
  - 尝试覆盖 RUNNER_OS 后仍读到真实值，覆盖被拒绝或不生效

验证点:
  - [正向] step 第一行立即读取系统变量，验证启动前注入完成
  - [负向] echo 未定义变量不应报错导致 step 失败；尝试覆盖 RUNNER_OS 应被拒绝或至少不生效
  - [非功能] 注入时机与不可覆盖约束文档化；默认 shell 的严格模式标志（是否有 -u）文档明确

清理:      无
