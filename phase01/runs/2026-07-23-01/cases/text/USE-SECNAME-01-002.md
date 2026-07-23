用例 ID:   USE-SECNAME-01-002
维度标签:   ['usability', 'security']
维度:      usability/security
优先级:    P1
溯源意图:  INTENT-USE-028
母意图:    —
标题:      Secret 名称以数字开头时应给出命名规则错误

前置条件:
  - workflow 文件位于 .gitcode/workflows/

操作步骤:
  1. 在 workflow 中引用 ${{ secrets.1SECRET }}

预期结果:
  系统给出命名规则提示，说明允许字符与格式

验证点:
  - [负向] 不应仅报 Secret not found
  - [非功能] 报错中是否包含命名格式说明

清理:      无

