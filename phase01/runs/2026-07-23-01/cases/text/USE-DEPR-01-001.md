用例 ID:   USE-DEPR-01-001
维度标签:   ['usability', 'compatibility']
维度:      usability/compatibility
优先级:    P1
溯源意图:  INTENT-USE-010
母意图:    —
标题:      使用 ATOMGIT_OUTPUT 文件协议时正常生效

前置条件:
  - workflow 在 GitCode Runner 上执行

操作步骤:
  1. 在 run 步骤中使用 echo key=val >> $ATOMGIT_OUTPUT

预期结果:
  输出参数正确设置，下游步骤可引用

验证点:
  - [正向] 下游步骤通过 steps.*.outputs.key 获取到值
  - [正向] 运行成功完成

清理:      无

