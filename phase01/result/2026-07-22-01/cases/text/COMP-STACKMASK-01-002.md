用例 ID:   COMP-STACKMASK-01-002
维度标签:   [completeness, security]
维度:      功能完备性
优先级:    P0
溯源意图:  INTENT-COMP-012
母意图:    COMP-STACKMASK-01-001
标题:      secret 在步骤摘要 ATOMGIT_STEP_SUMMARY 中的脱敏验证

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN
  - workflow 在默认分支存在

操作步骤:
  1. 提交一个将 secret 值写入 ATOMGIT_STEP_SUMMARY 的 workflow
  2. 触发 workflow 并查看步骤摘要渲染结果
  3. 检查摘要中是否泄露 secret 明文

预期结果:
  - ATOMGIT_STEP_SUMMARY 中不出现 DEPLOY_TOKEN 明文
  - 系统在步骤摘要输出路径中保持脱敏

验证点:
  - [负向] 步骤摘要不含 DEPLOY_TOKEN 明文
  - [正向] 运行日志显示 SUMMARY_WRITTEN

清理:      fixture
