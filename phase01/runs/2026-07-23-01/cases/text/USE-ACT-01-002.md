用例 ID:   USE-ACT-01-002
维度标签:   ['usability', 'compatibility']
维度:      usability/compatibility
优先级:    P1
溯源意图:  INTENT-USE-007
母意图:    —
标题:      使用 actions/checkout@v4 时报错应给出迁移指引

前置条件:
  - workflow 文件位于 .gitcode/workflows/

操作步骤:
  1. 在 step 中写 uses: actions/checkout@v4

预期结果:
  系统报错并提示 GitCode 官方 Action 使用短名引用

验证点:
  - [负向] 不应静默失败或报泛化的 Action 不存在
  - [非功能] 报错中应包含 checkout 短名提示

清理:      无

