用例 ID:   USE-MASK-01-002
维度标签:   ['usability', 'security']
维度:      usability/security
优先级:    P0
溯源意图:  INTENT-USE-016
母意图:    —
标题:      直接 echo secrets 值时文档描述的绕过风险与实际一致

前置条件:
  - 仓库配置了 TEST_SECRET
  - 文档声明 echo secrets 可能绕过脱敏

操作步骤:
  1. 在 workflow 中直接执行 echo ${{ secrets.TEST_SECRET }}

预期结果:
  实际行为与文档声明一致；若确实可绕过，文档已给出缓解建议

验证点:
  - [负向] 若绕过确实发生，日志中可能出现明文
  - [非功能] 文档是否给出不要在 run 中直接 echo secrets 的缓解建议

清理:      无

