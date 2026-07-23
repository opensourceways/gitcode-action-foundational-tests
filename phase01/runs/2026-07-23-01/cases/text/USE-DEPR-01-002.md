用例 ID:   USE-DEPR-01-002
维度标签:   ['usability', 'compatibility']
维度:      usability/compatibility
优先级:    P1
溯源意图:  INTENT-USE-010
母意图:    —
标题:      使用 ::set-output 时应给出弃用警告与替代示例

前置条件:
  - workflow 在 GitCode Runner 上执行

操作步骤:
  1. 在 run 步骤中使用 echo ::set-output name=key::val

预期结果:
  日志中出现明确的弃用警告，包含替代命令示例

验证点:
  - [负向] 不应静默生效
  - [非功能] 日志警告中应包含 deprecated/废弃/ATOMGIT_OUTPUT 字样

清理:      无

